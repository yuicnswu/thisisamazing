"""Re-key committed label files to a locally parsed reviews.parquet.

review_id is a row number from parse.py, so two machines that parsed slightly different versions of the
code or file can number the same review differently. label_sample.parquet (committed) carries the natural
key (author_id, product_id, date); this script maps every committed label file and the dev/test sample to
the local ids, dropping the few reviews the local parse does not contain. Originals are kept as *.orig.

Usage: python remap_ids.py <source>
"""
from __future__ import annotations

import glob
import json
import os
import shutil
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
KEY = ["author_id", "product_id", "date"]


def main(source):
    out = os.path.join(HERE, "outputs", source)
    local = pd.read_parquet(os.path.join(out, "reviews.parquet"), columns=["review_id"] + KEY)
    frames = [pd.read_parquet(os.path.join(out, "label_sample.parquet"))]
    dt = os.path.join(out, "codebook", "dev_test_sample.parquet")
    if os.path.exists(dt):
        frames.append(pd.read_parquet(dt))
    keyed = pd.concat([f[["review_id"] + KEY] for f in frames]).drop_duplicates("review_id")
    m = keyed.merge(local.rename(columns={"review_id": "new_id"}), on=KEY, how="left")
    mapping = dict(zip(m.review_id, m.new_id))
    print(f"{m.new_id.notna().mean():.4%} of labelled reviews found locally")
    for path in [os.path.join(out, "label_sample.parquet")] + ([dt] if os.path.exists(dt) else []):
        if not os.path.exists(path + ".orig"):
            shutil.copy(path, path + ".orig")
        d = pd.read_parquet(path + ".orig")
        d["review_id"] = d.review_id.map(mapping)
        d[d.review_id.notna()].to_parquet(path, index=False)
    for path in glob.glob(os.path.join(out, "labels_*.jsonl")) + glob.glob(os.path.join(out, "codebook", "*.jsonl")):
        if not os.path.exists(path + ".orig"):
            shutil.copy(path, path + ".orig")
        with open(path + ".orig") as f, open(path, "w") as g:
            for line in f:
                r = json.loads(line)
                new = mapping.get(r["review_id"])
                if isinstance(new, str):
                    r["review_id"] = new
                    g.write(json.dumps(r) + "\n")


if __name__ == "__main__":
    main(sys.argv[1])
