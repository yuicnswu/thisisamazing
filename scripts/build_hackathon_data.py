import csv
import json
import os
from collections import defaultdict

reviews_path = "/Users/cattleya.c/Downloads/All_Beauty.jsonl"
meta_path = "/Users/cattleya.c/Downloads/meta_All_Beauty.jsonl"

meta_full_csv = "/Users/cattleya.c/Downloads/meta_All_Beauty.csv"
scratch_dir = "/Users/cattleya.c/.gemini/antigravity/scratch/all_beauty"
os.makedirs(scratch_dir, exist_ok=True)
meta_sample_csv = os.path.join(scratch_dir, "meta_All_Beauty_sample_1000.csv")
hackathon_csv_scratch = os.path.join(scratch_dir, "hackathon_beauty_gmv.csv")
hackathon_sample_csv = os.path.join(scratch_dir, "hackathon_beauty_gmv_sample_500.csv")
hackathon_csv_downloads = "/Users/cattleya.c/Downloads/hackathon_beauty_gmv.csv"

meta_fields = [
    "parent_asin",
    "title",
    "store",
    "price",
    "average_rating",
    "rating_number",
    "features",
    "description",
    "details",
    "main_category",
    "categories",
]


def parse_price(val):
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return float(val) if val > 0 else None
    if isinstance(val, str):
        s = val.strip().replace("$", "").replace(",", "")
        try:
            v = float(s)
            return v if v > 0 else None
        except ValueError:
            return None
    return None


print("Step 1: Reading meta_All_Beauty.jsonl and writing CSVs...")
meta_by_asin = {}
total_meta = 0
priced_meta = 0
with_features = 0
with_description = 0
with_details = 0

with (
    open(meta_path, "r", encoding="utf-8") as infile,
    open(meta_full_csv, "w", newline="", encoding="utf-8") as full_out,
    open(meta_sample_csv, "w", newline="", encoding="utf-8") as sample_out,
):
    full_writer = csv.DictWriter(full_out, fieldnames=meta_fields, extrasaction="ignore")
    sample_writer = csv.DictWriter(sample_out, fieldnames=meta_fields, extrasaction="ignore")
    full_writer.writeheader()
    sample_writer.writeheader()

    for line in infile:
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        pasin = rec.get("parent_asin")
        price_val = parse_price(rec.get("price"))
        feats = rec.get("features") or []
        desc = rec.get("description") or []
        details = rec.get("details") or {}

        if price_val is not None:
            priced_meta += 1
        if feats:
            with_features += 1
        if desc:
            with_description += 1
        if details:
            with_details += 1

        # Store compact version in memory for joining
        meta_by_asin[pasin] = {
            "title": rec.get("title") or "",
            "store": rec.get("store") or "",
            "price": price_val,
            "average_rating": rec.get("average_rating"),
            "rating_number": rec.get("rating_number"),
            "features": feats,
            "description": desc,
            "details": details,
        }

        row_out = {
            "parent_asin": pasin,
            "title": rec.get("title") or "",
            "store": rec.get("store") or "",
            "price": price_val if price_val is not None else "",
            "average_rating": rec.get("average_rating", ""),
            "rating_number": rec.get("rating_number", ""),
            "features": json.dumps(feats, ensure_ascii=False),
            "description": json.dumps(desc, ensure_ascii=False),
            "details": json.dumps(details, ensure_ascii=False),
            "main_category": rec.get("main_category") or "",
            "categories": json.dumps(rec.get("categories") or [], ensure_ascii=False),
        }
        full_writer.writerow(row_out)
        if total_meta < 1000:
            sample_writer.writerow(row_out)
        total_meta += 1

print(f"Total products in meta: {total_meta}")
print(f"  With valid price (GMV-ready): {priced_meta} ({priced_meta/total_meta*100:.1f}%)")
print(f"  With bullet features:         {with_features} ({with_features/total_meta*100:.1f}%)")
print(f"  With description text:        {with_description} ({with_description/total_meta*100:.1f}%)")
print(f"  With structured details:      {with_details} ({with_details/total_meta*100:.1f}%)")

