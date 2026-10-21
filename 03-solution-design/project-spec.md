# Project Specification

*Stage 3 of [WORKFLOW.md](../WORKFLOW.md). Update whenever a feature is added, removed or changed downstream. Written 2026-10-21 for the repositioning that followed the RQ1 pilot (`05-report/report.md`) and the 2025–2026 field check (`02-literature-review/summary/review.md` §8–9). Theory lives in [`theory.md`](theory.md); modules in [`implement-spec.md`](implement-spec.md).*

## Positioning in one paragraph

AI shopping assistants recommend products on priors and self-reported confidence. For a new product, with no reviews and an incomplete listing, that means recommendations nobody can check. **EvidenceGuard** recommends a product for a shopper's need only when every checkable constraint of the need is backed by a verbatim, typed quote from the listing, rejects when the listing contradicts one, and otherwise abstains and tells the seller exactly which fact to disclose. The paper's claims are, in order: a benchmark that scores abstaining when the listing is silent; the finding that quote-certified grounding can be certified at a chosen risk level while model confidence and strict prompting cannot; and a truthful-disclosure loop that turns abstentions into coverage without raising risk, positioned against generative engine optimisation (GEO). Brand bias and the conformal template are background, cited to Chu and Hou (2026), De Toni et al. (2025) and Mohri and Hashimoto (2024).

## Contributions (re-ranked 2026-10-21)

| # | Contribution | Evidence today | What it still needs | Venue weight |
|---|---|---|---|---|
| **C1** | **Listing-silent benchmark.** Real listings × checkable needs with k = 1–3 constraints; per constraint the evidence is stated, paraphrased, missing, vague, contradicted, or a usage-text distractor; brand-mask and famous-brand overlays; labels from hidden `details` + two independent extractors (+ a gold audit set if yui agrees). Abstention is a scored outcome. | 1,356 + 1,783 items on All_Beauty (one constraint, Claude-only); hard-split cells (k = 2, paraphrase) built and run 2026-10-21 (report) | ≥ 2 categories, ≥ 10× scale, open-weight matchers and judge, dense encoders, dataset card | Core of an Evaluations & Datasets / RecSys resource paper |
| **C2** | **Certifiable vs calibrated grounding.** On the same items and α, Learn-then-Test certifies a quote-certified (NeSy) verifier but not confidence, strict-prompt support scores or keyword rules. Plus a quote-only NLI typed check to recover paraphrased evidence without losing the certificate. | Pilot: NeSy certifies α = 0.10 in 100% of 50 splits (URR ≈ 4%, recall 88–90%); every other score certifies 0% | Open-weight and dense-encoder rows; NLI verifier baseline (Chen et al., 2026); per-k results; informativeness reported next to URR | The main empirical finding |
| **C3** | **Truthful disclosure loop (headline).** Each abstention is attributed to the constraint that caused it, ranked by shopper demand, and sent to the seller as a verification request ("does this apply? if so, state it"). Measured as disclosure yield (certified coverage gained per disclosed fact at fixed URR), entrant exposure gap, and against GEO rewriting (rank gain vs faithfulness) and impute-then-verify. | Inventory: 37% of 6,503 All_Beauty listings have a checkable attribute in `details` but not in visible text (29% without item form) | The yield experiment (oracle-truthful seller = `details`), the adversarial seller (fabricated disclosures), E-GEO baseline, the disclosure theorem's literature check (Grossman, 1981; Milgrom, 1981) | Most novel part per the field check; headline of the IS paper too |
| C4 (stretch) | **Selective conjunctive risk for new items under proxy labels.** Extend semi-supervised risk control (Einbinder et al., 2024) from marginal risks to URR = P(unsupported \| recommend) over conjunctions, with one-sided proxy errors and launch-time shift; plus a non-vacuity (minimum coverage) statement. | `theory.md` Thms 1, 3 (labels-relative); Thm 3's independence assumption is weak (judge and verifier share a model family) | A gold set of ~300–500 human-labelled items (reverses the 17 Oct no-annotator decision; yui's call), proof, independent proof check | Required for the NeurIPS main track |

