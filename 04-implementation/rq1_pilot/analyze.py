"""Tables for the report: RQ1 recommend rates by variant, prior effect, and Learn-then-Test URR / coverage.

    python analyze.py            # reads outputs/items.jsonl + outputs/preds/*.json, writes outputs/results.{json,md}
"""
from __future__ import annotations

import glob
import json
import os

import numpy as np

from ltt import evaluate, risk_coverage, summarize

OUT = os.path.join(os.path.dirname(__file__), "outputs")
VARIANTS = ["original", "remove", "vague", "remove_prior", "contradict", "natural_missing"]
ALPHAS = [0.05, 0.10, 0.20]


def load():
    items = [json.loads(l) for l in open(os.path.join(OUT, "items.jsonl"))]
    preds = {}
    for p in sorted(glob.glob(os.path.join(OUT, "preds", "*.json"))):
        preds[os.path.basename(p)[:-5]] = json.load(open(p))
    return items, preds


def cluster_ci(values, groups, n_boot=1000, seed=0):
    """Mean with a product-level (cluster) bootstrap 95% interval."""
    values, groups = np.asarray(values, float), np.asarray(groups)
    if len(values) == 0:
        return (float("nan"),) * 3
    uniq = np.unique(groups)
    idx = {g: np.where(groups == g)[0] for g in uniq}
    rng = np.random.default_rng(seed)
    boots = []
    for _ in range(n_boot):
        pick = np.concatenate([idx[g] for g in rng.choice(uniq, len(uniq))])
        boots.append(values[pick].mean())
    return float(values.mean()), float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))


def dense_decisions(items, pred):
    """Dense probes output only a similarity. Threshold = 20th percentile of original-item similarity, so the
    probe 'recommends' 80% of complete listings; then ask how often it still recommends edited ones."""
    orig = [pred[i["item_id"]]["score"] for i in items if i["variant"] == "original"]
    tau = float(np.percentile(orig, 20))
    return {k: {"decision": "recommend" if v["score"] >= tau else "abstain", "score": v["score"]}
            for k, v in pred.items()}, tau


def audited_out() -> set[str]:
    """Items where the independent quote judge disagrees with the construction / parser label (§11.3)."""
    p = os.path.join(OUT, "label_audit.json")
    if not os.path.exists(p):
        return set()
    return {r["item_id"] for r in json.load(open(p))["rows"] if not r["agree"]}


def main():
    items, preds = load()
    full = analyse(items, preds)
    drop = audited_out()
    clean = analyse([i for i in items if i["item_id"] not in drop], preds)
    clean["dropped_items"] = len(drop)
    json.dump({"all": full, "audited": clean}, open(os.path.join(OUT, "results.json"), "w"), indent=1)
    md = "## All items\n\n" + to_md(full) + f"\n## Audited items (construction label and quote judge agree; {len(drop)} items dropped)\n\n" + to_md(clean)
    open(os.path.join(OUT, "results.md"), "w").write(md)
    print(md)


