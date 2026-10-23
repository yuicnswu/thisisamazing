"""RQ1 hard split: where does a strict "only if stated" prompt stop being enough? (03-solution-design/project-spec.md §RQ1)

The first pilot (05-report, 2026-10-17) used one-constraint needs with evidence stated in the parser's own words, and a
strict prompt brought URR down to 5-10%. This module builds the two cells the redesign says matter most and that can
be built from All_Beauty without new data:

  conj      Needs with TWO checkable constraints (k = 2) on products whose visible text and hidden `details` agree on
            both. Variants: original (both entailed), and one constraint removed / blurred / contradicted while the
            other stays entailed. Conjunctive label: contradicted if any constraint is, else unresolved if any is,
            else entailed.
  para      One-constraint needs where the stating passage is PARAPHRASED by an LLM so that the rule parser no longer
            finds it, and an independent quote judge still finds a verbatim passage that states it. Label: entailed.
            Tests recall on evidence a keyword or typed check can't see.

Matchers (all see only Listing.render()):
  strict_joint      the strict prompt, given the whole k-constraint need at once (what a deployed assistant does)
  strict_decomp     the strict prompt per constraint; recommend only if every constraint is recommended
  nesy_decomp       the NeSy verifier per constraint; e = min, c = max over constraints (theory.md Prop 4)
  keyword_decomp    the keyword rule per constraint

    python hard_split.py build         # outputs/hard/items.jsonl (+ paraphrase generation and its judge, cached)
    python hard_split.py run           # all matchers, Claude Haiku + Sonnet, cached in outputs/hard/llm_cache.jsonl
    python hard_split.py analyze       # outputs/hard/results.{json,md}
"""
from __future__ import annotations

import json
import os
import random
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass

OUT = os.path.join(os.path.dirname(__file__), "outputs", "hard")
os.environ.setdefault("LLM_CACHE", os.path.join(OUT, "llm_cache.jsonl"))

import numpy as np  # noqa: E402

import matchers as M  # noqa: E402
from attributes import Need, find_values, support_label  # noqa: E402
from data import Listing, load_listings  # noqa: E402
from edits import _map_text, _sentences, _spans, candidate_needs, contradict, remove, vague  # noqa: E402

JUDGE_MODEL = "claude-opus-5-5"
PARA_MODEL = "claude-sonnet-5-5"
MODELS = ["claude-haiku-5-5", "claude-sonnet-5-5"]
N_CONJ, N_PARA, SEED = 240, 320, 7


@dataclass
class Sub:
    """One (listing, single constraint) case, the unit the per-constraint matchers see."""
    item_id: str
    need: Need
    listing: Listing


class JointNeed:
    def __init__(self, needs):
        self.needs = needs

    def text(self) -> str:
        return " ".join(n.text() for n in self.needs) + " All of these must hold."


@dataclass
class Joint:
    item_id: str
    need: JointNeed
    listing: Listing


def conj_label(labels: list[str]) -> str:
    if "contradicted" in labels or "conflicting" in labels:
        return "contradicted"
    if "unresolved" in labels:
        return "unresolved"
    return "entailed"


# ---------------------------------------------------------------- build
def _text_needs(l: Listing) -> list[Need]:
    """Values the visible text states (parser), excluding named scents and 'all' (as candidate_needs does)."""
    out = []
    text = l.visible_text()
    for attr in ("skin_type", "hair_type", "scent", "item_form", "free_from"):
        for val in sorted(find_values(attr, text)):
            if val == "all" or (attr == "scent" and val != "unscented"):
                continue
            out.append(Need(attr, val))
    return out


def _two_needs(l: Listing, rng: random.Random):
    """Edited constraint: agreed by visible text AND hidden `details` (as in the first pilot). Second constraint: any
    other attribute the visible text states (the quote judge audits it). Prefer non-item-form constraints."""
    agreed = [n for n in candidate_needs(l)]
    if not agreed:
        return None
    rng.shuffle(agreed)
    agreed.sort(key=lambda n: n.attr == "item_form")
    first = agreed[0]
    others = [n for n in _text_needs(l) if n.attr != first.attr]
    if not others:
        return None
    rng.shuffle(others)
    others.sort(key=lambda n: n.attr == "item_form")
    return [first, others[0]]


