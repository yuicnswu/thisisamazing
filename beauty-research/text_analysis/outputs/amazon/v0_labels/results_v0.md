# Review text analysis: amazon

693,547 reviews after cleaning (701,528 raw, 7,276 exact duplicates and 705 empty reviews dropped), 112,496 products, 2000-11-01 to 2023-09-09. Shares are of all reviews, with 95% PPI++ intervals from a 1,499-review random calibration sample. They estimate what the LLM annotator would say about every review; they are not human-validated.

## Label quality

- Verbatim quotes: 99.6% of train labels and 99.8% of calib labels had a quote found word for word in the review. Labels without one were dropped.
- Second annotator (claude-sonnet-5-5) on 400 calib reviews: median Cohen's kappa for aspect mention 0.80 (range 0.67–0.97, aspects with at least 10 positives).

## T1. What reviews talk about

| Aspect | Mentions | Criticises (neg or mixed) | Praises | Low-star reviews that criticise it (T3) |
|---|---|---|---|---|
| overall | 61.7% [59.6%, 63.8%] | 13.0% [11.6%, 14.5%] | 51.7% [49.7%, 53.8%] | 46.0% [40.8%, 51.2%] |
| efficacy | 30.1% [28.3%, 31.9%] | 9.4% [8.2%, 10.7%] | 23.5% [21.7%, 25.2%] | 29.8% [25.4%, 34.1%] |
| ease_of_use | 18.1% [16.6%, 19.7%] | 6.5% [5.4%, 7.6%] | 12.4% [10.9%, 13.9%] | 12.7% [9.5%, 15.8%] |
| authenticity_quality | 15.9% [14.4%, 17.4%] | 8.1% [6.9%, 9.3%] | 8.0% [6.9%, 9.2%] | 27.1% [22.5%, 31.6%] |
| price_value | 12.8% [11.6%, 14.0%] | 4.7% [3.8%, 5.7%] | 8.6% [7.4%, 9.8%] | 12.9% [9.6%, 16.1%] |
| hair_result | 11.4% [10.3%, 12.5%] | 4.2% [3.4%, 5.1%] | 8.2% [7.1%, 9.3%] | 10.3% [7.6%, 12.9%] |
| size_quantity | 11.2% [9.9%, 12.5%] | 5.6% [4.6%, 6.5%] | 6.0% [4.9%, 7.2%] | 10.4% [7.7%, 13.2%] |
| colour_shade | 9.8% [8.8%, 10.9%] | 3.3% [2.5%, 4.1%] | 7.3% [6.2%, 8.4%] | 7.7% [5.1%, 10.2%] |
| scent | 9.6% [8.7%, 10.6%] | 2.9% [2.1%, 3.6%] | 6.5% [5.5%, 7.5%] | 7.2% [4.9%, 9.6%] |
| packaging | 9.2% [7.9%, 10.5%] | 4.7% [3.8%, 5.7%] | 5.0% [3.9%, 6.0%] | 11.7% [8.4%, 15.0%] |
| texture | 9.1% [7.8%, 10.4%] | 3.9% [3.0%, 4.9%] | 5.9% [4.8%, 7.0%] | 9.2% [6.1%, 12.3%] |
| longevity | 7.3% [6.1%, 8.4%] | 3.1% [2.3%, 3.9%] | 4.5% [3.5%, 5.6%] | 8.0% [5.3%, 10.8%] |
| delivery_service | 6.3% [5.2%, 7.3%] | 2.7% [2.0%, 3.5%] | 3.6% [2.8%, 4.5%] | 11.0% [7.8%, 14.2%] |
| hydration_skin_feel | 5.3% [4.3%, 6.3%] | 0.7% [0.3%, 1.2%] | 4.8% [3.9%, 5.8%] | 2.1% [0.5%, 3.6%] |
| skin_reaction | 3.6% [2.7%, 4.4%] | 1.4% [0.9%, 2.0%] | 2.3% [1.6%, 3.1%] | 3.6% [1.6%, 5.6%] |
| ingredients | 1.9% [1.2%, 2.5%] | 0.5% [0.1%, 0.8%] | 1.5% [0.9%, 2.1%] | 1.1% [0.0%, 2.2%] |

## T2. Criticism by star rating (share of reviews at that rating)

