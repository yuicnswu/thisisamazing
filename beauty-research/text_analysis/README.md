# Review text analysis

Aspect-based sentiment analysis (ABSA) of beauty reviews, scaled to the full corpus with valid
confidence intervals. The same code runs on Amazon All_Beauty and on Sephora.

## Method

| Step | Script | What it does | Why this method |
|---|---|---|---|
| 1 | `parse.py` | One clean table per source: HTML stripped, whitespace normalised, exact duplicates (same author, product, rating, title, text, date) and empty texts dropped | Same schema for both retailers |
| 2 | `discover.py` | NMF topic model on TF-IDF 1–2-grams (30 topics, generic evaluative words removed) and weighted log-odds with an informative Dirichlet prior for 1–2★ vs 4–5★ (Monroe, Colaresi & Quinn, 2008) | Grounds the aspect list in the data before any labelling; log-odds with a prior is the standard way to find distinctive words without rare-word noise |
| 3 | `label.py`, `aspects.py` | An LLM (Claude Haiku 5.5) labels each review with aspects, a polarity per aspect and a verbatim quote, plus customer context it states (skin type, hair type, gift, repeat purchase). A label is kept only if its quote occurs word for word in the review. A second model (Claude Sonnet 5.5) labels 400 reviews for agreement | LLM ABSA is the current state of the art for open-domain aspect extraction; the verbatim check is the grounding rule that worked in this project's EvidenceGuard pilot |
| 4 | `scale.py` | Logistic regression on TF-IDF word and character n-grams, one per target, trained on a rating-stratified 2,000-review sample and applied to every review. Prevalence by prediction-powered inference with power tuning (PPI++; Angelopoulos et al., 2023), using a separate 1,500-review simple random sample | Labelling 0.7–1.1M reviews with an LLM is not affordable; PPI gives unbiased shares and valid 95% intervals from a cheap classifier plus a small labelled sample, and is never worse than the labelled sample alone |
| 5 | `analyze.py` | Tables T1–T7: aspect prevalence, criticism by star, what low ratings are about, customer context, concentration in top products, groups, and the precision PPI adds | |
| 6 | `join_meta.py` (Amazon) | Joins product metadata: title-derived segment, price band, listing completeness, store; criticism by group with PPI++ | |
| 7 | `listing_nlp.py` (Amazon) | Parses listing titles, features and descriptions; extracts 9 claim types; compares criticism of the claimed aspect with and without the claim | Descriptive claim-experience test |

Key findings across EDA, RCA and NLP: [KEY_FINDINGS.md](KEY_FINDINGS.md).

## Aspect taxonomy and where it came from

`aspects.py` lists 16 aspects and 12 customer-context tags. The step-2 NMF topics (`outputs/amazon/topics.json`) map onto them as follows: hair (topics 0, 12), quality (1), price and value (3, 6, 23, 25), ease of use (4), colour (5, 10), size (7, 14, 29), scent (8, 9, 19), skin feel (11), gift (13, 18), longevity (17), delivery and service (16, 21, 24), not as pictured (22, 28; folded into authenticity_quality). Topics about product types (brushes, lashes, nails) are not aspects. Low-star log-odds terms (waste, broke, broken, returned, dried, fell apart, picture) point to efficacy, packaging, authenticity and value criticism.

## What the numbers mean

Shares estimate what the LLM annotator would say if it read every review. They are not human-validated, and LLM labelling errors carry over. Agreement with a second model is reported as a check. Reviews are self-selected, so a share of reviews is not a share of customers.

## Reproduce

```bash
pip install scikit-learn pandas pyarrow scipy
python parse.py amazon /path/to/All_Beauty.jsonl        # or: python parse.py sephora ~/Downloads/archive
python discover.py amazon
python label.py amazon --workers 6                       # needs the Claude Code CLI (set CLAUDE_BIN if not on PATH); cached in outputs/llm_cache.jsonl
python scale.py amazon
python analyze.py amazon                                 # -> outputs/amazon/results.md
python join_meta.py /path/to/meta_All_Beauty.jsonl.gz    # Amazon only
python listing_nlp.py /path/to/meta_All_Beauty.jsonl.gz
python -m pytest tests
```

Large files (`reviews.parquet`, `predictions.parquet`) are not committed; everything else, including the LLM cache, is.