print("\nStep 2: Scanning All_Beauty.jsonl to build user timelines & product launch timelines...")
user_reviews = defaultdict(list)
product_timestamps = defaultdict(list)
total_reviews = 0
joined_priced_reviews = 0
total_priced_gmv = 0.0
satisfied_priced_gmv = 0.0
regret_priced_gmv = 0.0

with open(reviews_path, "r", encoding="utf-8") as infile:
    for line in infile:
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        total_reviews += 1
        uid = r.get("user_id")
        pasin = r.get("parent_asin")
        ts = r.get("timestamp", 0)
        rating = float(r.get("rating", 0.0))
        vp = bool(r.get("verified_purchase", False))

        m = meta_by_asin.get(pasin)
        if m and m["price"] is not None:
            joined_priced_reviews += 1
            p = m["price"]
            if vp:
                total_priced_gmv += p
                if rating >= 4.0:
                    satisfied_priced_gmv += p
                elif rating <= 2.0:
                    regret_priced_gmv += p

        product_timestamps[pasin].append(ts)
        user_reviews[uid].append(
            {
                "timestamp": ts,
                "parent_asin": pasin,
                "asin": r.get("asin", ""),
                "rating": rating,
                "title": r.get("title") or "",
                "text": r.get("text") or "",
                "verified_purchase": vp,
                "helpful_vote": r.get("helpful_vote", 0),
            }
        )

for pasin in product_timestamps:
    product_timestamps[pasin].sort()

users_ge2 = sum(1 for u, revs in user_reviews.items() if len(revs) >= 2)
users_ge3 = sum(1 for u, revs in user_reviews.items() if len(revs) >= 3)
users_ge5 = sum(1 for u, revs in user_reviews.items() if len(revs) >= 5)

print(f"Total reviews: {total_reviews}")
print(f"Reviews matching a priced product: {joined_priced_reviews}")
print(f"Total Verified-Purchase GMV ($):   ${total_priced_gmv:,.2f}")
print(f"  Satisfied GMV (rating >= 4):     ${satisfied_priced_gmv:,.2f} ({satisfied_priced_gmv/max(total_priced_gmv,1)*100:.1f}%)")
print(f"  Regret GMV (rating <= 2):        ${regret_priced_gmv:,.2f} ({regret_priced_gmv/max(total_priced_gmv,1)*100:.1f}%)")
print(f"Unique users: {len(user_reviews)} | >=2 reviews: {users_ge2} | >=3 reviews: {users_ge3} | >=5 reviews: {users_ge5}")

print("\nStep 3: Building hackathon_beauty_gmv.csv (repeat buyers with prior history + priced product metadata)...")
import bisect

hackathon_fields = [
    "user_id",
    "parent_asin",
    "asin",
    "timestamp",
    "user_total_reviews",
    "user_prior_reviews_count",
    "user_prior_avg_rating",
    "user_prior_history_text",
    "product_launch_timestamp",
    "product_prior_reviews_at_purchase",
    "is_cold_start_launch",
    "store_brand",
    "price_usd",
    "meta_average_rating",
    "meta_rating_number",
    "product_title",
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
    "rating",
    "verified_purchase",
    "helpful_vote",
    "review_title",
    "review_text",
    "order_gmv",
    "satisfied_gmv",
    "regret_gmv",
]

