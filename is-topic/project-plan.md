# IS project plan: AI-native launch matching for new skincare products

> **Superseded by `refined-thesis-plan.md` (17 Oct 2026), which merges this plan with yui's research proposal.** Kept for reference.

Topic: **AI-Native Products & Operations** (การออกแบบผลิตภัณฑ์และโมเดลการทำงานที่มี AI เป็นหัวใจหลักตั้งแต่เริ่มต้น), framed by the **Reinvent Commerce** brief: help a business understand its customers and take better action.

## Research question

_Updated: the current research question and hypotheses are in the Novelty and Making-it-conference-level sections below. This one is the original launch-matching version._

> **How can an AI-native system help a retailer launch new skincare products to the customers whose needs they actually solve, before the products have reviews or popularity, and how much does this improve launch conversion and satisfaction compared with popularity-based targeting?**

> ระบบที่มี AI เป็นแกนหลักจะช่วยให้ร้านค้าเปิดตัวสินค้าสกินแคร์ใหม่ไปยังลูกค้าที่สินค้าแก้ปัญหาให้ได้จริง ตั้งแต่ก่อนมีรีวิวหรือความนิยมได้อย่างไร และเพิ่ม conversion และความพึงพอใจได้มากแค่ไหนเมื่อเทียบกับการเลือกกลุ่มเป้าหมายตามความนิยม

Sub-questions:
1. What needs (skin type, concern, sensitivities) can AI reliably extract from customers' past reviews and from a new product's catalogue text?
2. Does need-based matching rank customers who end up satisfied higher than popularity-based or plain-similarity targeting does?
3. Which merchant actions (who to target, what message to send, which promotion to run) does the match support, and what's their estimated effect on conversion and returns?

## The product: "Launch Match"

A merchant-side tool for when a retailer adds a new skincare product with no reviews yet:

1. **Catalogue enrichment.** AI reads the product's title, features and description and tags it with structured attributes: skin types, concerns treated, key ingredients, exclusions (fragrance, alcohol).
2. **Customer need profiles.** AI reads each customer's past reviews of *other* products and extracts their skin type, concerns, what worked and what irritated them.
3. **Matching and scoring.** A scoring model (not the LLM) predicts each customer's probability of a satisfied purchase from need–attribute overlap features.
4. **Actions.** For the top-scored customers, the tool produces:
   - a launch target list (who gets the launch email or ad)
   - a personalised message that leads with *their* problem ("for oily, acne-prone skin…")
   - a promotion suggestion: sampling or a discount for high-fit, low-certainty customers instead of a blanket discount
   - a "do not target" list of customers likely to be irritated (e.g. fragrance-sensitive), which cuts returns and bad first reviews

**Why it's AI-native and not an AI feature:** the merchant's launch *workflow* is built around the AI. Enrichment, segmentation, messaging and the target list are produced by the system from day one, replacing the old "launch to best-sellers' buyers and wait for reviews" process. Without the AI, the operating model doesn't exist. That's the AI-Native Products & Operations angle.

## How it meets the brief

| Brief criterion | How this project meets it |
|---|---|
| **Disconnected data sources** | Joins product data (item metadata), transactions (verified purchases) and reviews into one customer-need ↔ product-attribute view. Support conversations and marketing results aren't in the dataset, so state that as a limitation (or simulate a small marketing-result log in the demo). |
| **Attract / serve / convert / retain** | Mainly *convert* (the right first buyers) and *retain* (fewer bad-fit purchases and returns). It also *attracts* through personalised launch messages. |
| **Idea categories used** | Product discovery and recommendations, catalogue enrichment, review and sentiment analysis, promotion planning. |
| **Real merchant problem** | New products have no reviews, so retailers fall back on broad promotion and best-seller audiences. That wastes ad spend, and early bad-fit buyers leave bad reviews that sink the launch. |
| **Useful commercial action** | A target list, a message per segment, a promotion type, and an exclusion list. |
| **Relevant personalisation** | Messages and targeting are based on each customer's own stated skin needs, not on demographics or popularity. |
| **Measurable effect** | Conversion and satisfaction (see metrics below), with a simple revenue/margin simulation. |
| **"Explain how the prediction was calculated; no LLM-only forecasting"** | The LLM only *extracts* attributes and needs. The prediction comes from a **logistic regression (or gradient-boosted trees)** on interpretable features: need–attribute overlap, ingredient conflicts, the customer's past rating behaviour, and price fit relative to their history. It's trained on historical launches and explained with feature weights / SHAP. |

