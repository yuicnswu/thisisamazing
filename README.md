# Before the First Review: evidence-grounded matching of new beauty products

> **Core question:** *How can a new product find the customers it genuinely serves, before it has reviews, popularity, or an established brand?*

- **RQ1 (Diagnosis):** Do AI recommenders match new products on the evidence in the listing, or on priors such as brand, popularity, and persuasive wording?
- **RQ2 (Method):** Can an agent match on evidence alone, abstain when evidence is missing, and guarantee a bounded rate of unsupported matches (URR ≤ α)?
- **RQ3 (Outcome):** Do evidence-based matches made at launch predict which customers were satisfied after launch?

The plan of record is [`is-topic/refined-thesis-plan.md`](is-topic/refined-thesis-plan.md) (Beauty as main category, §12; no human annotators, §11).

## Status (17 Oct 2026)

| Part | Status |
|---|---|
| Data cohort and EDA (`hackathon_beauty_gmv_dedup.csv`, `EDA_REPORT.md`, `eda_outputs/`) | Real. Data-quality checks (dedup, unverified-review skew at launch, evidence missingness) are reproducible from `scripts/`. |
| RQ1–RQ3 benchmark | **Not run yet.** The only benchmark in the repo is a simulated mock-up (below). The real pilot is the November go/no-go (plan §10.5). |
| Theory (URR guarantee, §11.2 selective-risk corollary) | Statements in the plan; proofs not written yet. |

### About `benchmark_outputs/simulated_mockup/`

The tables in [`benchmark_outputs/simulated_mockup/`](benchmark_outputs/simulated_mockup/) come from [`scripts/simulated_mockup_benchmark.py`](scripts/simulated_mockup_benchmark.py). **They are not experimental results and must not be cited.** No model is run: baseline decisions are hard-coded coin flips, and the "proposed" matcher reads the variant name or the ground-truth label. They are kept only as a skeleton for the table layouts of the real pilot. See the banner at the top of each file.

## A note on "GMV"

In the hackathon cohort, `order_gmv` is the item's current list price (one unit per review), and `satisfied_gmv` / `regret_gmv` are that price when the review is ≥ 4 or ≤ 2 stars. That is a **rating-weighted list price**, not observed sales: a review isn't a purchase, and list price isn't the price paid. Research outputs call it *rating-weighted price*; the column names are unchanged for compatibility.

## Repository structure

```text
.
├── README.md
├── EDA_REPORT.md                      # Exploratory data analysis of the beauty cohort
├── FIVE_WHYS_ANALYSIS.md              # 5-Whys root-cause analysis
├── hackathon_beauty_gmv_dedup.csv     # Deduplicated cohort (N = 15,606; one row per user × parent_asin)
├── hackathon_beauty_gmv_sample_500.csv
├── All_Beauty_sample_1000.csv         # 1,000-row sample of raw reviews
├── meta_All_Beauty_sample_1000.csv    # 1,000-row sample of raw product metadata
├── eda_outputs/                       # EDA tables and HTML report
├── benchmark_outputs/
│   └── simulated_mockup/              # NOT RESULTS: placeholder tables, see above
├── scripts/                           # Data build, EDA, 5-Whys evidence, simulated mock-up
├── is-topic/                          # Thesis plan, proposal, literature review, mock reviews
└── .agents/                           # Team role briefs and the NeurIPS standard
```

## Reproducing

Every script takes its paths as command-line arguments (run with `--help`). Defaults are relative to the repository root, and the raw Amazon Reviews 2023 files (`All_Beauty.jsonl`, `meta_All_Beauty.jsonl`) are expected under `data/raw/` unless you pass other paths.

```bash
python scripts/build_hackathon_data.py --reviews data/raw/All_Beauty.jsonl --meta data/raw/meta_All_Beauty.jsonl
python scripts/run_eda.py
python scripts/run_eda_deep.py
```