Demoted to method or background: URR ≤ α calibration itself, brand bias, regret claims, "robust by construction".

## Features

| ID | Feature | Who uses it | Status |
|---|---|---|---|
| F1 | Checkable-need representation: a need is a conjunction of constraints from a controlled vocabulary (§12.1 of the thesis plan for Beauty; dimensions, capacity, voltage, compatibility for Home & Kitchen) | All modules | Beauty done (`attributes.py`); Home & Kitchen vocabulary to write |
| F2 | Per-constraint evidence verifier: LLM proposes verbatim support / contradiction quotes; symbolic certificate checks grounded + typed; optional quote-only NLI for paraphrase | Matcher | Done (`matchers.nesy_verifier`); NLI check to add |
| F3 | Three-way decision with Learn-then-Test calibration of (λ, τ) on one item per product; conjunctive e = min, c = max | Matcher | Done for k = 1 (`conformal.py`); k ≥ 2 path in `hard_split.py` (decisions only, no calibration yet) |
| F4 | Disclosure request generator: gap attribution (which constraint blocked the match), demand ranking (how many mined shopper needs it would unlock), request text phrased as a question the seller must confirm | Seller | To build |
| F5 | Seller simulator: truthful seller discloses the `details` value; adversarial seller fabricates; GEO seller rewrites for rank (E-GEO prompts) | Evaluation | To build |
| F6 | Benchmark builder: edits (remove, vague, contradict, paraphrase, distractor, brand mask / famous brand), conjunctions, label audit | Benchmark | k = 1 done (`edits.py`); k = 2 and paraphrase done (`hard_split.py`); distractors, brand mask, k = 3 to add |
| F7 | Entrant exposure audit: coverage of zero-review vs established products at equal evidence, before and after disclosure | Evaluation | To build |
| F8 | Hackathon demo (pitch) | Demo | Pitch rewritten 2026-10-21; no UI yet |

## Scope
- **In:** needs whose constraints a listing can state and a parser can check; new products (0–9 reviews at decision time); listing text only (`details` hidden, used as truth); English Amazon Reviews 2023.
- **Out:** experiential needs ("won't break me out") are an abstention class, not a target; reviews as evidence at decision time; claims that a stated fact is *true* (the verifier checks that the listing *states* it, so a fabricated claim passes; the adversarial-seller experiment measures this, and disclosure requests are verification tasks, never auto-filled text); causal claims about sales or regret.

## Categories (decision for yui)

The listing-side G0 count needs the metadata files, which neither the cloud container nor the Mac's sandboxed shell can download (both return 403). What can be computed is in `04-implementation/category_check/outputs/category_check.json`:

| | All_Beauty | Appliances (stand-in for hard goods) |
|---|---|---|
| Early verified reviews (first 10 per product) | 343,706 | 396,393 |
| Share mentioning a checkable attribute (rule proxy) | 5.2% | 8.6% (mostly fit / compatibility with a named model) |
| Products with ≥ 10 verified reviews | 11% | 25% |

Independent products Algorithm 1 needs at the pilot's coverage (13%), δ = 0.10, 90% power:

| Target α | true URR 2% | 3% | 4% |
|---|---|---|---|
| 0.10 | 1,000 | 1,500 | 2,231 |
| 0.05 | 4,962 | 12,616 | 56,481 |

Published sizes of the candidates (Amazon Reviews 2023 statistics page, not counted here): Beauty_and_Personal_Care about 1.0M items, Home_and_Kitchen about 3.7M. At All_Beauty's agreement rate (3.7%) Beauty_and_Personal_Care would give about 38,000 products with ≥ 2 agreeing attributes, but that rate need not transfer.

