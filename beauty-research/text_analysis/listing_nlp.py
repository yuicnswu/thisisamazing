"""Step 7 (Amazon only). NLP on listing text, linked to what reviewers criticise.

1. Parse each listing's title, feature bullets and description; normalise; count words.
2. Extract claims with transparent patterns (hydrating, long-lasting, gentle/sensitive, natural/organic,
   fragrance-free, multipack and others).
3. Claim-experience test: for each claim, compare the share of reviews that criticise the matching
   aspect on products that make the claim vs products that don't. Both shares are PPI++ estimates;
   the difference gets a normal-approximation 95% interval from the two standard errors.
   This is descriptive: products that make a claim differ in many other ways.

Usage: python listing_nlp.py /path/to/meta_All_Beauty.jsonl[.gz] -> outputs/amazon/listing_nlp.{json,md}
"""
from __future__ import annotations

import gzip
import json
import os
import re
import sys
from collections import Counter

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from analyze import pct  # noqa: E402
from parse import clean_text, tokens  # noqa: E402
from scale import load_labels, ppi_mean  # noqa: E402

# claim -> (pattern over title + features + description, aspect whose criticism tests it)
CLAIMS = {
    "hydrating": (r"\b(hydrat\w*|moisturi[sz]\w*)\b", "hydration_skin_feel"),
    "long_lasting": (r"\b(long[ -]?lasting|all[ -]day|24[ -]?h(ou)?rs?|waterproof|smudge[ -]?proof|transfer[ -]?proof)\b", "longevity"),
    "gentle_sensitive": (r"\b(sensitive skin|gentle|hypoallergenic|non[ -]?irritating|dermatologist[ -]tested)\b", "skin_reaction"),
    "natural_organic": (r"\b(natural|organic|plant[ -]based|chemical[ -]free|non[ -]?toxic)\b", "ingredients"),
    "fragrance_free": (r"\b(fragrance[ -]free|unscented|no fragrance)\b", "scent"),
    "scented": (r"\b(scent(ed)?|fragrance|aroma|smells?)\b", "scent"),
    "easy_to_use": (r"\b(easy to (use|apply)|easy[ -]application|beginner)\b", "ease_of_use"),
    "multipack": (r"\b(pack of \d+|\d+[ -]?(pack|pcs|pieces|count)|set of \d+)\b", "size_quantity"),
    "premium_quality": (r"\b(premium|high[ -]quality|professional|salon[ -]quality|luxury)\b", "authenticity_quality"),
}
CLAIM_RE = {k: re.compile(p, re.I) for k, (p, _) in CLAIMS.items()}


def load_listings(path):
    op = gzip.open if path.endswith(".gz") else open
    rows = []
    with op(path, "rt") as f:
        for line in f:
            r = json.loads(line)
            title = clean_text(r.get("title") or "")
            feat = clean_text(" ".join(map(str, r.get("features") or [])))
            desc = clean_text(" ".join(map(str, r.get("description") or [])))
            text = " . ".join(x for x in (title, feat, desc) if x)
            row = {"product_id": r["parent_asin"], "title_words": len(tokens(title)), "feature_words": len(tokens(feat)),
                   "description_words": len(tokens(desc))}
            for k, rx in CLAIM_RE.items():
                row["claim_" + k] = bool(rx.search(text))
            rows.append(row)
    return pd.DataFrame(rows)


