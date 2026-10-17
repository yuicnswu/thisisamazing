# IS topic comparison

**Topic A:** How can a new product find the customers it genuinely serves before it has reviews, popularity, or an established brand? (the "cold-start" customer discovery problem)

**Topic B:** AI-Native Products & Operations: การออกแบบผลิตภัณฑ์และโมเดลการทำงานที่มี AI เป็นหัวใจหลักตั้งแต่เริ่มต้น ไม่ใช่แค่การนำ AI มาใส่เป็นเพียงฟีเจอร์เสริม

## Recommendation

**Go with Topic A, and use AI as the lens inside it.** A is a real, sharp question with a clear "before vs. after" a researcher can observe. B is a trend label, not yet a question. It's interesting, but it's broad, the literature is moving every month, and it's hard to get data on "operating models" as a student.

The strongest version is a combination:

> **How can AI-native go-to-market methods help a new product find the customers it genuinely serves before it has reviews, popularity, or brand?**

This keeps A's focused question and B's novelty, and it scopes "AI-native" down to one thing you can actually study (customer discovery and matching) instead of a whole company's operating model.

## Side by side

| | Topic A: cold-start customer fit | Topic B: AI-native products & ops |
|---|---|---|
| Is it a question? | Yes, already phrased as one | No, it's a theme; needs narrowing first |
| Focus | Narrow: one stage (pre-traction) and one problem (finding the right customers) | Wide: product design + org design + operations |
| Novelty | Classic problem (cold start, signaling, product-market fit), so novelty must come from the angle (e.g. the AI era, a specific market like Thai SMEs/D2C) | High novelty, but much of it is hype; hard to separate signal from marketing |
| Literature | Solid base: product-market fit, Lean Startup / customer development, signaling theory, information asymmetry, recommender cold-start, diffusion of innovations | Thin and fast-changing: mostly practitioner essays, consultancy reports, very recent papers |
| Data access | Good: interview founders, run small experiments (landing pages, ads, communities), case studies of launches | Hard: companies rarely share internal operating models; risk of relying on vendor claims |
| Doable as a student project | Yes, can even run a live mini-experiment with a real or mock product | Harder; risks becoming a literature review or opinion piece |
| Biggest risk | Ending up as generic "marketing tips" if you don't define "genuinely serves" and measure it | Too broad, outdated by the time you submit, no clear finding |

## What each could look like

### Topic A
- **Research question:** What signals and channels let a new product reach customers with genuine fit (high retention / problem match) without relying on social proof?
- **Sub-questions:** How do early-stage founders find their first true-fit customers? Which substitutes for reviews (demos, guarantees, founder credibility, niche communities, free trials) actually work, and for whom?
- **Method options:**
  1. Qualitative: 10–15 founder interviews (Thai startups / SMEs / D2C brands), coded into a framework.
  2. Multiple case study: 3–5 product launches, comparing how first customers were found.
  3. Field experiment: same product, different pre-reputation signals (guarantee vs. demo vs. founder story) via landing page or small ad test; measure sign-up and fit.
- **Output:** A framework or playbook ("cold-start fit model") validated with evidence.
- **Define early:** what "genuinely serves" means (e.g. retained after 30 days, problem-solution match score, would-be-very-disappointed test).

### Topic B
- **Must narrow first.** e.g. "How do AI-native startups differ from AI-added incumbents in team structure and unit economics?" or "What design principles distinguish AI-native products?"
- **Method options:** case studies of a few AI-native companies (public info + interviews), or a design-framework paper built from cases.
- **Output:** A typology or set of design principles.
- **Risk:** without inside access, findings lean on public claims; hard to defend rigor.

### Combined (recommended)
- **Research question:** Can AI-native discovery methods (AI-driven segmentation, synthetic-persona testing, AI-personalized outreach, AI matchmaking/recommendation) find true-fit customers for a product with no reputation better than traditional cold-start methods?
- **Method:** small comparative experiment or case study. Run one traditional approach and one AI-native approach for the same product, and compare reach, conversion and fit quality. Back it with founder interviews.
- **Why it's stronger:** a focused question from A, a timely angle from B, and a measurable outcome.

