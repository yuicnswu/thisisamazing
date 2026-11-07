"""Step 2b. LLM topic modelling (TopicGPT; Pham et al., NAACL 2024) as a coverage audit of the aspect taxonomy.

NMF (discover.py) gives word clusters that need human reading. TopicGPT instead has an LLM propose
natural-language topics from the reviews, merge them, and assign them back to documents with evidence:
1. Generation (claude-sonnet-5-5): reviews from a star-stratified sample (outside train, calib, dev and
   test) are read in batches; the model keeps a running topic list, adding a topic only when no existing
   one fits.
2. Refinement (claude-opus-5-5): near-duplicate topics are merged, rare ones dropped (at most 30 kept),
   and each topic is mapped to one aspect id of aspects.py or marked "new" if no aspect covers it.
3. Assignment (claude-haiku-5-5): topics are assigned to every review of the random calib sample with a
   verbatim quote; assignments whose quote is not in the review are dropped.
Because calib is a simple random sample, topic shares carry Wilson 95% intervals. Coverage = share of
reviews whose every assigned topic maps to an existing aspect; the "new" topics show what the fixed
taxonomy misses.

Usage: python topicgpt.py <source> [--gen 400] [--workers 12]
Writes outputs/<source>/topicgpt.json and topicgpt.md.
"""
from __future__ import annotations

import argparse
import json
import os
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd

from label import ASPECTS, HERE, PRIMARY, SECOND, complete, parse_json, quote_ok

JUDGE = "claude-opus-5-5"
GEN_BATCH = 40

GEN = """You are building a topic list for beauty and personal-care product reviews, as in TopicGPT.
You receive the current topic list and a batch of reviews. Topics are aspects of the product or the
purchase experience that reviewers evaluate (not product types, not brands). For each review, check
whether an existing topic covers what it discusses; add a new topic ONLY if none does. Topic names are
2-5 words; descriptions are one sentence. Return the full updated list.
Answer with a JSON array only: [{"name": "...", "description": "..."}]"""

REFINE = """You refine a topic list for beauty and personal-care reviews. Merge topics that are the same
or near-duplicates, drop topics that are too specific to matter, keep at most 30. Then map each topic to
exactly one of these existing aspect ids if that aspect clearly covers it, otherwise "new":
{aspects}
Answer with a JSON array only: [{{"id": "t1", "name": "...", "description": "...", "aspect": "<aspect id or new>"}}]"""

ASSIGN = """Assign topics to beauty and personal-care reviews. Use only these topics:
{topics}
For each review list every topic the reviewer actually discusses, each with a short quote copied
EXACTLY from the review (max 20 words). A review may have no topic.
Answer with a JSON array only: [{{"id": "...", "topics": [{{"t": "t1", "q": "..."}}]}}]"""


def wilson(k, n, z=1.96):
    if n == 0:
        return (float("nan"),) * 3
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, c - h, c + h


