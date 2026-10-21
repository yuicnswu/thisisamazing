"""Category feasibility evidence that can be computed without the Amazon Reviews 2023 metadata files.

The G0 count (refined-thesis-plan §12.3) needs `meta_Beauty_and_Personal_Care.jsonl` and
`meta_Home_and_Kitchen.jsonl`, which neither the cloud container nor the Mac's sandboxed shell can download
(both answer 403). This script computes the two things that do not need them:

1. Sample size. How many independent products Algorithm 1 (theory.md, one item per product) needs to certify
   URR <= alpha with probability >= power, at the coverage the NeSy verifier reached in the pilot.
2. Review-side need rate. Share of early verified reviews (first 10 per product) that mention a checkable
   attribute, in All_Beauty and in Appliances (the only hard-goods review file available here; a stand-in for
   Home & Kitchen, not a substitute for counting it). Rule proxy only, same idea as g0_count.early_review_share.

Usage:  python category_check.py [PROJECT_FILES]   -> writes outputs/category_check.{json,md}
"""
from __future__ import annotations

import gzip
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict

from scipy.stats import binom

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "rq1_pilot"))
from attributes import find_values  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- 1. sample size

def certify_prob(n: int, r: float, alpha: float, delta: float) -> float:
    """P(exact binomial test of URR <= alpha passes at level delta) when n recommended items have true URR r."""
    # Largest k with P(Binom(n, alpha) <= k) <= delta.
    k_max = int(binom.ppf(delta, n, alpha))
    while k_max >= 0 and binom.cdf(k_max, n, alpha) > delta:
        k_max -= 1
    return float(binom.cdf(k_max, n, r)) if k_max >= 0 else 0.0


def min_recommended(r: float, alpha: float, delta: float, power: float) -> int:
    n = max(1, math.ceil(math.log(delta) / math.log(1 - alpha)))
    while certify_prob(n, r, alpha, delta) < power:
        n += 1 if n < 200 else max(1, n // 100)
    return n


def sample_size_table(delta=0.10, power=0.90, coverage=0.13, certify_share=0.5 * 0.8):
    """coverage: share of products the deployed matcher recommends (pilot NeSy: 12.7-13.1%).
    certify_share: share of all products that land in the certify half (cal 50%, of which 80% certify)."""
    rows = []
    for alpha in (0.05, 0.10):
        for r in (0.02, 0.03, 0.04):
            n_rec = min_recommended(r, alpha, delta, power)
            rows.append({"alpha": alpha, "true_urr": r, "recommended_items_needed": n_rec,
                         "products_needed": math.ceil(n_rec / (coverage * certify_share))})
    return rows


# ---------------------------------------------------------------- 2. review-side need rate

_APPLIANCE = {
    "fit_compat": [r"\b(?:fits?|fitted|works? (?:with|on|in)) (?:my|our) \w+", r"\bcompatible with\b", r"\bmodel (?:#|no\.?|number)",
                   r"\bpart (?:#|no\.?|number)", r"\breplacement for\b", r"\b(?:did(?:n'?t| not)|does(?:n'?t| not)|won'?t) fit\b", r"\bwrong size\b"],
    "dimensions": [r"\b\d+(?:\.\d+)?\s*(?:inch(?:es)?|in\.|\"|cm|mm|ft|feet|foot)\b"],
    "electrical": [r"\b\d+\s*(?:v|volts?|watts?|w|amps?)\b"],
    "capacity": [r"\b\d+(?:\.\d+)?\s*(?:cu\.?\s*ft|cubic feet|quarts?|qt|gallons?|cups?|liters?|litres?|oz)\b"],
}
_APPLIANCE_RE = {k: [re.compile(p, re.I) for p in v] for k, v in _APPLIANCE.items()}


def appliance_mentions(text: str) -> list[str]:
    return [k for k, ps in _APPLIANCE_RE.items() if any(p.search(text) for p in ps)]


def beauty_mentions(text: str) -> list[str]:
    return [a for a in ("skin_type", "hair_type", "scent", "free_from") if find_values(a, text)]


def _open(path):
    return gzip.open(path, "rt") if path.endswith(".gz") else open(path)


def early_review_stats(path: str, detector, k: int = 10) -> dict:
    by_item = defaultdict(list)
    n_reviews = 0
    with _open(path) as f:
        for line in f:
            r = json.loads(line)
            n_reviews += 1
            if r.get("verified_purchase"):
                by_item[r["parent_asin"]].append((r["timestamp"], (r.get("title") or "") + ". " + (r.get("text") or "")))
    n = hit = 0
    per = Counter()
    sizes = Counter()
    for items in by_item.values():
        sizes[min(len(items), 10)] += 1
        for _, t in sorted(items)[:k]:
            n += 1
            found = detector(t)
            hit += bool(found)
            per.update(found)
    n_items = len(by_item)
    return {"reviews": n_reviews, "products_with_verified": n_items,
            "products_ge10_verified": sizes[10], "share_products_ge10": sizes[10] / n_items if n_items else 0,
            "early_verified_reviews": n, "with_checkable_mention": hit, "share": hit / n if n else 0.0,
            "per_type": {kk: v / n for kk, v in per.most_common()}}


def main(root: str) -> dict:
    res = {"sample_size": sample_size_table()}
    beauty = os.path.join(root, "All_Beauty.jsonl")
    appl = os.path.join(root, "Appliances.jsonl.gz")
    if os.path.exists(beauty):
        res["all_beauty"] = early_review_stats(beauty, beauty_mentions)
    if os.path.exists(appl):
        res["appliances"] = early_review_stats(appl, appliance_mentions)
    os.makedirs(os.path.join(HERE, "outputs"), exist_ok=True)
    with open(os.path.join(HERE, "outputs", "category_check.json"), "w") as f:
        json.dump(res, f, indent=2)
    return res


if __name__ == "__main__":
    print(json.dumps(main(sys.argv[1] if len(sys.argv) > 1 else os.environ.get("PROJECT_FILES", "/mnt/project-files")),
                     indent=2))
