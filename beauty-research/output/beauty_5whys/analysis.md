# 5 Whys: reliability of marketing decisions from the Beauty catalog

## Problem statement

**What:** Metadata-based selection can exclude most products; average-star rankings can prioritize products with little rating evidence; inferred product categories can contain false matches.
**When:** During preparation of a product shortlist from this historical metadata file.
**Where:** `~/Downloads/meta_All_Beauty.jsonl` and the title-derived categories in the initial EDA.
**Impact:** Diagnostic completeness requirements retain only 4,332 of 112,590 products (3.85%). No financial loss or conversion impact is measured.

This analysis distinguishes observations, verified implementation behavior, and unverified upstream explanations. A causal chain stops when evidence runs out; five answers are not manufactured.

## A. Why does a complete-record shortlist exclude so much of the catalog?

| Level | Question | Answer | Evidence / status |
|---|---|---|---|
| 1 | Why does requiring price, description and features leave only 3.85%? | Only 4,332 records satisfy all three requirements. | Full-file filter audit, verified. |
| 2 | Why do the other records fail? | Most fail one or more metadata requirements; 80,031 records lack all three fields. | Raw JSONL audit, verified. |
| 3 | Why are those source fields absent? | Unknown. Possible explanations include original-page absence, historical unavailability, extraction failure or preprocessing omission. | Hypotheses, not identified causes. No alternative nonempty price-named detail field was found among records missing top-level price. |

**Identified operational cause:** Using completeness as an eligibility rule excludes 96.15% of this catalog. This is a deterministic property of that rule, not proof of upstream scraping failure or commercial harm.
**Type:** Selection-rule design. **Confidence:** High for exclusion; unknown for upstream missingness.

**Selection diagnostic:** All products have median rating count 9; priced products have median 15; products with all three fields have median 20. Composition changes accompany completeness filtering. Differences do not establish that missingness causes lower ratings or that excluded items deserve promotion.

**Validation:** Removing a diagnostic requirement must recover products failing that requirement alone. It does not make their missing information available. Recovering source metadata would increase eligibility, but no claim is made that this improves sales.

**Next evidence:** Audit a stratified sample against archived pages from the collection period, extraction code and parsing logs. Current pages can assess present enrichment opportunities but cannot establish the historical cause of missingness.

## B. Why can a high-star shortlist have weak supporting evidence?

| Level | Question | Answer | Evidence / status |
|---|---|---|---|
| 1 | Why can a product with little evidence qualify? | A rule based only on average stars does not require rating volume. | Verified rule definition. |
| 2 | Why is this material here? | Of 14,519 five-star products, 12,189 have fewer than five ratings and 5,931 have one rating. | Raw JSONL audit, verified. |
| 3 | Why do those products have few ratings? | Unknown. Listing age, exposure, demand and incomplete source histories are possible explanations. | The file cannot distinguish these explanations. |

**Identified operational cause:** Average-only ranking ignores evidence volume. **Type:** Measurement/selection design. **Confidence:** High. This is not evidence of fake reviews or a measured product-quality difference.

**Sensitivity diagnostic:** Rating >=4.5 selects 31,004 products (median rating count 5). Adding rating count >=20 retains 7,472 (median count 64). The value 20 is a diagnostic threshold, not a validated universal requirement. Such thresholds may exclude new products; compare several thresholds and keep an exploration route.

**Validation:** Requiring at least 20 ratings necessarily prevents products with fewer than 20 from entering that shortlist. It does not guarantee genuine feedback, superior quality, or future satisfaction. Rating-level observations and exposure/age information would be needed for stronger inference.

## C. Why can inferred beauty segments include unrelated products?

| Level | Question | Answer | Evidence / status |
|---|---|---|---|
| 1 | Why does the initial EDA classify leather conditioner as Hair care? | Its Hair care regex matches the word 'conditioner' regardless of what is being conditioned. | `scripts/beauty_eda.py`, verified code inspection; product B01CUPMQZE in the drift export. |
| 2 | Why can that lexical match become a category assignment? | The first matching keyword rule supplies the primary heuristic segment, without resolving word meaning or target material. | Verified code path. |
| 3 | Why can we not validate it against category paths in this file? | Every categories list is empty. The broad main_category field supplies no detailed beauty taxonomy. | Full-file schema audit, verified. This is a separate validation constraint, not the cause of the regex match. |
| 4 | Why are category paths empty upstream? | Unknown from the metadata file. | Requires source schema, page evidence and extraction history. Stop here. |

**Identified operational cause:** A context-free keyword rule produces a false category assignment. **Type:** Classification design. **Confidence:** High for this example; aggregate classification error rate is unknown.

**Validation:** A contextual exclusion for leather conditioner should prevent this example from entering Hair care. It would not establish accuracy for every other category. Verify a held-out, manually labeled sample and report per-category precision/recall before relying on inferred segments.

**Dataset issue remains separate:** Mobility equipment and a livestock brush appear under broad beauty labels. Their inclusion is observed; its upstream cause is unverified. Do not automatically remove products based on a narrow keyword audit.

## D. Why cannot this file establish marketing ROI?

1. ROI needs attributable costs and returns; the metadata file contains neither campaign spend nor transactions.
2. The record represents a product, with aggregate feedback and descriptive attributes, rather than an exposure, click or purchase event.
3. The reason the upstream collector did not include those other datasets is outside this file's evidence. Do not invent an organizational cause.

**Identified constraint:** A mismatch between the proposed business outcome and the observed unit of data. **Type:** Data scope. **Confidence:** High. Rating count is not revenue, conversion or incrementality.

**Validation:** Joining compatible event and transaction data supplies missing measures but does not automatically identify causal campaign lift. That needs a suitable attribution or experimental design.

## Countermeasures (proposed, not assigned commitments)

| Type | Action | Proposed owner | Timing |
|---|---|---|---|
| Immediate | Label complete-case subsets and inferred categories; keep missing-price products in an enrichment queue rather than imputing zero. | Analyst | Before the next shortlist |
| Immediate | Compare star-only selection with several minimum-count rules; explicitly retain low-evidence products as a separate exploration set. | Analyst / merchandiser | Before product ranking |
| Preventive | Replace ambiguous category rules with contextual rules or a validated classifier, and create a held-out manual labeling set. | Data engineer / domain reviewer | Initial 1-2 week pilot |
| Preventive | Audit historical source pages and extraction logs for a stratified sample of missing fields. | Dataset maintainer | When provenance is accessible |
| Detection | Track field availability by verified product type, shortlist composition changes, low-count high-star selections and classification error. | Analyst / QA | Each catalog refresh |
| Measurement | Join current stock, currency, package units, transactions, exposure, spend and margin where the use case requires them. | Marketing analytics / commerce owner | Before ROI claims |

## Best next action

Use the existing filter audit to choose a diagnostic shortlist policy, then manually label a stratified set of products (including leather conditioners, beauty products and equipment) before interpreting differences by category. Investigate upstream missingness only with provenance evidence. No root cause for absent prices, low customer demand, review fraud or poor marketing performance has been established.

## Reproducibility

`evidence.json` contains the new full-file counts and filter comparisons. Original EDA tables remain in `../beauty_eda/`. This analysis changes neither source metadata nor the initial heuristic classifier.
