"""Step 6 (Amazon only). Join the product metadata to the review-level aspect estimates.

Adds per product: title-derived segment (the EDA's keyword rules, with the RCA fix that "leather
conditioner" is not Hair care), price band, listing completeness (price, description, features),
store. Then reports criticism shares by segment, price band and listing completeness with PPI++
intervals (the calib sample is joined the same way), and how concentrated criticism is by store.

Usage: python join_meta.py /path/to/meta_All_Beauty.jsonl[.gz]  -> outputs/amazon/meta_results.{json,md}
"""
from __future__ import annotations

import gzip
import json
import os
import re
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from analyze import group_ppi, pct  # noqa: E402
from aspects import ASPECTS  # noqa: E402
from scale import gold_name, load_labels  # noqa: E402

SEGMENTS = {  # same order and patterns as scripts/beauty_eda.py; first match wins
    "Hair extensions / wigs": r"\b(wig|wigs|weave|weft|extensions|braiding|toupee|hairpiece)\b",
    "Hair care": r"\b(shampoo|(?<!leather )conditioner|hair oil|hair mask|scalp|hair growth|hair spray|hairspray)\b",
    "Skin care": r"\b(serum|moisturiz\w*|cleanser|sunscreen|facial|face cream|retinol|toner|acne|lotion)\b",
    "Makeup": r"\b(lipstick|lip gloss|eyeliner|eyeshadow|mascara|foundation|concealer|blush|makeup|cosmetic)\b",
    "Nail products": r"\b(nail|nails|manicure|pedicure|cuticle)\b",
    "Fragrance": r"\b(perfume|cologne|fragrance|eau de|body mist)\b",
    "Grooming / removal": r"\b(razor|shav\w*|trimmer|epilator|depilatory|waxing|beard)\b",
    "Tools / accessories": r"\b(brush|comb|mirror|dryer|straightener|curler|scissors|tweezer|headband|bonnet|clip|clips)\b",
}
SEG_RE = {k: re.compile(v, re.I) for k, v in SEGMENTS.items()}


def segment(title: str) -> str:
    for k, r in SEG_RE.items():
        if r.search(title or ""):
            return k
    return "Unclassified"


def price_band(p):
    if p is None or (isinstance(p, float) and np.isnan(p)):
        return "no price"
    return "<$10" if p < 10 else "$10-25" if p < 25 else "≥$25"


def load_meta(path):
    op = gzip.open if path.endswith(".gz") else open
    rows = []
    with op(path, "rt") as f:
        for line in f:
            r = json.loads(line)
            price = r.get("price")
            try:
                price = float(price) if price not in (None, "", "None") else None
            except (TypeError, ValueError):
                price = None
            desc = " ".join(map(str, r.get("description") or [])).strip()
            feat = " ".join(map(str, r.get("features") or [])).strip()
            rows.append({"product_id": r["parent_asin"], "store": r.get("store"), "segment": segment(r.get("title")),
                         "price_band": price_band(price), "has_description": bool(desc), "has_features": bool(feat),
                         "complete_listing": price is not None and bool(desc) and bool(feat)})
    return pd.DataFrame(rows)


def main(meta_path):
    out = os.path.join(HERE, "outputs", "amazon")
    meta = load_meta(meta_path)
    df = pd.read_parquet(os.path.join(out, "reviews.parquet"), columns=["review_id", "product_id", "rating"])
    df = df.merge(pd.read_parquet(os.path.join(out, "predictions.parquet")), on="review_id")
    df = df.merge(meta, on="product_id", how="left")
    for c in ("has_description", "has_features", "complete_listing"):
        df[c] = df[c].astype(str)
    ca = load_labels(out, "calib", gold_name(out))
    ca = ca.rename(columns={c: "y_" + c for c in ca.columns if c != "review_id"}).merge(df, on="review_id")
    have = [a for a in ASPECTS if f"neg_{a}" in df.columns]
    R = {"products_in_meta": len(meta), "reviews_matched": int(df.segment.notna().sum()), "reviews": len(df)}
    specs = {"segment": list(SEGMENTS) + ["Unclassified"], "price_band": ["<$10", "$10-25", "≥$25", "no price"],
             "complete_listing": ["True", "False"], "has_description": ["True", "False"]}
    for col, vals in specs.items():
        R[col] = {"reviews": {v: int((df[col] == v).sum()) for v in vals},
                  "calib": {v: int((ca[col] == v).sum()) for v in vals},
                  "neg": {a: group_ppi(df, ca, f"neg_{a}", col, vals) for a in have + []},
                  "mention": {a: group_ppi(df, ca, f"mention_{a}", col, vals) for a in have}}
    big = df.groupby("product_id").review_id.transform("size") >= 20
    st = {}
    for a in have:
        s = df[big].groupby("store")[f"neg_{a}"].sum().sort_values(ascending=False)
        st[a] = {"top_store": s.index[0], "top_store_share": float(s.iloc[0] / s.sum()), "top10_share": float(s.iloc[:10].sum() / s.sum())}
    R["store_concentration"] = st
    with open(os.path.join(out, "meta_results.json"), "w") as f:
        json.dump(R, f, indent=1, default=str)
    write_md(R, out, have)
    return R


def write_md(R, out, have):
    L = [f"# Review aspects joined to product metadata: amazon\n",
         f"{R['reviews_matched']:,} of {R['reviews']:,} reviews matched one of {R['products_in_meta']:,} metadata records. "
         "Shares are of reviews in each group, criticising the aspect (neg or mixed), PPI++ point estimates; "
         "95% intervals are in meta_results.json. Segments come from keyword rules on the title (heuristic, not Amazon's taxonomy).\n"]
    for col in ("segment", "price_band", "complete_listing", "has_description"):
        tab = R[col]
        vals = list(tab["reviews"])
        L.append(f"## Criticism by {col}\n")
        L.append("| Aspect | " + " | ".join(f"{v} (n={tab['reviews'][v]:,}; calib {tab['calib'][v]})" for v in vals) + " |")
        L.append("|---|" + "---|" * len(vals))
        for a in sorted(have, key=lambda a: -sum(tab["neg"][a][v]["est"] for v in vals if not np.isnan(tab["neg"][a][v]["est"]))):
            L.append(f"| {a} | " + " | ".join(pct(tab["neg"][a][v]["est"]) + ("*" if tab["neg"][a][v].get("classifier_only") else "") for v in vals) + " |")
        L.append("")
    L.append("\\* fewer than 40 calibration reviews: classifier estimate only, no interval.\n")
    L.append("## Store concentration of criticism (products with ≥ 20 reviews, classifier estimates)\n")
    L.append("| Aspect | Top store | Its share | Top 10 stores' share |")
    L.append("|---|---|---|---|")
    for a, r in R["store_concentration"].items():
        L.append(f"| {a} | {r['top_store']} | {pct(r['top_store_share'])} | {pct(r['top10_share'])} |")
    with open(os.path.join(out, "meta_results.md"), "w") as f:
        f.write("\n".join(L) + "\n")


if __name__ == "__main__":
    main(sys.argv[1])
    print(open(os.path.join(HERE, "outputs", "amazon", "meta_results.md")).read())
