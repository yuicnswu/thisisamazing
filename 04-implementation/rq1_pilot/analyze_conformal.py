"""Algorithm 1 (theory.md) for every matcher: certified URR / URJ / coverage on held-out products.

    python analyze_conformal.py      # writes outputs/conformal.{json,md}

Pools: the pilot items (outputs/items.jsonl, up to 5 variants per product; Algorithm 1 draws one per product)
and the one-item-per-product calibration pool (outputs/calpool.jsonl, POOL=cal), each with its own quote-judge
audit and predictions. A matcher run on both pools is calibrated and tested on their union.
"""
from __future__ import annotations

import glob
import json
import os

import numpy as np

from conformal import algorithm1, summarize1

OUT = os.path.join(os.path.dirname(__file__), "outputs")
ALPHAS, ALPHA_REJ, DELTA, N_SPLITS = [0.10, 0.20], 0.10, 0.10, 50


def scores(name, pred, ids):
    """(e, c) per matcher. Matchers with no contradiction score get c from their own reject decision."""
    def col(f):
        return np.array([f(pred[i]) for i in ids], float)
    rej = lambda r: 1.0 if r.get("decision") == "reject" else 0.0
    if name.startswith("nesy-neural"):
        return col(lambda r: r["e_neural"]), col(lambda r: r["c_neural"])
    if name.startswith("nesy"):
        return col(lambda r: r["e"]), col(lambda r: r["c"])
    if name.startswith(("naive", "dense")):
        return col(lambda r: r["score"]), np.zeros(len(ids))
    return col(lambda r: r["score"]), col(rej)


def main():
    items, judge, preds, pools = [], {}, {}, {}
    for pool, f_items, f_audit, d_preds in (("pilot", "items.jsonl", "label_audit.json", "preds"),
                                            ("cal", "calpool.jsonl", "label_audit_cal.json", "preds_cal")):
        if not os.path.exists(os.path.join(OUT, f_audit)):
            continue
        items += [json.loads(l) for l in open(os.path.join(OUT, f_items))]
        judge.update({r["item_id"]: r["judge"] for r in json.load(open(os.path.join(OUT, f_audit)))["rows"]})
        for p in sorted(glob.glob(os.path.join(OUT, d_preds, "*.json"))):
            name = os.path.basename(p)[:-5]
            preds.setdefault(name, {}).update(json.load(open(p)))
            pools.setdefault(name, []).append(pool)
    for k in [k for k in preds if k.startswith("nesy__")]:
        preds["nesy-neural__" + k.split("__", 1)[1]] = preds[k]
        pools["nesy-neural__" + k.split("__", 1)[1]] = pools[k]
    labels = {
        # Theorem 3: consensus of the rule parser and the independent quote judge
        "consensus": (lambda i: not (i["label"] == "entailed" and judge.get(i["item_id"]) == "entailed"),
                      lambda i: not (i["label"] == "contradicted" and judge.get(i["item_id"]) == "contradicted")),
        # Theorem 2: parser / construction label alone
        "parser": (lambda i: i["label"] != "entailed", lambda i: i["label"] != "contradicted"),
        # agreement-filtered population (plan §11.3): keep only items where parser and judge agree; the guarantee
        # then covers listings that pass the filter, as theory.md §3 says of the filtered L2 pool
        "agreed": (lambda i: i["label"] != "entailed", lambda i: i["label"] != "contradicted"),
    }
    keep = {"consensus": lambda i: True, "parser": lambda i: True,
            "agreed": lambda i: judge.get(i["item_id"]) == i["label"]}
    res = {"alpha_rej": ALPHA_REJ, "delta": DELTA, "n_splits": N_SPLITS, "matchers": {}}
    for name, pred in preds.items():
        scored = [i for i in items if (pred.get(i["item_id"]) or {}).get("score") is not None]
        r = {"n_scored": len(scored), "pools": pools[name], "n_products": len({i["asin"] for i in scored})}
        for lab, (fu, fc) in labels.items():
            ok = [i for i in scored if keep[lab](i)]
            e, c = scores(name, pred, [i["item_id"] for i in ok])
            groups = [i["asin"] for i in ok]
            diag = {  # share of test recommendations where the two labellers disagree (Lemma 1 diagnostic)
                "diag_parser_E_judge_not": [i["label"] == "entailed" and judge.get(i["item_id"]) != "entailed" for i in ok],
                "diag_judge_E_parser_not": [i["label"] != "entailed" and judge.get(i["item_id"]) == "entailed" for i in ok],
            }
            unsup, uncon = [fu(i) for i in ok], [fc(i) for i in ok]
            for a in ALPHAS:
                rows = algorithm1(e, c, unsup, uncon, groups, a, ALPHA_REJ, DELTA, N_SPLITS, extra=diag)
                r[f"{lab}@{a}"] = summarize1(rows, a, ALPHA_REJ)
        res["matchers"][name] = r
        print(name, {k: (round(v["urr"][0], 3), round(v["coverage"][0], 3), v["no_threshold_rate"])
                     for k, v in r.items() if "@" in k})
    json.dump(res, open(os.path.join(OUT, "conformal.json"), "w"), indent=1)
    open(os.path.join(OUT, "conformal.md"), "w").write(to_md(res))


def _p(x):
    return f"{100 * x:.1f}%"


def _ci(t):
    return f"{_p(t[0])} [{_p(t[1])}, {_p(t[2])}]"


def to_md(res):
    L = [f"Algorithm 1 of theory.md: {res['n_splits']} product splits (50% calibration, one item per product; 20% of it tunes the path), δ = {res['delta']}, "
         f"α' (URJ) = {res['alpha_rej']}. Test metrics weight each held-out product equally. Mean [2.5%, 97.5%] "
         "across splits.", ""]
    for lab in ("consensus", "parser", "agreed"):
        L += [f"### Labels: {lab}", "",
              "| Matcher | products | α | URR | URJ | coverage | recall of supported | URR > α | no certified θ | "
              "parser E, judge not (of recs) |", "|---|---|---|---|---|---|---|---|---|---|"]
        for n, r in res["matchers"].items():
            for a in ALPHAS:
                s = r[f"{lab}@{a}"]
                L.append(f"| {n} | {r['n_products']} | {a} | {_ci(s['urr'])} | {_ci(s['urj'])} | {_ci(s['coverage'])} | {_ci(s['recall'])} "
                         f"| {_p(s['violation_rate'])} | {_p(s['no_threshold_rate'])} | {_p(s['diag_parser_E_judge_not'][0])} |")
        L.append("")
    return "\n".join(L)


if __name__ == "__main__":
    main()
