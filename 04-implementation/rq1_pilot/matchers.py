"""Matchers. Every matcher sees only the rendered listing text (title, brand, bullets, description) and the
shopper's need. None sees `details`, the variant name or the label.

Each matcher returns, per item, a decision in {recommend, reject, abstain} and a score in [0, 1] where a
higher score means "more willing to recommend". Learn-then-Test thresholds the score (ltt.py).
"""
from __future__ import annotations

import json
import random
import re
from concurrent.futures import ThreadPoolExecutor

from attributes import Need
from llm import complete, parse_json

NAIVE_SYS = """You are an AI shopping assistant for an online beauty store. For each case you get a shopper's need and a product listing. Decide whether you would recommend the product to this shopper.
Reply with only a JSON array, one object per case, in the same order:
[{"id": "<case id>", "decision": "recommend" or "not_recommend", "confidence": <0-100, how confident you are that the product meets the shopper's need>}]"""

STRICT_SYS = """You check whether a product listing supports a shopper's requirement, for a recommender that must never recommend on assumptions.
Use ONLY what the listing text explicitly states. Do not use brand reputation, popularity, marketing claims, your own knowledge of the product, or what is typical for this kind of product.
- "recommend": the listing explicitly states the requirement is met. A statement that the product suits all skin types (or all hair types) counts for any single skin (or hair) type.
- "reject": the listing explicitly states something that contradicts the requirement.
- "abstain": the requirement is not stated, only implied, or stated vaguely.
Reply with only a JSON array, one object per case, in the same order:
[{"id": "<case id>", "decision": "recommend" or "reject" or "abstain", "support": <0-100, probability that the listing text explicitly states the requirement is met>}]"""

EXTRACT_SYS = """You extract product attributes that a listing text EXPLICITLY states. Never infer from the product type, ingredients, brand or marketing tone; if it is not stated, leave it empty.
Use only these values:
- skin_types: dry, oily, sensitive, combination, normal, acne_prone, all
- hair_types: curly, straight, wavy, fine, thick, dry, damaged, oily, all
- scent: "unscented" if it says unscented / fragrance-free; otherwise a named scent it says it has; else null
- item_forms: gel, cream, spray, powder, oil, lotion, foam, bar, balm, stick, serum, liquid, wax, paste
- free_from: paraben, sulfate, alcohol, fragrance, cruelty, vegan, gluten, silicone, oil (only if it says "X-free", "no X", "without X", "cruelty-free", "vegan")
- contains: any of paraben, sulfate, alcohol, fragrance, silicone, oil that it explicitly says it contains or is based on
Reply with only a JSON array, one object per listing, in the same order:
[{"id": "<listing id>", "skin_types": [], "hair_types": [], "scent": null, "item_forms": [], "free_from": [], "contains": []}]"""


def _case(item) -> str:
    return f"### Case {item.item_id}\nShopper's need: {item.need.text()}\nProduct listing:\n{item.listing.render()}\n"


def _batches(items, size, seed):
    order = list(items)
    random.Random(seed).shuffle(order)  # variants of one product never sit together in a predictable way
    return [order[i:i + size] for i in range(0, len(order), size)]


def _run_batched(items, system, backend, model, size, workers, seed, render=_case, key="item_id"):
    batches = _batches(items, size, seed)

    def one(batch):
        prompt = "\n".join(render(it) for it in batch)
        got = {}
        for attempt in range(3):
            raw = complete(backend, model, system, prompt + ("" if attempt == 0 else f"\n(retry {attempt})"))
            try:
                rows = parse_json(raw)
                got.update({str(r.get("id")): r for r in rows if isinstance(r, dict)})
            except ValueError:
                continue
            if all(getattr(it, key) in got for it in batch):
                break
        return {getattr(it, key): got.get(getattr(it, key)) for it in batch}

    out = {}
    with ThreadPoolExecutor(workers) as ex:
        for res in ex.map(one, batches):
            out.update(res)
    return out


def llm_naive(items, backend, model, size=10, workers=6, seed=0):
    raw = _run_batched(items, NAIVE_SYS, backend, model, size, workers, seed)
    out = {}
    for it in items:
        r = raw.get(it.item_id) or {}
        dec = "recommend" if str(r.get("decision", "")).lower().startswith("rec") else "abstain"
        conf = float(r.get("confidence", 50)) / 100
        out[it.item_id] = {"decision": dec, "score": conf if r else None}
    return out


def llm_strict(items, backend, model, size=10, workers=6, seed=0):
    raw = _run_batched(items, STRICT_SYS, backend, model, size, workers, seed)
    out = {}
    for it in items:
        r = raw.get(it.item_id) or {}
        d = str(r.get("decision", "abstain")).lower()
        dec = "recommend" if d.startswith("rec") else "reject" if d.startswith("rej") else "abstain"
        out[it.item_id] = {"decision": dec, "score": float(r.get("support", 0)) / 100 if r else None}
    return out


# ---- LLM extract, then rule ------------------------------------------------------------------
class _L:  # one listing to extract from
    def __init__(self, lid, text):
        self.lid, self.text = lid, text


