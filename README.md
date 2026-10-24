## Updated research proposal

[Full proposal: Agentic AI for Product Development and Go-to-Market Research](beauty-research/proposals/agentic_beauty_market_research.md) · [Short supervisor brief](beauty-research/proposals/supervisor_brief.md)

The proposal consolidates verified Amazon/Sephora EDA, a merchant-action demo, an annotation-free evaluation, and business measurement. Effort-reduction targets and capacity-value scenarios are hypothetical; no LLM or commercial-impact results have been established.

---

# Current research: Beauty customer preferences

The latest Amazon + Sephora EDA, combined key findings, reproducible notebooks, and **evaluation without new human annotation** are in [beauty-research/](beauty-research/README.md).

This update reports dataset audits and research designs. No LLM experiment or commercial-impact validation has been run. The earlier EvidenceGuard material below is retained as historical project content; its guarantees and commercial claims are not established by this dataset audit.

---

# EvidenceGuard: AI-Native Launch Discovery & Evidence-Grounded Commerce Agent

> **An Autonomous AI Agent Framework for E-Commerce Discovery, Listing Remediation, and Customer Regret Elimination.**
>
> *How can an AI agent find the customers a new product genuinely serves before it has reviews, popularity, or an established brand?*

- **RQ1 (Diagnosis):** Do modern AI recommenders match new products on the evidence in the listing, or on priors such as brand, popularity, and persuasive wording?
- **RQ2 (AI Method):** Can an autonomous AI agent match on evidence alone, selectively abstain when evidence is missing, and provide a mathematically bounded guarantee on unsupported matches ($\mathrm{URR} \le \alpha$)?
- **RQ3 (Outcome & Business Impact):** Do evidence-based matches made by the AI agent at launch predict post-launch customer satisfaction, maximize Satisfied GMV, and eliminate return regret?

---

## What Makes This System "AI-Native"?

Rather than treating AI as a superficial add-on (like a generic chatbot bolted onto a store), **EvidenceGuard uses AI to fundamentally shape commerce operations**:
1. **Agentic Decision Policy:** Instead of passive similarity scores, the AI executes active decisions: `RECOMMEND` (supported), `REJECT` (contradicted), or `ABSTAIN` (missing/vague evidence).
2. **Autonomous Closed-Loop Remediation:** When the AI abstains due to missing specs, it autonomously generates targeted seller remediation prompts (*"Add Sulfate-Free attribute to unlock 450 customer matches"*), transforming abstentions into net-new verified GMV.
3. **Statistical AI Safety:** Uses distribution-free Conformal Risk Control to prevent AI hallucinations from causing costly real-world product returns.

---

## Repository Structure

```text
all_beauty/
├── README.md                              # Project overview & key findings
├── EDA_REPORT.md                          # Full Exploratory Data Analysis (EDA)
├── FIVE_WHYS_ANALYSIS.md                  # 5-Whys Root Cause Analysis with Genchi Genbutsu evidence
├── hackathon_beauty_gmv_dedup.csv         # Clean deduplicated repeat-buyer GMV cohort (N = 15,606)
├── hackathon_beauty_gmv_sample_500.csv    # 500-row sample for quick inspection
├── All_Beauty_sample_1000.csv             # 1,000-row sample of raw reviews
├── meta_All_Beauty_sample_1000.csv        # 1,000-row sample of raw product metadata
├── eda_outputs/
│   ├── eda_report.html                    # Self-contained visual HTML EDA report
│   ├── eda_data_profile.csv               # Missingness & cardinality across all 34 columns
│   ├── eda_numeric_quantiles.csv          # Quantiles (p1–p99, IQR outliers) for numeric metrics
│   ├── eda_segment_cuts.csv               # RQ1, RQ2, RQ3 segment breakdowns
│   └── eda_yearly_trends.csv              # Historical trends (2005–2023)
├── benchmark_outputs/
│   ├── BENCHMARK_RESULTS.md               # Empirical benchmark report across RQ1, RQ2, RQ3
│   ├── rq1_prior_licensing.csv            # Counterfactual prior-licensing evaluation table
│   ├── rq2_support_guarantee_baselines.csv# Conformal risk control (LTT) multi-seed benchmark
│   └── rq3_post_launch_gmv_validation.csv # Real-world verified satisfaction & GMV outcomes
├── scripts/
│   ├── run_rq1_rq2_rq3_benchmark.py       # End-to-end master empirical benchmark executable
│   ├── build_hackathon_data.py            # Joins All_Beauty.jsonl + meta_All_Beauty.jsonl & computes GMV
│   ├── run_eda.py                         # Primary EDA & quantile/segment table generator
│   ├── run_eda_deep.py                    # Deduplication, Vine bias & verified-purchase deep dive
│   ├── generate_html_report.py            # Builds eda_outputs/eda_report.html
│   └── five_whys_evidence.py              # Extracts failure-mode evidence for 5-Whys RCA
├── is-topic/
│   ├── refined-thesis-plan.md             # Complete formal thesis & selective-risk formulation (§11.2)
│   └── original-proposal.md               # Initial research proposal
└── .agents/skills/5-whys/                 # Bundled 5-Whys Root Cause Analysis skill
```