## Data: Amazon Reviews 2023, Beauty_and_Personal_Care, skincare subset

- Use the **raw (0-core)** files, not 5-core, because 5-core removes new products.
- **Time split:** cutoff date T. "New products" are those whose first review comes after T.
- **Customers:** at least 3 reviews before T (needs profile) and at least 1 purchase of a new product after T.
- **Matcher inputs:** new product's metadata with brand/store masked; customer's reviews from before T. **Excluded:** the new product's ratings, rating count and reviews.
- **Ground truth ("satisfied purchase"):** verified purchase after T, rating of 4 or more, and review text confirming their need was addressed (LLM judge, checked by hand on a sample).
- **Training the scorer:** use launches from an earlier window (before T) as training data, then test on launches after T.

## Evaluation and business metrics

Compare three targeting strategies for each new product:
1. **Popularity:** target buyers of the category's best-sellers (the current default)
2. **Text similarity:** embedding similarity between product text and the customer's history
3. **Launch Match:** need extraction plus the explainable scoring model

| Metric | What it shows | Business meaning |
|---|---|---|
| Hit rate / precision@K of satisfied buyers in the top-K target list | Are the right people being targeted? | **Conversion** of the launch campaign |
| Share of targeted buyers who rated ≤2 stars | Bad-fit targeting | **Returns, refunds, early bad reviews** (service quality, margin) |
| Simulated launch revenue for a fixed budget of K contacts × assumed conversion × price | Money impact | **Revenue / marketing ROI** |
| Coverage of new products with zero prior reviews | Does it work when nothing is known? | Cold-start capability |

Report results like: *"With the same 1,000-contact budget, Launch Match reached X% more satisfied buyers and Y% fewer bad-fit buyers than popularity targeting."*

## Demo (what to show)

1. A merchant uploads a new serum with no reviews. The tool shows the extracted attributes ("oily/combination skin, acne, contains niacinamide, fragrance-free").
2. It shows the top 20 matched customers, each with the *reason* ("past reviews mention hormonal breakouts; liked other niacinamide products") and the score breakdown from the model.
3. It shows the exclusion list ("dry, sensitive skin; past reviews complain about drying acids").
4. It generates a personalised launch message for one segment, plus a promotion suggestion.
5. It ends on a results panel: back-tested precision, bad-fit rate and simulated revenue for Launch Match vs. popularity targeting.

A simple Streamlit or web app over a pre-computed subset is enough.

## Scope and risks

- **Size:** sample a few hundred new products and 1–2k customers. Don't process the full category.
- **LLM brand leakage:** mask brand and store names. Report any remaining effect as a limitation.
- **Selection bias:** you only see people who bought, not people who would have been satisfied but never found the product. Frame precision as measured among actual buyers.
- **Missing data types:** there are no support chats or campaign logs. Say so, and describe how they'd plug in (e.g. support chats as another source of need statements).
- **Generalisability:** the data is US Amazon up to 2023. Discuss how the approach transfers to Thai marketplaces (Shopee/Lazada) and D2C brands.

## Suggested chapter outline

1. Introduction: the cold-start launch problem and AI-native operations
2. Literature: product-market fit and signalling; recommender cold start (content/knowledge-based); LLMs for attribute extraction; AI-native operating models
3. Method: design science; data, split, features, scoring model, baselines
4. System design: Launch Match architecture and merchant workflow
5. Results: offline evaluation and business simulation
6. Discussion: implications for merchants and new brands; limitations
7. Conclusion

## Novelty (aligned with literature-review.md §5)

