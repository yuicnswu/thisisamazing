# Provisional research questions

Scores (1–5) are planning judgments. Originality is unscored pending a literature audit. No LLM evaluation or causal experiment has been run.

- **Q1 (24/25; pilot):** Can an LLM distinguish explicit preference mismatch from product defects and delivery complaints? Evidence: E7, E8; chain: W3. Assumption: Review text contains enough explicit evidence for humans to distinguish these explanations.

- **Q6 (22/25; secondary pilot):** Does evaluation only on complete listings overstate LLM interpretation performance? Evidence: E1, E2; chain: W1. Assumption: Human labels can be sampled across completeness strata.

- **Q3 (21/25; secondary pilot):** Do LLM conclusions remain stable when irrelevant brand and rating cues are masked? Evidence: E9; chain: W3. Assumption: Human validators can confirm that edits preserve relevant product information.

- **Q2 (20/25; park pending shopper labels):** Does explicit usage context improve customer–product fit judgments beyond product ratings? Evidence: E5, E7; chain: W2. Assumption: Independent shoppers can supply needs and compare plausible products.

- **Q4 (17/25; park pending variant mapping):** Does variant-aware review retrieval improve aspect interpretation? Evidence: E8; chain: W3. Assumption: Variant identity and corresponding listing attributes can be verified independently.

- **Q5 (15/25; park pending history audit):** Do earlier reviewer histories improve fit judgments over explicit current needs? Evidence: E5, E6; chain: W2. Assumption: Enough time-valid multi-product histories and independent fit labels exist.

## Q1: Distinguishing preference mismatch from product failure

**Research Question:**

Can an LLM distinguish explicit preference mismatch from product defects and delivery complaints?

**Stake:**

A merchant needs different actions for unsuitable targeting, a defective product and delivery problems.

**Hidden Assumption:**

Review text contains enough explicit evidence for humans to distinguish these explanations.

**Competing Hypotheses:**

- H1: Explicit context and aspect spans improve preference-mismatch classification.
- H2: Sentiment and complaint keywords explain apparent gains without context reasoning.
- H3: Humans cannot reliably separate these causes from available text.

**Discriminating Test:**

Compare majority/keyword baselines, text-only LLM and context/aspect-guided LLM under an equal model budget. Use two independent annotators plus adjudication; allow unclear and multiple labels. Split by parent product and remove exact duplicates; exclude listing aggregate ratings and reviewer identifiers. Report macro-F1, per-class recall, span F1, uncertainty coverage, product-cluster bootstrap intervals, cost and latency.

**Falsifier:**

No reliable human agreement, or no held-out improvement over the strongest baseline after controlling for sentiment and review length. Treat inconclusive intervals as inconclusive.

**Two Week Pilot:**

Days 1–3: refine schema on 50 reviews. Days 4–7: independently label 300 additional reviews across rating and completeness strata, including mixed-rating products and controls. Days 8–10: freeze schema and product-disjoint split; lock prompts on development data. Days 11–14: evaluate baselines and context ablation on untouched test products. Use pilot variance to plan a powered follow-up.

**Minimum Resources:**

Two annotators, one adjudicator, local review text, annotation budget; model access and cost approval before running LLM experiments.

**Strongest Reviewer Objection:**

This may be ordinary complaint classification; no independently verified customer fit or demonstrated novelty.

**Next Action:**

Review the 200-row annotation seed, extend it beyond rating-balanced sampling, and label the first 50 with uncertainty.

**Status:**

Provisional design; no experiment has been run.

## Q6: Selection effects from listing completeness

**Research Question:**

Does evaluation only on complete listings overstate LLM interpretation performance?

**Stake:**

A shopping assistant evaluated only on complete listings may leave most of a merchant catalog untested.

**Hidden Assumption:**

Human labels can be sampled across completeness strata.

**Competing Hypotheses:**

- H1: Restricting to complete listings changes measured LLM performance.
- H2: Differences reflect review length, product type or review volume rather than completeness.
- H3: Performance is stable across completeness strata.

**Discriminating Test:**

Sample independently labeled reviews in complete and incomplete product strata. Keep test products disjoint from development. Compare the same frozen model; report within-stratum macro-F1 and catalog-weighted estimates. Match or stratify on observable review length and volume; validate product types manually. Report residual confounding and do not interpret a stratum difference as a causal effect of missingness.

**Falsifier:**

No meaningful stratum difference, or the difference disappears under observable controls; either result limits the selection-bias claim.

**Two Week Pilot:**

Week 1: cross-tab eligibility and design a 300-review stratified annotation sample. Week 2: adjudicate, freeze prompts, evaluate a single fixed model and reweight to known catalog proportions. Report uncertainty and strata with insufficient labels.

**Minimum Resources:**

Same annotators and frozen model as Q1; extra labels may be necessary for sparse strata.

**Strongest Reviewer Objection:**

Observed groups are confounded, listing timestamps are unknown, and the pilot may be underpowered.

**Next Action:**

Audit the eligibility table and preregister the strata and estimand before looking at model scores.

**Status:**

Provisional design; no experiment has been run.

## Claims to verify before a paper claim

- Audit current literature for equivalent complaint/context benchmarks and methods.
- Establish annotation agreement and construct validity independently of model outputs.
- Obtain prospective shopper needs and judgments before claiming customer–product fit.
- Obtain merchant action/outcome data or run an experiment before claiming conversion, margin or retention gains.
