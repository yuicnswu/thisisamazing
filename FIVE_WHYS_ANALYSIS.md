# 5-Whys Root Cause Analysis: Cold-Start Mismatch & Post-Purchase regret-rated price

> **Terminology.** "GMV" in the hackathon cohort is a **rating-weighted list price**, not observed sales: `order_gmv` is the current list price (one unit per review), and `satisfied_gmv` / `regret_gmv` are that price when the rating is ≥ 4 or ≤ 2 stars. This report uses "rating-weighted price" in prose; column names are unchanged.

## Phase 1: Problem Statement

- **What:** **16.4% (`2,106 / 12,935`)** of verified repeat-customer purchases (and **16.5% / `$640,220.28`** of all priced verified purchases in `All_Beauty.jsonl`) end in severe post-purchase regret (`rating <= 2.0`), while genuinely well-suited cold-start products (`<10` reviews, High Evidence) capture only **8.8%** of cohort volume.
- **When:** Most severe when customers have multi-attribute constraints and buy listings with **Partial Evidence Support** (**22.4% regret rate / 20.8% regret-rated price**) or **High Persuasive Hype + Low/Missing Evidence** (**19.8% regret rate / 19.0% regret-rated price**).
- **Where:** Product-to-customer matching across `All_Beauty.jsonl` x `meta_All_Beauty.jsonl` (`N = 15,606` deduplicated repeat-buyer purchases; `n = 12,935` verified purchases).
- **Impact:** **`$41,699.45` in verified regret-rated price** inside the repeat-buyer cohort alone (`$640,220.28` across all priced verified purchases), plus widespread promotional review distortion (**25.6%–29.8% unverified/Vine reviews** during the `1–9` review cold-start window).

---

## Phase 2: The 5-Whys Chain (with Firsthand Data Evidence)

| Level | Question | Answer | Firsthand Dataset Evidence (`scripts/five_whys_evidence.py`) |
| :--- | :--- | :--- | :--- |
| **Why 1** | **Why do 16.4% (`2,106`) of verified repeat buyers rate their purchase 1–2 stars?** | Customers receive products that violate a specific physical, chemical, or functional constraint they care about (expectation mismatch, adverse scent/ingredient reaction, or wrong form/texture). | Across the `2,106` verified `<= 2*` reviews:<br>• **20.4% (`429`, `$9,182` list price):** Explicit expectation/listing mismatch<br>• **17.0% (`357`, `$8,375` list price):** Scent, chemical, or skin/scalp irritation<br>• **12.0% (`252`, `$4,873` list price):** Form/texture mismatch |
| **Why 2** | **Why did customers (and baseline AI recommenders) select products that violated their constraints?** | Because matching was driven by **partial headline overlap** (matching 1 need while ignoring a 2nd constraint) or **persuasive hype wording** + **popularity priors**, rather than verifying all customer requirements. | • **Partial-Match Trap:** When a listing supports *some* stated customer needs but omits others, verified regret spikes to **22.4% (`20.8%` regret-rated price)** vs. **14.9% (`12.6%` regret-rated price)** when *all* needs are supported.<br>• **Hype Trap:** Listings with `>= 2` persuasive hype tokens + low evidence reach **19.8% regret (`19.0%` regret-rated price)**. |
| **Why 3** | **Why do recommenders rely on partial matches, hype words, and priors instead of checking all customer constraints?** | Because **structured product evidence is missing in 42%–98% of listings**, whereas **priors and titles are 96%–100% populated**. | In `N = 15,606` cohort rows:<br>• **Priors Present:** `meta_rating_number` (**100%**), `meta_average_rating` (**100%**), `price_usd` (**100%**), `store_brand` (**96.3%**).<br>• **Evidence Missing:** `features_text` (**42.4% missing**), `item_form` (**52.2% missing**), `hair_type` (**82.6% missing**), `scent` (**83.5% missing**), `skin_type` (**84.2% missing**), `material_type_free` (**95.9% missing**), `active_ingredients` (**97.6% missing**). |
| **Why 4** | **Why do sellers leave verifiable evidence sparse and instead invest in hype copy and unverified launch reviews?** | Because marketplace discovery heavily rewards **cumulative popularity priors (`meta_rating_number`)** and broad keyword recall, while penalizing narrow specification constraints—forcing new products to "fake" popularity at launch. | • **60.2% (`$163,032`)** of all verified list price goes to already-popular items (`>= 100` ratings).<br>• To overcome the cold-start penalty, **25.6%–29.8%** of reviews in the early/cold-start window (`1–9` prior reviews) are **unverified/Vine seeded reviews (`verified_purchase = False`)** with **82.5%–84.2%** positive ratings (vs. only **5.2%** unverified in established `50+` review items). |
| **Why 5** | **Why does the underlying matching paradigm reward popularity priors and broad claims instead of verifiable evidence?** | **Root Cause:** Standard AI recommenders treat matching as **unconstrained, holistic similarity scoring (`Score(u, i)`) without atomic requirement verification or an `ABSTAIN` option**. They treat *missing evidence* as neutral/compatible rather than as an unverified risk. | Because holistic scorers always output a ranked list without abstaining on missing evidence, a cold-start product with complete, honest evidence (`13.2%` regret) has no structural advantage over a vague, hyped listing (`19.8%` regret). |

---

## Phase 3: Countermeasures Mapped to RQ1–RQ3

| Type | Action | Target Component | Verification Metric |
| :--- | :--- | :--- | :--- |
| **Immediate (Data Hygiene)** | Lock evaluation to deduplicated `(user_id, parent_asin)` rows (`hackathon_beauty_gmv_dedup.csv`) and `verified_purchase == True` (`n = 12,935`, `n = 5,233` cold-start). | Dataset Pipeline | `0` duplicate `(user_id, parent_asin)` pairs; `0%` unverified review contamination in `RQ3`. |
| **Preventive (`RQ1` De-biasing)** | Construct **Evidence-Only Listings** that mask `store_brand`, `meta_rating_number`, `meta_average_rating`, and persuasive superlatives. | `RQ1` Diagnostic Benchmark | Measure `Delta_prior` vs. `Delta_evidence` across `2 x 2` counterfactual swaps. |
| **Preventive (`RQ2` Agent Design)** | Enforce **Conjunctive Atomic Entailment + Conformal Risk Control (CRC)**: decompose customer history into atomic requirements and **ABSTAIN** whenever minimum entailment falls below calibrated threshold. | `RQ2` Evidence-Only Agent | Finite-sample unsupported match rate `<= alpha` on held-out test split. |
| **Detection (`RQ3` Outcome Guardrail)** | Track **Regret-rated price share (`regret_gmv / order_gmv`)** and **Partial-Match Leakage Rate** across launch stages (`0`, `1–4`, `5–9` prior reviews). | `RQ3` Launch Evaluation | Reduction in regret-rated price % and increase in Satisfied rating-weighted price per matched dollar vs. prior-based baselines. |