def generate(rows):
    topics = []
    for i in range(0, len(rows), GEN_BATCH):
        b = [{"title": r["title"], "review": r["text"][:1500]} for r in rows[i:i + GEN_BATCH]]
        prompt = json.dumps({"current_topics": topics, "reviews": b}, ensure_ascii=False)
        try:
            new = [t for t in parse_json(complete("claude", SECOND, GEN, prompt)) if isinstance(t, dict) and t.get("name")]
            topics = new or topics
        except ValueError:
            pass
        print("gen batch", i // GEN_BATCH, len(topics), flush=True)
    return topics


def refine(topics):
    a = "\n".join(f"- {k}: {v}" for k, v in ASPECTS.items())
    raw = complete("claude", JUDGE, REFINE.format(aspects=a), json.dumps(topics, ensure_ascii=False))
    out = [t for t in parse_json(raw) if isinstance(t, dict) and t.get("id")]
    for t in out:
        if t.get("aspect") not in ASPECTS:
            t["aspect"] = "new"
    return out


def _assign_batch(system, rows, tids):
    payload = [{"id": r["review_id"], "title": r["title"], "review": r["text"][:3000]} for r in rows]
    try:
        got = {str(x.get("id")): x for x in parse_json(complete("claude", PRIMARY, system, json.dumps(payload, ensure_ascii=False)))
               if isinstance(x, dict)}
    except ValueError:
        got = {}
    out = []
    for r in rows:
        x = got.get(r["review_id"])
        full = r["title"] + " " + r["text"]
        ts = sorted({t["t"] for t in (x or {}).get("topics") or [] if isinstance(t, dict) and t.get("t") in tids and quote_ok(str(t.get("q", "")), full)})
        out.append({"review_id": r["review_id"], "parsed": x is not None, "topics": ts})
    return out


def main(source, n_gen=400, workers=12):
    out = os.path.join(HERE, "outputs", source)
    df = pd.read_parquet(os.path.join(out, "reviews.parquet"), columns=["review_id", "title", "text", "rating"])
    sample = pd.read_parquet(os.path.join(out, "label_sample.parquet"))
    used = set(sample.review_id)
    dt = os.path.join(out, "codebook", "dev_test_sample.parquet")
    if os.path.exists(dt):
        used |= set(pd.read_parquet(dt).review_id)
    pool = df[~df.review_id.isin(used)]
    gen = pool.groupby("rating", group_keys=False).apply(lambda g: g.sample(n=min(n_gen // 5, len(g)), random_state=7)).sample(frac=1, random_state=7)
    rows = gen.assign(title=gen.title.fillna("")).to_dict("records")
    raw_topics = generate(rows)
    topics = refine(raw_topics)
    tids = {t["id"] for t in topics}
    system = ASSIGN.format(topics="\n".join(f"- {t['id']}: {t['name']}: {t['description']}" for t in topics))
    ca = sample[sample["sample"] == "calib"]
    crow = ca.assign(title=ca.title.fillna(""))[["review_id", "title", "text"]].to_dict("records")
    batches = [crow[i:i + 20] for i in range(0, len(crow), 20)]
    assigned = []
    with ThreadPoolExecutor(workers) as ex:
        for part in ex.map(lambda b: _assign_batch(system, b, tids), batches):
            assigned.extend(part)
    ok = [a for a in assigned if a["parsed"]]
    n = len(ok)
    aspect_of = {t["id"]: t["aspect"] for t in topics}
    shares = []
    for t in topics:
        k = sum(t["id"] in a["topics"] for a in ok)
        p, lo, hi = wilson(k, n)
        shares.append(dict(t, n=k, share=p, lo=lo, hi=hi))
    with_topic = [a for a in ok if a["topics"]]
    covered = sum(all(aspect_of[t] != "new" for t in a["topics"]) for a in with_topic)
    any_new = sum(any(aspect_of[t] == "new" for t in a["topics"]) for a in with_topic)
    res = {"generation_reviews": len(rows), "raw_topics": len(raw_topics), "topics": sorted(shares, key=lambda x: -x["n"]),
           "calib_reviews": n, "reviews_with_topic": len(with_topic),
           "coverage_all_topics_mapped": wilson(covered, len(with_topic)),
           "share_with_new_topic": wilson(any_new, len(with_topic)),
           "aspects_without_topic": sorted(set(ASPECTS) - set(aspect_of.values()))}
    with open(os.path.join(out, "topicgpt.json"), "w") as f:
        json.dump(res, f, indent=2)
    with open(os.path.join(out, "topicgpt_assignments.jsonl"), "w") as f:
        for a in assigned:
            f.write(json.dumps(a) + "\n")
    L = [f"# TopicGPT coverage audit: {source}\n",
         f"{len(raw_topics)} topics generated from {len(rows)} reviews, refined to {len(topics)}; assigned to {n} random calib reviews "
         f"({len(with_topic)} with at least one topic).\n",
         f"- Reviews whose topics all map to an existing aspect: {100 * res['coverage_all_topics_mapped'][0]:.1f}% "
         f"(95% CI {100 * res['coverage_all_topics_mapped'][1]:.1f}–{100 * res['coverage_all_topics_mapped'][2]:.1f}%).",
         f"- Reviews with at least one topic outside the taxonomy: {100 * res['share_with_new_topic'][0]:.1f}% "
         f"(95% CI {100 * res['share_with_new_topic'][1]:.1f}–{100 * res['share_with_new_topic'][2]:.1f}%).\n",
         "| Topic | Maps to aspect | Share of reviews (95% CI) | Description |", "|---|---|---|---|"]
    for t in res["topics"]:
        L.append(f"| {t['name']} | {t['aspect']} | {100 * t['share']:.1f}% ({100 * t['lo']:.1f}–{100 * t['hi']:.1f}) | {t['description']} |")
    with open(os.path.join(out, "topicgpt.md"), "w") as f:
        f.write("\n".join(L) + "\n")
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("source"); ap.add_argument("--gen", type=int, default=400); ap.add_argument("--workers", type=int, default=12)
    a = ap.parse_args()
    r = main(a.source, a.gen, a.workers)
    print(open(os.path.join(HERE, "outputs", a.source, "topicgpt.md")).read())
