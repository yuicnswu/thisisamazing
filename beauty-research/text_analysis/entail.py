"""Step 3c. Semantic support check: does each verbatim quote actually support its label?

The verbatim check (label.py) proves a quote exists in the review, not that it supports the claim
"the reviewer evaluates <aspect> as <polarity>". This step adds a claim-quote entailment judgement,
in the spirit of attribution and citation evaluation (ALCE, Gao et al. 2023; FActScore, Min et al. 2023;
AIS, Rashkin et al. 2023), with a judge model that did not produce the labels.

Validation without human annotators: a contrast set with known answers. For a random sample of labels
we build perturbed claims that should NOT be supported:
  flip   : same aspect and quote, polarity reversed (pos<->neg, mixed->pos)
  swap   : same quote and polarity, an aspect the review was not labelled with
  wrong  : same claim, but the quote of a different-aspect label from the same review
The judge's rejection rate on perturbations (specificity) and acceptance of originals are reported.
Some perturbations can be genuinely supported (a quote may cover two aspects), so specificity is a
lower bound.

Then every gold (calib jury) label is judged; unsupported labels are dropped to give
labels_calib__jury_entailed.jsonl, the gold side used by scale.py and analyze.py.

Usage: python entail.py <source> [--workers 6] [--contrast 300]
"""
from __future__ import annotations

import argparse
import json
import os
import random
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd

from label import ASPECTS, HERE, complete, parse_json

JUDGE = "claude-opus-5-5"
BATCH = 30
POL = {"pos": "positively", "neg": "negatively", "mixed": "with mixed (both positive and negative) views"}

SYSTEM = """You check whether evidence supports a claim about a product review.
Each item has the review text, a claim of the form "The reviewer evaluates <aspect> <polarity>", and a
quote from the review offered as evidence. Answer "supported" only if the quote, read in the context of
the review, shows the reviewer evaluating that aspect with that polarity. Otherwise answer "not_supported"
(wrong aspect, wrong polarity, the quote does not concern the aspect, or it is not the reviewer's own
evaluation). Judge the claim, not the product.
Answer with a JSON array only: [{"id": "...", "verdict": "supported" | "not_supported"}]"""


def claim_text(a: str, p: str) -> str:
    return f"The reviewer evaluates {a.replace('_', ' ')} ({ASPECTS[a]}) {POL[p]}."


def _judge_batch(items):
    payload = [{"id": i["id"], "review": i["review"][:2000], "claim": claim_text(i["a"], i["p"]), "quote": i["q"]} for i in items]
    raw = complete("claude", JUDGE, SYSTEM, "Judge these items:\n" + json.dumps(payload, ensure_ascii=False))
    try:
        got = {str(x.get("id")): x.get("verdict") for x in parse_json(raw) if isinstance(x, dict)}
    except ValueError:
        got = {}
    return {i["id"]: got.get(i["id"]) for i in items}


def judge(items, workers):
    res = {}
    batches = [items[k:k + BATCH] for k in range(0, len(items), BATCH)]
    with ThreadPoolExecutor(workers) as ex:
        for part in ex.map(_judge_batch, batches):
            res.update(part)
    return res


def contrast_set(recs, text, n, seed=0):
    rng = random.Random(seed)
    pool = [(r["review_id"], k, l) for r in recs for k, l in enumerate(r["labels"]) if l["a"] != "overall"]
    rng.shuffle(pool)
    items = []
    for rid, k, l in pool[:n]:
        rec = next(r for r in recs if r["review_id"] == rid)
        base = {"review": text[rid], "a": l["a"], "p": l["p"], "q": l["q"]}
        items.append(dict(base, id=f"{rid}:{k}:orig", kind="orig"))
        items.append(dict(base, id=f"{rid}:{k}:flip", kind="flip", p={"pos": "neg", "neg": "pos", "mixed": "pos"}[l["p"]]))
        have = {x["a"] for x in rec["labels"]}
        other = [a for a in ASPECTS if a not in have and a != "overall"]
        items.append(dict(base, id=f"{rid}:{k}:swap", kind="swap", a=rng.choice(other)))
        alt = [x for x in rec["labels"] if x["a"] != l["a"] and x["a"] != "overall"]
        if alt:
            items.append(dict(base, id=f"{rid}:{k}:wrong", kind="wrong", q=rng.choice(alt)["q"]))
    return items


def main(source, workers=6, n_contrast=300):
    out = os.path.join(HERE, "outputs", source)
    gold = os.path.join(out, "labels_calib__jury.jsonl")
    recs = [json.loads(l) for l in open(gold)]
    df = pd.read_parquet(os.path.join(out, "label_sample.parquet"), columns=["review_id", "title", "text"])
    text = {r.review_id: (r.title or "") + " . " + r.text for r in df.itertuples()}

    # 1. contrast-set validation of the judge
    cs = contrast_set(recs, text, n_contrast)
    v = judge(cs, workers)
    val = {}
    for kind in ("orig", "flip", "swap", "wrong"):
        ks = [i for i in cs if i["kind"] == kind and v.get(i["id"]) in ("supported", "not_supported")]
        sup = np.mean([v[i["id"]] == "supported" for i in ks]) if ks else float("nan")
        val[kind] = {"n": len(ks), "supported_rate": round(float(sup), 4)}
    pert = [i for i in cs if i["kind"] != "orig" and v.get(i["id"]) in ("supported", "not_supported")]
    val["specificity_all_perturbations"] = round(float(np.mean([v[i["id"]] == "not_supported" for i in pert])), 4)
    val["unparsed"] = sum(v.get(i["id"]) not in ("supported", "not_supported") for i in cs)

    # 2. judge every gold label
    items = [{"id": f"{r['review_id']}:{k}", "review": text[r["review_id"]], **l} for r in recs for k, l in enumerate(r["labels"])]
    v2 = judge(items, workers)
    kept, dropped, unparsed = [], 0, 0
    by_aspect = {}
    for r in recs:
        labs = []
        for k, l in enumerate(r["labels"]):
            verdict = v2.get(f"{r['review_id']}:{k}")
            st = by_aspect.setdefault(l["a"], [0, 0])
            st[1] += 1
            if verdict == "not_supported":
                dropped += 1
                st[0] += 1
                continue
            unparsed += verdict is None      # kept: a failed judgement is not evidence against the label
            labs.append(l)
        kept.append(dict(r, labels=labs, entail_dropped=len(r["labels"]) - len(labs)))
    with open(os.path.join(out, "labels_calib__jury_entailed.jsonl"), "w") as f:
        for r in kept:
            f.write(json.dumps(r) + "\n")
    n = len(items)
    res = {"judge": JUDGE, "contrast_validation": val, "gold_labels": n, "not_supported": dropped,
           "verbatim_but_unsupported_rate": round(dropped / n, 4) if n else None, "judge_unparsed_kept": unparsed,
           "unsupported_rate_by_aspect": {a: {"n": t, "rate": round(d / t, 4)} for a, (d, t) in sorted(by_aspect.items())}}
    with open(os.path.join(out, "entail_results.json"), "w") as f:
        json.dump(res, f, indent=2)
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("source"); ap.add_argument("--workers", type=int, default=6); ap.add_argument("--contrast", type=int, default=300)
    a = ap.parse_args()
    print(json.dumps(main(a.source, a.workers, a.contrast), indent=2))