| Aspect | 1★ | 2★ | 3★ | 4★ | 5★ |
|---|---|---|---|---|---|
| overall | 47.8% | 41.4% | 28.9% | 7.8% | 0.6% |
| efficacy | 28.2% | 33.6% | 20.6% | 9.1% | 1.2% |
| ease_of_use | 13.7% | 10.1% | 16.2% | 13.3% | 1.7% |
| authenticity_quality | 27.6% | 25.8% | 16.5% | 6.0% | 0.9% |
| price_value | 15.0% | 7.5% | 9.5% | 3.0% | 1.6% |
| hair_result | 10.2% | 10.4% | 13.8% | 2.6% | 1.1% |
| size_quantity | 9.7% | 12.1% | 13.4% | 9.2% | 2.1% |
| colour_shade | 8.7% | 5.2% | 9.8% | 4.6% | 0.6% |
| scent | 7.4% | 7.0% | 8.4% | 1.8% | 0.6% |
| packaging | 12.2% | 10.4% | 7.2% | 5.5% | 1.8% |
| texture | 7.0% | 14.3% | 10.4% | 4.4% | 1.1% |
| longevity | 7.9% | 8.3% | 7.5% | 4.7% | 0.5% |
| delivery_service | 13.9% | 3.9% | 1.3% | 1.5% | 0.4% |
| hydration_skin_feel | 2.9% | 0.0% | 0.8% | 1.6% | 0.1% |
| skin_reaction | 4.5% | 1.3% | 0.9% | 3.1% | 0.4% |
| ingredients | 1.5% | 0.0% | 0.0% | 2.1% | 0.0% |

## T4. Customer context stated in reviews

| Context | Share of reviews |
|---|---|
| repeat_buyer | 4.9% [3.9%, 6.0%] |
| gift | 3.0% [2.2%, 3.8%] |
| hair_thick_coarse | 1.3% [0.7%, 1.8%] |
| hair_curly | 1.0% [0.5%, 1.5%] |
| hair_fine | 0.9% [0.4%, 1.3%] |
| skin_sensitive | 0.8% [0.3%, 1.2%] |

## T5. Is criticism concentrated in a few products? (products with ≥ 20 reviews, classifier estimates)

| Aspect | Predicted criticisms | Top product's share | Top 10 products' share |
|---|---|---|---|
| authenticity_quality | 41,275 | 0.5% | 4.1% |
| overall | 41,095 | 0.6% | 3.8% |
| efficacy | 41,029 | 0.6% | 4.1% |
| ease_of_use | 16,196 | 0.9% | 6.1% |
| packaging | 15,701 | 0.6% | 3.9% |
| longevity | 13,734 | 0.9% | 3.9% |
| size_quantity | 12,669 | 0.9% | 5.1% |
| hair_result | 10,203 | 1.8% | 10.3% |
| price_value | 7,132 | 0.6% | 4.0% |
| scent | 6,568 | 1.6% | 9.0% |
| texture | 6,315 | 0.9% | 5.0% |
| colour_shade | 5,797 | 2.8% | 8.8% |
| ingredients | 3,310 | 0.5% | 3.7% |
| delivery_service | 3,118 | 0.6% | 4.4% |
| skin_reaction | 1,661 | 1.5% | 6.2% |
| hydration_skin_feel | 1,045 | 1.0% | 5.0% |

## T6. Criticism by group

**period**

| Aspect | ≤2015 | 2016-18 | 2019-20 | 2021-23 |
|---|---|---|---|---|
| overall | 4.2% | 13.2% | 11.7% | 16.6% |
| efficacy | 7.9% | 9.1% | 8.0% | 11.9% |
| ease_of_use | 6.2% | 5.0% | 7.1% | 7.5% |
| authenticity_quality | 4.5% | 9.5% | 8.2% | 7.6% |
| price_value | 1.5% | 3.6% | 3.9% | 7.8% |
| hair_result | 2.4% | 3.1% | 4.1% | 6.0% |
| size_quantity | 4.6% | 4.7% | 6.3% | 6.0% |
| colour_shade | 3.0% | 2.7% | 3.9% | 3.3% |
| scent | 1.8% | 1.9% | 2.9% | 4.0% |
| packaging | 2.0% | 5.4% | 4.9% | 4.8% |
| texture | 0.6% | 2.6% | 4.3% | 5.8% |
| longevity | 4.2% | 2.0% | 2.6% | 4.4% |
| delivery_service | 1.3% | 2.5% | 3.9% | 2.0% |
| hydration_skin_feel | 0.6% | 1.0% | 0.6% | 0.7% |
| skin_reaction | 2.4% | 1.5% | 0.6% | 1.9% |
| ingredients | 1.3% | 0.8% | 0.2% | 0.2% |

