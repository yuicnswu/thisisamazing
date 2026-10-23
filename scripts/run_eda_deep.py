import csv
import datetime
import html
import json
import math
import os
import re
from collections import Counter, defaultdict

import argparse

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--input", default=os.path.join(REPO_ROOT, "data/hackathon_beauty_gmv.csv"), help="pre-dedup cohort CSV")
parser.add_argument("--out-dir", default=os.path.join(REPO_ROOT, "eda_outputs"), help="output directory")
parser.add_argument("--dedup-out", default=os.path.join(REPO_ROOT, "hackathon_beauty_gmv_dedup.csv"), help="deduplicated cohort CSV to write")
args = parser.parse_args()

input_csv = args.input
out_dir = args.out_dir
os.makedirs(out_dir, exist_ok=True)

raw_rows = []
with open(input_csv, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for r in reader:
        raw_rows.append(r)

raw_N = len(raw_rows)

# Deduplicate on (user_id, parent_asin) keeping earliest timestamp, and also verify prior history doesn't contain same parent_asin
seen_user_pasin = set()
dedup_rows = []
# Sort by timestamp first
raw_rows.sort(key=lambda x: int(x["timestamp"]))
for r in raw_rows:
    key = (r["user_id"], r["parent_asin"])
    if key in seen_user_pasin:
        continue
    seen_user_pasin.add(key)
    dedup_rows.append(r)

N = len(dedup_rows)
print(f"Raw rows: {raw_N} | Deduplicated on (user_id, parent_asin): {N} (removed {raw_N - N} multi-variant duplicate rows)")

# Save cleaned deduplicated CSV back to scratch
clean_csv = args.dedup_out
with open(clean_csv, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(dedup_rows)

evidence_cols = [
    "item_form",
    "skin_type",
    "hair_type",
    "scent",
    "product_benefits",
    "material_type_free",
    "active_ingredients",
]

persuasive_pattern = re.compile(
    r"\b(miracle|instant|instantly|magic|revolutionary|best|ultimate|perfect|flawless|luxury|luxurious|guaranteed|amazing|incredible|super|transform|transforms|youthful|radiant|salon-quality|professional|secret|diva|dynamo)\b",
    re.IGNORECASE,
)

need_keywords = {
    "sensitive_skin": re.compile(r"\b(sensitive|irritat\w*|gentle|hypoallergenic|redness)\b", re.I),
    "dry_skin_or_hair": re.compile(r"\b(dry|moistur\w*|hydrat\w*|flak\w*|chapped)\b", re.I),
    "curly_wavy_hair": re.compile(r"\b(curl\w*|wavy|friz\w*|coils?)\b", re.I),
    "fine_thin_hair": re.compile(r"\b(fine hair|thin hair|volum\w*|limp)\b", re.I),
    "clean_chemical_free": re.compile(
        r"\b(natural|organic|sulfate[- ]?free|paraben[- ]?free|formaldehyde|chemical\w*|cruelty[- ]?free|vegan)\b",
        re.I,
    ),
    "fragrance_sensitive": re.compile(r"\b(unscented|fragrance[- ]?free|odorless|strong smell|overpowering)\b", re.I),
}

rows = dedup_rows
for r in rows:
    ts_sec = int(r["timestamp"]) / 1000.0
    dt = datetime.datetime.fromtimestamp(ts_sec, tz=datetime.timezone.utc)
    r["_year"] = dt.year
    r["_date"] = dt.strftime("%Y-%m-%d")
    r["_price"] = float(r["price_usd"])
    r["_rating"] = float(r["rating"])
    r["_sat_gmv"] = float(r["satisfied_gmv"])
    r["_reg_gmv"] = float(r["regret_gmv"])
    r["_prior_u"] = int(r["user_prior_reviews_count"])
    r["_prior_p"] = int(r["product_prior_reviews_at_purchase"])
    r["_meta_rn"] = int(r["meta_rating_number"]) if r["meta_rating_number"] else 0
    r["_meta_ar"] = float(r["meta_average_rating"]) if r["meta_average_rating"] else 0.0
    r["_vp"] = r["verified_purchase"] == "True"

    ev_struct_cnt = sum(1 for c in evidence_cols if r[c].strip() != "")
    has_feat = 1 if r["features_text"].strip() != "" else 0
    try:
        det_dict = json.loads(r["details_json"]) if r["details_json"] else {}
    except Exception:
        det_dict = {}
    trivial_keys = {
        "UPC",
        "Item model number",
        "Package Dimensions",
        "Product Dimensions",
        "Manufacturer",
        "Is Discontinued By Manufacturer",
        "Date First Available",
        "ASIN",
    }
    substantive_det_keys = [k for k in det_dict.keys() if k not in trivial_keys]
    r["_ev_struct_cnt"] = ev_struct_cnt
    r["_substantive_det_cnt"] = len(substantive_det_keys)
    r["_has_feat"] = has_feat

    listing_copy = f"{r['product_title']} {r['features_text']} {r['description_text']}"
    r["_hype_words"] = len(persuasive_pattern.findall(listing_copy))
    r["_listing_words"] = len(listing_copy.split())

    u_hist = r["user_prior_history_text"]
    listing_ev_text = " ".join(
        [
            r["features_text"],
            r["details_json"],
            r["item_form"],
            r["skin_type"],
            r["hair_type"],
            r["scent"],
            r["product_benefits"],
            r["material_type_free"],
            r["active_ingredients"],
        ]
    )
    user_needs_found = []
    supported_needs = []
    for nk, pat in need_keywords.items():
        if pat.search(u_hist):
            user_needs_found.append(nk)
            if pat.search(listing_ev_text):
                supported_needs.append(nk)
    r["_user_needs_cnt"] = len(user_needs_found)
    r["_supported_needs_cnt"] = len(supported_needs)
    if len(user_needs_found) == 0:
        r["_need_match_status"] = "4. No Explicit Keyword Need in Prior"
    elif len(supported_needs) == len(user_needs_found):
        r["_need_match_status"] = "1. All Stated Needs Supported in Listing"
    elif len(supported_needs) > 0:
        r["_need_match_status"] = "2. Partially Supported in Listing"
    else:
        r["_need_match_status"] = "3. Missing Evidence for Stated Needs"

# Check how unverified reviews concentrate in Cold-Start Launch!
print("\n=== LAUNCH STAGE x VERIFIED PURCHASE SHARE ===")
launch_groups = defaultdict(list)
for r in rows:
    p = r["_prior_p"]
    if p == 0:
        b = "1. Day-1 Launch (0 prior reviews)"
    elif p <= 4:
        b = "2. Early Launch (1-4 prior reviews)"
    elif p <= 9:
        b = "3. Cold-Start Window (5-9 prior reviews)"
    elif p <= 49:
        b = "4. Growth Stage (10-49 prior reviews)"
    else:
        b = "5. Established (50+ prior reviews)"
    launch_groups[b].append(r)

for b in sorted(launch_groups.keys()):
    grp = launch_groups[b]
    vp_grp = [r for r in grp if r["_vp"]]
    unvp_grp = [r for r in grp if not r["_vp"]]
    vp_share = len(vp_grp) / len(grp) * 100
    vp_sat = sum(1 for r in vp_grp if r["_rating"] >= 4.0) / max(len(vp_grp), 1) * 100
    vp_reg = sum(1 for r in vp_grp if r["_rating"] <= 2.0) / max(len(vp_grp), 1) * 100
    unvp_sat = sum(1 for r in unvp_grp if r["_rating"] >= 4.0) / max(len(unvp_grp), 1) * 100
    print(
        f"{b:42s} | Total={len(grp):4d} | Unverified(Vine/Promo)%={100-vp_share:5.1f}% | Verified Sat%={vp_sat:5.1f}% | Verified Regret%={vp_reg:5.1f}% | Unverified Sat%={unvp_sat:5.1f}%"
    )

# Check Verified Purchases Only: Hype vs Evidence (RQ1 & RQ2)
vp_rows = [r for r in rows if r["_vp"]]
print(f"\n=== VERIFIED PURCHASES ONLY (n={len(vp_rows)}) : HYPE x EVIDENCE (RQ1 & RQ2) ===")
hype_ev_groups = defaultdict(list)
for r in vp_rows:
    high_ev = r["_ev_struct_cnt"] >= 3 and r["_has_feat"] == 1
    low_ev = r["_ev_struct_cnt"] <= 1 and r["_has_feat"] == 0
    high_hype = r["_hype_words"] >= 2
    if high_ev and not high_hype:
        k = "1. High Evidence + Low/Factual Hype"
    elif high_ev and high_hype:
        k = "2. High Evidence + High Persuasive Hype"
    elif low_ev and not high_hype:
        k = "3. Low/Missing Evidence + Low Hype"
    elif low_ev and high_hype:
        k = "4. Low/Missing Evidence + High Persuasive Hype"
    else:
        k = "5. Moderate Evidence Mix"
    hype_ev_groups[k].append(r)

for k in sorted(hype_ev_groups.keys()):
    g = hype_ev_groups[k]
    gmv = sum(r["_price"] for r in g)
    sat = sum(1 for r in g if r["_rating"] >= 4.0) / len(g) * 100
    reg = sum(1 for r in g if r["_rating"] <= 2.0) / len(g) * 100
    reg_gmv = sum(r["_reg_gmv"] for r in g) / max(gmv, 1) * 100
    print(f"{k:48s} | n={len(g):5d} | GMV=${gmv:10,.2f} | Sat%={sat:5.1f}% | Regret%={reg:5.1f}% | RegretGMV%={reg_gmv:5.1f}%")

# Check Verified Purchases Only: Customer Need Alignment
print(f"\n=== VERIFIED PURCHASES ONLY (n={len(vp_rows)}) : CUSTOMER NEED SUPPORT (RQ2 -> RQ3) ===")
need_groups = defaultdict(list)
for r in vp_rows:
    need_groups[r["_need_match_status"]].append(r)

for k in sorted(need_groups.keys()):
    g = need_groups[k]
    gmv = sum(r["_price"] for r in g)
    sat = sum(1 for r in g if r["_rating"] >= 4.0) / len(g) * 100
    reg = sum(1 for r in g if r["_rating"] <= 2.0) / len(g) * 100
    reg_gmv = sum(r["_reg_gmv"] for r in g) / max(gmv, 1) * 100
    print(f"{k:48s} | n={len(g):5d} | GMV=${gmv:10,.2f} | Sat%={sat:5.1f}% | Regret%={reg:5.1f}% | RegretGMV%={reg_gmv:5.1f}%")

# Check Cold-Start Verified Purchases Only: Customer Need Alignment
cold_vp_rows = [r for r in vp_rows if r["_prior_p"] < 10]
print(f"\n=== COLD-START LAUNCH VERIFIED PURCHASES ONLY (n={len(cold_vp_rows)}) : CUSTOMER NEED SUPPORT ===")
c_need_groups = defaultdict(list)
for r in cold_vp_rows:
    c_need_groups[r["_need_match_status"]].append(r)

for k in sorted(c_need_groups.keys()):
    g = c_need_groups[k]
    gmv = sum(r["_price"] for r in g)
    sat = sum(1 for r in g if r["_rating"] >= 4.0) / len(g) * 100
    reg = sum(1 for r in g if r["_rating"] <= 2.0) / len(g) * 100
    reg_gmv = sum(r["_reg_gmv"] for r in g) / max(gmv, 1) * 100
    print(f"{k:48s} | n={len(g):5d} | GMV=${gmv:10,.2f} | Sat%={sat:5.1f}% | Regret%={reg:5.1f}% | RegretGMV%={reg_gmv:5.1f}%")

# Missingness profile print
print("\n=== MISSINGNESS OF KEY EVIDENCE & PRIOR FIELDS (N=15,606 deduped) ===")
for col in [
    "store_brand",
    "price_usd",
    "meta_average_rating",
    "meta_rating_number",
    "features_text",
    "description_text",
    "item_form",
    "skin_type",
    "hair_type",
    "scent",
    "product_benefits",
    "material_type_free",
    "active_ingredients",
    "details_json",
]:
    miss = sum(1 for r in rows if r[col].strip() == "" or r[col].strip() == "{}")
    print(f"{col:24s} | missing={miss:5d} ({miss/N*100:5.1f}%) | present={N-miss:5d} ({(N-miss)/N*100:5.1f}%)")