def build_conj(listings, rng):
    rows = []
    pool = [l for l in listings]
    rng.shuffle(pool)
    for l in pool:
        needs = _two_needs(l, rng)
        if not needs:
            continue
        target = 0  # the edit hits the details-agreed constraint; the other stays as stated
        n = needs[target]
        variants = {"original": l, f"remove": remove(l, n.attr), f"vague": vague(l, n.attr, n.value),
                    f"contradict": contradict(l, n.attr, n.value, rng)}
        intended = {"original": "entailed", "remove": "unresolved", "vague": "unresolved", "contradict": "contradicted"}
        built = []
        for name, lv in variants.items():
            if lv is None or not lv.title:
                continue
            labs = [support_label(x, lv.visible_text()) for x in needs]
            other = labs[1 - target]
            if labs[target] != intended[name] or other != "entailed":
                continue  # the edit must hit the target constraint only, and leave the other one entailed
            built.append({"item_id": f"{l.asin}|conj|{name}", "asin": l.asin, "cell": "conj", "variant": name,
                          "needs": [[x.attr, x.value] for x in needs], "target": target,
                          "label": conj_label(labs), "listing": _dump(lv)})
        if any(b["variant"] == "original" for b in built) and len(built) >= 3:
            rows += built
        if len({r["asin"] for r in rows}) >= N_CONJ:
            break
    return rows


PARA_SYS = """You rewrite short passages of a product listing. For each case you get passages and a fact they state.
Rewrite EACH passage so that it still states the same fact explicitly and unambiguously, keeps everything else it says, and reads naturally, but does NOT use any of the banned phrases (or close spelling variants of them). Use a different, everyday way of saying the fact (for example "for coils and ringlets" instead of "curly hair", "free of added perfume" instead of "fragrance-free").
Reply with only a JSON array, one object per case, in the same order:
[{"id": "<case id>", "passages": ["<rewritten passage 1>", "..."]}]"""

BANNED = {
    "skin_type": lambda v: [f"{v.replace('_', '-')} skin", f"{v.replace('_', ' ')} skin", "all skin types"],
    "hair_type": lambda v: [f"{v} hair", "all hair types"] + (["curls"] if v == "curly" else []),
    "scent": lambda v: ["unscented", "fragrance-free", "fragrance free", "scent-free", "no fragrance",
                        "without fragrance", "perfume-free", "no added fragrance"],
    "free_from": lambda v: [f"{v}-free", f"{v} free", f"no {v}", f"no {v}s", f"without {v}", f"without {v}s",
                            f"free of {v}s", f"free from {v}s"],
}


class _Case:
    def __init__(self, cid, text):
        self.cid, self.text = cid, text


def build_para(listings, rng, exclude):
    pool = []
    for l in listings:
        if l.asin in exclude:
            continue
        needs = [n for n in candidate_needs(l) if n.attr in BANNED]
        if needs:
            pool.append((l, rng.choice(needs)))
    rng.shuffle(pool)
    pool = pool[:N_PARA]
    cases, segs = [], {}
    for i, (l, n) in enumerate(pool):
        # Passages that state the value: the title and any bullet / description sentence with a parser span.
        passages = []
        if _spans(n.attr, l.title):
            passages.append(("title", l.title))
        for k, b in enumerate(l.bullets):
            for s in _sentences(b):
                if _spans(n.attr, s):
                    passages.append((f"b{k}", s))
        for k, d in enumerate(l.description):
            for s in _sentences(d):
                if _spans(n.attr, s):
                    passages.append((f"d{k}", s))
        if not passages or len(passages) > 6:
            continue
        cid = f"P{i:04d}"
        segs[cid] = (l, n, passages)
        body = "\n".join(f"  passage {j + 1}: {p}" for j, (_, p) in enumerate(passages))
        cases.append(_Case(cid, f"### Case {cid}\nFact: {n.text()}\nBanned phrases: {', '.join(BANNED[n.attr](n.value))}\n"
                                f"Passages:\n{body}\n"))
    raw = M._run_batched(cases, PARA_SYS, "claude", PARA_MODEL, 8, 6, SEED, render=lambda c: c.text, key="cid", shown=str)
    rows = []
    for cid, r in raw.items():
        l, n, passages = segs[cid]
        new = (r or {}).get("passages") or []
        if len(new) != len(passages):
            continue
        lv = _apply(l, passages, [str(x) for x in new])
        if support_label(n, lv.visible_text()) != "unresolved":
            continue  # the rule parser still sees it (or sees a contradiction): not a paraphrase
        rows.append({"item_id": f"{l.asin}|para|paraphrase", "asin": l.asin, "cell": "para", "variant": "paraphrase",
                     "needs": [[n.attr, n.value]], "target": 0, "label": "entailed", "listing": _dump(lv)})
        rows.append({"item_id": f"{l.asin}|para|original", "asin": l.asin, "cell": "para", "variant": "original",
                     "needs": [[n.attr, n.value]], "target": 0, "label": "entailed", "listing": _dump(l)})
    return rows