The literature review (`literature-review.md`) found three papers closer to this idea than earlier versions of this plan assumed. The novelty claims below follow its §5 revised statement. If the two files ever differ, **literature-review.md is the reference**.

### Closest prior work
- **Fainmesser, Lauga & Ofek (2021, Management Science):** in theory, firms do better by advertising to a narrower, well-matched group so that first-generation ratings are higher. → The core intuition of fit-first seeding already exists *as theory*.
- **Park, Shin & Xie (2021, Marketing Science):** a product's first review has lasting effects on later review valence and volume. → Early-review path dependence is documented.
- **Wang et al. (2025, Google):** item-centric recommendation that selects the best users for new items, optimising engagement. → Choosing an audience for a new item exists in AI.
- Also related: LLMs for cold-start items (Wang et al. 2024), review-based user profiles, BLaIR on Amazon Reviews 2023, and skincare recommenders. See `literature-review.md` §5.1 for the full comparison table.

### What's new, by field (revised)
- **Marketing (moderate to high).** The contribution is **empirical and operational**: measuring individual first-buyer need fit from text, testing whether it predicts the review trajectory, and comparing need-fit seeding with popularity seeding. It empirically tests and operationalises what Fainmesser et al. modelled in theory.
- **Entrepreneurship (high, the cleanest claim).** No study found frames first-customer selection as a substitute for costly legitimacy signals under the liability of newness, or tests whether early fit matters more for small or new brands.
- **AI / IS (moderate to high).** Compared with Wang et al. (2025), the new parts are the **objective** (downstream reputation, not immediate engagement), the **do-not-target** output (contraindications), the explainable **LLM-extraction + interpretable-scoring** split, and the **closed-loop launch process** in commerce.

### Novelty statement (use this wording)
> Prior research shows that a product's first reviews have lasting consequences (Park et al., 2021), that firms in theory benefit from targeting better-matched early buyers (Fainmesser et al., 2021), and that recommender systems can select audiences for new items (Wang et al., 2025). No study has measured the need fit of a new product's first buyers from what they say they need, tested whether that fit predicts the product's review trajectory, or built a system that selects first buyers to protect it. This thesis does all three, and tests whether the effect is strongest for small, unknown brands facing a liability of newness.

### Research question (current)
> Does the need fit of a new product's first buyers predict its long-term rating and review trajectory, and can an AI-native system that seeds launches with need-matched buyers improve launch outcomes, especially for small, unknown brands?

### Three contributions (unchanged in substance)
1. **Empirical finding:** first-buyer need fit (and contraindication share) vs. 6–12-month rating and review volume on Amazon Reviews 2023 skincare (H1–H3).
2. **AI-native artifact:** Launch Match, a closed-loop seeding agent: seed best-fit customers, read early reviews, update the target profile, re-target (H4–H5).
3. **Evaluation:** replayed and simulated launches comparing popularity, similarity, one-shot need-fit and closed-loop seeding, calibrated with Study 1 estimates.

### Caveats
- Study 1 is observational: self-selection (good products attracting better-fit buyers) is the main threat. Use within-brand comparisons, attribute and price controls, the contraindication signal (H2), and the sales-event natural experiment below.
- Amazon's own recommendations shaped historical purchases (a feedback loop), so report this as a limitation.
- Simulation results depend on assumptions: calibrate them with H1 estimates and report sensitivity ranges.
- Don't use "free samples to anyone" as a baseline; incentivised early reviews are known to be biased.

## Making it conference-level

**Target:** PACIS or HICSS (realistic), with ICIS or ECIS as a stretch. These venues expect: a clear theory-based hypothesis, a credible empirical method, a well-evaluated artifact, and stated implications. Below is what to add to the current plan.

