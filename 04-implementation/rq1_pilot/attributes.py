"""Checkable Beauty attributes (refined-thesis-plan §12.1) and a rule parser over listing text.

The parser is used for three things, and the pilot reports each one separately:
  * G0: does the visible text state the same value as the hidden `details` field?
  * Edit construction: find the spans a real edit must delete or replace.
  * Labels on natural listings (L2): entailed / contradicted / unresolved from visible text.

Scope for the pilot: skin type, hair type, scent (incl. fragrance-free), item form, free-from.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

ATTRS = ("skin_type", "hair_type", "scent", "item_form", "free_from")

# Canonical value -> regexes that state it in free text. Patterns are deliberately
# conservative: a match must name the value next to its attribute noun.
_SKIN_WORDS = {"dry": "dry", "oily": "oily", "sensitive": "sensitive", "combination": "combination",
               "normal": "normal", "acne-prone": "acne_prone", "acne prone": "acne_prone"}
_HAIR_WORDS = {"curly": "curly", "straight": "straight", "wavy": "wavy", "fine": "fine", "thin": "fine",
               "thick": "thick", "coarse": "thick", "dry": "dry", "damaged": "damaged", "oily": "oily", "greasy": "oily"}


def _list_pattern(words: dict, noun: str) -> str:
    alt = "|".join(sorted(map(re.escape, words), key=len, reverse=True))
    sep = r"\s*(?:,|/|&|-|\band\b|\bor\b|\bto\b|\bvery\b)?\s*"
    return rf"\b((?:(?:{alt}){sep})+)-?{noun}s?\b"


_SKIN = {"all": [r"\ball skin types?\b", r"\bevery skin type\b", r"\bany skin type\b", r"\ball types of skin\b"]}
_HAIR = {"all": [r"\ball hair types?\b", r"\bevery hair type\b", r"\bany hair type\b", r"\ball types of hair\b"],
         "curly": [r"\bcurls\b"]}
_LISTS = {"skin_type": (_SKIN_WORDS, _list_pattern(_SKIN_WORDS, "skin")),
          "hair_type": (_HAIR_WORDS, _list_pattern(_HAIR_WORDS, "hair"))}
_SCENT = {
    "unscented": [r"\bunscented\b", r"\bfragrance[- ]free\b", r"\bscent[- ]free\b", r"\bno (?:added )?fragrance\b",
                  r"\bwithout (?:added )?fragrance\b", r"\bperfume[- ]free\b"],
    "lavender": [r"\blavender\b"], "vanilla": [r"\bvanilla\b"], "coconut": [r"\bcoconut\b"],
    "rose": [r"\brose\b(?! gold)", r"\brosewater\b"], "citrus": [r"\bcitrus\b"], "lemon": [r"\blemon\b"],
    "mint": [r"\b(?:pepper|spear)?mint\b"], "eucalyptus": [r"\beucalyptus\b"], "aloe": [r"\baloe\b"],
    "floral": [r"\bfloral\b"], "unscented_strict": [],
}
_FORM = {
    "gel": [r"\bgel\b"], "cream": [r"\bcream\b"], "spray": [r"\bspray\b", r"\bmist\b"], "powder": [r"\bpowder\b"],
    "oil": [r"\boil\b(?!\s*-?\s*free)"], "lotion": [r"\blotion\b"], "foam": [r"\bfoam(?:ing)?\b", r"\bmousse\b"],
    "bar": [r"\bbar\b"], "balm": [r"\bbalm\b"], "stick": [r"\bstick\b"], "serum": [r"\bserum\b"],
    "liquid": [r"\bliquid\b"], "wax": [r"\bwax\b"], "paste": [r"\bpaste\b"],
}
_FREE = {
    "paraben": [r"\bparaben[- ]free\b", r"\bfree (?:of|from) parabens?\b", r"\bno parabens?\b", r"\bwithout parabens?\b"],
    "sulfate": [r"\bsul(?:f|ph)ate[- ]free\b", r"\bno sul(?:f|ph)ates?\b", r"\bwithout sul(?:f|ph)ates?\b"],
    "alcohol": [r"\balcohol[- ]free\b", r"\bno alcohol\b", r"\bwithout alcohol\b"],
    "fragrance": [r"\bfragrance[- ]free\b", r"\bno (?:added )?fragrance\b", r"\bunscented\b"],
    "cruelty": [r"\bcruelty[- ]free\b", r"\bnot tested on animals\b"],
    "vegan": [r"\bvegan\b"],
    "gluten": [r"\bgluten[- ]free\b"],
    "silicone": [r"\bsilicone[- ]free\b", r"\bno silicones?\b"],
    "oil": [r"\boil[- ]free\b"],
}
PATTERNS = {"skin_type": _SKIN, "hair_type": _HAIR, "scent": _SCENT, "item_form": _FORM, "free_from": _FREE}

# Explicit contradiction of a free-from claim ("contains parabens") is only produced by edits.
_FREE_CONTRA = {k: [rf"\bcontains {k}s?\b", rf"\bwith (?:added )?{k}s?\b", rf"\b{k}-(?:based|containing|preserved)\b"]
                for k in _FREE}
_FREE_CONTRA["fragrance"].append(r"\bfragranced\b")

# Values whose co-occurrence with the needed value means the listing contradicts the need,
# when the needed value itself is not stated. Kept to unambiguous opposites.
OPPOSITES = {
    "skin_type": {"dry": {"oily"}, "oily": {"dry"}},
    "hair_type": {"curly": {"straight"}, "straight": {"curly", "wavy"}, "wavy": {"straight"},
                  "fine": {"thick"}, "thick": {"fine"}, "oily": {"dry"}, "dry": {"oily"}},
    "scent": {"unscented": {"lavender", "vanilla", "coconut", "rose", "citrus", "lemon", "mint", "eucalyptus", "floral"}},
    "item_form": {"gel": {"cream", "powder", "bar", "stick"}, "cream": {"gel", "spray", "powder", "liquid"},
                  "spray": {"cream", "bar", "stick", "balm", "powder"}, "powder": {"cream", "gel", "liquid", "oil", "lotion", "spray"},
                  "oil": {"powder", "bar"}, "lotion": {"powder", "bar", "stick"}, "bar": {"liquid", "gel", "spray", "cream", "lotion"},
                  "balm": {"spray", "liquid"}, "stick": {"spray", "liquid", "gel"}, "foam": {"powder", "bar", "stick"}},
}


def find_values(attr: str, text: str) -> dict[str, list[tuple[int, int]]]:
    """Return {canonical value: [spans]} stated in `text` for one attribute."""
    out: dict[str, list[tuple[int, int]]] = {}
    low = text.lower()
    for value, pats in PATTERNS[attr].items():
        spans = [m.span() for p in pats for m in re.finditer(p, low)]
        if spans:
            out[value] = sorted(set(spans))
    if attr in _LISTS:
        words, pat = _LISTS[attr]
        wpat = "|".join(sorted(map(re.escape, words), key=len, reverse=True))
        for m in re.finditer(pat, low):
            for w in re.findall(rf"\b(?:{wpat})\b", m.group(1)):
                out.setdefault(words[w], []).append(m.span())
        out = {k: sorted(set(v)) for k, v in out.items()}
    return out


def free_from_contradictions(text: str) -> set[str]:
    low = text.lower()
    return {k for k, pats in _FREE_CONTRA.items() if any(re.search(p, low) for p in pats)}


# ---- hidden `details` field -> canonical values -------------------------------------------
_DETAIL_KEYS = {"skin_type": ["Skin Type"], "hair_type": ["Hair Type"], "scent": ["Scent"],
                "item_form": ["Item Form"], "free_from": ["Material Type Free"]}


def details_values(attr: str, details: dict) -> set[str]:
    """Canonical values the hidden `details` field gives for an attribute."""
    raw = " , ".join(str(details[k]) for k in _DETAIL_KEYS[attr] if k in details)
    if not raw:
        return set()
    low = raw.lower()
    vals: set[str] = set()
    if attr in ("skin_type", "hair_type"):
        noun = "skin" if attr == "skin_type" else "hair"
        for tok in re.split(r"[,;/&]| and ", low):
            tok = tok.strip()
            if not tok:
                continue
            if tok in ("all", "all skin types", "all hair types", "all types"):
                vals.add("all")
                continue
            vals |= set(find_values(attr, f"{tok} {noun}"))
    elif attr == "scent":
        if re.search(r"unscented|fragrance[- ]free|no scent|scent[- ]free", low):
            vals.add("unscented")
        else:
            vals |= {v for v in find_values("scent", low) if v != "unscented"}
    elif attr == "item_form":
        vals |= set(find_values("item_form", low))
    elif attr == "free_from":
        for k in _FREE:
            if re.search(rf"\b{k}", low):
                vals.add(k)
        if "unscented" in low:
            vals.add("fragrance")
    return vals


# ---- support decision for one constraint over visible text ---------------------------------
@dataclass(frozen=True)
class Need:
    attr: str
    value: str

    def text(self) -> str:
        return NEED_TEXT[self.attr](self.value)


NEED_TEXT = {
    "skin_type": lambda v: f"I have {v.replace('_', '-')} skin, so it has to be made for {v.replace('_', '-')} skin.",
    "hair_type": lambda v: f"I have {v} hair, so it has to be made for {v} hair.",
    "scent": lambda v: ("It must be fragrance-free / unscented." if v == "unscented" else f"I want a {v} scent."),
    "item_form": lambda v: f"I want it as a {v}, not another form.",
    "free_from": lambda v: (f"It must be {v}-free." if v not in ("cruelty", "vegan") else
                            ("It must be cruelty-free." if v == "cruelty" else "It must be vegan.")),
}


def support_label(need: Need, text: str) -> str:
    """Deterministic L2 label of one need against visible listing text.

    entailed      the needed value (or 'all' for skin/hair type) is stated
    contradicted  an opposite value is stated and the needed one is not
    conflicting   the needed value and an opposite are both stated
    unresolved    otherwise
    """
    found = find_values(need.attr, text)
    if need.attr == "free_from":
        contra = need.value in free_from_contradictions(text)
        stated = need.value in found
        if stated and contra:
            return "conflicting"
        return "entailed" if stated else ("contradicted" if contra else "unresolved")
    stated = need.value in found or (need.attr in ("skin_type", "hair_type") and "all" in found)
    opp = OPPOSITES.get(need.attr, {}).get(need.value, set()) & set(found)
    if stated and opp:
        return "conflicting"
    if stated:
        return "entailed"
    if opp:
        return "contradicted"
    return "unresolved"
