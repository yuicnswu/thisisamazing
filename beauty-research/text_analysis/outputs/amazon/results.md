# Review text analysis: amazon

693,547 reviews after cleaning (701,528 raw, 7,276 exact duplicates and 705 empty reviews dropped), 112,496 products, 2000-11-01 to 2023-09-09. Shares are of all reviews, with 95% PPI++ intervals from a 1,500-review random calibration sample. They estimate what the three-model jury (after the semantic support check) would say about every review; they are not human-validated.

## Label quality

- Self-refining guide (no human coders): 2 refinement round(s), 20 learned rules. Dev macro kappa claude-haiku-5-5 vs claude-sonnet-5-5: 0.799 → 0.864 → 0.872. Held-out test (200 reviews): 0.807 with the original guide, 0.826 with the selected guide.
- Gold labels (jury_entailed): calib reviews where the two coders disagreed (37.5%) were adjudicated by claude-opus-5-5. Primary coder vs jury on calib: macro kappa 0.915.
- Semantic support check (claude-opus-5-5): 9.4% of verbatim gold labels were judged not supported by their quote and dropped. On a known-answer contrast set the judge accepted 99.0% of original labels and rejected 97.9% of perturbed ones (flipped polarity 99.7%, swapped aspect 100.0%, wrong quote 92.7%).
- Verbatim quotes: 99.6% of train labels and 99.8% of calib labels had a quote found word for word in the review. Labels without one were dropped.
- Second annotator (claude-sonnet-5-5) on 1499 calib reviews: median Cohen's kappa for aspect mention 0.85 (range 0.75–0.96, aspects with at least 10 positives).

## T1. What reviews talk about

| Aspect | Mentions | Criticises (neg or mixed) | Praises | Low-star reviews that criticise it (T3) |
|---|---|---|---|---|
| overall | 58.5% [56.3%, 60.7%] | 13.1% [11.7%, 14.5%] | 47.5% [45.4%, 49.6%] | 50.2% [45.0%, 55.3%] |
| efficacy | 27.8% [26.0%, 29.6%] | 7.3% [6.2%, 8.5%] | 22.3% [20.5%, 24.0%] | 24.1% [20.0%, 28.2%] |
| authenticity_quality | 18.5% [16.9%, 20.0%] | 11.0% [9.7%, 12.3%] | 7.9% [6.7%, 9.1%] | 34.4% [29.9%, 39.0%] |
| ease_of_use | 14.3% [12.9%, 15.6%] | 4.4% [3.4%, 5.4%] | 10.3% [8.9%, 11.7%] | 8.5% [5.5%, 11.5%] |
| size_quantity | 12.6% [11.3%, 14.0%] | 6.0% [5.0%, 7.0%] | 6.9% [5.7%, 8.2%] | 12.1% [9.0%, 15.2%] |
| price_value | 10.1% [9.0%, 11.3%] | 2.4% [1.7%, 3.2%] | 8.0% [6.8%, 9.1%] | 3.8% [1.7%, 6.0%] |
| scent | 9.2% [8.3%, 10.1%] | 2.7% [2.0%, 3.5%] | 6.2% [5.2%, 7.2%] | 7.2% [4.8%, 9.7%] |
| colour_shade | 8.4% [7.4%, 9.4%] | 2.6% [1.9%, 3.3%] | 6.2% [5.2%, 7.2%] | 5.7% [3.3%, 8.0%] |
| texture | 8.3% [7.1%, 9.6%] | 3.2% [2.4%, 4.1%] | 5.9% [4.8%, 7.0%] | 7.8% [5.0%, 10.7%] |
| hair_result | 7.8% [6.7%, 8.9%] | 2.3% [1.6%, 2.9%] | 5.9% [4.9%, 7.0%] | 5.2% [3.3%, 7.1%] |
| longevity | 5.5% [4.5%, 6.5%] | 2.2% [1.5%, 2.8%] | 3.6% [2.7%, 4.5%] | 5.5% [3.2%, 7.8%] |
| hydration_skin_feel | 5.3% [4.4%, 6.3%] | 0.7% [0.3%, 1.2%] | 4.8% [3.8%, 5.8%] | 2.4% [0.7%, 4.1%] |
| packaging | 5.3% [4.3%, 6.3%] | 2.8% [2.0%, 3.6%] | 2.7% [1.9%, 3.5%] | 7.6% [4.7%, 10.5%] |
| delivery_service | 4.8% [3.9%, 5.8%] | 1.5% [0.9%, 2.0%] | 3.4% [2.5%, 4.2%] | 5.7% [3.3%, 8.2%] |
| skin_reaction | 3.2% [2.4%, 4.0%] | 1.2% [0.7%, 1.8%] | 1.9% [1.3%, 2.6%] | 3.6% [1.6%, 5.6%] |
| ingredients | 1.8% [1.2%, 2.5%] | – | 1.4% [0.8%, 2.0%] | – |

