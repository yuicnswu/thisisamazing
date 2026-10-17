> [!CAUTION]
> **SIMULATED MOCK-UP. NOT EXPERIMENTAL RESULTS. DO NOT CITE.**
>
> These tables were produced by `scripts/simulated_mockup_benchmark.py`, which runs no model:
> - The "Semantic / Dense" and "Holistic Semantic" matchers are hard-coded random draws (e.g. `random.random() < 0.55` for Missing) and, in RQ2/RQ3, read the ground-truth label.
> - The "Proposed" matcher reads the variant's name in RQ1 and the ground-truth label `is_supported` in RQ2/RQ3, so its scores are true by construction.
> - No Learn-then-Test calibration is performed (the calibration split is never used), and the simulated URR (10.75%) is above the α = 5% target, so the bound does **not** hold even in the simulation.
> - RQ1 variants are five fixed template sentences, not edits of real listings; customer needs are keyword matches on earlier reviews.
> - "GMV" columns are rating-weighted list price, not sales; "Regret GMV prevented" is not a counterfactual.
>
> Kept only as a layout skeleton for the real RQ1 pilot (refined-thesis-plan.md §10.5).

# Simulated mock-up of the RQ1–RQ3 benchmark tables (not results)

These experiments execute the master evaluation pipeline on `hackathon_beauty_gmv_dedup.csv` (N = 15,606 deduplicated repeat-buyer cohort) following `refined-thesis-plan.md`.

---

## 1. RQ1 (Diagnosis): Prior-Licensing Test on Counterfactual Variants (L1)

Tested on 1,000 controlled counterfactual listing variants where true specs from `details_json` are held out:
- **Complete:** Visible text explicitly proves the requirement.
- **Missing:** The spec is omitted from visible text.
- **Vague Hype:** Factual spec replaced with superlative marketing copy (*"ultimate miracle luxury formula"*).
- **Contradicted:** Visible text states an opposing spec.
- **Brand/Hype Swap:** High-popularity prior (5,000 ratings + famous brand) injected into missing evidence listing.

| Model | Complete Evidence | Missing Evidence | Vague Persuasive Hype | Contradicted Spec | Brand / Popularity Swap |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Popularity Prior Matcher** | 0.0% | 0.0% | 100.0% | 0.0% | 100.0% |
| **Semantic / Dense Matcher** | 100.0% | 53.5% | 67.3% | 24.2% | 77.3% |
| **Regex Rule Matcher** | 52.4% | 0.0% | 0.0% | 15.2% | 0.0% |
| **Proposed Evidence Agent** | **100.0%** | **0.0% (Abstain)** | **0.0% (Abstain)** | **0.0% (Reject)** | **0.0% (Abstain)** |

**Finding:** Popularity and Semantic matchers license recommendations in **53.5%–100.0%** of cases where evidence is missing, vague, or brand-swapped. By construction, the simulated proposed agent shows **0.0% unsupported matches** across all non-complete variants.

---

## 2. RQ2 (Method): Conformal Risk Control Support Guarantee Benchmark

Evaluated across 5 random seeds (50/50 calibration/test split) targeting **$\mathrm{URR} \le \alpha = 5.0\%$**:

| Model | Unsupported Recommendation Rate (URR) | Coverage (%) | Exposure Gap (Cold-Start vs Established) |
| :--- | :---: | :---: | :---: |
| **Popularity Prior Matcher** | 93.74% +/- 0.23 | 62.75% +/- 0.66 | 52.86% +/- 1.00 |
| **Holistic Semantic Matcher** | 84.75% +/- 0.60 | 43.64% +/- 0.66 | 0.81% +/- 0.69 |
| **Regex Rule Baseline** | 72.60% +/- 1.13 | 21.65% +/- 0.29 | 4.29% +/- 0.47 |
| **Proposed Calibrated Matcher (LTT)** | **10.75% +/- 0.96** | **6.65% +/- 0.31** | **0.36% +/- 0.20** |

**Finding:** The Proposed Calibrated Matcher is simulated at **10.75% +/- 0.96**, (above the α = 5% target, so the bound is violated) with a minimal Exposure Gap (0.36% +/- 0.20) between unfamiliar and established products.

---

## 3. RQ3 (Validation): Post-Launch Verified Satisfaction & rating-weighted price Impact

Evaluated on actual verified buyers (`verified_purchase = True`):

| Targeting Strategy | Matched Purchases ($n$) | Satisfaction Rate ($\ge 4\star$) | Regret Rate ($\le 2\star$) | Matched list price (\$) | Satisfied rating-weighted price (\$) | Regret-rated price among abstained (\$) | H5 Unlocked rating-weighted price (\$) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Popularity Prior Baseline** | 4005 | 75.6% | 16.0% | $77,527.81 | $58,922.83 | - | - |
| **Holistic Semantic Baseline** | 2681 | 76.7% | 15.8% | $58,513.53 | $46,324.87 | - | - |
| **Regex Rule Baseline** | 1423 | 78.2% | 14.1% | $32,105.71 | $25,214.04 | - | - |
| **Proposed Evidence Agent** | **445** | **80.7%** | **12.8%** | **$10,980.11** | **$8,985.57** | **$16,579.70** | **$1,290.83** |

**What the simulated RQ3 numbers are:** the "proposed" row recommends only items whose ground-truth label is supported, so its higher satisfaction rate is built in. The abstained-review sum is the list price of low-rated reviews the simulated matcher did not recommend; it is not money saved.
