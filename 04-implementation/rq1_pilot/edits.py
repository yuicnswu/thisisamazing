"""Real edits of real listings (refined-thesis-plan §11.1, L1 labels).

Each benchmark item starts from a real listing whose visible text and hidden `details` agree on an
attribute value, then applies one minimal edit. The support label is known by construction and is
re-checked with the rule parser; items whose edit does not produce the intended label are dropped.

  original          no edit                                            -> entailed
  remove            delete every bullet / sentence stating the attribute,
                    and the phrase itself from the title                -> unresolved
  vague             replace each statement with vague wording
                    ("for your skin", "gentle, clean feel")             -> unresolved
  contradict        replace the stated value with an opposite value      -> contradicted
  remove_prior      `remove`, plus a famous-brand swap and a hype bullet -> unresolved
  natural_missing   no edit; `details` has the value, the text does not  -> unresolved (natural, L2)
"""
from __future__ import annotations

import copy
import random
import re
from dataclasses import dataclass

from attributes import OPPOSITES, Need, details_values, find_values, support_label
from data import Listing

LABEL = {"original": "entailed", "remove": "unresolved", "vague": "unresolved", "contradict": "contradicted",
         "remove_prior": "unresolved", "natural_missing": "unresolved"}

VAGUE = {"skin_type": "your skin", "hair_type": "your hair", "item_form": "formula", "free_from": "clean"}
PHRASE = {"skin_type": lambda v: f"{v.replace('_', '-')} skin", "hair_type": lambda v: f"{v} hair",
          "item_form": lambda v: v, "scent": lambda v: ("lavender scented" if v == "unscented" else f"{v} scent"),
          "free_from": lambda v: (None if v in ("cruelty", "vegan") else "fragranced" if v == "fragrance"
                                  else f"{v}-based")}
FAMOUS = {"skin_type": "CeraVe", "hair_type": "Olaplex", "scent": "L'Occitane", "item_form": "L'Oréal Paris",
          "free_from": "The Ordinary"}
HYPE = "#1 dermatologist-recommended brand, loved by millions of customers worldwide and a best seller for years"


@dataclass
class Item:
    item_id: str
    asin: str
    variant: str
    need: Need
    label: str
    listing: Listing


def _merge(spans):
    out = []
    for s, e in sorted(spans):
        if out and s <= out[-1][1]:
            out[-1] = (out[-1][0], max(e, out[-1][1]))
        else:
            out.append((s, e))
    return out


def _spans(attr: str, text: str, value: str | None = None) -> list[tuple[int, int]]:
    """Spans stating the attribute; with `value`, only spans stating that value (or 'all' types)."""
    found = find_values(attr, text)
    if value is not None:
        found = {k: v for k, v in found.items() if k == value or k == "all"}
    return _merge([sp for v in found.values() for sp in v])


def _replace(text: str, spans, repl: str) -> str:
    for s, e in reversed(spans):
        text = text[:s] + repl + text[e:]
    return re.sub(r"\s{2,}", " ", re.sub(r"\s+([,.;])", r"\1", text)).strip(" ,-|")


def _sentences(s: str) -> list[str]:
    return [p for p in re.split(r"(?<=[.!?])\s+", s) if p]


def _map_text(listing: Listing, fn_title, fn_seg) -> Listing:
    l = copy.deepcopy(listing)
    l.title = fn_title(l.title)
    l.bullets = [b for b in (fn_seg(b) for b in l.bullets) if b]
    l.description = [d for d in (fn_seg(d) for d in l.description) if d]
    return l


def remove(listing: Listing, attr: str) -> Listing:
    def seg(s):
        keep = [x for x in _sentences(s) if not _spans(attr, x)]
        return " ".join(keep)
    return _map_text(listing, lambda t: _replace(t, _spans(attr, t), ""), seg)


def vague(listing: Listing, attr: str, value: str) -> Listing:
    if attr == "scent":
        repl = "gentle" if value == "unscented" else "pleasant scent"
    else:
        repl = VAGUE[attr]
    f = lambda t: _replace(t, _spans(attr, t, value), repl)
    return _map_text(listing, f, f)


def contradict(listing: Listing, attr: str, value: str, rng: random.Random) -> Listing | None:
    if attr == "free_from":
        repl = PHRASE[attr](value)
    else:
        opp = sorted(OPPOSITES.get(attr, {}).get(value, set()))
        if not opp:
            return None
        repl = PHRASE[attr](rng.choice(opp))
    if repl is None:
        return None
    f = lambda t: _replace(t, _spans(attr, t, value), repl)
    return _map_text(listing, f, f)


def add_prior(listing: Listing, attr: str) -> Listing:
    l = copy.deepcopy(listing)
    brand = FAMOUS[attr]
    if l.store:
        pat = re.compile(re.escape(l.store), re.I)
        l.title = pat.sub(brand, l.title)
        l.bullets = [pat.sub(brand, b) for b in l.bullets]
        l.description = [pat.sub(brand, d) for d in l.description]
    if brand.lower() not in l.title.lower():
        l.title = f"{brand} {l.title}"
    l.store = brand
    l.bullets = [HYPE] + l.bullets
    return l