def llm_extract_then_rule(items, backend, model, size=10, workers=6, seed=0):
    uniq = {}
    for it in items:
        txt = it.listing.render()
        uniq.setdefault(txt, _L(f"L{len(uniq)}", txt))
    raw = _run_batched(list(uniq.values()), EXTRACT_SYS, backend, model, size, workers, seed,
                       render=lambda l: f"### Listing {l.lid}\n{l.text}\n", key="lid")
    out = {}
    for it in items:
        ex = raw.get(uniq[it.listing.render()].lid) or {}
        dec = rule_on_extraction(it.need, ex)
        out[it.item_id] = {"decision": dec, "score": {"recommend": 1.0, "abstain": 0.5, "reject": 0.0}[dec],
                           "extraction": ex}
    return out


def rule_on_extraction(need: Need, ex: dict) -> str:
    from attributes import OPPOSITES
    norm = lambda xs: {str(x).lower().replace("-", "_").replace(" ", "_") for x in (xs or [])}
    if need.attr == "free_from":
        stated, contra = need.value in norm(ex.get("free_from")), need.value in norm(ex.get("contains"))
        return "recommend" if stated and not contra else "reject" if contra else "abstain"
    field = {"skin_type": "skin_types", "hair_type": "hair_types", "item_form": "item_forms"}.get(need.attr)
    if field:
        vals = norm(ex.get(field))
    else:
        s = ex.get("scent")
        vals = {str(s).lower()} if s else set()
    stated = need.value in vals or (need.attr in ("skin_type", "hair_type") and "all" in vals)
    if need.attr == "scent" and need.value == "unscented":
        opp = vals - {"unscented"}
    else:
        opp = OPPOSITES.get(need.attr, {}).get(need.value, set()) & vals
    if stated and not opp:
        return "recommend"
    return "reject" if opp and not stated else "abstain"


# ---- keyword rule (deliberately simple, independent of the edit generator's patterns) ---------
_KW = {
    "skin_type": lambda v: [f"{v.replace('_', '-')} skin", f"{v.replace('_', ' ')} skin", "all skin types"],
    "hair_type": lambda v: [f"{v} hair", "all hair types"],
    "scent": lambda v: ["unscented", "fragrance free", "fragrance-free"] if v == "unscented" else [v],
    "item_form": lambda v: [v],
    "free_from": lambda v: [f"{v}-free", f"{v} free", f"no {v}"],
}
_KW_OPP = {
    "skin_type": {"dry": ["oily skin"], "oily": ["dry skin"]},
    "hair_type": {"curly": ["straight hair"], "straight": ["curly hair", "wavy hair"], "wavy": ["straight hair"],
                  "fine": ["thick hair"], "thick": ["fine hair"], "dry": ["oily hair"], "oily": ["dry hair"]},
}


def keyword_rule(items, **_):
    out = {}
    for it in items:
        t = it.listing.render().lower()
        n = it.need
        hit = any(re.search(rf"\b{re.escape(k)}\b", t) for k in _KW[n.attr](n.value))
        opp = _KW_OPP.get(n.attr, {}).get(n.value, [])
        if n.attr == "free_from":
            opp = [f"{n.value}-based", f"contains {n.value}"] + (["fragranced"] if n.value == "fragrance" else [])
        if n.attr == "scent" and n.value == "unscented":
            opp = ["scented", "scent"]
        ohit = any(re.search(rf"\b{re.escape(k)}\b", t) for k in opp)
        dec = "recommend" if hit and not ohit else "reject" if ohit and not hit else "abstain"
        out[it.item_id] = {"decision": dec, "score": {"recommend": 1.0, "abstain": 0.5, "reject": 0.0}[dec]}
    return out


# ---- dense similarity probe: BLaIR (Hou et al.) and a generic sentence encoder ---------------
def dense_similarity(items, model="hyp1231/blair-roberta-base", batch=32, **_):
    """Cosine similarity between need and listing, CLS pooling as in BLaIR's released usage example.

    Needs `torch` + `transformers` and access to the Hugging Face hub (run on a machine that has it).
    """
    import numpy as np
    import torch
    from transformers import AutoModel, AutoTokenizer

    tok, enc = AutoTokenizer.from_pretrained(model), AutoModel.from_pretrained(model).eval()

    def embed(texts):
        vecs = []
        for i in range(0, len(texts), batch):
            x = tok(texts[i:i + batch], padding=True, truncation=True, max_length=512, return_tensors="pt")
            with torch.no_grad():
                h = enc(**x).last_hidden_state[:, 0]
            vecs.append(torch.nn.functional.normalize(h, dim=-1).numpy())
        return dict(zip(texts, np.concatenate(vecs)))

    tv = embed(sorted({it.listing.render() for it in items}))
    nv = embed(sorted({it.need.text() for it in items}))
    return {it.item_id: {"decision": None, "score": float(nv[it.need.text()] @ tv[it.listing.render()])}
            for it in items}


def save(results: dict, path: str):
    with open(path, "w") as f:
        json.dump(results, f)
