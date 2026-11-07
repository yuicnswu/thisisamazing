import csv
import re
from collections import Counter

import argparse
import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--input", default=os.path.join(REPO_ROOT, "hackathon_beauty_gmv_dedup.csv"), help="deduplicated cohort CSV")
args = parser.parse_args()

clean_csv = args.input
with open(clean_csv, "r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

vp_rows = [r for r in rows if r["verified_purchase"] == "True"]
regret_rows = [r for r in vp_rows if float(r["rating"]) <= 2.0]
sat_rows = [r for r in vp_rows if float(r["rating"]) >= 4.0]

print(f"Verified purchases: {len(vp_rows)} | Verified Regret (<=2*): {len(regret_rows)} | Verified Sat (>=4*): {len(sat_rows)}")

# Failure mode taxonomy in regret_rows review_text + review_title
failure_modes = {
    "1. Ineffective / Claimed Benefit Failed": re.compile(
        r"\b(didn'?t work|does not work|doesn'?t work|no difference|useless|waste of money|nothing|not effective|didn'?t do anything|zero results)\b",
        re.I,
    ),
    "2. Physical Form / Texture / Consistency Mismatch": re.compile(
        r"\b(sticky|greasy|watery|too thick|too thin|clump\w*|runny|powder|paste|dry|dried out|hard to apply|cakey|oily|heavy|residue)\b",
        re.I,
    ),
    "3. Scent / Fragrance / Chemical / Skin Reaction": re.compile(
        r"\b(smell\w*|scent|odor|stink\w*|perfume|fragrance|burn\w*|irritat\w*|rash|broke me out|allergic|itch\w*|formaldehyde|chemical\w*|alcohol|sting\w*)\b",
        re.I,
    ),
    "4. Misleading Listing / Expectation Mismatch": re.compile(
        r"\b(misleading|not as described|pictured|expected|thought it was|false|fake|deceptive|disappointed|not what i|wrong|tiny|small)\b",
        re.I,
    ),
    "5. Defective Packaging / Pump / Applicator": re.compile(
        r"\b(broke|broken|leak\w*|pump|sprayer|bottle|cap|nozzle|stopped working|defective|arrived open)\b",
        re.I,
    ),
}

mode_counts = Counter()
mode_gmv = Counter()
any_matched = 0
for r in regret_rows:
    txt = f"{r['review_title']} {r['review_text']}"
    p = float(r["price_usd"])
    hit = False
    for mname, pat in failure_modes.items():
        if pat.search(txt):
            mode_counts[mname] += 1
            mode_gmv[mname] += p
            hit = True
    if hit:
        any_matched += 1

print(f"\n=== WHY 1 EVIDENCE: Post-Purchase Regret Failure Modes (n={len(regret_rows)} verified <=2* reviews) ===")
for mname in sorted(failure_modes.keys()):
    c = mode_counts[mname]
    g = mode_gmv[mname]
    print(f"  {mname:52s}: {c:4d} ({c/len(regret_rows)*100:5.1f}%) | Regret GMV = ${g:9,.2f}")
print(f"  Any identifiable mismatch/defect pattern            : {any_matched:4d} ({any_matched/len(regret_rows)*100:5.1f}%)")

# Why 4 evidence: Popularity concentration of GMV
total_vp_gmv = sum(float(r["price_usd"]) for r in vp_rows)
pop_100_gmv = sum(float(r["price_usd"]) for r in vp_rows if int(r["meta_rating_number"] or 0) >= 100)
pop_1000_gmv = sum(float(r["price_usd"]) for r in vp_rows if int(r["meta_rating_number"] or 0) >= 1000)
print(f"\n=== WHY 4 EVIDENCE: GMV Concentration in Popularity Priors ===")
print(f"  Total Verified GMV: ${total_vp_gmv:,.2f}")
print(f"  GMV in products with >=100 ratings:  ${pop_100_gmv:,.2f} ({pop_100_gmv/total_vp_gmv*100:.1f}%)")
print(f"  GMV in products with >=1000 ratings: ${pop_1000_gmv:,.2f} ({pop_1000_gmv/total_vp_gmv*100:.1f}%)")