## Next step
Pick the version (A alone, or combined), then pin down: the product/market you'll study, your definition of "genuine fit," and which method you can actually get data for. Those three decide whether the IS is finishable.

---

## Update: assessing yui's new research question

> **How can an AI-native system match new products with customers whose needs they demonstrably satisfy, without relying on reviews, popularity, or brand recognition?**
> ระบบที่ออกแบบโดยมี AI เป็นแกนหลัก จะจับคู่สินค้าใหม่กับลูกค้าที่สินค้าแก้ปัญหาให้ได้จริงอย่างไร โดยไม่พึ่งรีวิว ความนิยม หรือชื่อเสียงของแบรนด์?

**Verdict: this is a better question than either original.** It keeps topic A's focused problem (cold start) and turns topic B from a vague theme into one concrete thing: a matching system. It also points toward a clear method. You design a matcher and test whether it beats popularity-based matching.

### What's strong
- One clear problem, one clear mechanism (matching), one clear constraint (no social proof).
- It suits **design science research**: build an artifact (a prototype matcher), then evaluate it. Many IS programmes accept this method and are familiar with it.
- It links to established literature: recommender-system cold start, content-based and knowledge-based recommendation, jobs-to-be-done (needs over popularity), and signaling theory.

### What needs sharpening
1. **"AI-native system" is undefined.** Say what makes it AI-native. For example, an LLM reads the customer's stated problem and the product's description and matches on need, rather than relying on purchase history or ratings. Otherwise a reader can't tell it apart from a normal recommender.
2. **"Demonstrably satisfy" needs a measurable definition.** Pick one: the user rates the match as solving their problem, they would buy or try it, they still use it after 30 days, or an expert judges the problem–product fit. This is the single most important decision. It decides your evaluation.
3. **"Without relying on" is too absolute.** Rephrase it as "without using reviews, popularity or brand *as inputs*". That's testable: the system simply doesn't see those signals.
4. **"How can" is open-ended.** Pair it with an evaluative sub-question, so you have a finding and not only a design.
5. **No context yet.** Choose one market or category (e.g. Thai SMEs or D2C brands, skincare, SaaS tools for small businesses). A general version is too big for an IS.

### Sharpened version (suggested)

> **RQ:** How can an LLM-based, need-matching system connect new products with customers whose stated problems they solve, using only product information and customer needs (no reviews, popularity or brand signals), in [chosen category]?
>
> **SQ1:** What product and customer information does such a system need to infer problem–solution fit?
> **SQ2:** How does its match quality compare with a popularity-based baseline, judged by [chosen fit measure]?
> **SQ3:** Under what conditions does need-based matching fail (e.g. vague needs, crowded categories)?

### Method sketch
1. Pick a category and collect ~20–50 products, including some new or unknown ones, with their descriptions.
2. Gather real customer needs: a short survey or interviews where people describe a problem in their own words.
3. Build a simple prototype: an LLM prompt or pipeline that matches needs to products using only descriptions and needs.
4. Evaluate it against a baseline (best-sellers or most-reviewed). Participants or experts rate which matches actually solve their problem.
5. Add a few founder or marketer interviews on how new products currently find customers, so the findings have practical context.

### Risks
- **Building can eat the timeline.** Keep the prototype minimal (prompts plus a spreadsheet is enough); the evaluation is the contribution.
- **Small sample size.** Frame the results as exploratory or proof-of-concept.
- **LLM bias:** the model may still favour well-known brands it has seen in training. Blind the brand names during testing and report this as a limitation. This bias is itself an interesting finding.

---

## Dataset choice: Amazon Reviews 2023

Source: https://amazon-reviews-2023.github.io/ (McAuley Lab, UCSD). It has 33 categories. Each one has a **reviews** file (rating, title, text, user, timestamp, verified purchase, helpful votes) and an **item metadata** file (title, features, description, details, price, store/brand, average rating, rating count). The page itself couldn't be opened from this environment, so check the category sizes on the site before relying on them.