**verified**

| Aspect | True | False |
|---|---|---|
| overall | 12.4% | 18.2% |
| efficacy | 8.8% | 14.9% |
| ease_of_use | 6.5% | 7.3% |
| authenticity_quality | 8.4% | 5.5% |
| price_value | 4.4% | 7.8% |
| hair_result | 4.3% | 2.7% |
| size_quantity | 5.5% | 6.5% |
| colour_shade | 3.3% | 3.2% |
| scent | 3.0% | 1.3% |
| packaging | 4.8% | 4.0% |
| texture | 4.0% | 3.1% |
| longevity | 3.2% | 2.5% |
| delivery_service | 2.8% | 2.4% |
| hydration_skin_feel | 0.6% | 2.0% |
| skin_reaction | 1.4% | 1.9% |
| ingredients | 0.3% | 1.9% |

\* fewer than 40 calibration reviews in the group: classifier estimate only, no interval.

## T7. Precision gained by scaling (criticism shares)

| Aspect | LLM labels alone (calib) ± | PPI++ ± |
|---|---|---|
| efficacy | 9.8% ± 1.5% | 9.4% ± 1.3% |
| skin_reaction | 1.4% ± 0.6% | 1.4% ± 0.6% |
| hydration_skin_feel | 0.7% ± 0.4% | 0.7% ± 0.4% |
| texture | 3.9% ± 1.0% | 3.9% ± 0.9% |
| scent | 2.8% ± 0.8% | 2.9% ± 0.7% |
| longevity | 3.1% ± 0.9% | 3.1% ± 0.8% |
| colour_shade | 3.7% ± 1.0% | 3.3% ± 0.8% |
| hair_result | 4.1% ± 1.0% | 4.2% ± 0.9% |
| packaging | 4.7% ± 1.1% | 4.7% ± 1.0% |
| size_quantity | 5.9% ± 1.2% | 5.6% ± 0.9% |
| price_value | 4.7% ± 1.1% | 4.7% ± 1.0% |
| authenticity_quality | 7.8% ± 1.4% | 8.1% ± 1.2% |
| delivery_service | 2.7% ± 0.8% | 2.7% ± 0.7% |
| ease_of_use | 6.9% ± 1.3% | 6.5% ± 1.1% |
| ingredients | 0.5% ± 0.3% | 0.5% ± 0.3% |
| overall | 13.0% ± 1.7% | 13.0% ± 1.4% |

## Distinctive terms, 1–2★ vs 4–5★ (weighted log-odds, z-scores)

- **Low-star:** money (91.5), disappointed (72.8), waste (66.4), don't (65.9), star (63.7), work (61.0), cheap (57.4), didn't (57.2), return (51.7), did (51.2), broke (50.1), bad (50.1), horrible (49.7), broken (46.9), terrible (46.3), doesn't (46.0), waste money (42.6), poor (40.2), doesn't work (38.9), returned (36.6), worst (36.1), didn't work (35.3), awful (35.1), wouldn't (34.8), does work (34.7)
- **High-star:** great (-90.4), love (-80.8), works (-48.1), easy (-43.5), perfect (-43.2), nice (-41.5), stars (-38.4), best (-38.2), good (-36.3), amazing (-34.3), soft (-33.0), price (-31.8), great product (-31.7), beautiful (-30.8), skin (-29.2), easy use (-27.7), little (-27.2), awesome (-26.5), works great (-24.8), cute (-24.4), excellent (-24.4), highly (-23.3), value (-22.3), loved (-21.7), favorite (-21.7)

## Example verbatim quotes