def main(meta_path):
    out = os.path.join(HERE, "outputs", "amazon")
    lst = load_listings(meta_path)
    df = pd.read_parquet(os.path.join(out, "reviews.parquet"), columns=["review_id", "product_id"])
    df = df.merge(pd.read_parquet(os.path.join(out, "predictions.parquet")), on="review_id").merge(lst, on="product_id", how="left")
    ca = load_labels(out, "calib")
    ca = ca.rename(columns={c: "y_" + c for c in ca.columns if c != "review_id"}).merge(df, on="review_id")
    words = lst[["title_words", "feature_words", "description_words"]]
    R = {"listings": len(lst),
         "text_length": {c: {"median": float(words[c].median()), "share_zero": float((words[c] == 0).mean())} for c in words},
         "claim_share_of_listings": {k: float(lst["claim_" + k].mean()) for k in CLAIMS},
         "claims": {}}
    for k, (_, aspect) in CLAIMS.items():
        t, c = f"neg_{aspect}", "claim_" + k
        res = {"aspect": aspect, "listings_with_claim": int(lst[c].sum())}
        for v, name in ((True, "with"), (False, "without")):
            ma, mc = df[c] == v, ca[c] == v
            r = ppi_mean(ca.loc[mc, "y_" + t], ca.loc[mc, t], df.loc[ma, t])
            r["reviews"] = int(ma.sum())
            res[name] = r
        d = res["with"]["est"] - res["without"]["est"]
        se = np.sqrt(res["with"]["se"] ** 2 + res["without"]["se"] ** 2)
        res["diff"] = {"est": float(d), "lo": float(d - 1.96 * se), "hi": float(d + 1.96 * se)}
        res["classifier_ratio"] = float(df.loc[df[c] == True, t].mean() / df.loc[df[c] == False, t].mean())  # noqa: E712
        R["claims"][k] = res
    # most frequent listing bigrams in titles, for the record
    cnt = Counter()
    with (gzip.open if meta_path.endswith(".gz") else open)(meta_path, "rt") as f:
        for line in f:
            tk = tokens(clean_text(json.loads(line).get("title") or ""))
            cnt.update(" ".join(p) for p in zip(tk, tk[1:]))
    R["top_title_bigrams"] = cnt.most_common(30)
    with open(os.path.join(out, "listing_nlp.json"), "w") as f:
        json.dump(R, f, indent=1, default=str)
    write_md(R, out)
    return R


def write_md(R, out):
    L = ["# Listing text NLP linked to review criticism: amazon\n",
         f"{R['listings']:,} listings. Median words: title {R['text_length']['title_words']['median']:.0f}, "
         f"features {R['text_length']['feature_words']['median']:.0f}, description {R['text_length']['description_words']['median']:.0f}. "
         f"Listings with no feature text: {pct(R['text_length']['feature_words']['share_zero'])}; no description: "
         f"{pct(R['text_length']['description_words']['share_zero'])}.\n",
         "## Claim vs experience\n",
         "Share of reviews criticising the matching aspect, on products whose listing makes the claim vs products whose listing doesn't. "
         "PPI++ estimates with 95% intervals; the difference interval assumes the two estimates are independent. Descriptive, not causal.\n",
         "| Claim | Listings with it | Aspect tested | Criticism, with claim | Without | Difference (pp) |",
         "|---|---|---|---|---|---|"]
    for k, r in R["claims"].items():
        w, wo, d = r["with"], r["without"], r["diff"]
        L.append(f"| {k} | {r['listings_with_claim']:,} ({pct(R['claim_share_of_listings'][k])}) | {r['aspect']} | "
                 f"{pct(w['est'])} [{pct(max(w['lo'], 0))}, {pct(w['hi'])}] (calib {w['n']}) | {pct(wo['est'])} [{pct(max(wo['lo'], 0))}, {pct(wo['hi'])}] | "
                 f"{100 * d['est']:+.1f} [{100 * d['lo']:+.1f}, {100 * d['hi']:+.1f}] |")
    L.append("\n## Most frequent title bigrams\n")
    L.append(", ".join(f"{b} ({n:,})" for b, n in R["top_title_bigrams"]))
    with open(os.path.join(out, "listing_nlp.md"), "w") as f:
        f.write("\n".join(L) + "\n")


if __name__ == "__main__":
    main(sys.argv[1])
    print(open(os.path.join(HERE, "outputs", "amazon", "listing_nlp.md")).read())
