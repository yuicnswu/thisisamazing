"""Step 3. LLM aspect-based sentiment labels on two samples, with verbatim-quote checks.

Samples (drawn once, seeded, saved):
  train : stratified by star rating (equal per star), used to train the scaled classifier (step 4).
  calib : simple random sample of the corpus, never used for training. Its LLM labels are the
          "gold" side of prediction-powered inference, so its estimates are unbiased for the corpus.

For each review the model returns the aspects it discusses, a polarity per aspect, and a verbatim
quote. A label is kept only if its quote occurs in the review text (case- and space-insensitive);
otherwise it is dropped and counted. A second model labels a random subset for agreement.

Usage: python label.py <source> [--train 2000] [--calib 1500] [--agree 400] [--workers 4]
Writes outputs/<source>/labels_<sample>__<model>.jsonl and labels_summary.json.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault("LLM_CACHE", os.path.join(HERE, "outputs", "llm_cache.jsonl"))
sys.path.insert(0, os.path.join(HERE, "..", "..", "04-implementation", "rq1_pilot"))
from llm import complete, parse_json  # noqa: E402

from aspects import ASPECTS, CONTEXT  # noqa: E402

PRIMARY = "claude-haiku-5-5"
SECOND = "claude-sonnet-5-5"
BATCH = 20

SYSTEM = """You annotate beauty and personal-care product reviews for aspect-based sentiment analysis.
Use only the review text. Do not infer what is not written.

Aspects (use these ids only):
{aspects}

For each review return every aspect the reviewer actually comments on, with:
- "a": aspect id
- "p": "pos", "neg" or "mixed" (the reviewer's evaluation of that aspect)
- "q": a short quote copied EXACTLY, character for character, from the review that shows it (max 25 words)
Also return "ctx": the customer-context ids the reviewer states about themselves (may be empty):
{context}

Rules: a general verdict with no aspect ("love it", "great product") gets aspect "overall". Do not tag an
aspect only because a word appears; the reviewer must evaluate it. Quotes must be verbatim.
Answer with a JSON array only: [{{"id": "...", "labels": [{{"a": "...", "p": "...", "q": "..."}}], "ctx": ["..."]}}]"""


def system_prompt(rules: list[str] | None = None) -> str:
    """The annotation guide. `rules` are the clarifications learned by codebook.py (self-refining loop)."""
    a = "\n".join(f"- {k}: {v}" for k, v in ASPECTS.items())
    c = "\n".join(f"- {k}: {v}" for k, v in CONTEXT.items())
    s = SYSTEM.format(aspects=a, context=c)
    if rules:
        s += "\n\nAdditional rules (from adjudicated disagreements):\n" + "\n".join(f"{i}. {r}" for i, r in enumerate(rules, 1))
    return s


_norm = lambda s: re.sub(r"\s+", " ", s.lower()).strip()


def quote_ok(q: str, text: str) -> bool:
    q = _norm(q).strip(" .,!\"'")
    return bool(q) and q in _norm(text)


def draw_samples(df: pd.DataFrame, n_train: int, n_calib: int, seed: int = 0) -> pd.DataFrame:
    calib = df.sample(n=n_calib, random_state=seed)
    rest = df.drop(calib.index)
    per = n_train // 5
    train = rest.groupby("rating", group_keys=False).apply(lambda g: g.sample(n=min(per, len(g)), random_state=seed))
    return pd.concat([train.assign(sample="train"), calib.assign(sample="calib")])


def check_labels(x: dict | None, r: dict) -> dict:
    """Keep only valid aspect/polarity labels whose quote is verbatim in the review."""
    rec = {"review_id": r["review_id"], "parsed": x is not None, "labels": [], "ctx": [], "dropped_quotes": 0}
    if x:
        full = (r.get("title") or "") + " " + r["text"]
        for lab in x.get("labels") or []:
            if lab.get("a") not in ASPECTS or lab.get("p") not in ("pos", "neg", "mixed"):
                continue
            if quote_ok(str(lab.get("q", "")), full):
                rec["labels"].append({"a": lab["a"], "p": lab["p"], "q": lab["q"]})
            else:
                rec["dropped_quotes"] += 1
        rec["ctx"] = sorted({c for c in x.get("ctx") or [] if c in CONTEXT})
    return rec


def label_batch(model: str, rows: list[dict], rules: list[str] | None = None) -> list[dict]:
    payload = [{"id": r["review_id"], "title": r["title"], "review": r["text"][:3000]} for r in rows]
    prompt = "Annotate these reviews:\n" + json.dumps(payload, ensure_ascii=False)
    raw = complete("claude", model, system_prompt(rules), prompt)
    try:
        got = {str(x.get("id")): x for x in parse_json(raw) if isinstance(x, dict)}
    except ValueError:
        got = {}
    return [check_labels(got.get(r["review_id"]), r) for r in rows]


def run(model: str, rows: list[dict], workers: int, rules: list[str] | None = None) -> list[dict]:
    batches = [rows[i:i + BATCH] for i in range(0, len(rows), BATCH)]
    res = []
    with ThreadPoolExecutor(workers) as ex:
        for part in ex.map(lambda b: label_batch(model, b, rules), batches):
            res.extend(part)
    return res


def main(source, n_train=2000, n_calib=1500, n_agree=400, workers=4):
    out = os.path.join(HERE, "outputs", source)
    spath = os.path.join(out, "label_sample.parquet")
    if os.path.exists(spath):
        sample = pd.read_parquet(spath)
    else:
        df = pd.read_parquet(os.path.join(out, "reviews.parquet"))
        sample = draw_samples(df, n_train, n_calib)
        sample.to_parquet(spath, index=False)
    summary = {}
    for name in ("train", "calib"):
        rows = sample[sample["sample"] == name].to_dict("records")
        recs = run(PRIMARY, rows, workers)
        with open(os.path.join(out, f"labels_{name}__{PRIMARY}.jsonl"), "w") as f:
            for r in recs:
                f.write(json.dumps(r) + "\n")
        kept = sum(len(r["labels"]) for r in recs)
        drop = sum(r["dropped_quotes"] for r in recs)
        summary[name] = {"reviews": len(recs), "parsed": sum(r["parsed"] for r in recs),
                         "labels_kept": kept, "labels_dropped_nonverbatim": drop,
                         "verbatim_rate": round(kept / (kept + drop), 4) if kept + drop else None}
    agree_rows = sample[sample["sample"] == "calib"].head(n_agree).to_dict("records")
    recs2 = run(SECOND, agree_rows, workers)
    with open(os.path.join(out, f"labels_agree__{SECOND}.jsonl"), "w") as f:
        for r in recs2:
            f.write(json.dumps(r) + "\n")
    summary["agree"] = {"reviews": len(recs2), "model": SECOND}
    with open(os.path.join(out, "labels_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)
    return summary


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("source"); ap.add_argument("--train", type=int, default=2000)
    ap.add_argument("--calib", type=int, default=1500); ap.add_argument("--agree", type=int, default=400)
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    print(json.dumps(main(a.source, a.train, a.calib, a.agree, a.workers), indent=2))
