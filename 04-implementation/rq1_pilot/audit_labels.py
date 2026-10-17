"""Estimate the rule parser's label error ε on unedited listings (refined-thesis-plan §11.3), without humans.

A second, independent judge (Claude Opus, a model not evaluated as a matcher, with its own prompt) must QUOTE
the listing passage that states or contradicts the requirement. A quote counts only if it occurs verbatim in the
listing. The judge's label (verbatim support quote -> entailed; else verbatim contradiction quote ->
contradicted; else unresolved) is compared with the parser / construction label on every item, edited or not.
Disagreements are where the parser or the edit (or the judge) is wrong; their rate estimates ε, and the
"audited" analysis keeps only items where both agree (the two-extractor agreement filter of §11.3).

    python audit_labels.py
"""
from __future__ import annotations

import json
import os
import re
from collections import Counter

from matchers import _run_batched
from run_pilot import OUT, load_items

JUDGE_MODEL = "claude-opus-5-5"

JUDGE_SYS = """For each case, find evidence in the product listing for the shopper's requirement.
"support_quote": copy, word for word, the shortest passage of the listing that explicitly states the requirement is met (a statement that it suits all skin or hair types counts for any single type). Use "" if nothing in the listing states it explicitly; implied or typical is not enough.
"contradict_quote": copy word for word a passage that explicitly contradicts the requirement, or "".
Reply with only a JSON array, one object per case, in the same order:
[{"id": "<case id>", "support_quote": "...", "contradict_quote": "..."}]"""


def _norm(s):
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", s.lower())).strip()


def main():
    items = load_items()
    raw = _run_batched(items, JUDGE_SYS, "claude", JUDGE_MODEL, 10, 6, 1)
    rows, c = [], Counter()
    for it in items:
        r = raw.get(it.item_id) or {}
        page = _norm(it.listing.render())
        q = str(r.get("support_quote") or "")
        cq = str(r.get("contradict_quote") or "")
        sup = bool(q) and _norm(q) in page
        con = bool(cq) and _norm(cq) in page
        judge = "entailed" if sup else "contradicted" if con else "unresolved"
        c["unverbatim_quote"] += (bool(q) and not sup) + (bool(cq) and not con)
        c["unparsed"] += not r
        rows.append({"item_id": it.item_id, "variant": it.variant, "need": it.need.text(), "parser": it.label,
                     "judge": judge if r else None, "judge_quote": q, "contradict_quote": cq,
                     "agree": bool(r) and judge == it.label})
    n = len(items)
    by_variant = {}
    for v in sorted({x["variant"] for x in rows}):
        sub = [x for x in rows if x["variant"] == v]
        by_variant[v] = {"n": len(sub), "agree": sum(x["agree"] for x in sub),
                         "judge_labels": dict(Counter(x["judge"] for x in sub))}
    res = {"n": n, "judge_model": JUDGE_MODEL, "agreement_rate": sum(x["agree"] for x in rows) / n,
           "by_variant": by_variant, "judge_quotes_not_verbatim": c["unverbatim_quote"], "unparsed": c["unparsed"]}
    json.dump({"summary": res, "rows": rows}, open(os.path.join(OUT, "label_audit.json"), "w"), indent=1)
    print(json.dumps(res, indent=2))
    for x in rows[:400]:
        if not x["agree"]:
            print("-", x["variant"], "|", x["need"], "| parser:", x["parser"], "| judge:", x["judge"], "|",
                  (x["judge_quote"] or x["contradict_quote"])[:120])


if __name__ == "__main__":
    main()