def analyse(items, preds):
    res = {"n_items": len(items), "n_products": len({i["asin"] for i in items}),
           "variants": {v: sum(i["variant"] == v for i in items) for v in VARIANTS}, "matchers": {}}
    for name, pred in preds.items():
        extra = {}
        if name.startswith("dense"):
            pred, tau = dense_decisions(items, pred)
            extra["tau"] = tau
        ok = [i for i in items if pred.get(i["item_id"], {}).get("score") is not None]
        r = {"n_scored": len(ok), **extra, "recommend_rate": {}, "mean_score": {}}
        for v in VARIANTS:
            sub = [i for i in ok if i["variant"] == v]
            rec = [pred[i["item_id"]]["decision"] == "recommend" for i in sub]
            r["recommend_rate"][v] = cluster_ci(rec, [i["asin"] for i in sub])
            r["mean_score"][v] = float(np.mean([pred[i["item_id"]]["score"] for i in sub])) if sub else None
        # native URR (the matcher's own decisions)
        rec_items = [i for i in ok if pred[i["item_id"]]["decision"] == "recommend"]
        r["native_urr"] = cluster_ci([i["label"] != "entailed" for i in rec_items], [i["asin"] for i in rec_items])
        r["native_coverage"] = len(rec_items) / len(ok) if ok else 0
        # prior effect: same product, remove vs remove_prior
        by = {}
        for i in ok:
            by.setdefault(i["asin"], {})[i["variant"]] = pred[i["item_id"]]["decision"] == "recommend"
        pairs = [(d["remove"], d["remove_prior"]) for d in by.values() if "remove" in d and "remove_prior" in d]
        r["prior_flip"] = {"n": len(pairs), "abstain_to_recommend": sum((not a) and b for a, b in pairs),
                           "recommend_to_abstain": sum(a and (not b) for a, b in pairs)}
        # per attribute, on unresolved variants
        r["unresolved_rec_by_attr"] = {}
        for attr in ("skin_type", "hair_type", "scent", "item_form", "free_from"):
            sub = [i for i in ok if i["need"][0] == attr and i["label"] == "unresolved"]
            if sub:
                r["unresolved_rec_by_attr"][attr] = (float(np.mean([pred[i["item_id"]]["decision"] == "recommend"
                                                                     for i in sub])), len(sub))
        # Learn-then-Test on the score
        scores = [pred[i["item_id"]]["score"] for i in ok]
        uns = [i["label"] != "entailed" for i in ok]
        groups = [i["asin"] for i in ok]
        r["ltt"] = {str(a): summarize(evaluate(scores, uns, groups, a, delta=0.1, n_splits=50), a) for a in ALPHAS}
        r["risk_coverage"] = risk_coverage(scores, uns)
        res["matchers"][name] = r
    return res


def _p(t):
    return "–" if t is None or (isinstance(t, float) and np.isnan(t)) else f"{100 * t:.0f}%"


def _ci(t):
    return f"{_p(t[0])} [{_p(t[1])}, {_p(t[2])}]"


def to_md(res):
    L = [f"Items: {res['n_items']} from {res['n_products']} products. Variants: {res['variants']}", ""]
    L.append("**Recommend rate by variant** (product-cluster bootstrap 95% CI). Correct behaviour: original high, "
             "every other column 0.")
    L.append("")
    L.append("| Matcher | " + " | ".join(VARIANTS) + " | native URR |")
    L.append("|---|" + "---|" * (len(VARIANTS) + 1))
    for n, r in res["matchers"].items():
        L.append(f"| {n} | " + " | ".join(_ci(r["recommend_rate"][v]) for v in VARIANTS) + f" | {_ci(r['native_urr'])} |")
    L += ["", "**Prior effect** (same product: evidence removed, then famous brand + hype added)", "",
          "| Matcher | pairs | abstain→recommend | recommend→abstain |", "|---|---|---|---|"]
    for n, r in res["matchers"].items():
        p = r["prior_flip"]
        L.append(f"| {n} | {p['n']} | {p['abstain_to_recommend']} | {p['recommend_to_abstain']} |")
    L += ["", "**Learn-then-Test** (50 product splits, 50/50 calibration/test, δ = 0.1). URR and coverage on test, "
          "mean [2.5%, 97.5%] across splits; 'viol.' = share of splits with test URR > α.", "",
          "| Matcher | α | URR | coverage | recall of supported | viol. | no threshold |", "|---|---|---|---|---|---|---|"]
    for n, r in res["matchers"].items():
        for a, s in r["ltt"].items():
            L.append(f"| {n} | {a} | {_ci(s['urr'])} | {_ci(s['coverage'])} | {_ci(s['recall'])} | "
                     f"{_p(s['violation_rate'])} | {_p(s['no_threshold_rate'])} |")
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    main()