def candidate_needs(listing: Listing) -> list[Need]:
    """Needs whose value is stated in BOTH visible text and hidden details (agreement filter, §11.3)."""
    text = listing.visible_text()
    out = []
    for attr in ("skin_type", "hair_type", "scent", "item_form", "free_from"):
        d = details_values(attr, listing.details)
        v = set(find_values(attr, text))
        for val in sorted(d & v):
            if val == "all" or (attr == "scent" and val != "unscented"):
                continue  # named scents ("lavender oil") are usually ingredients, not a scent claim
            out.append(Need(attr, val))
        if attr in ("skin_type", "hair_type") and "all" in d and "all" in v:
            out.append(Need(attr, "dry"))  # "all skin/hair types" entails any single type (§12.1 rule)
    return out


def missing_needs(listing: Listing) -> list[Need]:
    """Needs true per hidden details but not stated in visible text (natural missing evidence)."""
    text = listing.visible_text()
    out = []
    for attr in ("skin_type", "hair_type", "scent", "free_from"):
        d = details_values(attr, listing.details) - {"all"}
        if attr == "scent":
            d &= {"unscented"}
        if d and not find_values(attr, text):
            out.append(Need(attr, sorted(d)[0]))
    return out


def build_items(listings: list[Listing], n_products: int, n_missing: int, seed: int = 0) -> list[Item]:
    rng = random.Random(seed)
    pool = [(l, n) for l in listings for n in candidate_needs(l)]
    rng.shuffle(pool)
    # Balance attributes: item form is far more common, so cap it.
    by_attr: dict[str, list] = {}
    for l, n in pool:
        by_attr.setdefault(n.attr, []).append((l, n))
    seen, chosen = set(), []
    cap = {"item_form": n_products // 5}
    for attr in ("free_from", "skin_type", "hair_type", "scent", "item_form"):
        k = 0
        for l, n in by_attr.get(attr, []):
            if l.asin in seen or k >= cap.get(attr, n_products):
                continue
            seen.add(l.asin)
            chosen.append((l, n))
            k += 1
    rng.shuffle(chosen)
    items: list[Item] = []
    for l, n in chosen:
        if len({i.asin for i in items}) >= n_products:
            break
        variants = {"original": l, "remove": remove(l, n.attr), "vague": vague(l, n.attr, n.value),
                    "contradict": contradict(l, n.attr, n.value, rng)}
        variants["remove_prior"] = add_prior(variants["remove"], n.attr)
        built = []
        for name, lv in variants.items():
            if lv is None or not lv.title:
                continue
            if support_label(n, lv.visible_text()) != LABEL[name]:
                continue  # edit did not produce the intended label: drop, never relabel
            built.append(Item(f"{l.asin}:{n.attr}:{n.value}:{name}", l.asin, name, n, LABEL[name], lv))
        if any(b.variant == "original" for b in built) and len(built) >= 3:
            items += built
    miss = [(l, n) for l in listings if l.asin not in seen for n in missing_needs(l)]
    rng.shuffle(miss)
    for l, n in miss[:n_missing]:
        items.append(Item(f"{l.asin}:{n.attr}:{n.value}:natural_missing", l.asin, "natural_missing", n,
                          "unresolved", l))
    return items


def build_calpool(listings: list[Listing], exclude: set[str], n_missing: int, seed: int = 1) -> list[Item]:
    """ONE item per product (theory.md assumption A1), from products not used by `build_items`.

    Per product: one need (a non-item-form need when the listing has one), all edits that pass the label check,
    then one of them drawn uniformly. Plus `n_missing` natural-missing products."""
    rng = random.Random(seed)
    items: list[Item] = []
    used = set(exclude)
    for l in listings:
        if l.asin in used:
            continue
        needs = candidate_needs(l)
        if not needs:
            continue
        non_form = [n for n in needs if n.attr != "item_form"]
        n = rng.choice(non_form or needs)
        variants = {"original": l, "remove": remove(l, n.attr), "vague": vague(l, n.attr, n.value),
                    "contradict": contradict(l, n.attr, n.value, rng)}
        variants["remove_prior"] = add_prior(variants["remove"], n.attr) if variants["remove"] else None
        ok = [(name, lv) for name, lv in variants.items()
              if lv is not None and lv.title and support_label(n, lv.visible_text()) == LABEL[name]]
        if not ok:
            continue
        name, lv = rng.choice(ok)
        used.add(l.asin)
        items.append(Item(f"{l.asin}:{n.attr}:{n.value}:{name}", l.asin, name, n, LABEL[name], lv))
    miss = [(l, n) for l in listings if l.asin not in used for n in missing_needs(l)[:1]]
    rng.shuffle(miss)
    for l, n in miss[:n_missing]:
        items.append(Item(f"{l.asin}:{n.attr}:{n.value}:natural_missing", l.asin, "natural_missing", n,
                          "unresolved", l))
    return items