## T2. Criticism by star rating (share of reviews at that rating)

| Aspect | 1★ | 2★ | 3★ | 4★ | 5★ |
|---|---|---|---|---|---|
| overall | 53.8% | 41.1% | 21.9% | 7.9% | 0.5% |
| efficacy | 24.5% | 22.9% | 15.0% | 6.0% | 1.0% |
| authenticity_quality | 35.5% | 31.9% | 24.6% | 9.2% | 1.0% |
| ease_of_use | 8.2% | 9.2% | 9.5% | 9.0% | 1.3% |
| size_quantity | 11.8% | 12.8% | 16.9% | 10.2% | 1.5% |
| price_value | 4.4% | 2.5% | 7.2% | 2.4% | 1.1% |
| scent | 7.4% | 6.9% | 7.4% | 1.8% | 0.5% |
| colour_shade | 5.6% | 5.8% | 8.5% | 2.7% | 0.6% |
| texture | 6.5% | 11.0% | 7.9% | 3.5% | 1.0% |
| hair_result | 5.0% | 5.6% | 9.8% | 1.4% | 0.2% |
| longevity | 4.9% | 7.0% | 3.8% | 4.1% | 0.3% |
| hydration_skin_feel | 2.9% | 1.2% | 0.8% | 0.6% | 0.2% |
| packaging | 9.2% | 3.8% | 2.5% | 4.0% | 0.9% |
| delivery_service | 7.7% | 1.0% | 0.9% | 1.5% | 0.1% |
| skin_reaction | 4.5% | 1.3% | 0.8% | 2.6% | 0.2% |

## T4. Customer context stated in reviews

| Context | Share of reviews |
|---|---|
| repeat_buyer | 3.4% [2.5%, 4.3%] |
| gift | 3.1% [2.3%, 3.9%] |
| hair_curly | 0.9% [0.4%, 1.4%] |
| hair_fine | 0.9% [0.4%, 1.3%] |
| skin_sensitive | 0.8% [0.4%, 1.2%] |

## T5. Is criticism concentrated in a few products? (products with ≥ 20 reviews, classifier estimates)

| Aspect | Predicted criticisms | Top product's share | Top 10 products' share |
|---|---|---|---|
| overall | 61,162 | 0.5% | 3.7% |
| authenticity_quality | 40,692 | 0.6% | 4.3% |
| efficacy | 36,968 | 0.6% | 4.0% |
| size_quantity | 27,266 | 0.5% | 4.0% |
| ease_of_use | 25,204 | 0.6% | 4.1% |
| hair_result | 7,285 | 1.6% | 9.9% |
| scent | 6,824 | 1.6% | 9.0% |
| texture | 6,287 | 1.5% | 6.2% |
| delivery_service | 5,486 | 0.5% | 3.8% |
| hydration_skin_feel | 5,181 | 0.7% | 3.7% |
| colour_shade | 4,639 | 3.2% | 9.2% |
| price_value | 4,186 | 0.7% | 4.3% |
| packaging | 4,140 | 1.9% | 6.8% |
| longevity | 3,744 | 1.5% | 6.0% |
| skin_reaction | 1,553 | 1.6% | 6.2% |

## T6. Criticism by group

**period**

| Aspect | ≤2015 | 2016-18 | 2019-20 | 2021-23 |
|---|---|---|---|---|
| overall | 7.0% | 12.2% | 13.7% | 14.5% |
| efficacy | 6.4% | 6.3% | 6.4% | 9.7% |
| authenticity_quality | 7.5% | 10.9% | 11.1% | 11.9% |
| ease_of_use | 3.8% | 3.9% | 5.6% | 3.9% |
| size_quantity | 4.7% | 4.5% | 6.7% | 7.1% |
| price_value | 1.5% | 1.4% | 1.4% | 5.0% |
| scent | 1.8% | 1.8% | 3.0% | 3.6% |
| colour_shade | 2.7% | 1.9% | 2.7% | 3.1% |
| texture | 0.6% | 1.9% | 3.4% | 5.3% |
| hair_result | 1.1% | 1.4% | 2.4% | 3.0% |
| longevity | 2.9% | 1.9% | 1.5% | 2.8% |
| hydration_skin_feel | 0.6% | 1.2% | 0.4% | 0.7% |
| packaging | 2.0% | 2.5% | 2.9% | 3.1% |
| delivery_service | 0.7% | 1.5% | 2.2% | 0.9% |
| skin_reaction | 1.2% | 1.5% | 0.6% | 1.6% |