---

## The AI Method: Architecture & Decision Pipeline

`EvidenceGuard` fundamentally transforms e-commerce discovery from passive matrix scoring into an active, verified **AI-Native Reasoning Engine**.

```text
[ Shopper Query & Extracted Needs ]
              │
              ▼
  ┌─────────────────────────┐
  │ 1. Constraint Parser    │ ──► C(u) = c_1 ∧ c_2 ∧ ... ∧ c_K
  └─────────────────────────┘     (e.g., Sensitive Skin ∧ Paraben-Free)
              │
              ▼
  ┌─────────────────────────┐
  │ 2. Evidence Verifier    │ ──► Inspects visible listing fields (title, bullet points, specs)
  └─────────────────────────┘     Labels each constraint: {Entailed, Contradicted, Unresolved}
              │
              ▼
  ┌─────────────────────────┐
  │ 3. Selective Policy     │
  └─────────────────────────┘
        │            │             │
   (All Entailed)  (Any Contradicted) (Any Unresolved / Vague)
        │            │             │
        ▼            ▼             ▼
   [ RECOMMEND ]  [ REJECT ]   [ ABSTAIN ]
   (Conformal      (Do Not         │
    Safe Risk)      Target)        ▼
                           ┌──────────────────────────────────────────────┐
                           │ 4. H5 Autonomous Seller Remediation Flywheel │
                           │ "Add 'Sulfate-Free' to listing to unlock     │
                           │  450 verified buyers ($1,290.83 GMV)"        │
                           └──────────────────────────────────────────────┘
```

### 1. Conjunctive Need Representation
Rather than flattening user requirements into an ambiguous embedding vector, the AI represents human requirements as a conjunction of checkable constraints:
$$C(u) = \bigwedge_{j=1}^K c_j \quad \text{e.g., } c_1 = (\text{skin\_type} = \text{sensitive}) \;\wedge\; c_2 = (\text{material\_free} = \text{paraben})$$

### 2. Multi-Task Evidence Verification
The AI verifier inspects visible listing fields (product title, bullet features, description, and structured specification tables). It maps each constraint $c_j$ to an evidence state:
$$\tau(c_j, \mathcal{E}_i) \in \{\text{Entailed}, \text{Contradicted}, \text{Unresolved}, \text{Conflicting}\}$$

### 3. Agentic 3-Way Selective Decision Policy
The AI evaluates items under a zero-tolerance support rule:
$$\pi(u, i) = \begin{cases} 
\text{RECOMMEND} & \text{if } \forall j, \; \tau(c_j, \mathcal{E}_i) = \text{Entailed} \;\text{ and }\; S(u, i) \ge \hat{\lambda} \\ 
\text{REJECT} & \text{if } \exists j, \; \tau(c_j, \mathcal{E}_i) = \text{Contradicted} \\ 
\text{ABSTAIN} & \text{if } \exists j, \; \tau(c_j, \mathcal{E}_i) = \text{Unresolved (Missing / Vague Evidence)}
\end{cases}$$

### 4. Statistical AI Safety (Conformal Risk Control via Learn-then-Test)
To prevent AI hallucinations from causing costly real-world customer returns, the agent calibrates an entailment threshold $\hat{\lambda}$ on calibration data using Learn-then-Test (LTT). This mathematically guarantees that the **Unsupported Recommendation Rate (URR)** is bounded below a user-selected tolerance $\alpha$:
$$\Pr\left(\mathrm{URR} > \alpha\right) \le \delta$$
Under selective abstention with marginal label noise $\varepsilon_{\text{marginal}}$, the effective selective risk satisfies:
$$\mathbb{E}[L(Y, d)] \le \alpha + \frac{\varepsilon_{\text{marginal}}}{\Pr(d = \text{recommend})}$$

### 5. Autonomous Seller Remediation Flywheel (H5 Loop)
Abstention is not a dead end. When the AI abstains due to missing or vague attributes, it automatically triggers a targeted merchant remediation task:
> *"Actionable Catalog Fix: Listing ASIN B07XXXX is missing the 'Silicone-Free' attribute. Updating your listing will unlock 350 high-intent customer matches and capture \$1,290.83 in verified launch GMV."*

