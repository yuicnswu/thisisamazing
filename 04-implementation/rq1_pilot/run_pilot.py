"""Build the pilot benchmark and run matchers.

    python run_pilot.py build                       # outputs/items.jsonl
    python run_pilot.py run <matcher> [backend model]

Matchers: naive, strict, extract, nesy (LLM; need backend + model), keyword, dense.
Predictions go to outputs/preds/<matcher>__<model>.json.
"""
from __future__ import annotations

import json
import os
import sys

import matchers as M
from attributes import Need
from data import Listing, load_listings
from edits import Item, build_calpool, build_items

OUT = os.path.join(os.path.dirname(__file__), "outputs")
# POOL=cal switches every command to the one-item-per-product calibration pool (theory.md A1)
POOL = os.environ.get("POOL", "")
ITEMS = os.path.join(OUT, "calpool.jsonl" if POOL == "cal" else "items.jsonl")
PREDS = os.path.join(OUT, "preds_cal" if POOL == "cal" else "preds")
N_PRODUCTS, N_MISSING, SEED = 250, 150, 0
N_CAL_MISSING = 300


def build():
    if POOL == "cal":
        exclude = {json.loads(l)["asin"] for l in open(os.path.join(OUT, "items.jsonl"))}
        items = build_calpool(load_listings(), exclude, N_CAL_MISSING)
    else:
        items = build_items(load_listings(), N_PRODUCTS, N_MISSING, SEED)
    os.makedirs(OUT, exist_ok=True)
    with open(ITEMS, "w") as f:
        for it in items:
            l = it.listing
            f.write(json.dumps({"item_id": it.item_id, "asin": it.asin, "variant": it.variant,
                                "need": [it.need.attr, it.need.value], "need_text": it.need.text(), "label": it.label,
                                "listing": {"asin": l.asin, "title": l.title, "bullets": l.bullets,
                                            "description": l.description, "store": l.store, "source": l.source},
                                "rendered": l.render()}) + "\n")
    print(f"{len(items)} items -> {ITEMS}")


def load_items() -> list[Item]:
    out = []
    with open(ITEMS) as f:
        for line in f:
            r = json.loads(line)
            L = r["listing"]
            out.append(Item(r["item_id"], r["asin"], r["variant"], Need(*r["need"]), r["label"],
                            Listing(L["asin"], L["title"], L["bullets"], L["description"], {}, L["store"], L["source"])))
    return out


def run(name, backend=None, model=None):
    items = load_items()
    fn = {"naive": M.llm_naive, "strict": M.llm_strict, "extract": M.llm_extract_then_rule,
          "keyword": M.keyword_rule, "dense": M.dense_similarity, "nesy": M.nesy_verifier}[name]
    if name == "dense":
        kw = {"model": backend} if backend else {}  # `run dense <hf model id>`
        model = backend or "hyp1231/blair-roberta-base"
    else:
        kw = {"backend": backend, "model": model} if backend else {}
    if backend == "ollama":
        kw.update(size=5, workers=1)
    res = fn(items, **kw)
    os.makedirs(PREDS, exist_ok=True)
    tag = f"{name}__{(model or 'none').replace('/', '_').replace(':', '_')}"
    M.save(res, os.path.join(PREDS, tag + ".json"))
    missing = sum(v["score"] is None for v in res.values())
    print(f"{tag}: {len(res)} predictions, {missing} unparsed")


if __name__ == "__main__":
    if sys.argv[1] == "build":
        build()
    else:
        run(sys.argv[2], *sys.argv[3:5])
