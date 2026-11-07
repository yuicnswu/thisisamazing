import csv
import datetime
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
args = parser.parse_args()

input_csv = args.input
out_dir = args.out_dir
os.makedirs(out_dir, exist_ok=True)

rows = []
with open(input_csv, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for r in reader:
        rows.append(r)

N = len(rows)
print(f"Loaded {N} rows and {len(fieldnames)} columns from {input_csv}")

# Helper for quantiles
def compute_stats(vals):
    s = sorted(vals)
    n = len(s)
    if n == 0:
        return {}
    mean = sum(s) / n
    var = sum((x - mean) ** 2 for x in s) / n
    std = math.sqrt(var)

    def q(p):
        idx = p * (n - 1)
        lo = int(math.floor(idx))
        hi = int(math.ceil(idx))
        if lo == hi:
            return s[lo]
        return s[lo] + (idx - lo) * (s[hi] - s[lo])

    p25, p75 = q(0.25), q(0.75)
    iqr = p75 - p25
    outliers_hi = sum(1 for x in s if x > p75 + 1.5 * iqr)
    return {
        "count": n,
        "min": round(s[0], 2),
        "p1": round(q(0.01), 2),
        "p5": round(q(0.05), 2),
        "p25": round(p25, 2),
        "p50": round(q(0.50), 2),
        "p75": round(p75, 2),
        "p95": round(q(0.95), 2),
        "p99": round(q(0.99), 2),
        "max": round(s[-1], 2),
        "mean": round(mean, 2),
        "std": round(std, 2),
        "iqr_outliers_hi": outliers_hi,
    }


# 1. Missingness, Cardinality, Duplicate check
pk_counter = Counter((r["user_id"], r["parent_asin"], r["timestamp"]) for r in rows)
dup_pk = sum(v - 1 for v in pk_counter.values() if v > 1)
user_asin_counter = Counter((r["user_id"], r["parent_asin"]) for r in rows)
dup_user_asin = sum(v - 1 for v in user_asin_counter.values() if v > 1)

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

# Enrich rows in memory for analysis
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

    # Evidence richness count (0..7 structured cols + features + details count)
    ev_struct_cnt = sum(1 for c in evidence_cols if r[c].strip() != "")
    has_feat = 1 if r["features_text"].strip() != "" else 0
    try:
        det_dict = json.loads(r["details_json"]) if r["details_json"] else {}
    except Exception:
        det_dict = {}
    # Count non-trivial detail keys (excluding UPC, Item model number, Package Dimensions, Product Dimensions, Manufacturer, Is Discontinued)
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
    r["_evidence_score"] = ev_struct_cnt + has_feat + min(len(substantive_det_keys), 3)

    # Persuasive hype word count in listing
    listing_copy = f"{r['product_title']} {r['features_text']} {r['description_text']}"
    r["_hype_words"] = len(persuasive_pattern.findall(listing_copy))
    r["_listing_words"] = len(listing_copy.split())

    # Check user need alignment with listing evidence
    u_hist = r["user_prior_history_text"]
    listing_ev_text = " ".join(
        [r["features_text"], r["details_json"], r["item_form"], r["skin_type"], r["hair_type"], r["scent"], r["product_benefits"], r["material_type_free"], r["active_ingredients"]]
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
        r["_need_match_status"] = "No Explicit Keyword Need in Prior"
    elif len(supported_needs) == len(user_needs_found):
        r["_need_match_status"] = "All Stated Needs Supported in Listing"
    elif len(supported_needs) > 0:
        r["_need_match_status"] = "Partially Supported in Listing"
    else:
        r["_need_match_status"] = "Missing Evidence for Stated Needs"

# Write Field Profile CSV
profile_rows = []
for col in fieldnames:
    non_empty = [r[col] for r in rows if r[col] != "" and r[col] is not None]
    miss_cnt = N - len(non_empty)
    miss_pct = round(miss_cnt / N * 100, 2)
    uniq_cnt = len(set(non_empty))
    top_val = Counter(non_empty).most_common(1)[0][0][:50] if non_empty else ""
    profile_rows.append(
        {
            "column": col,
            "missing_count": miss_cnt,
            "missing_pct": miss_pct,
            "unique_count": uniq_cnt,
            "most_frequent_sample": top_val,
        }
    )

with open(os.path.join(out_dir, "eda_data_profile.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(
        f, fieldnames=["column", "missing_count", "missing_pct", "unique_count", "most_frequent_sample"]
    )
    w.writeheader()
    w.writerows(profile_rows)

# Numeric quantiles table
numeric_metrics = [
    ("price_usd (Order GMV $)", [r["_price"] for r in rows]),
    ("rating (1-5 Stars)", [r["_rating"] for r in rows]),
    ("user_prior_reviews_count", [r["_prior_u"] for r in rows]),
    ("product_prior_reviews_at_purchase", [r["_prior_p"] for r in rows]),
    ("meta_rating_number (Popularity Prior)", [r["_meta_rn"] for r in rows]),
    ("meta_average_rating (Rating Prior)", [r["_meta_ar"] for r in rows]),
    ("evidence_struct_cols_count (0-7)", [r["_ev_struct_cnt"] for r in rows]),
    ("substantive_detail_keys_count", [r["_substantive_det_cnt"] for r in rows]),
    ("listing_hype_words_count", [r["_hype_words"] for r in rows]),
]

quantile_rows = []
for name, vals in numeric_metrics:
    st = compute_stats(vals)
    st["metric"] = name
    quantile_rows.append(st)

with open(os.path.join(out_dir, "eda_numeric_quantiles.csv"), "w", newline="", encoding="utf-8") as f:
    q_fields = ["metric", "count", "mean", "std", "min", "p1", "p5", "p25", "p50", "p75", "p95", "p99", "max", "iqr_outliers_hi"]
    w = csv.DictWriter(f, fieldnames=q_fields)
    w.writeheader()
    w.writerows(quantile_rows)


# Segment aggregation helper
def summarize_segment(dim_name, bucket_fn, bucket_order=None):
    groups = defaultdict(list)
    for r in rows:
        groups[bucket_fn(r)].append(r)
    keys = bucket_order if bucket_order else sorted(groups.keys())
    out = []
    total_gmv_all = sum(r["_price"] for r in rows)
    for k in keys:
        grp = groups[k]
        if not grp:
            continue
        n = len(grp)
        gmv = sum(r["_price"] for r in grp)
        sat_n = sum(1 for r in grp if r["_rating"] >= 4.0)
        reg_n = sum(1 for r in grp if r["_rating"] <= 2.0)
        sat_gmv = sum(r["_sat_gmv"] for r in grp)
        reg_gmv = sum(r["_reg_gmv"] for r in grp)
        mean_r = sum(r["_rating"] for r in grp) / n
        mean_p = gmv / n
        out.append(
            {
                "dimension": dim_name,
                "segment": str(k),
                "n_purchases": n,
                "share_purchases_pct": round(n / N * 100, 1),
                "mean_price_usd": round(mean_p, 2),
                "total_gmv_usd": round(gmv, 2),
                "share_gmv_pct": round(gmv / total_gmv_all * 100, 1),
                "mean_rating": round(mean_r, 2),
                "satisfaction_rate_pct": round(sat_n / n * 100, 1),
                "regret_rate_pct": round(reg_n / n * 100, 1),
                "satisfied_gmv_usd": round(sat_gmv, 2),
                "satisfied_gmv_share_pct": round(sat_gmv / gmv * 100, 1) if gmv > 0 else 0.0,
                "regret_gmv_usd": round(reg_gmv, 2),
                "regret_gmv_share_pct": round(reg_gmv / gmv * 100, 1) if gmv > 0 else 0.0,
            }
        )
    return out


seg_rows = []

# Cut 1: Launch Stage (RQ3 Cold Start)
def launch_bucket(r):
    p = r["_prior_p"]
    if p == 0:
        return "1. Day-1 Launch (0 prior reviews)"
    elif p <= 4:
        return "2. Early Launch (1-4 prior reviews)"
    elif p <= 9:
        return "3. Cold-Start Window (5-9 prior reviews)"
    elif p <= 49:
        return "4. Growth Stage (10-49 prior reviews)"
    else:
        return "5. Established (50+ prior reviews)"

seg_rows.extend(summarize_segment("Launch Stage (Cold-Start vs Established)", launch_bucket))

# Cut 2: Listing Evidence Completeness (RQ2 Evidence Sufficiency)
def evidence_bucket(r):
    sc = r["_ev_struct_cnt"]
    hf = r["_has_feat"]
    if sc == 0 and hf == 0:
        return "1. Zero Structured Evidence & No Bullets"
    elif sc <= 2 and hf == 0:
        return "2. Low Evidence (1-2 specs, no bullets)"
    elif sc <= 2 and hf == 1:
        return "3. Moderate Evidence (1-2 specs + bullets)"
    elif sc >= 3 and hf == 0:
        return "4. Rich Specs Only (3+ specs, no bullets)"
    else:
        return "5. High Verifiable Evidence (3+ specs + bullets)"

seg_rows.extend(summarize_segment("Listing Evidence Tier (RQ2)", evidence_bucket))

# Cut 3: Customer Prior Need vs Listing Evidence Match (RQ2 -> RQ3)
seg_rows.extend(
    summarize_segment(
        "Customer Prior Need Support in Listing (RQ2 -> RQ3)",
        lambda r: r["_need_match_status"],
        [
            "All Stated Needs Supported in Listing",
            "Partially Supported in Listing",
            "Missing Evidence for Stated Needs",
            "No Explicit Keyword Need in Prior",
        ],
    )
)

# Cut 4: Brand / Popularity Prior vs Hype Quadrant (RQ1 Diagnosis)
def prior_hype_quadrant(r):
    high_pop = r["_meta_rn"] >= 100
    high_ev = (r["_ev_struct_cnt"] >= 3) or (r["_ev_struct_cnt"] >= 2 and r["_has_feat"] == 1)
    if high_ev and not high_pop:
        return "1. New/Niche Product + High Listing Evidence"
    elif not high_ev and not high_pop:
        return "2. New/Niche Product + Low/Missing Evidence"
    elif high_ev and high_pop:
        return "3. Popular Product + High Listing Evidence"
    else:
        return "4. Popular Product + Low/Missing Evidence"

seg_rows.extend(summarize_segment("Popularity Prior x Evidence Quadrant (RQ1)", prior_hype_quadrant))

# Cut 5: Price Tier (GMV Exposure)
def price_bucket(r):
    p = r["_price"]
    if p < 10:
        return "1. Budget (<$10)"
    elif p < 20:
        return "2. Mid-Low ($10-$19.99)"
    elif p < 40:
        return "3. Mid-High ($20-$39.99)"
    else:
        return "4. Premium ($40+)"

seg_rows.extend(summarize_segment("Price / GMV Tier", price_bucket))

# Cut 6: Verified Purchase Status
seg_rows.extend(
    summarize_segment(
        "Verified Purchase Status (Selection Bias Check)",
        lambda r: "Verified Purchase (True)" if r["_vp"] else "Unverified / Vine / Free Sample (False)",
    )
)

with open(os.path.join(out_dir, "eda_segment_cuts.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(seg_rows[0].keys()))
    w.writeheader()
    w.writerows(seg_rows)

# Yearly Trends
year_rows = summarize_segment("Calendar Year", lambda r: r["_year"])
with open(os.path.join(out_dir, "eda_yearly_trends.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(year_rows[0].keys()))
    w.writeheader()
    w.writerows(year_rows)

print("\n=== NUMERIC QUANTILES ===")
for qr in quantile_rows:
    print(
        f"{qr['metric']:38s} | mean={qr['mean']:8.2f} | std={qr['std']:8.2f} | p25={qr['p25']:6.2f} | p50={qr['p50']:6.2f} | p75={qr['p75']:6.2f} | p95={qr['p95']:7.2f} | max={qr['max']:8.2f}"
    )

print("\n=== SEGMENT SUMMARIES ===")
for sr in seg_rows:
    print(
        f"[{sr['dimension']}] {sr['segment']:48s} | n={sr['n_purchases']:5d} ({sr['share_purchases_pct']:4.1f}%) | GMV=${sr['total_gmv_usd']:10,.2f} | MeanR={sr['mean_rating']:.2f} | Sat={sr['satisfaction_rate_pct']:4.1f}% | Regret={sr['regret_rate_pct']:4.1f}% | RegretGMV%={sr['regret_gmv_share_pct']:4.1f}%"
    )

print(f"\nDuplicate (user_id, parent_asin, timestamp): {dup_pk}")
print(f"Repeat (user_id, parent_asin) pairs across timestamps: {dup_user_asin}")
print(f"Date range: {min(r['_date'] for r in rows)} to {max(r['_date'] for r in rows)}")
print(f"Unique users in cohort: {len(set(r['user_id'] for r in rows))}")
print(f"Unique parent_asins in cohort: {len(set(r['parent_asin'] for r in rows))}")
print(f"Unique brands (store_brand) in cohort: {len(set(r['store_brand'] for r in rows if r['store_brand']))}")
