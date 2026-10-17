# Evidence-Based Launch Matching & GMV Benchmark (`All_Beauty` + `meta_All_Beauty`)

> **Core Question:** *How can a new product find the customers it genuinely serves, before it has reviews, popularity, or an established brand?*

- **RQ1 (Diagnosis):** Do AI recommenders match new products on the evidence in the listing, or on priors such as brand, popularity, and persuasive wording?
- **RQ2 (Method):** Can an agent match on evidence alone, abstain when evidence is missing, and guarantee a bounded rate of unsupported matches?
- **RQ3 (Outcome):** Do evidence-based matches made at launch predict which customers were satisfied after launch (and maximize Satisfied GMV while preventing Regret GMV)?

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
├── scripts/
│   ├── build_hackathon_data.py            # Joins All_Beauty.jsonl + meta_All_Beauty.jsonl & computes GMV
│   ├── run_eda.py                         # Primary EDA & quantile/segment table generator
│   ├── run_eda_deep.py                    # Deduplication, Vine bias & verified-purchase deep dive
│   ├── generate_html_report.py            # Builds eda_outputs/eda_report.html
│   └── five_whys_evidence.py              # Extracts failure-mode evidence for 5-Whys RCA
└── .agents/skills/5-whys/                 # Bundled 5-Whys Root Cause Analysis skill
```
