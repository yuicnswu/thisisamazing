"""Step 3b. Self-refining annotation without human annotators, and jury labels for the gold sample.

There are no human coders, so label quality is raised and measured with three independent models:
  A = claude-haiku-5-5 (cheap labeller, used at scale), B = claude-sonnet-5-5 (second labeller),
  J = claude-opus-5-5 (adjudicator and guide editor).

1. Codebook refinement on a dev sample (240 reviews, 48 per star, outside train/calib):
   round r: A and B label dev under guide_r; reliability = macro Cohen's kappa over aspect-mention,
   aspect-negative and context targets. J adjudicates every disagreeing review and, when the guide was
   ambiguous, writes one general rule. J then edits the rule list (merge, dedupe, at most 20 rules) into
   guide_{r+1}. Stop after MAX_ROUNDS or when kappa improves by less than MIN_GAIN; keep the best guide.
   This is iterative codebook development (as in qualitative content analysis) with model coders,
   using adjudicated disagreement as the error signal (Self-Refine, Madaan et al. 2023; LLM juries,
   Verga et al. 2024).
2. Held-out check on a test sample (200 random reviews, never used to edit the guide): A-B kappa under
   guide_0 vs the selected guide, so the gain is not an artefact of tuning on dev.
3. Production: A and B relabel train (A only) and calib (A and B) with the selected guide. On calib,
   agreeing reviews keep the shared labels and disagreeing ones take J's adjudication. The result,
   labels_calib__jury.jsonl, is the gold side of PPI. All quotes are re-checked verbatim.

Limitation stated in the paper: jury labels measure model consensus under an explicit guide, not human
judgement. The guide, every adjudication and every rule are saved so a human audit can be added later.

Usage: python codebook.py <source> [--workers 6] [--rounds 3]
Writes outputs/<source>/codebook/*.json and the production label files.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd

from label import ASPECTS, CONTEXT, HERE, PRIMARY, SECOND, check_labels, complete, draw_samples, parse_json, run, system_prompt

JUDGE = "claude-opus-5-5"
MAX_ROUNDS = 3
MIN_GAIN = 0.01
ADJ_BATCH = 10

ADJ = """

You are now the ADJUDICATOR. Two annotators (A and B) labelled each review under the guide above and
disagreed. For each review decide the correct labels under the guide: you may keep labels from A, from
B, or neither. Quotes must be copied exactly from the review. Then, only if the disagreement came from an
ambiguity or gap in the guide, write one general rule (at most 30 words, no product or brand names) that
would make annotators agree next time; otherwise write "".
Answer with a JSON array only:
[{"id": "...", "labels": [{"a": "...", "p": "...", "q": "..."}], "ctx": ["..."], "rule": "..."}]"""

EDITOR = """You maintain the annotation guide for aspect-based sentiment labelling of beauty and
personal-care reviews. The aspect ids and context ids are fixed and must not change.
You receive the current additional rules and candidate rules written by an adjudicator after resolving
annotator disagreements (with how often each was proposed). Produce the revised list of additional rules:
- keep a current rule unless a candidate clearly improves or contradicts it;
- merge duplicates and near-duplicates; prefer rules proposed more often;
- every rule must be general (no product or brand names), unambiguous, at most 30 words;
- at most 20 rules in total.
Answer with a JSON array of strings only."""


# ---------- comparison and reliability ----------

def tgt(rec: dict) -> dict:
    y = {}
    ps = {}
    for l in rec["labels"]:
        ps.setdefault(l["a"], set()).add(l["p"])
    for a in ASPECTS:
        y[f"mention_{a}"] = int(a in ps)
        y[f"neg_{a}"] = int(bool(ps.get(a, set()) & {"neg", "mixed"}))
    for c in CONTEXT:
        y[f"ctx_{c}"] = int(c in rec["ctx"])
    return y


def canon(rec: dict):
    return frozenset((l["a"], l["p"]) for l in rec["labels"]), frozenset(rec["ctx"])


def kappa(x: np.ndarray, y: np.ndarray) -> float:
    po = (x == y).mean()
    pe = x.mean() * y.mean() + (1 - x.mean()) * (1 - y.mean())
    return float((po - pe) / (1 - pe)) if pe < 1 else float("nan")


def reliability(ra: list[dict], rb: list[dict], min_pos: int = 5) -> dict:
    """Macro kappa over targets with at least min_pos positives (either coder), plus exact-set agreement."""
    ok = [(a, b) for a, b in zip(ra, rb) if a["parsed"] and b["parsed"]]
    A = pd.DataFrame([tgt(a) for a, _ in ok])
    B = pd.DataFrame([tgt(b) for _, b in ok])
    ks = {}
    for t in A.columns:
        if A[t].sum() + B[t].sum() >= min_pos:
            ks[t] = round(kappa(A[t].values, B[t].values), 3)
    by = lambda p: [v for k, v in ks.items() if k.startswith(p) and not np.isnan(v)]
    return {"n": len(ok), "macro_kappa": round(float(np.nanmean(list(ks.values()))), 4),
            "macro_kappa_mention": round(float(np.mean(by("mention_"))), 4),
            "macro_kappa_neg": round(float(np.mean(by("neg_"))), 4),
            "macro_kappa_ctx": round(float(np.mean(by("ctx_"))), 4) if by("ctx_") else None,
            "exact_agreement": round(float(np.mean([canon(a) == canon(b) for a, b in ok])), 4),
            "per_target": ks}


# ---------- adjudication and guide editing ----------

def _adj_batch(rules, items):
    payload = []
    for r, a, b in items:
        payload.append({"id": r["review_id"], "title": r["title"], "review": r["text"][:3000],
                        "A": {"labels": a["labels"], "ctx": a["ctx"]}, "B": {"labels": b["labels"], "ctx": b["ctx"]}})
    raw = complete("claude", JUDGE, system_prompt(rules) + ADJ, "Adjudicate:\n" + json.dumps(payload, ensure_ascii=False))
    try:
        got = {str(x.get("id")): x for x in parse_json(raw) if isinstance(x, dict)}
    except ValueError:
        got = {}
    out = []
    for r, a, b in items:
        x = got.get(r["review_id"])
        rec = check_labels(x, r)
        rec["rule"] = (x or {}).get("rule") or ""
        if not rec["parsed"]:          # adjudicator failed: fall back to the cheaper coder, flagged
            rec = dict(a, rule="", adjudication_failed=True)
        out.append(rec)
    return out


def adjudicate(rules, rows, ra, rb, workers):
    """Returns the jury record for every row: shared labels where A and B agree, J's ruling otherwise."""
    dis = [(r, a, b) for r, a, b in zip(rows, ra, rb) if canon(a) != canon(b) or not (a["parsed"] and b["parsed"])]
    batches = [dis[i:i + ADJ_BATCH] for i in range(0, len(dis), ADJ_BATCH)]
    ruled = {}
    with ThreadPoolExecutor(workers) as ex:
        for part in ex.map(lambda bt: _adj_batch(rules, bt), batches):
            for rec in part:
                ruled[rec["review_id"]] = rec
    jury = []
    for r, a in zip(rows, ra):
        if r["review_id"] in ruled:
            jury.append(dict(ruled[r["review_id"]], source="adjudicated"))
        else:
            jury.append(dict(a, source="agreed", rule=""))
    return jury


