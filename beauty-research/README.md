# Beauty customer-preference research

Reproducible local analysis of Amazon All Beauty and Sephora products/reviews, connecting exploratory data analysis, evidence-bounded 5 Whys, and falsifiable LLM research questions.

## Key findings

| Observed metric | Amazon All Beauty | Sephora |
|---|---:|---:|
| Catalog products | 112,590 | 8,494 |
| Raw review records | 701,528 | 1,094,411 |
| Reviews after exact deduplication | 694,253 | 1,094,187 |
| Reviewers with at least two reviewed products | 42,823 | 209,105 |
| Reviewers with at least five reviewed products | 1,471 | 40,433 |
| Existing binary recommendation labels | Not provided | 926,314 |
| Within-source product–review match | 100% | 100% |

Sephora contains 412,406 labeled reviews with a strictly earlier review of another product by the same customer, and 907,247 reviews with both an observed recommendation label and self-reported skin type. These are eligibility counts, not frozen test sizes or model results.

Amazon has broader product coverage but sparse reviewer histories: 93.2% of reviewers have one observed product. Requiring price, description and features retains 3.85% of catalog products. Among five-star products, 83.95% have fewer than five catalog ratings. Catalog aggregates and collected reviews represent different populations.

## Research direction without new human annotation

**Does an LLM's use of earlier customer reviews and customer context improve prediction of later reported product recommendations beyond popularity and history-based baselines?**

Use Sephora as the primary existing-label evaluation dataset. Keep Amazon as a separate robustness domain with a different rating outcome; no customer or product identity mapping across retailers is established.

Exclude target-review text, title, ratings, recommendation and feedback from inputs. Use strictly earlier histories; control repeated products and duplicate content. Freeze prompts, thresholds and chronology using development data. Compare against majority/popularity, structured history and text-embedding baselines. Audit undated customer profiles and product snapshots; remove future aggregate ratings. Report class balance, macro-F1, balanced accuracy, AUROC/PR-AUC, calibration, uncertainty, cost and latency.

Existing recommendation labels measure retrospective reported preferences. Neither dataset independently establishes prospective suitability, causal explanations, sales uplift or product safety. No LLM evaluation has been run. No new human annotation is required by the Sephora evaluation protocol. Older Amazon question cards include optional annotation-based directions; they are not prerequisites for this protocol.

## Workflows

- `notebooks/beauty_eda.ipynb`: full-file Amazon catalog EDA.
- `notebooks/beauty_reviews.ipynb`: review integration and quality audit.
- `notebooks/beauty_research_workflow.ipynb`: deterministic EDA tools → evidence ledger → 5 Whys → provisional question cards.
- `notebooks/sephora.ipynb`: Sephora integration and existing-label feasibility.
- `notebooks/eda_tools_agent.ipynb`: upstream agent example with local setup and a link to the combined workflow.

See [installation and execution](INSTALLATION.md). Runners in `scripts/` generate local HTML reports and Parquet datasets. No API key is needed for the deterministic integration workflows; the optional upstream LLM demo requires separate configuration.

## Data and publication scope

Obtain Amazon Reviews 2023 from https://amazon-reviews-2023.github.io/ and Sephora Products and Skincare Reviews from https://www.kaggle.com/datasets/nadyinky/sephora-products-and-skincare-reviews under their respective terms. Source registries record snapshot hashes and schemas. Review text, reviewer IDs, large derived data tables, raw downloads, virtual environments and credentials are not part of the GitHub publication package. Regenerate full data artifacts locally.

EDA tools originate from [business-science/ai-data-science-team](https://github.com/business-science/ai-data-science-team), pinned in the dependency lock. Research framing uses the locally installed [5 Whys](https://github.com/awesome-skills/5-whys-skill) and [Good Question](https://github.com/Rimagination/good-question) methodologies; these are methodological aids, not autonomous agents executed by the offline scripts.