**verified**

| Aspect | True | False |
|---|---|---|
| overall | 12.8% | 15.5% |
| efficacy | 7.0% | 10.2% |
| authenticity_quality | 11.3% | 8.0% |
| ease_of_use | 4.4% | 4.7% |
| size_quantity | 5.9% | 6.6% |
| price_value | 2.1% | 4.7% |
| scent | 2.9% | 1.3% |
| colour_shade | 2.5% | 3.3% |
| texture | 3.2% | 3.4% |
| hair_result | 2.2% | 2.7% |
| longevity | 2.1% | 2.2% |
| hydration_skin_feel | 0.6% | 2.0% |
| packaging | 2.9% | 1.3% |
| delivery_service | 1.4% | 1.8% |
| skin_reaction | 1.2% | 1.3% |

\* fewer than 40 calibration reviews in the group: classifier estimate only, no interval.

## T7. Precision gained by scaling (criticism shares)

| Aspect | LLM labels alone (calib) ± | PPI++ ± |
|---|---|---|
| efficacy | 7.5% ± 1.3% | 7.3% ± 1.1% |
| skin_reaction | 1.2% ± 0.6% | 1.2% ± 0.5% |
| hydration_skin_feel | 0.7% ± 0.4% | 0.7% ± 0.4% |
| texture | 3.2% ± 0.9% | 3.2% ± 0.9% |
| scent | 2.7% ± 0.8% | 2.7% ± 0.7% |
| longevity | 2.1% ± 0.7% | 2.2% ± 0.7% |
| colour_shade | 2.8% ± 0.8% | 2.6% ± 0.7% |
| hair_result | 2.3% ± 0.8% | 2.3% ± 0.7% |
| packaging | 2.7% ± 0.8% | 2.8% ± 0.8% |
| size_quantity | 6.1% ± 1.2% | 6.0% ± 1.0% |
| price_value | 2.3% ± 0.8% | 2.4% ± 0.7% |
| authenticity_quality | 10.6% ± 1.6% | 11.0% ± 1.3% |
| delivery_service | 1.5% ± 0.6% | 1.5% ± 0.6% |
| ease_of_use | 4.5% ± 1.1% | 4.4% ± 1.0% |
| overall | 13.5% ± 1.7% | 13.1% ± 1.4% |

## Distinctive terms, 1–2★ vs 4–5★ (weighted log-odds, z-scores)

- **Low-star:** money (91.5), disappointed (72.8), waste (66.4), don't (65.9), star (63.7), work (61.0), cheap (57.4), didn't (57.2), return (51.7), did (51.2), broke (50.1), bad (50.1), horrible (49.7), broken (46.9), terrible (46.3), doesn't (46.0), waste money (42.6), poor (40.2), doesn't work (38.9), returned (36.6), worst (36.1), didn't work (35.3), awful (35.1), wouldn't (34.8), does work (34.7)
- **High-star:** great (-90.4), love (-80.8), works (-48.1), easy (-43.5), perfect (-43.2), nice (-41.5), stars (-38.4), best (-38.2), good (-36.3), amazing (-34.3), soft (-33.0), price (-31.8), great product (-31.7), beautiful (-30.8), skin (-29.2), easy use (-27.7), little (-27.2), awesome (-26.5), works great (-24.8), cute (-24.4), excellent (-24.4), highly (-23.3), value (-22.3), loved (-21.7), favorite (-21.7)

## Example verbatim quotes