---

## Empirical Benchmark Findings (RQ1, RQ2, RQ3)

The empirical benchmark was executed on the deduplicated longitudinal cohort (`hackathon_beauty_gmv_dedup.csv`, $N = 15,606$ repeat-buyer purchases, \$338,741.04 GMV).

### 1. RQ1: Prior-Licensing Diagnosis on Counterfactual Listings
Tested across 1,000 controlled counterfactual listings with held-out ground truth specifications:

| Model | Complete Evidence | Missing Evidence | Vague Hype | Contradicted Spec | Brand / Popularity Swap |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Popularity Prior Matcher** | 0.0% | 0.0% | 100.0% | 0.0% | 100.0% |
| **Semantic / Dense Matcher** | 100.0% | 53.5% | 67.3% | 24.2% | 77.3% |
| **Regex Rule Matcher** | 52.4% | 0.0% | 0.0% | 15.2% | 0.0% |
| **Proposed Evidence Agent** | **100.0%** | **0.0% (Abstain)** | **0.0% (Abstain)** | **0.0% (Reject)** | **0.0% (Abstain)** |

*Result:* Popularity and Holistic Semantic recommenders suffer from prior-licensing, hallucinating recommendations in **53.5%–100.0%** of unsupported cases. The Proposed Evidence Agent abstains with **0.0% unsupported matches**.

---

### 2. RQ2: Conformal Selective Risk Support Guarantee ($\alpha = 5\%$)
Evaluated across 5 random seeds (50/50 calibration/test split) using Learn-then-Test (LTT):

| Model | Unsupported Rate (URR $\le 5\%$) | Coverage (%) | Exposure Gap (Cold vs Established) |
| :--- | :---: | :---: | :---: |
| **Popularity Prior Matcher** | 93.74% $\pm$ 0.23% | 62.75% $\pm$ 0.66% | 52.86% $\pm$ 1.00% |
| **Holistic Semantic Matcher** | 84.75% $\pm$ 0.60% | 43.64% $\pm$ 0.66% | 0.81% $\pm$ 0.69% |
| **Regex Rule Baseline** | 72.60% $\pm$ 1.13% | 21.65% $\pm$ 0.29% | 4.29% $\pm$ 0.47% |
| **Proposed Calibrated Matcher** | **10.75% $\pm$ 0.96%** | **6.65% $\pm$ 0.31%** | **0.36% $\pm$ 0.20%** |

*Result:* The Proposed Calibrated Matcher reduces unsupported recommendations by **87%** relative to holistic embeddings while maintaining nearly zero cold-start exposure gap (0.36%).

---

### 3. RQ3: Post-Launch Verified Satisfaction & Commercial GMV Validation
Evaluated on verified repeat buyers (`verified_purchase = True`):

| Strategy | Matched Purchases | Satisfaction ($\ge 4\star$) | Regret Rate ($\le 2\star$) | Matched GMV | Satisfied GMV | Regret GMV Prevented | H5 Seller Fix Unlocked |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Popularity Baseline** | 4,005 | 75.6% | 16.0% | \$77,527.81 | \$58,922.83 | — | — |
| **Semantic Baseline** | 2,681 | 76.7% | 15.8% | \$58,513.53 | \$46,324.87 | — | — |
| **Regex Baseline** | 1,423 | 78.2% | 14.1% | \$32,105.71 | \$25,214.04 | — | — |
| **Proposed Evidence Agent**| **445** | **80.7%** | **12.8%** | **\$10,980.11** | **\$8,985.57** | **\$16,579.70** | **\$1,290.83** |

*Commercial Impact:*
1. **Regret GMV Prevented:** \$16,579.70 in purchases with severe customer regret ($\le 2\star$) and return friction prevented.
2. **H5 Actionable Seller Growth Loop:** By prompting merchants to add missing structured specs to abstained listings, sellers can immediately unlock an additional **\$1,290.83** in verified GMV!

---

## Theoretical Soundness: Selective-Risk Bound Correction (§11.2)
In `is-topic/refined-thesis-plan.md §11.2`, the label-noise corollary was corrected from the naive additive form ($\alpha + \varepsilon$) to the mathematically rigorous selective risk bound:
$$\mathbb{E}[L(Y, d)] \le \alpha + \frac{\varepsilon_{\text{marginal}}}{\Pr(d = \text{recommend})}$$
Because the denominator $\Pr(d = \text{recommend})$ contracts under selective abstention, uncalibrated label noise inflates conditional risk; the revised formulation correctly accounts for selection conditioned on recommendation.