**Recommendation:** count G0 on **both** Beauty_and_Personal_Care and Home_and_Kitchen on the Mac host (not the sandbox), and build the benchmark on both. Two categories is what an Evaluations & Datasets reviewer expects anyway; Beauty keeps continuity with the pilot, BLaIR and the hackathon; Home & Kitchen brings numeric and compatibility constraints, where checkability is higher. Whichever category clears ≥ 20,000 products with ≥ 2 agreeing attributes carries the α = 0.05 results; the other reports α = 0.10. If only one is counted by 31 Oct, start with it and add the second by the 31 Jan benchmark freeze.

## RQ1 redesign: where strict prompting fails

The first pilot measured the easy cell: one constraint, stated in the parser's own words. The redesign makes the hard cells primary and crosses them.

| Factor | Levels | Why |
|---|---|---|
| Constraints per need (k) | 1, 2, 3 (one constraint varied, the others entailed) | Real needs are conjunctions; a prompt that checks "the gist" can miss one missing constraint |
| Evidence form of the varied constraint | stated verbatim · **paraphrased** (LLM rewrite the parser can't see, judge-verified) · missing · vague · contradicted · **usage-text distractor** (mentions the value without claiming it: "apply on dry hair") | Paraphrase tests recall; distractors test precision; both were where the pilot's parser and judge disagreed |
| Brand overlay | original · **brand masked** · famous brand + hype | Reconciles with Chu & Hou (2026): brand in single-listing checks vs choice sets |
| Protocol | single-listing accept / reject / abstain · **choice set** of two identical-spec listings, known vs unknown brand (Chu & Hou replication on the same items) | Same items under both protocols isolates the task difference |
| Item age | new (≤ 9 reviews at decision time) · established | Theorem 4 / H-E |

**Matchers per cell:** naive and strict prompts (frontier + open-weight), strict per constraint, extract-then-rule, keyword rule, BM25, BLaIR, Qwen3-Embedding (thresholded similarity), confidence abstention as in Ravikumar (2026), NLI verifier, NeSy verifier, NeSy + quote-only NLI.

**Size:** ≥ 400 products per (k × evidence form) cell per category, one item per product for calibration, so recommend rates carry about ±5 pp CIs.

**Pre-registered reading (fixed before the full run):**
- RQ1 claims "strict prompting fails" only if, in at least one hard cell (k ≥ 2 with a missing / vague constraint, or distractor), strict-prompt URR exceeds 0.10 with the bootstrap CI above it, or its paraphrase recall is below 50%.
- If neither happens, RQ1 is reported as "strict prompting suffices on checkable needs", and C1 + C2 carry the paper (the benchmark and the certifiability result do not depend on prompting failing).

**First evidence:** the k = 2 and paraphrase cells were built on All_Beauty and run with Claude Haiku / Sonnet on 2026-10-21 (`05-report/report.md`). They are small (one category, Claude-only) and decide nothing alone.

## Merchant-fix loop: evaluation design (C3)

1. **Gap attribution.** For each abstention, the constraint(s) whose e fell below λ. Measured: attribution accuracy against the edit that created the gap (known by construction).
2. **Demand ranking.** For each listing and missing attribute, the number of mined shopper needs (from early reviews of the same subcategory) the fix would turn from abstain into recommend. Output: ranked requests per seller.
3. **Truthful seller (oracle).** Discloses the `details` value in one plain sentence. Measured: **disclosure yield** = certified coverage gained per disclosed fact at the same calibrated (λ, τ); URR after disclosure; the entrant exposure gap before vs after.
4. **Adversarial seller.** Discloses a value that `details` contradicts. Measured: URR against `details` truth. Expected to rise, since the verifier checks statement, not truth; reported as the method's honest limit.
5. **GEO seller.** E-GEO-style rewrite of the same listing (Bagga et al., 2025). Measured: rank change under an LLM reranker and the share of rewrites that introduce claims not supported by `details` (faithfulness), next to EvidenceGuard's yield.
6. **Impute-then-verify baseline.** An LLM guesses the missing value (CatalogRAG-style); measured against `details`.
7. **Theory.** The disclosure result (abstain-unless-supported makes disclosure the truthful seller's best response; with a foolable verifier only above a fit-share threshold) after a search of the voluntary-disclosure and unravelling literature, so the unconditional half is credited to Grossman (1981) and Milgrom (1981).

## Evaluation criteria

| Metric | Definition | Reported for |
|---|---|---|
| URR | P(not supported \| recommend), conjunctive | Every matcher, cell, α |
| URJ | P(not contradicted \| reject) | Three-way matchers |
| Coverage / recall of supported | P(recommend); P(recommend \| supported) | Always next to URR (vacuity check, Chen et al., 2026) |
| Certifiability | Share of calibration splits where LTT certifies a threshold at α; test URR > α rate | C2 |
| Abstention correctness | P(abstain \| unresolved) and P(not abstain \| entailed) | C1 |
| Paraphrase recall / distractor precision | Recommend rate on paraphrased-entailed; recommend rate on distractor-unresolved | RQ1 hard cells |
| Brand effect | Δ recommend rate, famous brand vs masked, per protocol | H-C |
| Disclosure yield | Certified coverage gained per disclosed fact | C3 |
| Entrant exposure gap | Coverage of new vs established products among supported items | H-E, Theorem 4 |
| GEO faithfulness | Share of rewrites adding claims not supported by `details` | C3 baseline |
| Cost | Calls, tokens, GPU-hours, latency | All |

Statistics: product-cluster bootstrap 95% CIs; ≥ 5 seeds for anything trained; paired tests with multiple-comparison correction.

## Venue bar

| Target | What it needs beyond today |
|---|---|
| **NeurIPS 2027 Evaluations & Datasets** (primary) | C1 on 2 categories at ≥ 10× pilot scale; open-weight and dense baselines; dataset card, licence, croissant metadata; C2 and C3 results; label audit with ε reported |
| **RecSys 2027 / SIGIR 2027** (alternative; check the calls for dates) | Same core; RecSys rewards C3 and the entrant-exposure audit more, SIGIR the benchmark and retrieval baselines |
| **NeurIPS 2027 main track** (stretch) | All of the above plus C4 proved and independently checked, a gold set of ~300–500 items, a non-vacuity result, and NeSy beating NLI and conformal-filtering baselines on the risk–coverage frontier |
| **IS paper** (Paper B / C3) | Disclosure and entrant exposure as design science, or with a preregistered experiment; the 22.4% vs 14.9% association only as motivation |

## Blocked on the Mac (owned by the "Real RQ1 pilot" thread)

What those runs must now measure, in priority order:
1. **Open-weight judge.** Re-label the pilot and calibration pools with an open-weight quote judge (not Claude) and rebuild consensus labels; re-run Algorithm 1. Closes the shared-model-family objection to Theorem 3.
2. **Open-weight matchers.** One 7–9B model as naive, strict and NeSy proposer on `items.jsonl`, `calpool.jsonl` and `outputs/hard/items.jsonl`. Report certifiability (C2) and the hard cells (H-B).
3. **Dense encoders.** BLaIR-base / large, Qwen3-Embedding (largest that fits), BM25: similarity on original vs remove / vague / contradict / paraphrase of the same need; AUROC supported vs not; LTT certifiability of a similarity threshold at α = 0.10 / 0.20.
4. **Quote-only NLI typed check.** A small NLI model judging (quote, constraint) on the NeSy quotes; recall on the 162 parser-missed items and the paraphrase cell; re-certify.
5. **G0 on Beauty_and_Personal_Care and Home_and_Kitchen** with `g0_count.py` (`META_JSONL=...`), from the Mac host's own shell.