def _apply(l: Listing, passages, new) -> Listing:
    rep = dict(zip([p for _, p in passages], new))
    title = rep.get(l.title, l.title)

    def seg(s):
        return " ".join(rep.get(x, x) for x in _sentences(s))
    out = _map_text(l, lambda t: t, seg)
    out.title = title
    return out


def _dump(l: Listing) -> dict:
    return {"asin": l.asin, "title": l.title, "bullets": l.bullets, "description": l.description, "store": l.store,
            "source": l.source}


def _load_listing(d) -> Listing:
    return Listing(d["asin"], d["title"], d["bullets"], d["description"], {}, d["store"], d["source"])


def subs_of(row) -> list[Sub]:
    l = _load_listing(row["listing"])
    return [Sub(f"{row['item_id']}#{i}", Need(*n), l) for i, n in enumerate(row["needs"])]


def judge(rows):
    """Independent quote judge (as in audit_labels.py) on every constraint; returns per-row agreement."""
    from audit_labels import JUDGE_SYS, _norm
    subs = [s for r in rows for s in subs_of(r)]
    raw = M._run_batched(subs, JUDGE_SYS, "claude", JUDGE_MODEL, 10, 6, 1)
    per = {}
    for s in subs:
        r = raw.get(s.item_id) or {}
        page = _norm(s.listing.render())
        q, cq = str(r.get("support_quote") or ""), str(r.get("contradict_quote") or "")
        lab = "entailed" if q and _norm(q) in page else "contradicted" if cq and _norm(cq) in page else "unresolved"
        per[s.item_id] = lab if r else None
    for r in rows:
        labs = [per.get(s.item_id) for s in subs_of(r)]
        r["judge"] = None if None in labs else conj_label(labs)
        r["judge_agree"] = r["judge"] == r["label"]


