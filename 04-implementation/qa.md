# QA

*Stage 4 of [WORKFLOW.md](../WORKFLOW.md). Every module must be tested; record the method and result here.*

| Module | Test method | Result | Date (YYYY-MM-DD) |
|---|---|---|---|
| `rq1_pilot/attributes.py` (parser, `details` normaliser, support label) | Unit tests on 9 phrasing cases (lists like "Oily, Combination, Dry skin", "all skin types", negative "dry hands"), 5 `details` cases, 9 label cases incl. the "all types" rule, "absence is never contradiction" and conflicting text (`tests/test_pilot.py`) | Pass | 2026-10-17 |
| `rq1_pilot/attributes.py` on real listings | Independent quote judge (Claude, verbatim-quote check) on 400 unedited listings: parser vs judge disagree on 11.8% (27 parser false positives, e.g. "apply on dry hair", "Do not use on dry skin", wigs; 20 misses, e.g. "Fragrance and Colorant Free", "dry, lifeless hair") | Known error rate ε ≈ 12%; reported, not fixed in this pilot | 2026-10-17 |
| `rq1_pilot/data.py` | Unit test: `render()` never shows the `details` field | Pass | 2026-10-17 |
| `rq1_pilot/edits.py` | Unit tests: remove deletes every statement and keeps unrelated sentences; vague → unresolved; contradict → contradicted; famous-brand swap removes the old brand and adds hype. In the build, every edited item is re-labelled by the parser and dropped if the label is not the intended one | Pass; 1,356 items kept from 250 products + 150 natural-missing | 2026-10-17 |
| `rq1_pilot/edits.py` on real listings | Same quote judge on every edited item (`audit_labels.py`): residual evidence the parser missed ("coily hair", "dull, damaged, thin hair", "Safe for all skin") | Judge agrees with 80% of all items (original 88%, remove 85%, vague 80%, contradict 53%); disagreements dropped from the audited analysis | 2026-10-17 |
| `rq1_pilot/matchers.py` | Unit tests: extract-then-rule decisions (6 cases), keyword rule, JSON parsing with fences/prose, **prompt shows no variant name, label, ASIN or attribute key** | Pass. The first Claude runs leaked the variant through case ids; caught on inspection, ids made opaque, runs discarded and redone | 2026-10-17 |
| `rq1_pilot/llm.py` | Unit test: cache hit on second call (no second backend call) | Pass | 2026-10-17 |
| `rq1_pilot/ltt.py` | Unit tests: binomial p-value edge cases; separable scores give a threshold in the gap; 50%-risk scores give no threshold; validity simulation (200 splits) has violation rate ≤ 0.15 at δ = 0.1 | Pass | 2026-10-17 |
| `rq1_pilot/mine_needs.py` | Automatic checks on 600 real reviews: 43/43 quotes verbatim, 43/43 in vocabulary, 24/43 lexical match; second model on 200 reviews: 98.5% review-level agreement, precision 0.80 / recall 0.86 vs the second model | Pass | 2026-10-17 |

Run: `cd 04-implementation/rq1_pilot && python -m pytest -q tests` → 32 passed.