- **overall, neg:** “I won’t be purchasing these again.”
- **overall, pos:** “I would recommend this polyglot kit.”
- **efficacy, neg:** “it still has a little bit of the fun house mirror affect.”
- **efficacy, pos:** “they work great for poly gel and hard gel”
- **ease_of_use, neg:** “Have to bend them to fit my eye”
- **ease_of_use, pos:** “To my surprise it was really easy to work with.”
- **authenticity_quality, neg:** “I did not see anywhere in the description that this was randomly picked”
- **authenticity_quality, pos:** “It was came exactly as described.”
- **price_value, neg:** “I personally think the price is a bit much.”
- **price_value, pos:** “I love the price on these tart mini products.”
- **hair_result, neg:** “looks like yarn will be very damaging to my hair”
- **hair_result, pos:** “this works great at cleansing my aging, thinnning, dry hair”
- **size_quantity, neg:** “The one that I got in this delivery BARELY has any gel.”
- **size_quantity, pos:** “I was able to try out the products before I purchase the full-size ones.”
- **colour_shade, neg:** “the color you have to apply like 10 layer”
- **colour_shade, pos:** “Beautiful and the color is very unusal”
- **scent, neg:** “the scents are good but all three had this subtle weird smell”
- **scent, pos:** “It has a VERY SUBTLE PLEASANT FRAGRANCE.”
- **packaging, neg:** “The bottle appears to be used or just really damaged but not the box it came in.”
- **packaging, pos:** “I was able to put the smaller bag inside the larger bag and pop it into my luggage.”
- **texture, neg:** “It is basically Vaseline and wax and very greasy.”
- **texture, pos:** “came out like mousse, which is what I already had and liked.”
- **longevity, neg:** “they don’t hold curl as long.”
- **longevity, pos:** “They definitely do have longer retention due to the grooves.”
- **delivery_service, neg:** “FINALLY received my package today after ordering over a month ago!!”
- **delivery_service, pos:** “Shipping was great no issues with the product”
- **hydration_skin_feel, neg:** “it does leave your skin a little oily shinny looking but that it okay”
- **hydration_skin_feel, pos:** “Keeps my lips nice and smooth and moisturized.”
- **skin_reaction, neg:** “it burns for a couple days after I apply”
- **skin_reaction, pos:** “my sensitive skin actually likes this exotic facial astringent.”
- **ingredients, neg:** “they really overlooked the synthetic fragrance”
- **ingredients, pos:** “food grade. This was unnecessarily hard to find pure”

## Classifier quality on the held-out calib sample (vs LLM labels)

| Target | AUROC | Avg precision | Calib positives |
|---|---|---|---|
| mention_efficacy | 0.879 | 0.778 | 465 |
| neg_efficacy | 0.901 | 0.596 | 147 |
| mention_skin_reaction | 0.901 | 0.463 | 53 |
| neg_skin_reaction | 0.93 | 0.469 | 21 |
| mention_hydration_skin_feel | 0.969 | 0.685 | 79 |
| neg_hydration_skin_feel | 0.899 | 0.199 | 11 |
| mention_texture | 0.872 | 0.476 | 137 |
| neg_texture | 0.847 | 0.211 | 59 |
| mention_scent | 0.986 | 0.884 | 131 |
| neg_scent | 0.97 | 0.448 | 42 |
| mention_longevity | 0.911 | 0.589 | 107 |
| neg_longevity | 0.94 | 0.477 | 46 |
| mention_colour_shade | 0.957 | 0.812 | 158 |
| neg_colour_shade | 0.952 | 0.564 | 56 |
| mention_hair_result | 0.961 | 0.785 | 166 |
| neg_hair_result | 0.941 | 0.472 | 61 |
| mention_packaging | 0.883 | 0.55 | 135 |
| neg_packaging | 0.902 | 0.425 | 70 |
| mention_size_quantity | 0.907 | 0.67 | 168 |
| neg_size_quantity | 0.932 | 0.621 | 89 |
| mention_price_value | 0.948 | 0.785 | 183 |
| neg_price_value | 0.929 | 0.493 | 71 |
| mention_authenticity_quality | 0.868 | 0.587 | 226 |
| neg_authenticity_quality | 0.882 | 0.436 | 117 |
| mention_delivery_service | 0.924 | 0.612 | 97 |
| neg_delivery_service | 0.945 | 0.501 | 41 |
| mention_ease_of_use | 0.911 | 0.76 | 274 |
| neg_ease_of_use | 0.914 | 0.516 | 104 |
| mention_ingredients | 0.968 | 0.569 | 27 |
| neg_ingredients | 0.958 | 0.085 | 7 |
| mention_overall | 0.805 | 0.871 | 934 |
| neg_overall | 0.868 | 0.541 | 195 |

Not modelled (too few training positives): ctx_skin_dry, ctx_skin_oily, ctx_skin_combination, ctx_skin_acne, ctx_skin_mature, ctx_hair_damaged.