def build():
    os.makedirs(OUT, exist_ok=True)
    rng = random.Random(SEED)
    listings = load_listings()
    conj = build_conj(listings, rng)
    para = build_para(listings, rng, {r["asin"] for r in conj})
    rows = conj + para
    judge(rows)
    with open(os.path.join(OUT, "items.jsonl"), "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    c = Counter((r["cell"], r["variant"], r["label"], r["judge_agree"]) for r in rows)
    for k, v in sorted(c.items()):
        print(k, v)


# ---------------------------------------------------------------- run
def load_rows():
    return [json.loads(l) for l in open(os.path.join(OUT, "items.jsonl"))]


def run():
    rows = load_rows()
    subs = [s for r in rows for s in subs_of(r)]
    joint = [Joint(r["item_id"], JointNeed([Need(*n) for n in r["needs"]]), _load_listing(r["listing"]))
             for r in rows if r["cell"] == "conj"]
    preds = {}
    preds["keyword_decomp"] = M.keyword_rule(subs)
    for m in MODELS:
        preds[f"strict_joint__{m}"] = M.llm_strict(joint, "claude", m)
        preds[f"strict_decomp__{m}"] = M.llm_strict(subs, "claude", m)
        preds[f"nesy_decomp__{m}"] = M.nesy_verifier(subs, "claude", m)
    json.dump(preds, open(os.path.join(OUT, "preds.json"), "w"))
    print({k: len(v) for k, v in preds.items()})


# ---------------------------------------------------------------- analyze
def decisions(rows, preds):
    """item_id -> {matcher: decision}. Per-constraint matchers combine: reject if any reject, recommend if all do."""
    out = defaultdict(dict)
    for name, p in preds.items():
        for r in rows:
            if name.startswith("strict_joint"):
                if r["cell"] != "conj":
                    continue
                d = (p.get(r["item_id"]) or {}).get("decision")
            else:
                ds = [(p.get(s.item_id) or {}).get("decision") for s in subs_of(r)]
                if None in ds:
                    d = None
                elif "reject" in ds:
                    d = "reject"
                elif all(x == "recommend" for x in ds):
                    d = "recommend"
                else:
                    d = "abstain"
            out[r["item_id"]][name] = d
    return out


def _ci(vals, groups, n_boot=1000, seed=0):
    from analyze import cluster_ci
    m, lo, hi = cluster_ci(vals, groups, n_boot, seed)
    return m, lo, hi


def analyze():
    rows = load_rows()
    preds = json.load(open(os.path.join(OUT, "preds.json")))
    dec = decisions(rows, preds)
    names = list(preds)
    res = {"n_items": len(rows), "cells": {}, "urr": {}}
    md = ["# RQ1 hard split: two-constraint needs and paraphrased evidence (Claude Haiku / Sonnet, real All_Beauty listings)", ""]
    for audited in (True, False):
        sub = [r for r in rows if r["judge_agree"]] if audited else rows
        tag = "audited" if audited else "all"
        md += [f"## {'Audited items (quote judge agrees with the label)' if audited else 'All items'}", "",
               "Recommend rate [product-cluster bootstrap 95% CI]. Ideal: high on `original` and `paraphrase`, 0 elsewhere.", ""]
        cells = [("conj", v) for v in ("original", "remove", "vague", "contradict")] + [("para", v) for v in ("original", "paraphrase")]
        md.append("| Matcher | " + " | ".join(f"{c} {v} (n)" for c, v in cells) + " | conj URR | para recall |")
        md.append("|" + "---|" * (len(cells) + 3))
        for name in names:
            line, stats = [name], {}
            for c, v in cells:
                rs = [r for r in sub if r["cell"] == c and r["variant"] == v and dec[r["item_id"]].get(name) is not None]
                if not rs:
                    line.append("–")
                    continue
                vals = [dec[r["item_id"]][name] == "recommend" for r in rs]
                m, lo, hi = _ci(vals, [r["asin"] for r in rs])
                stats[f"{c}/{v}"] = {"n": len(rs), "rec": m, "lo": lo, "hi": hi}
                line.append(f"{100 * m:.0f}% [{100 * lo:.0f}, {100 * hi:.0f}] ({len(rs)})")
            # URR on the conjunction cell: unsupported among recommended
            rec = [r for r in sub if r["cell"] == "conj" and dec[r["item_id"]].get(name) == "recommend"]
            if rec:
                bad = [r["label"] != "entailed" for r in rec]
                m, lo, hi = _ci(bad, [r["asin"] for r in rec])
                stats["conj_urr"] = {"n_rec": len(rec), "urr": m, "lo": lo, "hi": hi}
                line.append(f"{100 * m:.0f}% [{100 * lo:.0f}, {100 * hi:.0f}] (of {len(rec)})")
            else:
                line.append("–")
            pr = stats.get("para/paraphrase")
            line.append(f"{100 * pr['rec']:.0f}%" if pr else "–")
            md.append("| " + " | ".join(line) + " |")
            res["cells"].setdefault(tag, {})[name] = stats
        md.append("")
    agree = Counter((r["cell"], r["variant"], r["judge_agree"]) for r in rows)
    md += ["## Label audit (Claude Opus quote judge, per constraint)", "", "| cell | variant | judge agrees | judge disagrees |", "|---|---|---|---|"]
    for c, v in sorted({(r["cell"], r["variant"]) for r in rows}):
        md.append(f"| {c} | {v} | {agree[(c, v, True)]} | {agree[(c, v, False)]} |")
    json.dump(res, open(os.path.join(OUT, "results.json"), "w"), indent=1)
    open(os.path.join(OUT, "results.md"), "w").write("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    {"build": build, "run": run, "analyze": analyze}[sys.argv[1]]()