### Recommendation: **Beauty_and_Personal_Care**, narrowed to skincare

Why this category:
- **Customers state their needs in plain words.** Skincare reviews routinely describe the problem: "dry, sensitive skin", "hormonal acne", "dark spots". That's exactly what a need-based matcher needs, and what a judge needs to check whether the product solved it.
- **The cold-start problem is real here.** New indie brands launch constantly, and buyers lean heavily on reviews and influencers. Cold-start matching has direct business value: fewer failed launches, fewer returns, less ad spend wasted on the wrong audience.
- **It's relevant to Thailand.** Beauty and skincare is one of the biggest SME and D2C categories in Thailand, so the findings translate into practical recommendations.
- **Item metadata is rich.** Ingredients, skin type and claims usually appear in the features and description fields, so the matcher has enough to work with without reviews.

Fallbacks: **Health_and_Household** (similar need-driven buying, e.g. sleep or joint pain) or **Pet_Supplies** (needs like "picky eater" or "sensitive stomach" are clear in review text). Use **All_Beauty** only for a quick pilot, because it is small.

### Use the raw (0-core) data, not 5-core
5-core keeps only items and users with at least 5 reviews, which **removes exactly the new, unknown products you're studying**. Use the raw files and build your own subset. Use a **timestamp split**, not leave-last-out, so you can simulate "the product has just launched."

### Resolving the "no reviews" tension
The matcher must not use reviews or popularity *about the new product*. The dataset's reviews play other roles:

| Data | Role | Allowed as matcher input? |
|---|---|---|
| New item's metadata (title, features, description) | Product side of the match | ✅ Yes, with brand/store masked |
| New item's `average_rating`, `rating_number`, its reviews | Popularity / social proof | ❌ No, drop these columns |
| Customer's **earlier** reviews of *other* products (before the cutoff) | Customer's stated needs ("my oily skin…") | ✅ Yes, this is the need profile |
| Customer's **later** review of the new item | Ground truth: did it actually solve their need? | ❌ Evaluation only |

So the reviews give you two things: the customer's needs (from their history) and the evidence of satisfaction (from what happened after launch). They never act as social proof for the new product.

### Defining "demonstrably satisfied"
A match counts as successful when the customer later bought the item (**verified purchase**), rated it **≥4 stars**, **and** the review text says it addressed the need in their profile. An LLM judge or human coder checks the last part on a sample. Rating alone is too weak.

### Evaluation design
1. Choose a cutoff date, e.g. 1 Jan 2022. **Cold items** are skincare items whose first review comes after the cutoff.
2. **Users:** people with at least 3 reviews before the cutoff (enough to infer needs) and at least 1 review of a cold item after it.
3. For each user, rank a candidate set (the true cold item plus ~99 other cold items) using:
   - **Your matcher:** LLM needs-profile → masked product metadata
   - **Baseline 1, popularity:** best-sellers before the cutoff (shows why popularity fails for new items)
   - **Baseline 2, embedding similarity:** plain text similarity, no LLM reasoning
4. Measure hit rate / NDCG@10 against items the user was satisfied with, and break the results down by need type.
5. Size it for an IS: a few hundred cold items and 1–2k users is enough. Sample down; don't process the whole category.

### Business-impact framing
Report the results as what a new brand gains: "need-based matching put the right customers in the top 10 X% of the time, vs Y% for popularity." Then translate that into launch decisions such as targeting, messaging (lead with the problem solved) and where to place the product.

### Caveats to state
- Reviews only come from people who bought, so you can't observe customers who would have been satisfied but never found the product (selection bias).
- LLMs may recognise big brands from training data, so mask brand and store names, and treat any remaining leakage as a limitation.
- The dataset ends in 2023 and is US Amazon data, so be careful about generalising to Thai platforms like Shopee or Lazada.
