"""G0 feasibility count (refined-thesis-plan §12.3) on the listings available in this environment.

1. Per-attribute coverage in hidden `details`, and agreement between `details` and the visible text.
2. Products with >= 2 attributes where visible text and `details` agree (the L2 pool).
3. Share of early verified reviews (first 10 per product) that mention a checkable attribute (rule proxy;
   the LLM-mined estimate is in mine_needs.py).
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict

from attributes import ATTRS, details_values, find_values
from data import REVIEWS_JSONL, load_listings


def agreement(listing) -> dict[str, str]:
    """attr -> 'agree' | 'details_only' | 'text_only' | 'disagree' | 'none'."""
    text = listing.visible_text()
    out = {}
    for a in ATTRS:
        d = details_values(a, listing.details)
        v = set(find_values(a, text))
        if a in ("skin_type", "hair_type"):
            ok = bool(d & v) or ("all" in d and "all" in v)
        else:
            ok = bool(d & v)
        if d and ok:
            out[a] = "agree"
        elif d and not v:
            out[a] = "details_only"
        elif d and v:
            out[a] = "disagree"
        elif v:
            out[a] = "text_only"
        else:
            out[a] = "none"
    return out


def early_review_share(asins: set[str], k: int = 10) -> dict:
    by_item = defaultdict(list)
    with open(REVIEWS_JSONL) as f:
        for line in f:
            r = json.loads(line)
            if r["parent_asin"] in asins and r.get("verified_purchase"):
                by_item[r["parent_asin"]].append((r["timestamp"], r.get("title", "") + ". " + r.get("text", "")))
    n = hit = 0
    per_attr = Counter()
    for items in by_item.values():
        for _, t in sorted(items)[:k]:
            n += 1
            found = [a for a in ("skin_type", "hair_type", "scent", "free_from") if find_values(a, t)]
            hit += bool(found)
            per_attr.update(found)
    return {"products": len(by_item), "early_verified_reviews": n, "with_checkable_mention": hit,
            "share": hit / n if n else 0.0, "per_attr": dict(per_attr)}


def main(out_path: str) -> dict:
    listings = load_listings()
    status = {l.asin: agreement(l) for l in listings}
    res = {"listings": len(listings), "by_source": Counter(l.source for l in listings)}
    res["per_attr"] = {a: dict(Counter(s[a] for s in status.values())) for a in ATTRS}
    n_agree = Counter(sum(v == "agree" for v in s.values()) for s in status.values())
    res["agreeing_attrs_hist"] = dict(sorted(n_agree.items()))
    res["products_ge1_agree"] = sum(c for k, c in n_agree.items() if k >= 1)
    res["products_ge2_agree"] = sum(c for k, c in n_agree.items() if k >= 2)
    res["early_reviews"] = early_review_share({l.asin for l in listings})
    with open(out_path, "w") as f:
        json.dump(res, f, indent=2, default=dict)
    return res


if __name__ == "__main__":
    print(json.dumps(main(sys.argv[1] if len(sys.argv) > 1 else "g0.json"), indent=2, default=dict))