- **overall, neg:** “I won’t be purchasing these again. Ardells are way better.”
- **overall, pos:** “I would recommend this polyglot kit.”
- **efficacy, neg:** “it still has a little bit of the fun house mirror affect”
- **efficacy, pos:** “they work great for poly gel and hard gel”
- **authenticity_quality, neg:** “Instead, I received this ugly "forest green" color and not the shape in the picture.”
- **authenticity_quality, pos:** “It was came exactly as described.”
- **ease_of_use, neg:** “can’t remove you hair unless the unit is on”
- **ease_of_use, pos:** “it was really easy to work with”
- **size_quantity, neg:** “Too straight. Have to bend them to fit my eye”
- **size_quantity, pos:** “try out the products before I purchase the full-size ones”
- **price_value, neg:** “I personally think the price is a bit much.”
- **price_value, pos:** “I love the price on these tart mini products.”
- **scent, neg:** “the scents are good but all three had this subtle weird smell”
- **scent, pos:** “It has a VERY SUBTLE PLEASANT FRAGRANCE.”
- **colour_shade, neg:** “the color you have to apply like 10 layer”
- **colour_shade, pos:** “color fullness color and texture will purchase another one soon”
- **texture, neg:** “Inconsistent product, sometimes watery sometimes thick and correct consistency.”
- **texture, pos:** “color fullness color and texture will purchase another one soon”
- **hair_result, neg:** “I have a lot less hair loss in the shower with hairprint products, although I prefer the Amla shampoo, it's smoother.”
- **hair_result, pos:** “the balm tames it down and makes it very soft”
- **longevity, neg:** “keeps coming undone because it won’t stay curved”
- **longevity, pos:** “it stays on your lips for hours”
- **hydration_skin_feel, neg:** “it does leave your skin a little oily shinny looking”
- **hydration_skin_feel, pos:** “Keeps my lips nice and smooth and moisturized.”
- **packaging, neg:** “just really damaged but not the box it came in.”
- **packaging, pos:** “it has a nice cloth (light) case for traveling”
- **delivery_service, neg:** “FINALLY received my package today after ordering over a month ago!!”
- **delivery_service, pos:** “The nail drill came quickly and it was packaged very well.”
- **skin_reaction, neg:** “my fingers around my nails are extremely sore”
- **skin_reaction, pos:** “my sensitive skin actually likes this exotic facial astringent.”
- **ingredients, neg:** “It is basically Vaseline and wax”
- **ingredients, pos:** “This product is fluoride free and very healthy for you.”

## Classifier quality on the held-out calib sample (vs gold labels)

| Target | AUROC | Avg precision | Calib positives |
|---|---|---|---|
| mention_efficacy | 0.875 | 0.741 | 425 |
| neg_efficacy | 0.916 | 0.59 | 113 |
| mention_skin_reaction | 0.882 | 0.4 | 47 |
| neg_skin_reaction | 0.916 | 0.282 | 18 |
| mention_hydration_skin_feel | 0.962 | 0.634 | 80 |
| neg_hydration_skin_feel | 0.919 | 0.164 | 11 |
| mention_texture | 0.862 | 0.401 | 126 |
| neg_texture | 0.864 | 0.223 | 48 |
| mention_scent | 0.986 | 0.874 | 126 |
| neg_scent | 0.964 | 0.38 | 40 |
| mention_longevity | 0.93 | 0.532 | 82 |
| neg_longevity | 0.934 | 0.334 | 32 |
| mention_colour_shade | 0.973 | 0.766 | 134 |
| neg_colour_shade | 0.961 | 0.492 | 42 |
| mention_hair_result | 0.946 | 0.582 | 116 |
| neg_hair_result | 0.919 | 0.34 | 34 |
| mention_packaging | 0.93 | 0.459 | 77 |
| neg_packaging | 0.948 | 0.33 | 40 |
| mention_size_quantity | 0.887 | 0.644 | 188 |
| neg_size_quantity | 0.916 | 0.592 | 92 |
| mention_price_value | 0.943 | 0.715 | 143 |
| neg_price_value | 0.921 | 0.264 | 35 |
| mention_authenticity_quality | 0.878 | 0.617 | 264 |
| neg_authenticity_quality | 0.891 | 0.581 | 159 |
| mention_delivery_service | 0.906 | 0.493 | 75 |
| neg_delivery_service | 0.946 | 0.332 | 22 |
| mention_ease_of_use | 0.927 | 0.756 | 217 |
| neg_ease_of_use | 0.922 | 0.467 | 68 |
| mention_ingredients | 0.926 | 0.506 | 27 |
| mention_overall | 0.774 | 0.816 | 891 |
| neg_overall | 0.886 | 0.593 | 202 |

Not modelled (too few training positives): neg_ingredients, ctx_skin_dry, ctx_skin_oily, ctx_skin_combination, ctx_skin_acne, ctx_skin_mature, ctx_hair_thick_coarse, ctx_hair_damaged.
