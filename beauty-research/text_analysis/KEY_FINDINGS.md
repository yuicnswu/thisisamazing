# Amazon All_Beauty: EDA, root-cause analysis, text NLP and key findings

*7 November 2026. Data: `meta_All_Beauty.jsonl` (112,590 products, SHA-256 1cfbdf6d…, identical to the audited copy) and `All_Beauty.jsonl` (701,528 reviews), Amazon Reviews 2023. Every number below is reproducible from `beauty-research/scripts/beauty_eda.py` and `beauty-research/text_analysis/`. Review shares are PPI++ estimates with 95% intervals of what the LLM annotator would label; they are not human-validated, and reviews are self-selected, so a share of reviews is not a share of customers.*

## 1. EDA of the product metadata

The audited EDA script re-run on this copy reproduces every count of the 24 October EDA.

| Measure | Value |
|---|---|
| Products / stores / brands | 112,590 / 30,364 / 22,412 |
| Main category | All Beauty 112,135; Premium Beauty 455 |
| Listings with a price | 15.7% (median observed price $16.99; 90th percentile $49.99) |
| Listings with title only (no description or features) | 88,746 (78.8%) |
| Price, description and features all present | 4,332 (3.85%) |
| Rating evidence | 5,690,450 ratings in total; top 1% of products hold 38% of them, top 10% hold 74% |
| Five-star products with fewer than 5 ratings | 12,189 of 14,519 |
| Duplicates | 2,043 excess duplicate titles; 33,825 images shared across products; 1,653 products share a UPC |
| Price vs average rating | Spearman 0.14 (weak) |
| Largest title-derived segments | Unclassified 38%, hair extensions / wigs 17.5%, makeup 10.2%, tools 10.0%, nails 8.2%, skin care 8.0% |

Category paths are empty in every record, so segments come from keyword rules on titles and are heuristic.

## 2. Text parsing and NLP

**Reviews.** 693,547 after cleaning: 7,276 exact duplicates and 705 empty texts dropped; median 19 tokens.
- *Aspect discovery:* NMF topics (30) and weighted log-odds (Monroe et al., 2008) fixed a 16-aspect taxonomy. The strongest low-star terms are money (z = 91), disappointed, waste, don't, cheap, return, broke and "doesn't work".
- *Aspect-based sentiment:* Claude Haiku labelled 3,500 reviews; 99.7% of its quotes were verbatim; Claude Sonnet agreed with a median kappa of 0.80.
- *Scaling:* TF-IDF logistic classifiers (AUROC 0.81–0.99 against the LLM labels) on every review; prevalence by PPI++.

**Listings.** Title, feature and description text parsed for 112,590 products. Median title is 17 words; 84.6% have no feature bullets and 83.1% no description. Nine claim types were extracted; the most common are multipack (26.4%), natural/organic (17.6%) and premium/professional (8.9%). The most frequent title bigrams are "human hair", "for women", "hair extensions" and "pack of".

## 3. Root-cause analysis (5 Whys)

The original four chains (`output/beauty_5whys/analysis.md`, A–D) still hold: completeness filters exclude 96% of the catalogue, star-only ranking ignores evidence volume, keyword segments misassign products, and the data cannot show ROI. Two chains were added from the text evidence:
- **E. Low star ratings overstate product failure.** About half of low-star reviews are about the listing, the unit received, packaging or delivery, not whether the product works. The association with unpriced listings and with certain segments is verified; the mechanism is not.
- **F. Claimed aspects draw criticism of that aspect.** This holds for scent and hydration claims. Why is not established.

## 4. Key findings

1. **Most reviews say little.** 61.7% [59.6, 63.8] give an overall verdict; the most discussed specific aspect is efficacy, at 30.1% [28.3, 31.9].
2. **A low rating is often not about the product working.** Of 1–2★ reviews, 29.8% [25.4, 34.1] criticise efficacy, 27.1% [22.5, 31.6] authenticity or quality, 11.7% [8.4, 15.0] packaging and 11.0% [7.8, 14.2] delivery.
3. **What goes wrong depends on the segment.** Authenticity/quality criticism is 2.7% [0.5, 4.8] in skin care but about 11% in hair extensions, makeup and nails. Efficacy criticism peaks in skin care (13.2% [8.9, 17.5]) and grooming (14.4%), and is lowest for hair extensions (3.6%).
4. **Unpriced listings draw more authenticity complaints:** 9.3% [7.8, 10.8] of their reviews, against 4.2–6.1% for priced products.
5. **Scent and hydration claims draw criticism of those aspects.** Where a listing claims a scent, scent criticism is 9.1% vs 2.5% (+6.6 points [+0.9, +12.4]); hydration claims, +3.1 points [+0.1, +6.1]. Other claims show no clear difference.
6. **Customers rarely describe themselves.** Repeat purchase 4.9%, gift 3.0%, any skin or hair type ≤ 1.3%. Customer-context analysis needs Sephora's structured fields.
7. **Complaints are spread out.** No product holds more than 3% of any aspect's criticism, and no store more than 7.5% (scent, one store); the top 10 stores hold 6–18%.
8. **Criticism is rising.** Negative overall verdicts went from 4.2% [1.4, 7.1] of reviews up to 2015 to 16.6% [13.6, 19.7] in 2021–23; price criticism from 1.5% to 7.8% [5.5, 10.0].
9. **Listings are thin.** 78.8% are title-only and 15.7% show a price, so a brief that relies on listing facts covers a small, selected part of the catalogue.

## 5. What this means for the paper

These results are now §6.2 of the paper and two new RCA chains in §6.3. They justify reporting aspect-level criticism instead of star share (MR4), segment-specific cohorts (DP4), and association-only wording for claim effects (MR6). They also supply oracles for the trap tasks. Sephora results will follow from the same pipeline.

## Files

- Review aspects: `outputs/amazon/results.md`, `results.json`
- Metadata join (segments, price bands, completeness, stores): `outputs/amazon/meta_results.md`, `meta_results.json`
- Listing NLP and claim-experience tests: `outputs/amazon/listing_nlp.md`, `listing_nlp.json`
- Metadata EDA: `../output/beauty_eda/` (re-run identical)
- 5 Whys: `../output/beauty_5whys/analysis.md` (sections E and F added)