hack_rows = []
for uid, revs in user_reviews.items():
    if len(revs) < 2:
        continue
    # Sort user's reviews chronologically
    revs.sort(key=lambda x: x["timestamp"])
    for idx, cur in enumerate(revs):
        if idx == 0:
            # Need at least 1 prior review before this purchase to have a pre-purchase customer profile
            continue
        pasin = cur["parent_asin"]
        m = meta_by_asin.get(pasin)
        if not m or m["price"] is None:
            continue
        prior_revs = revs[:idx]
        prior_avg = round(sum(x["rating"] for x in prior_revs) / len(prior_revs), 2)
        prior_texts = []
        for pr in prior_revs[-5:]:  # up to 5 most recent prior reviews
            pm = meta_by_asin.get(pr["parent_asin"])
            ptitle = pm["title"][:60] if pm and pm["title"] else pr["parent_asin"]
            prior_texts.append(f"[{pr['rating']}* on {ptitle}]: {pr['title']} - {pr['text'][:250]}")
        prior_history_str = " || ".join(prior_texts)

        pts = product_timestamps[pasin]
        launch_ts = pts[0] if pts else cur["timestamp"]
        prior_prod_revs = bisect.bisect_left(pts, cur["timestamp"])

        det = m["details"] or {}
        price = m["price"]
        rating = cur["rating"]

        row = {
            "user_id": uid,
            "parent_asin": pasin,
            "asin": cur["asin"],
            "timestamp": cur["timestamp"],
            "user_total_reviews": len(revs),
            "user_prior_reviews_count": len(prior_revs),
            "user_prior_avg_rating": prior_avg,
            "user_prior_history_text": prior_history_str,
            "product_launch_timestamp": launch_ts,
            "product_prior_reviews_at_purchase": prior_prod_revs,
            "is_cold_start_launch": prior_prod_revs < 10,
            "store_brand": m["store"],
            "price_usd": price,
            "meta_average_rating": m["average_rating"],
            "meta_rating_number": m["rating_number"],
            "product_title": m["title"],
            "features_text": " | ".join(m["features"]) if m["features"] else "",
            "description_text": " ".join(m["description"]) if m["description"] else "",
            "item_form": det.get("Item Form", ""),
            "skin_type": det.get("Skin Type", ""),
            "hair_type": det.get("Hair Type", ""),
            "scent": det.get("Scent", ""),
            "product_benefits": det.get("Product Benefits", ""),
            "material_type_free": det.get("Material Type Free", ""),
            "active_ingredients": det.get("Active Ingredients", ""),
            "details_json": json.dumps(det, ensure_ascii=False),
            "rating": rating,
            "verified_purchase": cur["verified_purchase"],
            "helpful_vote": cur["helpful_vote"],
            "review_title": cur["title"],
            "review_text": cur["text"],
            "order_gmv": price,
            "satisfied_gmv": price if rating >= 4.0 else 0.0,
            "regret_gmv": price if rating <= 2.0 else 0.0,
        }
        hack_rows.append(row)

with (
    open(hackathon_csv_scratch, "w", newline="", encoding="utf-8") as f1,
    open(hackathon_csv_downloads, "w", newline="", encoding="utf-8") as f2,
    open(hackathon_sample_csv, "w", newline="", encoding="utf-8") as f3,
):
    w1 = csv.DictWriter(f1, fieldnames=hackathon_fields)
    w2 = csv.DictWriter(f2, fieldnames=hackathon_fields)
    w3 = csv.DictWriter(f3, fieldnames=hackathon_fields)
    w1.writeheader()
    w2.writeheader()
    w3.writeheader()
    for i, r in enumerate(hack_rows):
        w1.writerow(r)
        w2.writerow(r)
        if i < 500:
            w3.writerow(r)

hack_gmv = sum(r["order_gmv"] for r in hack_rows)
hack_sat_gmv = sum(r["satisfied_gmv"] for r in hack_rows)
hack_reg_gmv = sum(r["regret_gmv"] for r in hack_rows)
cold_rows = sum(1 for r in hack_rows if r["is_cold_start_launch"])

print(f"Hackathon GMV dataset rows (repeat buyers w/ prior history + price): {len(hack_rows)}")
print(f"  Cold-start launch purchases (<10 prior product reviews): {cold_rows}")
print(f"  Total Cohort GMV ($):      ${hack_gmv:,.2f}")
print(f"  Satisfied GMV ($):         ${hack_sat_gmv:,.2f}")
print(f"  Regret/Mismatch GMV ($):   ${hack_reg_gmv:,.2f}")
print(f"Saved to:\n  - {hackathon_csv_scratch}\n  - {hackathon_csv_downloads}\n  - {hackathon_sample_csv}")
