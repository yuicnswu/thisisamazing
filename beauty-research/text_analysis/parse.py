"""Step 1. Parse review files into one clean table, the same for Amazon and Sephora.

Columns: review_id, source, product_id, author_id, rating, title, text, date, skin_type,
is_recommended, category, n_chars, n_tokens. Exact duplicates (same author, product, rating, title,
text and date) are dropped, keeping the first. Reviews with no text after cleaning are dropped.

Usage:
  python parse.py amazon /mnt/project-files/All_Beauty.jsonl
  python parse.py sephora ~/Downloads/archive          # folder with product_info.csv, reviews_*.csv
Writes outputs/<source>/reviews.parquet and outputs/<source>/parse_summary.json.
"""
from __future__ import annotations

import glob
import html
import json
import os
import re
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
_TAG = re.compile(r"<[^>]+>")
_WS = re.compile(r"\s+")
_TOKEN = re.compile(r"[a-z]+(?:'[a-z]+)?")


def clean_text(s) -> str:
    if not isinstance(s, str):
        return ""
    s = html.unescape(s)
    s = _TAG.sub(" ", s)
    return _WS.sub(" ", s).strip()


def tokens(s: str) -> list[str]:
    return _TOKEN.findall(s.lower())


def load_amazon(path: str) -> pd.DataFrame:
    rows = []
    with open(path) as f:
        for line in f:
            r = json.loads(line)
            rows.append((r["parent_asin"], r["user_id"], r["rating"], r.get("title"), r.get("text"),
                         r["timestamp"], r.get("verified_purchase")))
    df = pd.DataFrame(rows, columns=["product_id", "author_id", "rating", "title", "text", "ts", "verified"])
    df["date"] = pd.to_datetime(df.pop("ts"), unit="ms", utc=True)
    df["skin_type"] = None
    df["is_recommended"] = float("nan")
    df["category"] = None
    return df


def load_sephora(folder: str) -> pd.DataFrame:
    folder = os.path.expanduser(folder)
    prod = pd.read_csv(os.path.join(folder, "product_info.csv"),
                       usecols=["product_id", "primary_category", "secondary_category", "tertiary_category"])
    parts = sorted(glob.glob(os.path.join(folder, "reviews_*.csv")))
    if not parts:
        raise FileNotFoundError(f"no reviews_*.csv in {folder}")
    df = pd.concat([pd.read_csv(p, dtype={"author_id": str}, low_memory=False) for p in parts], ignore_index=True)
    df = df.merge(prod, on="product_id", how="left")
    df = df.rename(columns={"review_title": "title", "review_text": "text"})
    df["date"] = pd.to_datetime(df["submission_time"], utc=True, errors="coerce")
    df["category"] = df["secondary_category"].fillna(df["primary_category"])
    df["tertiary_category"] = df["tertiary_category"]
    df["verified"] = None
    keep = ["product_id", "author_id", "rating", "title", "text", "date", "verified", "skin_type",
            "is_recommended", "category", "tertiary_category"]
    return df[keep]


def finalise(df: pd.DataFrame, source: str) -> tuple[pd.DataFrame, dict]:
    n_raw = len(df)
    df["title"] = df["title"].map(clean_text)
    df["text"] = df["text"].map(clean_text)
    key = ["author_id", "product_id", "rating", "title", "text", "date"]
    dup = df.duplicated(key, keep="first")
    df = df[~dup]
    empty = df["text"].str.len() == 0
    df = df[~empty].reset_index(drop=True)
    df.insert(0, "source", source)
    df.insert(0, "review_id", [f"{source[:2]}{i:07d}" for i in range(len(df))])
    df["n_chars"] = df["text"].str.len()
    df["n_tokens"] = df["text"].map(lambda s: len(tokens(s)))
    summary = {"source": source, "raw_rows": n_raw, "exact_duplicates_dropped": int(dup.sum()),
               "empty_text_dropped": int(empty.sum()), "reviews": len(df),
               "products": int(df.product_id.nunique()), "authors": int(df.author_id.nunique()),
               "date_min": str(df.date.min()), "date_max": str(df.date.max()),
               "median_tokens": float(df.n_tokens.median()),
               "rating_share": {str(k): round(v, 4) for k, v in df.rating.value_counts(normalize=True).sort_index().items()}}
    return df, summary


def main(source: str, path: str) -> dict:
    df = load_amazon(path) if source == "amazon" else load_sephora(path)
    df, summary = finalise(df, source)
    out = os.path.join(HERE, "outputs", source)
    os.makedirs(out, exist_ok=True)
    df.to_parquet(os.path.join(out, "reviews.parquet"), index=False)
    with open(os.path.join(out, "parse_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)
    return summary


if __name__ == "__main__":
    print(json.dumps(main(sys.argv[1], sys.argv[2]), indent=2))