def edit_rules(rules, candidates):
    cand = pd.Series([c.strip() for c in candidates if c and c.strip()]).value_counts()
    if cand.empty:
        return rules
    prompt = json.dumps({"current_rules": rules, "candidate_rules": [{"rule": k, "times_proposed": int(v)} for k, v in cand.items()]},
                        ensure_ascii=False)
    try:
        new = [str(x).strip() for x in parse_json(complete("claude", JUDGE, EDITOR, prompt)) if str(x).strip()]
    except ValueError:
        return rules
    return new[:20] or rules


# ---------- samples ----------

def dev_test_samples(df, used, seed=1):
    pool = df[~df.review_id.isin(used)]
    dev = pool.groupby("rating", group_keys=False).apply(lambda g: g.sample(n=min(48, len(g)), random_state=seed))
    test = pool.drop(dev.index).sample(n=200, random_state=seed + 1)
    return dev, test


def rows_of(d):
    return d[["review_id", "title", "text"]].assign(title=lambda x: x.title.fillna("")).to_dict("records")


def dump(path, recs):
    with open(path, "w") as f:
        for r in recs:
            f.write(json.dumps(r) + "\n")


def main(source, workers=6, rounds=MAX_ROUNDS):
    out = os.path.join(HERE, "outputs", source)
    cb = os.path.join(out, "codebook")
    os.makedirs(cb, exist_ok=True)
    df = pd.read_parquet(os.path.join(out, "reviews.parquet"), columns=["review_id", "title", "text", "rating"])
    spath = os.path.join(out, "label_sample.parquet")
    if not os.path.exists(spath):          # fresh source (e.g. Sephora): draw train and calib as label.py does
        full = pd.read_parquet(os.path.join(out, "reviews.parquet"))
        draw_samples(full, 2000, 1500).to_parquet(spath, index=False)
        del full
    sample = pd.read_parquet(spath)
    dpath = os.path.join(cb, "dev_test_sample.parquet")
    if os.path.exists(dpath):
        dt = pd.read_parquet(dpath)
        dev, test = dt[dt["sample"] == "dev"], dt[dt["sample"] == "test"]
    else:
        dev, test = dev_test_samples(df, set(sample.review_id))
        pd.concat([dev.assign(sample="dev"), test.assign(sample="test")]).to_parquet(dpath, index=False)
    dev_rows, test_rows = rows_of(dev), rows_of(test)

    # 1. refinement loop on dev
    history, rules, guides = [], [], [[]]
    for r in range(rounds + 1):
        ra, rb = run(PRIMARY, dev_rows, workers, rules), run(SECOND, dev_rows, workers, rules)
        rel = reliability(ra, rb)
        step = {"round": r, "n_rules": len(rules), **{k: v for k, v in rel.items() if k != "per_target"}}
        print("round", step, flush=True)
        stop = r == rounds or (r > 0 and rel["macro_kappa"] - history[-1]["macro_kappa"] < MIN_GAIN)
        if not stop:
            jury = adjudicate(rules, dev_rows, ra, rb, workers)
            cands = [j["rule"] for j in jury if j.get("rule")]
            step["disagreeing_reviews"] = sum(j["source"] == "adjudicated" for j in jury)
            step["candidate_rules"] = len(cands)
            dump(os.path.join(cb, f"dev_round{r}_jury.jsonl"), jury)
            rules = edit_rules(rules, cands)
            guides.append(rules)
        history.append(step)
        with open(os.path.join(cb, "history.json"), "w") as f:
            json.dump({"history": history, "guides": guides}, f, indent=2)
        if stop:
            break
    best = int(np.argmax([h["macro_kappa"] for h in history]))
    rules_best = guides[best]

    # 2. held-out reliability, guide_0 vs selected guide
    held = {}
    for name, rl in (("guide_0", []), ("selected", rules_best)):
        ta, tb = run(PRIMARY, test_rows, workers, rl), run(SECOND, test_rows, workers, rl)
        held[name] = reliability(ta, tb)
    # cheap coder against the jury on test (selected guide)
    ta, tb = run(PRIMARY, test_rows, workers, rules_best), run(SECOND, test_rows, workers, rules_best)
    tj = adjudicate(rules_best, test_rows, ta, tb, workers)
    held["haiku_vs_jury"] = reliability(ta, tj)
    held["sonnet_vs_jury"] = reliability(tb, tj)

    # 3. production labels with the selected guide
    legacy = os.path.join(out, "v0_labels")
    os.makedirs(legacy, exist_ok=True)
    for fn in os.listdir(out):
        if fn.startswith("labels_") and fn.endswith(".jsonl") and not os.path.exists(os.path.join(legacy, fn)):
            shutil.copy(os.path.join(out, fn), os.path.join(legacy, fn))
    tr_rows = rows_of(sample[sample["sample"] == "train"])
    ca_rows = rows_of(sample[sample["sample"] == "calib"])
    tr = run(PRIMARY, tr_rows, workers, rules_best)
    ca_a, ca_b = run(PRIMARY, ca_rows, workers, rules_best), run(SECOND, ca_rows, workers, rules_best)
    ca_j = adjudicate(rules_best, ca_rows, ca_a, ca_b, workers)
    dump(os.path.join(out, f"labels_train__{PRIMARY}.jsonl"), tr)
    dump(os.path.join(out, f"labels_calib__{PRIMARY}.jsonl"), ca_a)
    dump(os.path.join(out, f"labels_calib__{SECOND}.jsonl"), ca_b)
    dump(os.path.join(out, "labels_calib__jury.jsonl"), ca_j)
    prod = {"calib_haiku_vs_sonnet": reliability(ca_a, ca_b), "calib_haiku_vs_jury": reliability(ca_a, ca_j),
            "calib_adjudicated_share": round(float(np.mean([j["source"] == "adjudicated" for j in ca_j])), 4),
            "calib_adjudication_failed": int(sum(bool(j.get("adjudication_failed")) for j in ca_j)),
            "verbatim_dropped": {"train": sum(r["dropped_quotes"] for r in tr), "calib_haiku": sum(r["dropped_quotes"] for r in ca_a),
                                 "calib_jury": sum(r["dropped_quotes"] for r in ca_j)}}
    res = {"models": {"A": PRIMARY, "B": SECOND, "judge": JUDGE}, "history": history, "selected_round": best,
           "rules": rules_best, "held_out": held, "production": prod}
    with open(os.path.join(cb, "codebook_results.json"), "w") as f:
        json.dump(res, f, indent=2)
    with open(os.path.join(cb, "guide_selected.txt"), "w") as f:
        f.write(system_prompt(rules_best))
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("source"); ap.add_argument("--workers", type=int, default=6); ap.add_argument("--rounds", type=int, default=MAX_ROUNDS)
    a = ap.parse_args()
    r = main(a.source, a.workers, a.rounds)
    print(json.dumps({k: v for k, v in r.items() if k != "held_out"}, indent=2)[:3000])
