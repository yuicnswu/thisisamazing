import csv
import json
import os
import sys

import argparse

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--reviews", default=os.path.join(REPO_ROOT, "data/raw/All_Beauty.jsonl"), help="raw reviews JSONL")
parser.add_argument("--out-csv", default=os.path.join(REPO_ROOT, "data/raw/All_Beauty.csv"), help="full reviews CSV to write")
parser.add_argument("--sample-dir", default=os.path.join(REPO_ROOT, "."), help="directory for the 1,000-row sample")
args = parser.parse_args()

src_path = args.reviews
full_csv_path = args.out_csv
sample_dir = args.sample_dir
os.makedirs(sample_dir, exist_ok=True)
sample_csv_path = os.path.join(sample_dir, "All_Beauty_sample_1000.csv")

fieldnames = [
    "rating",
    "title",
    "text",
    "images",
    "asin",
    "parent_asin",
    "user_id",
    "timestamp",
    "helpful_vote",
    "verified_purchase",
]

total_rows = 0
with (
    open(src_path, "r", encoding="utf-8") as infile,
    open(full_csv_path, "w", newline="", encoding="utf-8") as full_out,
    open(sample_csv_path, "w", newline="", encoding="utf-8") as sample_out,
):
    full_writer = csv.DictWriter(full_out, fieldnames=fieldnames, extrasaction="ignore")
    sample_writer = csv.DictWriter(sample_out, fieldnames=fieldnames, extrasaction="ignore")
    full_writer.writeheader()
    sample_writer.writeheader()

    for line in infile:
        line = line.strip()
        if not line:
            continue
        record = json.loads(line)
        if isinstance(record.get("images"), (list, dict)):
            record["images"] = json.dumps(record["images"])
        full_writer.writerow(record)
        if total_rows < 1000:
            sample_writer.writerow(record)
        total_rows += 1

print(f"Converted {total_rows} rows.")
print(f"Full CSV: {full_csv_path} ({os.path.getsize(full_csv_path) / (1024*1024):.2f} MB)")
print(f"Sample CSV (1000 rows): {sample_csv_path} ({os.path.getsize(sample_csv_path) / 1024:.2f} KB)")
