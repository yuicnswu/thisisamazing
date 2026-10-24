"""LLM-mined checkable needs from real early verified reviews, with automatic checks (no human annotators).

    python mine_needs.py [n_reviews]

1. Sample early verified reviews (first 10 per product) of the pilot's listings.
2. Extractor A (Claude Haiku) lists checkable needs per review: attribute, value, verbatim quote.
3. Checks, all automatic:
   - grounding: the quote occurs verbatim in the review;
   - vocabulary: the value is in the §12.1 controlled vocabulary;
   - lexical: the rule parser finds the same attribute value in the quote;
   - agreement: extractor B (Claude Sonnet, a different model) on a subsample; Cohen-style set agreement.
4. Pair each grounded need with the listing the reviewer bought and label support from visible text: how often
   does the listing a real buyer chose actually state that buyer's checkable need?
"""
from __future__ import annotations

import json
import os
import random
import re
import sys
from collections import Counter, defaultdict

from attributes import Need, find_values, support_label
from data import REVIEWS_JSONL, load_listings
from matchers import _run_batched

OUT = os.path.join(os.path.dirname(__file__), "outputs")

MINE_SYS = """You read product reviews from a beauty store and list the shopper's CHECKABLE needs: requirements about the shopper or the product that a product listing could state and a parser could check.
Allowed attributes and values:
- skin_type: dry, oily, sensitive, combination, normal, acne_prone
- hair_type: curly, straight, wavy, fine, thick, dry, damaged, oily
- scent: unscented (shopper needs fragrance-free), or a named scent they wanted
- item_form: gel, cream, spray, powder, oil, lotion, foam, bar, balm, stick, serum, liquid, wax, paste (only if they say they wanted that form)
- free_from: paraben, sulfate, alcohol, fragrance, cruelty, vegan, gluten, silicone, oil
Only list a need the review states about the reviewer or what they wanted (e.g. "I have very dry skin", "I need something unscented", "my curly hair"). Do not list experiential outcomes ("broke me out", "feels greasy", "smells nice") or anything outside the list.
"quote" must be copied verbatim from the review.
Reply with only a JSON array, one object per review, in the same order:
[{"id": "<review id>", "needs": [{"attr": "...", "value": "...", "quote": "..."}]}]"""

VOCAB = {"skin_type": {"dry", "oily", "sensitive", "combination", "normal", "acne_prone"},
         "hair_type": {"curly", "straight", "wavy", "fine", "thick", "dry", "damaged", "oily"},
         "item_form": {"gel", "cream", "spray", "powder", "oil", "lotion", "foam", "bar", "balm", "stick", "serum",
                       "liquid", "wax", "paste"},
         "free_from": {"paraben", "sulfate", "alcohol", "fragrance", "cruelty", "vegan", "gluten", "silicone", "oil"}}


class _R:
    def __init__(self, rid, asin, text):
        self.rid, self.asin, self.text = rid, asin, text


def sample_reviews(asins: set[str], n: int, seed: int = 0, k: int = 10) -> list[_R]:
    by_item = defaultdict(list)
    with open(REVIEWS_JSONL) as f:
        for line in f:
            r = json.loads(line)
            if r["parent_asin"] in asins and r.get("verified_purchase"):
                by_item[r["parent_asin"]].append((r["timestamp"], (r.get("title") or "") + ". " + (r.get("text") or "")))
    early = [(a, t) for a, v in by_item.items() for _, t in sorted(v)[:k] if len(t) > 40]
    random.Random(seed).shuffle(early)
    return [_R(f"R{i}", a, t[:1500]) for i, (a, t) in enumerate(early[:n])]


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.lower()).strip()


def needs_of(row) -> list[dict]:
    if not row or not isinstance(row.get("needs"), list):
        return []
    out = []
    for n in row["needs"]:
        if isinstance(n, dict) and n.get("attr") and n.get("value"):
            out.append({"attr": str(n["attr"]).lower(), "value": str(n["value"]).lower().replace("-", "_").replace(" ", "_"),
                        "quote": str(n.get("quote", ""))})
    return out


def main(n: int = 600):
    listings = {l.asin: l for l in load_listings()}
    reviews = sample_reviews(set(listings), n)
    render = lambda r: f"### Review {r.rid}\n{r.text}\n"
    a = _run_batched(reviews, MINE_SYS, "claude", "claude-haiku-5-5", 20, 6, 0, render=render, key="rid", shown=str)
    sub = reviews[: min(200, len(reviews))]
    b = _run_batched(sub, MINE_SYS, "claude", "claude-sonnet-5-5", 20, 6, 0, render=render, key="rid", shown=str)

    stats = Counter()
    pairs = []
    per_attr = Counter()
    for r in reviews:
        ns = needs_of(a.get(r.rid))
        stats["reviews"] += 1
        stats["parsed"] += a.get(r.rid) is not None
        good = []
        for nd in ns:
            stats["needs"] += 1
            grounded = _norm(nd["quote"]) in _norm(r.text) and len(nd["quote"]) > 2
            in_vocab = nd["attr"] == "scent" or nd["value"] in VOCAB.get(nd["attr"], set())
            lexical = nd["attr"] in ("skin_type", "hair_type", "scent", "free_from", "item_form") and \
                nd["value"] in find_values(nd["attr"], nd["quote"])
            stats["grounded"] += grounded
            stats["in_vocab"] += in_vocab
            stats["lexical"] += lexical
            if grounded and in_vocab:
                good.append(nd)
        stats["reviews_with_need"] += bool(good)
        for nd in good:
            per_attr[nd["attr"]] += 1
            need = Need(nd["attr"], nd["value"])
            lab = support_label(need, listings[r.asin].visible_text()) if nd["attr"] in (
                "skin_type", "hair_type", "scent", "item_form", "free_from") else "unresolved"
            pairs.append({"rid": r.rid, "asin": r.asin, "attr": nd["attr"], "value": nd["value"],
                          "quote": nd["quote"], "listing_label": lab})

    # agreement between extractors on (attr, value) sets, over the subsample
    tp = fa = fb = both_empty = 0
    for r in sub:
        sa = {(x["attr"], x["value"]) for x in needs_of(a.get(r.rid))}
        sb = {(x["attr"], x["value"]) for x in needs_of(b.get(r.rid))}
        tp += len(sa & sb)
        fa += len(sa - sb)
        fb += len(sb - sa)
        both_empty += not sa and not sb
    agree = {"subsample": len(sub), "matched_needs": tp, "only_haiku": fa, "only_sonnet": fb,
             "precision_vs_sonnet": tp / (tp + fa) if tp + fa else None,
             "recall_vs_sonnet": tp / (tp + fb) if tp + fb else None,
             "review_level_agreement": sum(
                 bool(needs_of(a.get(r.rid))) == bool(needs_of(b.get(r.rid))) for r in sub) / len(sub)}
    res = {"stats": dict(stats), "share_reviews_with_checkable_need": stats["reviews_with_need"] / stats["reviews"],
           "per_attr": dict(per_attr), "listing_label_of_buyer_need": dict(Counter(p["listing_label"] for p in pairs)),
           "extractor_agreement": agree}
    with open(os.path.join(OUT, "mined_needs.json"), "w") as f:
        json.dump({"summary": res, "pairs": pairs}, f, indent=1)
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 600)
