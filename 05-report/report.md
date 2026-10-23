# Report

*Stage 5 of [WORKFLOW.md](../WORKFLOW.md). System test and experiment results. Every entry carries its test date (YYYY-MM-DD). Update after every new run.*

---

## 2026-10-21 · Category feasibility evidence that doesn't need the metadata files

Code: `04-implementation/category_check/category_check.py` (tests in `category_check/tests`). Output: `category_check/outputs/category_check.json`.

The G0 listing count for Beauty_and_Personal_Care and Home_and_Kitchen needs their metadata files. Both the cloud container and the Mac's sandboxed shell get HTTP 403 from the UCSD and Hugging Face hosts, so that count is still open (it has to run from the Mac host's own shell). This entry records what could be computed.

**1. Products Algorithm 1 needs** (exact binomial test, δ = 0.10, 90% chance of certifying, the NeSy verifier's pilot coverage of 13%, 40% of products in the certify split):

| Target α | verifier's true URR 2% | 3% | 4% |
|---|---|---|---|
| 0.10 | 52 recommended items → 1,000 products | 78 → 1,500 | 116 → 2,231 |
| 0.05 | 258 → 4,962 | 656 → 12,616 | 2,937 → 56,481 |

The pilot certified α = 0.10 on 2,182 products, consistent with the table. α = 0.05 is only realistic if the verifier's true URR is about 2–3% **and** the category gives 5,000–13,000 usable products.

**2. Early verified reviews that mention a checkable attribute** (first 10 per product, rule proxy; a mention is not a labelled need):

| | All_Beauty | Appliances |
|---|---|---|
| Reviews in file | 701,528 | 2,128,605 |
| Products with a verified review | 106,811 | 90,276 |
| … with ≥ 10 verified reviews | 11,851 (11%) | 22,283 (25%) |
| Early verified reviews | 343,706 | 396,393 |
| Mention a checkable attribute | 17,776 (**5.2%**) | 34,201 (**8.6%**) |
| By type | hair type 2.7%, scent 1.3%, skin type 1.1%, free-from 0.4% | fit / compatibility with a named model 7.2%, dimensions 0.8%, capacity 0.6%, electrical 0.3% |

Appliances is the only hard-goods review file available here, used as a stand-in for Home & Kitchen, not a substitute for counting it. Its fit/compatibility pattern was tightened after reading samples (the first version counted "fits perfectly", which names no target; that version gave 12.8%).

**3. Disclosure inventory** (from the pilot's 6,503 listings): 2,435 listings (37%) have at least one checkable attribute in the hidden `details` field that their visible text never states; 1,878 (29%) excluding item form. By attribute: skin type 864, item form 830, hair type 784, scent 236, free-from 106. This is the merchant-fix loop's test bed: `details` plays the truthful seller.

**What it means.** Neither category reaches the plan's 10% need-rate bar on a rule proxy, though hard goods do better and are better reviewed. The recommendation in `03-solution-design/project-spec.md` ("Categories") is to count G0 on both Beauty_and_Personal_Care and Home_and_Kitchen from the Mac host and build on both.

---

## 2026-10-18 · Neuro-symbolic selective matcher with a certified URR (Algorithm 1 of theory.md)

Code: `rq1_pilot/matchers.py` (`nesy_verifier`), `rq1_pilot/conformal.py` (Algorithm 1), `rq1_pilot/analyze_conformal.py`. Raw tables: `rq1_pilot/outputs/conformal.md`. The calibration follows `03-solution-design/theory.md` (PR #7) exactly: Theorem 1's fixed-sequence test with p = max(p_rec, p_rej), assumption A1 (one item per product), the 20% tune split that fixes the path start, and Theorem 3's consensus labels.

### Method

1. **Neural evidence proposer.** For each (listing, need) the LLM returns a verbatim support quote, a verbatim contradiction quote, and a confidence for each. It sees only the rendered listing, like every other matcher.
2. **Symbolic certificate.** Deterministic checks on each quote: *grounded* (it occurs verbatim in the listing) and *typed* (it names the needed value, or its opposite from the attribute ontology, e.g. "all skin" for any skin type; "fragrance-free" can never count as a contradiction). The surface-form lists are independent of the label parser's patterns.
3. **Score.** Entailment score e and contradiction score c are ordered lexicographically: certificate tier first (grounded and typed, then grounded only, then neither), neural confidence within a tier.
4. **Three-way decision with a guarantee.** Reject if c ≥ τ, recommend if e ≥ λ, otherwise abstain. Learn-then-Test fixed-sequence testing on calibration products certifies (λ, τ) with URR ≤ α and URJ ≤ α' = 0.10 with probability ≥ 1 − δ (δ = 0.10), or certifies nothing and abstains on everything.

**Calibration pool.** The 399 pilot products are far too few under A1, as theory.md §2 predicted: no matcher certifies α = 0.10 on them alone. So I built a second pool of **1,783 new products, one item each** (a random edit of its own listing, or natural missing evidence), labelled by the same parser plus the same independent Opus quote judge (85% agreement, no non-verbatim quotes). Combined: 2,182 products. There were 50 product splits: half for calibration (one item drawn per product, 20% of that tunes the path), half for test (each product weighted equally).

### Results (consensus labels, α = 0.10, δ = 0.10)

| Matcher | splits certified | test URR | coverage | recall of supported | splits with URR > α |
|---|---|---|---|---|---|
| **NeSy verifier, Sonnet** | 100% | **4.0%** [1.0, 8.8] | 12.7% | **88%** | 0% |
| **NeSy verifier, Haiku** | 100% | **4.1%** [1.1, 10.5] | 13.1% | **90%** | 6% |
| Same LLM outputs, no symbolic certificate (Sonnet / Haiku) | 0% / 0% | – | 0 | 0 | – |
| Strict "only if stated" prompt (Sonnet / Haiku) | 0% / 0% | – | 0 | 0 | – |
| Keyword rule | 0% | – | 0 | 0 | – |

Brackets are 2.5–97.5% across splits.
- **The symbolic certificate is what makes the guarantee reachable.** The neural scores alone, or the strict prompt's support score, put too many unsupported items among their most confident ones, and fixed-sequence testing stops at the first step. Grounded-and-typed quotes separate supported from unsupported items cleanly enough to certify at α = 0.10 with 88–90% recall of supported listings.
- **At α = 0.20 everyone certifies something, but the gap stays.** Strict Sonnet certifies in only 8% of splits (recall 3%), while the NeSy verifier certifies in 98–100% (recall 90–93%).
- **The guarantee held empirically.** Test URR exceeded α in 0–6% of splits, under δ = 10%.
- **Native decisions (calibration pool, consensus labels), without calibration.** The NeSy verifier recommends 0–0.7% of removed, vague, brand-plus-hype and natural-missing listings and 86–89% of originals (URR 3.3–4.8%). The strict prompt recommends 5–10% of them (URR 30%).

### What it costs, and what is still open

- **Paraphrased evidence is the price.** On pilot items where the judge found verbatim support the parser missed ("coily hair" for curly, "Safe for all skin"), the verifier recommends 0–2%, against ~60% for the strict prompt. The typed check wants the value named, so the verifier inherits part of the rule's recall gap. A learned typed check (an NLI model on the quote only) is the obvious next step and keeps the same guarantee.
- **The guarantee is against labels, not truth.** By Theorem 3 the true URR is at most α plus the rate at which the parser *and* the judge both wrongly say "entailed" on recommended items. The judge (Opus) is the same model family as the verifier, so assumption A2 is weaker than theory.md wants; an open-weight judge from the Mac run would fix that. The observable one-sided disagreement among the verifier's recommendations is 1.8–3.3%.
- **Not yet tested.** Prop 4 (conjunctions: needs here have one constraint) and Theorem 4 (the new-vs-established coverage gap) are not tested yet. α = 0.05 is also out of reach: it needs about 3,900 independent products at this coverage, and All_Beauty has about 2,200 usable ones.

---

## 2026-10-17 · RQ1 pilot on real All_Beauty listings (first real run)

Code: [`04-implementation/rq1_pilot`](../04-implementation/rq1_pilot). Module tests: [`04-implementation/qa.md`](../04-implementation/qa.md). Raw tables: `rq1_pilot/outputs/results.md`; every model reply is cached in `outputs/llm_cache.jsonl`, so all numbers below rerun for free with `python analyze.py`.

This replaces the RQ1 part of `benchmark_outputs/BENCHMARK_RESULTS.md`, which came from a simulation (coin-flip baselines, a "proposed" matcher that read the variant name). Nothing here is simulated: every decision is a model call on a real listing.

### Bottom line

1. **Naive LLM recommenders do license matches on priors.** Asked plainly whether to recommend, Claude Haiku 5.5 and Sonnet 5.5 still recommend **24–33%** of real listings after the deciding attribute was removed or blurred, and **27–31%** of unedited listings whose text never states it (audited items). Their unsupported recommendation rate (URR) is **54–57%**.
2. **But a strong "only if stated" prompt nearly closes the gap.** The same models with the strict prompt recommend **0–3%** of evidence-missing listings and **0%** of contradicted ones, keeping 80–90% of supported ones. URR falls to **5% (Haiku) and 10% (Sonnet)**. This is the reviewers' "rules / prompting may already solve it" point, and on this pilot it largely holds.
3. **Brand and hype did not move the models.** Swapping in a famous brand plus a "#1 dermatologist-recommended" bullet on top of the removed listing flipped decisions in both directions about equally (naive Sonnet: 18 abstain→recommend, 23 the other way; strict: 1 vs 2). The prior that drives naive matching here is the product type ("a hydrating cream suits dry skin"), not the brand.
4. **The deterministic labels are the weak link, not the matchers.** An independent quote judge (Claude Opus 5.5, must copy a verbatim passage) disagrees with the parser/construction label on **20%** of items. The keyword rule looks perfect on constructed items only because it shares the parser's blind spots: on the 162 items where the judge found verbatim support the parser missed ("wavy, curly and coily hair", "Paraben & Dye Free", "Safe for all skin"), the keyword rule recommends **0%** while strict LLMs recommend ~60%; on the 29 parser false positives ("apply on dry hair", "Do not use on dry skin"), the keyword rule recommends **79%**, strict LLMs **17%**.
5. **Learn-then-Test works but the pilot is too small for α ≤ 10%.** With the strict Sonnet support score, LTT certifies a threshold at α = 0.10 in every split (test URR 0.7%, coverage 11.5%, recall of supported 56%) and at α = 0.20 (URR 6.1%, coverage 16%, recall 74%; 1 of 50 splits over α). At α = 0.05 no split certifies: each calibration half has only ~100 recommended items, and showing URR ≤ 5% needs ~280.
6. **G0 on All_Beauty fails the plan's bar, and real needs are rarely checkable.** Only 243 of 6,503 listings (3.7%) state ≥ 2 checkable attributes that agree with `details`. About 6% of early verified reviews state a checkable need (bar: 10%), and when one does, the listing that buyer bought states it only 7 times in 43.

What this means for the plan is in the last section.

### Data and benchmark

| | |
|---|---|
| Listings | 6,503 unique All_Beauty products: the hackathon cohort (5,585, with title, bullets, description, `details`) plus 918 from the committed 1,000-item metadata sample. The full `meta_All_Beauty.jsonl` is not reachable from this environment |
| Matchers see | `Listing.render()`: title, brand, bullets, description. Never `details`, the variant, the label, the ASIN or the attribute name (case ids are opaque hashes; a unit test checks the prompt) |
| Constructed items (L1) | 250 products whose visible text and `details` agree on an in-scope attribute, each with real edits of its own listing: **original** (entailed), **remove** every sentence stating it (unresolved), **vague** wording ("your skin", "gentle", "clean") (unresolved), **contradict** with an opposite value (contradicted), **remove + famous brand + hype bullet** (unresolved). An edit is kept only if the parser confirms its intended label |
| Natural items (L2) | 150 unedited listings whose `details` gives the value but whose text never states it (unresolved) |
| Needs | One constraint per item, from `details`: skin type 83 products, hair type 97, free-from 28, item form 28, fragrance-free 14. Named scents are excluded (in Beauty listings "lavender" is usually an ingredient, not a scent claim) |
| Audited subset | 1,089 of 1,356 items where the quote judge agrees with the construction label (the §11.3 agreement filter) |

Edits are minimal and real, for example `Mitchum … Roll-On, Unscented 3.4 oz` → remove: `Mitchum … Roll-On, 3.4 oz`; vague: `…, gentle 3.4 oz`; contradict: `…, eucalyptus scent 3.4 oz`.

### Matchers

| Name | Model | What it does |
|---|---|---|
| naive | Claude Haiku 5.5, Claude Sonnet 5.5 | "Would you recommend this product to this shopper?" + confidence |
| strict | same | "Recommend only if the listing explicitly states it; reject if contradicted; abstain if missing, vague or implied; ignore brand, popularity, marketing and typical products" + support score |
| extract → rule | Claude Haiku 5.5 | LLM extracts explicitly stated attributes in a controlled vocabulary, a rule compares them with the need |
| keyword rule | none | Literal phrases ("dry skin", "all skin types", "paraben-free"), independent code from the edit generator but the same idea |
| BLaIR, open-weight LLM | — | **Not run yet** (see "Blocked") |

Ten of 1,356 strict-Sonnet replies could not be parsed after retries and are left out of its rates.

### RQ1 results, audited items (n = 1,089 from 381 products)

Recommend rate, product-cluster bootstrap 95% CI. The ideal row is high in *original* and 0% everywhere else.

| Matcher | original | remove | vague | remove + brand/hype | contradict | natural missing | URR |
|---|---|---|---|---|---|---|---|
| naive Haiku | 82% [77, 87] | 30% [24, 36] | 33% [27, 40] | 33% [27, 39] | 3% [0, 6] | 31% [23, 39] | 57% [53, 61] |
| naive Sonnet | 77% [71, 82] | 26% [20, 33] | 27% [21, 34] | 24% [19, 30] | 6% [2, 9] | 27% [20, 35] | 54% [50, 59] |
| strict Haiku | 90% [86, 94] | 1% [0, 3] | 1% [0, 3] | 0% [0, 1] | 0% | 2% [0, 5] | 5% [2, 8] |
| strict Sonnet | 80% [75, 85] | 2% [0, 5] | 3% [1, 5] | 2% [0, 4] | 0% | 2% [0, 5] | 10% [5, 15] |
| extract → rule (Haiku) | 95% [91, 97] | 3% [1, 6] | 4% [1, 7] | 3% [1, 5] | 1% [0, 3] | 11% [6, 17] | 15% [10, 20] |
| keyword rule | 89% [85, 93] | 0% | 0% | 0% | 0% | 0% | 0% * |

\* By construction: the audited labels come from a parser of the same kind, so this row is an upper bound, not evidence that rules solve the task. See the next table.

On all 1,356 items (no audit) the pattern is the same, with every LLM row higher on the edited columns (naive 31–45%, strict 9–12%), because those columns then include ~15% of items where the edit left evidence the parser didn't see. Full tables: `outputs/results.md`.

**Where the parser and the judge disagree** (recommend rate):

| Matcher | parser missed real evidence (n = 162; recommending is right) | parser false positive (n = 29; abstaining is right) |
|---|---|---|
| keyword rule | 0% | 79% |
| strict Haiku / Sonnet | 61% / 57% | 17% / 17% |
| extract → rule | 60% | 45% |
| naive Haiku / Sonnet | 80% / 80% | 34% / 45% |

### RQ2 preview: Learn-then-Test on audited items

Recommend iff score ≥ λ. λ is chosen on a 50% product split (21 label-free score quantiles, exact binomial test of URR ≤ α, Bonferroni at δ = 0.1) and evaluated on the other 50%; 50 splits. Mean [2.5%, 97.5%] across splits.

| Score | α | test URR | coverage (all items) | recall of supported | splits with URR > α | splits with no certified λ |
|---|---|---|---|---|---|---|
| strict Sonnet support | 0.20 | 6.1% [2, 16] | 16% [14, 19] | 74% [70, 84] | 2% | 0% |
| | 0.10 | 0.7% [0, 9] | 11.5% [10, 16] | 56% [49, 74] | 0% | 0% |
| | 0.05 | – | 0% | 0% | – | 100% |
| strict Haiku support | 0.20 | 7.0% [2, 12] | 20% [16, 21] | 89% [77, 95] | 0% | 0% |
| | 0.10 | 0.7% | 2% | 11% | 0% | 80% |
| naive confidence (both) | 0.05–0.20 | – | 0% | 0% | – | 100% |

Naive confidence never certifies, even at α = 0.20: high confidence doesn't separate supported from unsupported listings. Coverage is bounded by the share of supported items (~20%), so 16% coverage at α = 0.20 is most of what is available. To certify α = 0.05 with a URR near 2% the calibration split needs ~280 recommended items, so about 1,400 calibration items at this support rate: roughly 4–5× this pilot.

### Needs mined from real reviews

600 early verified reviews (first 10 per product) of the pilot's listings, Claude Haiku 5.5 extractor, all checks automatic:

| Check | Result |
|---|---|
| Reviews stating ≥ 1 checkable need | 36 / 600 = **6.0%** (the rule proxy over 36,992 early verified reviews gives 5.7%) |
| Quotes verbatim in the review | 43 / 43 |
| Values in the §12.1 vocabulary | 43 / 43 |
| Rule parser finds the same value in the quote | 24 / 43 (the rest are paraphrases such as "my hair is very thin") |
| Second extractor (Claude Sonnet 5.5) on 200 reviews | review-level agreement 98.5%; precision 0.80, recall 0.86 vs Sonnet |
| Listing the buyer chose states that need | **7 / 43**; 36 unresolved, 0 contradicted |

Needs are mostly skin type (20) and hair type (18).

### G0 count (§12.3) on the 6,503 available listings

| Attribute | visible text and `details` agree | `details` only | text only | disagree |
|---|---|---|---|---|
| item form | 1,523 | 830 | 1,006 | 212 |
| scent | 284 | 236 | 585 | 17 |
| hair type | 155 | 784 | 112 | 57 |
| skin type | 136 | 864 | 226 | 34 |
| free-from | 41 | 106 | 533 | 16 |

Products with ≥ 2 agreeing attributes: **243 (3.7%)**; ≥ 1: 1,875. At that rate All_Beauty (112,590 items) would give about 4,200, far under the 20,000 bar. Beauty_and_Personal_Care would need its own count; it isn't reachable from here. Note the large "`details` only" columns: for skin and hair type, six times as many listings carry the attribute in `details` as state it in text. That is the natural missing-evidence case and the strongest source of RQ1 items.

### Threats to validity found in this run

- **A label leak, caught and fixed.** The first Claude runs echoed case ids of the form `ASIN:attribute:value:variant`, so models could read the variant. Those runs were discarded; ids are now opaque and a test checks the prompt. Any future matcher must keep this test.
- **The judge is a Claude model**, and so are the evaluated matchers. Filtering on agreement with it may favour Claude matchers. An open-weight judge or matcher is needed before the paper claims a gap between models.
- **Hair type is ambiguous in All_Beauty.** Many listings are wigs, extensions and curlers, where "straight hair" describes the product, not the shopper. Both the parser and the judge struggle there.
- **Edits are lexical.** Remove/vague/contradict work on the parser's patterns, so ~15–20% of edited items keep evidence in a form the parser doesn't know (these are dropped in the audited set). The contradict edit is the weakest (53% judge agreement).
- **One constraint per need, 250 products, one category, one seed of edits.** Single-constraint needs make "rules solve it" easier than conjunctions would.
- **Contamination is not tested.** No post-cutoff listings yet.

### Blocked, and what is needed

- **Open-weight LLM and BLaIR.** This environment cannot reach Hugging Face or a local Ollama. A session on yui's Mac has been requested to run them (code ready: `run_pilot.py run strict ollama <model>`, `run_pilot.py run dense hyp1231/blair-roberta-base`); it still waits for yui to allow it.
- **Full G0.** Needs `meta_All_Beauty.jsonl` and `meta_Beauty_and_Personal_Care.jsonl` (Amazon Reviews 2023 site, not reachable from here). The same Mac session checks whether the first is already in ~/Downloads.

### What this means for the plan (for `01-brainstorm` and plan §11–§12; not edited here because another thread owns those files)

1. **RQ1 holds for naive prompting and mostly disappears with a strict prompt.** The paper can't rest on "LLMs license priors"; it has to show where strict prompting and extract-then-rule fail. On this data that is (a) evidence stated in paraphrase or lists the rules can't parse, (b) usage text that mentions the attribute without claiming it ("apply on dry hair"), and (c) multi-constraint needs (untested). That is the "hard but decidable" subset the mock review asked for, and the disagreement table above is its first sample.
2. **Labels need the two-extractor agreement filter from day one.** A single parser has ε ≈ 12% on unedited listings and ~20% on edited ones in Beauty. Report the guarantee against agreed labels, with ε from the disagreement rate.
3. **G0 points toward the §12.5 fallback for RQ2.** All_Beauty doesn't have enough agreeing attributes, and only 6% of early reviews carry a checkable need. Unless Beauty_and_Personal_Care counts much higher, keep Beauty for RQ1 and move the guarantee to Home & Kitchen as §12.5 already allows.
4. **Scale for LTT at α = 0.05:** about 1,400 calibration items per split at this support rate.