### 1. State formal hypotheses (theory first)
Use the five hypotheses from `literature-review.md` §5.3:
- **H1 (marketing):** the average need fit of a new product's first *k* buyers is positively associated with its average rating and review volume 6–12 months after launch, controlling for price, category, product attributes and brand size.
- **H2 (marketing):** a higher share of *contraindicated* first buyers (e.g. fragrance-sensitive customers buying a fragranced product) is associated with lower early ratings, more strongly than general mismatch.
- **H3 (entrepreneurship):** the H1 association is stronger for small or new brands than for established brands (liability of newness).
- **H4 (AI / IS):** in replayed launches, need-fit seeding reaches more need-confirmed satisfied buyers and fewer bad-fit buyers than popularity or plain-similarity seeding at the same contact budget, and yields a higher projected early rating.
- **H5 (AI / IS):** a closed-loop policy that updates the target profile from early reviews outperforms one-shot need-fit seeding.

Theory anchors: self-selection and rating dynamics (Li & Hitt 2008; Godes & Silva 2012), path dependence (Muchnik et al. 2013; Park et al. 2021), liability of newness and legitimacy (Stinchcombe 1965; Zimmerman & Zeitz 2002).

Reviewers like seeing named hypotheses tied to named theories.

### 2. Stronger causal evidence (the biggest upgrade)
Plain regression will get the comment "good products just attract good buyers." Add at least one of these:
- **Natural experiment via sales events.** Products whose first reviews arrive during big sales (Prime Day, Black Friday) get a broader, less-targeted wave of early buyers, which means lower fit for reasons unrelated to product quality. Compare similar products launched just before a sale vs. at quieter times (difference-in-differences or matching). This is the strongest design you can do with this data.
- **Within-brand comparison:** compare products from the same brand (fixed effects) to remove brand quality.
- **Matching on product attributes:** propensity-score match products on price, category, ingredients and description quality, then compare early-fit high vs. low.
- **Placebo test:** show that early fit does *not* predict things it shouldn't (e.g. a product's price changes).

### 3. Validate the AI components
- **Measure extraction accuracy:** hand-label ~200 reviews for skin type and concern, and ~100 products for attributes, and report the LLM's precision/recall. Use two coders and report inter-rater agreement (Cohen's kappa).
- **Ablation:** show what each part adds (needs only, attributes only, with/without the do-not-target rule, with/without the feedback loop).
- **Brand-leakage test:** run with brand names masked vs. visible, and report the difference.

### 4. Strong baselines
Popularity; item-to-item collaborative filtering; text embeddings (BLaIR, built for this dataset); and a zero-shot LLM ranker. Beating all four is what a RecSys or IS reviewer expects.

### 5. Optional, but it lifts it to top-tier: a small real-world test
Partner with a Thai indie skincare brand or a Shopee/LINE shop. At the next product launch, split the customer list in two: popularity/broad targeting vs. Launch Match targeting. Measure click-through, purchase and early review score. Even ~500–1,000 customers is publishable as a field pilot. If this isn't feasible, the sales-event natural experiment is the fallback.

### 6. Rigor and reproducibility
- Pre-register the hypotheses and analysis plan (e.g. on OSF) before running the main regression.
- Release code and the processed subset (the dataset licence allows research use; check the terms).
- Report robustness checks: different cutoff dates, first-10 vs. first-20 reviewers, other categories (a Health_and_Household replication strengthens generalisability).

### Paper structure (8–10 pages for PACIS/HICSS)
1. Introduction: the launch cold-start problem and the fit-first seeding idea
2. Theory and hypotheses (seeding, early-review bias, liability of newness, AI-native operations)
3. Study 1: empirical test of H1–H3 on Amazon Reviews 2023 (with the natural experiment)
4. Study 2: design and evaluation of the Launch Match artifact (H4–H5, ablations, baselines)
5. (Optional) Study 3: field pilot with a Thai brand
6. Discussion: contributions to marketing, entrepreneurship and IS/AI; managerial implications; limitations

### Timeline guide
| Weeks | Work |
|---|---|
| 1–2 | Literature review, hypotheses, data pipeline, sample selection |
| 3–4 | LLM extraction + hand-labelled validation |
| 5–6 | Study 1 regressions + natural experiment |
| 7–8 | Study 2 artifact, baselines, ablations, simulation |
| 9–10 | Demo, write-up, robustness checks |
| (parallel) | Field pilot outreach to a brand |

Check the PACIS and HICSS submission deadlines and page limits on their websites and plan backwards from them.
