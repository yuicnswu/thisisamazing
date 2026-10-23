# Literature Review: Before the First Review

*Evidence-grounded matching of new products to the customers they genuinely serve. Companion to [refined-thesis-plan.md](refined-thesis-plan.md) and yui's research proposal. Revised 17 October 2026.*

---

## How to read this document

- **Two papers, one thesis.** The thesis now has two outputs (see the refined plan):
  - **Paper A (NeurIPS 2027, AI method):** do AI recommenders match new products on listing *evidence* or on *priors*, and can a matcher recommend only on evidence, abstain otherwise, and bound the unsupported recommendation rate (URR ≤ α)? Categories: Appliances, Home & Kitchen, Tools & Home Improvement.
  - **Paper B (PACIS / HICSS, business outcome):** does evidence-supported fit among a new product's first buyers shape its review trajectory, and does this matter most for small, unknown brands?
- **Structure.** Part I reviews the literature for Paper A. Part II reviews the literature for Paper B. Part III links them into one thesis framework. Each part ends with a gap statement and a draft related-work section in conference style.
- **Verification.** Every reference was checked to exist (title, authors, venue, year) against a publisher page, DOI record, arXiv, ACL Anthology, PMLR, IDEAS/RePEc or an institutional repository. Details filled from memory (usually pages or issue numbers) are marked **[check details]**. Findings are taken from abstracts unless noted, so read the closest papers in full before quoting numbers.
- **Running example (from the proposal).** A new listing reads "Compact Bathroom Storage Cabinet, White", gives height 80 cm and MDF, but no width. For the need "white bathroom cabinet under 60 cm wide", the right answer is *cannot tell yet: add a width*. A prior-driven model says *yes* because similar cabinets usually fit.

---

# Key surveys to start from

*Added 17 October 2026. These are verified surveys closest to the thesis, to read first. Each one gives a map of a field the thesis draws on. **None of them covers our exact gap:** no survey treats recommendation decisions for new products that must be supported by listing evidence, with abstention and a bound on unsupported decisions.*

| Area | Survey | What it covers | What it leaves for us |
|---|---|---|---|
| LLMs for recommendation | Zhao et al. (2024), *IEEE TKDE*; Wu et al. (2024), *World Wide Web* | How LLMs are used in recommenders: pre-training, fine-tuning and prompting | Accuracy-focused. Nothing on whether recommendations are supported by item evidence. |
| Cold-start recommendation | Zhang et al. (2025), arXiv 2501.01945 | Cold-start methods, from content features and graphs to the "world knowledge" of LLMs | Treats LLM world knowledge as the *solution* to cold start. Paper A asks when that knowledge is a prior that licenses unsupported matches. |
| Trustworthy LLM recommendation | Wang et al. (2026), arXiv 2606.00540 | Over 200 studies on robustness, bias, explainability, factuality, controllability and privacy, including grounding and hallucination | **Closest survey.** It treats factuality as avoiding fictional items, and robustness as resisting attacks. In the visible text I found no abstention and no guarantee on support. Cite it as the field map Paper A extends. |
| Robust recommenders | Zhang et al. (2023/2025), arXiv 2309.02057 | Attacks (for example fake users) and natural noise in classic recommenders | Pre-LLM. Covers data poisoning, not missing or misleading listing text. |
| Knowledge conflicts | Xu et al. (2024), EMNLP | Context–memory, inter-context and intra-memory conflicts in LLMs | QA and generation only. No recommendation, and missing evidence is not a separate case. |
| Hallucination | Zhang et al. (2025), *Computational Linguistics* | Types, causes, detection and mitigation of LLM hallucination | General. Paper A's "unsupported recommendation" is a decision-level form of hallucination. |
| Abstention | Wen et al. (2025), *TACL* | When and how LLMs abstain, from the angle of the query, the model or human values; methods, benchmarks and metrics | No recommendation setting and no distribution-free guarantee. |
| Uncertainty in LLMs | Shorinwa et al. (2024/2025), arXiv 2412.05563 | A taxonomy of LLM uncertainty quantification methods and their applications | Uncertainty is about confidence. Paper A's Separation result shows that confidence is not support. |
| Conformal prediction in NLP | Campos et al. (2024), *TACL* | Conformal methods, their guarantees, and NLP applications, including hallucination risk | No conjunctive decision guarantee, and no recommendation. |
| Electronic word of mouth (marketing) | Babić Rosario et al. (2016), *JMR* | Meta-analysis of 96 studies: eWOM correlates with sales, and the effect depends on platform, product and metric (volume matters more than valence) | No study of who writes the first reviews, or whether those reviewers' needs fit the product (Paper B). |
| Seeding (marketing) | Haenlein & Libai (2017), *California Management Review* | Seeding, referral and recommendation programmes | Judges seeding by reach, not by the reviews seeded customers write (Paper B). |

**Should the thesis be a survey paper instead?** I don't recommend it as the main output. Wang et al. (2026) already maps trustworthy LLM recommendation broadly. A survey would also not be accepted at NeurIPS, which wants Paper A's method and theory. A *narrow* systematic review would be viable as a side paper for PACIS, which accepts literature reviews. Its topic would be evidence, priors and abstention in recommending new products, and it would reuse this document.

**Survey references**

- Babić Rosario, A., Sotgiu, F., De Valck, K., & Bijmolt, T. H. A. (2016). The effect of electronic word of mouth on sales: A meta-analytic review of platform, product, and metric factors. *Journal of Marketing Research, 53*(3), 297–318. https://doi.org/10.1509/jmr.14.0380 ✔
- Campos, M., Farinhas, A., Zerva, C., Figueiredo, M. A. T., & Martins, A. F. T. (2024). Conformal prediction for natural language processing: A survey. *Transactions of the Association for Computational Linguistics, 12*, 1497–1516. https://doi.org/10.1162/tacl_a_00715 ✔
- Shorinwa, O., Mei, Z., Lidard, J., Ren, A. Z., & Majumdar, A. (2024). *A survey on uncertainty quantification of large language models: Taxonomy, open research challenges, and future directions* (arXiv:2412.05563). ✔ **[check details: published venue]**
- Wang, B., Cui, Y., Xu, Z., Zhao, J., Fan, C., Zhang, J., Yang, W., Zhang, S., Chen, S., Zhang, Y., Zhao, X., Wang, W., Gao, C., Feng, F., He, X., & Chen, J. (2026). *Trustworthy recommendation in the era of large language models: Opportunities and challenges* (arXiv:2606.00540). ✔
- Wen, B., Yao, J., Feng, S., Xu, C., Tsvetkov, Y., Howe, B., & Wang, L. L. (2025). Know your limits: A survey of abstention in large language models. *Transactions of the Association for Computational Linguistics, 13*, 529–556. ✔
- Zhang, K., Cao, Q., Sun, F., Wu, Y., Tao, S., Shen, H., & Cheng, X. (2023). *Robust recommender system: A survey and future directions* (arXiv:2309.02057; ACM DOI 10.1145/3757057). ✔ **[check details: journal]**
- Zhang, W., Bei, Y., Yang, L., Zou, H. P., Zhou, P., Liu, A., Li, Y., Chen, H., Wang, J., Wang, Y., Huang, F., Zhou, S., Bu, J., Lin, A., Caverlee, J., Karray, F., King, I., & Yu, P. S. (2025). *Cold-start recommendation towards the era of large language models (LLMs): A comprehensive survey and roadmap* (arXiv:2501.01945). ✔
- Zhang, Y., Li, Y., Cui, L., Cai, D., Liu, L., Fu, T., Huang, X., Zhao, E., Zhang, Y., Chen, Y., Wang, L., Luu, A. T., Bi, W., Shi, F., & Shi, S. (2025). Siren's song in the AI ocean: A survey on hallucination in large language models. *Computational Linguistics, 51*(4), 1374–1404. https://doi.org/10.1162/COLI.a.16 ✔
- Zhao, Z., Fan, W., Li, J., Liu, Y., Mei, X., Wang, Y., Wen, Z., Wang, F., Zhao, X., Tang, J., & Li, Q. (2024). Recommender systems in the era of large language models (LLMs). *IEEE Transactions on Knowledge and Data Engineering, 36*(11), 6889–6907. ✔
- Also in the main references: Wu et al. (2024), Xu et al. (2024), Haenlein & Libai (2017).

---

# Part I. Paper A: evidence-grounded matching with abstention and a support guarantee

## 1. New products in recommender systems

### 1.1 Why new products are disadvantaged

Classic collaborative filtering recommends from purchases and ratings, so items with no history are invisible (Schein, Popescul, Ungar & Pennock, 2002). Recommenders can also reduce aggregate sales diversity by reinforcing what is already popular (Fleder & Hosanagar, 2009; Abdollahpouri, Burke & Mobasher, 2017). Reviews drive sales (Chevalier & Mayzlin, 2006), and for new products negative reviews weigh more than positive ones (Cui, Lui & Guo, 2012). A product's *first* review shifts its rating and review volume for up to three years (Park, Shin & Xie, 2021). A wrong early match is therefore costly to the new product itself, not only to the shopper: misfit buyers return the product and leave the first bad reviews.

### 1.2 How current systems handle new items

- **Content and hybrid models** use item attributes to score items with no interactions (Burke, 2002; Volkovs, Yu & Poutanen, 2017).
- **Text-based sequential recommenders** represent items by their text so that new items can be placed near similar known items: UniSRec (Hou et al., 2022), Recformer (Li et al., 2023) and LLM2Rec (He et al., 2025). **Generative retrieval** recommenders such as TIGER (Rajput et al., 2023) and ETEGRec (Liu et al., 2025) assign items semantic IDs derived from content.
- **LLM recommenders** rank or generate items from natural-language descriptions (Geng et al., 2022; Hou et al., 2024b; Wu et al., 2024). They are competitive in near-cold-start settings (Sanner et al., 2023) and can generate training signal for cold-start items (Wang et al., 2024). Recent evidence is sobering, though: in cold-start and long-tail settings, LLM rerankers do not consistently beat strong baselines, and retrieval often fails to put the new item in the candidate pool at all (Dong et al., 2026). LLM recommenders also rely heavily on memorised item transitions (Kim et al., 2026).
- **Item-centric audience selection** chooses users for a new item rather than items for a user (Wang et al., 2025; Lan et al., 2025; Ma et al., 2016).

**What this means for Paper A.** All of these place a new item by *similarity* to known items or users. Similarity is a prior: the cabinet is recommended because similar cabinets fit, not because its listing says it fits. None of these methods checks whether the listing's evidence supports a specific need, and none abstains when it does not.

### 1.3 Amazon Reviews 2023 as a research resource

Hou et al. (2026; arXiv 2024) released Amazon Reviews 2023 (over 570 million reviews, 48 million items, 33 categories) with BLaIR, a family of models that connect item metadata with review language. Work on the dataset has focused on next-item and generative recommendation (e.g. LLM2Rec, ETEGRec). **We found no work** that uses the `details` specification fields as hidden ground truth for evidence support, or post-launch reviews as validation of launch-time matches. The phrasing matters: the proposal's "never use" should be softened to "we found no work that…".

## 2. Evidence versus memory in language models

### 2.1 Knowledge conflicts

Language models store facts in their parameters (Petroni et al., 2019) and often prefer that memory to the context they are given. Longpre et al. (2021) substituted entities in reading-comprehension passages and found that QA models frequently answer from memory rather than the edited context, a behaviour they call over-reliance on parametric knowledge. Xie et al. (2024) found that LLMs are receptive to coherent counter-memory evidence, but show strong confirmation bias when evidence is mixed. Xu et al. (2024) survey context–memory, inter-context and intra-memory conflicts. The proposal's notion of **prior licensing** (a decision that would stay the same if the supporting evidence were removed) is a recommendation-specific form of context–memory conflict, with one important difference: the problem is often *absent* evidence, not *contradicting* evidence.

### 2.2 Making models follow context

- **Decoding.** Context-aware decoding (Shi et al., 2024) contrasts output probabilities with and without the context to amplify what the context says.
- **Prompting.** Context-faithful prompting (Zhou et al., 2023) uses opinion-style prompts and counterfactual demonstrations.
- **Training.** CANOE (Si et al., 2026) trains contextual faithfulness with synthetic tasks and reinforcement learning. Counterfactually augmented data (Kaushik, Hovy & Lipton, 2020) teaches models "the difference that makes a difference", which is the idea behind the proposal's evidence-sensitivity loss.
- **Benchmarks.** FaithEval (Ming et al., 2024) tests faithfulness when the context is unanswerable, inconsistent or counterfactual, and finds that even leading models often fail. Mo et al. (2026) show the opposite risk: models can follow fabricated medical evidence too readily. Faithfulness is therefore not "always follow the context" but "follow it when it supports the claim, and say so when it does not".

### 2.3 Attribution and support

The decision rule in Paper A needs a notion of *support*. Rashkin et al. (2023) define **Attributable to Identified Sources (AIS)**: a statement is attributable if a generic reader would agree that the source supports it. Gao et al. (2023) evaluate whether LLM citations actually support the generated statements (ALCE). These works judge support for generated *text*; Paper A applies the same idea to a *decision* over a conjunction of constraints, with four statuses (entailed, contradicted, unresolved, conflicting).

### 2.4 Shortcuts and invariance

A model trained only on match outcomes can learn shortcuts: brand, popularity or category cues that correlate with the label in training data (Geirhos et al., 2020). Invariant risk minimization (Arjovsky et al., 2019) formalizes learning predictors that rely only on features whose relationship with the label is stable across environments. The proposal's invariance loss (labels must not change under brand, popularity or marketing swaps) and Theory result 3 belong to this line.

**Gap.** Knowledge-conflict research diagnoses and reduces reliance on memory in QA and generation. It does not study recommendation decisions, it rarely treats *missing* or *vague* evidence as a separate case, and it offers no abstention rule or guarantee.

## 3. Abstention and distribution-free risk control

### 3.1 Selective prediction

The reject option dates to Chow (1970), who characterized the optimal trade-off between error and rejection. Geifman and El-Yaniv (2017) give selective classification for deep networks with a guaranteed risk at a chosen coverage. Kamath, Jia and Liang (2020) apply selective prediction to QA under domain shift. Rajpurkar, Jia and Liang (2018) made *unanswerable* questions part of SQuAD 2.0. Kadavath et al. (2022) show that LLMs are often, but not always, calibrated about whether they know an answer.

### 3.2 Conformal prediction and risk control

Conformal prediction gives finite-sample, distribution-free guarantees under exchangeability (Angelopoulos & Bates, 2023). Its risk-control extensions are the basis of the proposal's Theory result 4:

- **Risk-controlling prediction sets** bound the expected value of a chosen loss with high probability (Bates et al., 2021).
- **Conformal risk control** bounds the expected value of any monotone loss (Angelopoulos et al., 2024).
- **Learn then Test** recasts risk control as multiple hypothesis testing and handles non-monotone risks and multiple parameters (Angelopoulos et al., 2021/2025).

### 3.3 Conformal methods for LLMs

- **Conformal abstention** lets an LLM abstain with a bounded hallucination rate (Yadkori et al., 2024).
- **Conformal factuality** filters an LLM's output so that retained claims are entailed with probability at least 1 − α (Mohri & Hashimoto, 2024). **This is the closest guarantee to Paper A** and must be cited in the proposal's "support, not accuracy" sentence.
- **Coherent factuality** extends this to reasoning chains, where each retained step must be deducible from earlier ones (Rubin-Toles et al., 2025). Cherian, Gibbs and Candès (2024) improve conditional validity and usefulness of such filters.
- **In recommendation,** Ravikumar (2026) finds that LLM recommenders' verbalized confidence is nearly constant while catalogue-hallucination rates vary widely, so confidence-based abstention barely helps.

**Gap.** Existing guarantees bound *error* (selective prediction, conformal abstention) or bound *unsupported claims in generated text* (conformal factuality). None bounds the rate of **recommendation decisions** that are not fully supported over a **conjunction** of constraints, with a three-way recommend / reject / abstain rule. The claim to make is not "the first guarantee on support", but "the first support guarantee for conjunctive recommendation decisions with abstention". The proposal's Separation result (a perfectly calibrated policy can have URR near 1) explains why error-based guarantees are not enough.

**Caution from the literature.** A conformal bound holds with respect to the labels used for calibration. The plan uses no human annotators, so calibration uses only automatic, launch-time label sources: (i) constructed-variant labels (L1), which are known by construction, and (ii) deterministic spec labels (L2), where the hidden `details` fields decide whether each constraint is entailed, contradicted or unresolved. Post-launch review labels (fit and misfit statements, L3) are used only to validate matches in RQ3 and never for calibration (plan §11.1), so the validation set stays independent of the bound. The URR guarantee is therefore a guarantee relative to the L1/L2 labels. State it that way in the paper, report how often L2 disagrees with L3 as a measure of label error, and keep LLM-verifier judgements out of the calibration labels, since a bound on the verifier's own labels would be circular.

## 4. Information acquisition

### 4.1 Value of information and active feature acquisition

Howard (1966) defined the value of information for decisions. EDDI (Ma et al., 2019) acquires the next most informative feature with a partial VAE, and AFABench (Schütz et al., 2025) benchmarks active feature acquisition policies. Adaptive submodularity (Golovin & Krause, 2011) gives guarantees for greedy adaptive policies. Sequential testing of series systems (reviewed by Ünlüyurt, 2004) studies the cheapest order in which to test components when one failure is enough to stop, which is the structure of a conjunctive need: one contradicted constraint is enough to reject.

### 4.2 LLM agents that look things up

ReAct (Yao et al., 2023) interleaves reasoning with tool calls. AR-Bench (Zhou et al., 2025) shows that LLMs struggle to ask the right questions under incomplete information. In shopping, Shopping Companion (Yu et al., 2026) names **insufficient verification of product attributes** as the largest failure mode of GPT-5 shopping agents (39.1% of failures), which is direct motivation for Paper A.

**Gap.** Acquisition methods stop when confidence is high enough. When a prior is strong, confidence is high before any evidence is read, so myopic value-of-information stopping never looks (the proposal's VOI-blindness result). No work found makes **support**, rather than confidence, the stopping condition.

## 5. Bias and manipulation in LLM recommenders

### 5.1 Priors that are not evidence

- **Brand.** With identical specifications, LLMs recommend well-known brands every time; a tiny rating advantage or authority-style marketing can break this (Chu & Hou, 2026). Brand prominence in LLM recommendations tracks marketplace visibility rather than market size (Malthouse et al., 2026).
- **Injected cues.** BiasRecBench (Tang et al., 2026) shows that LLM agents choosing among options are swayed by injected biases even when they can identify the better option.
- **Popularity.** Lichtenberg, Buchholz and Schwöbel (2024) measure popularity bias in LLM recommenders and find it lower than in classic recommenders on movies, so popularity bias should be measured, not assumed.

### 5.2 Strategic text

Strategic text on a product page can push it up LLM recommendations (Kumar & Lakkaraju, 2024). Adversarial SEO for LLMs (Nestaas, Debenedetti & Tramèr, 2025) and generative engine optimization (Aggarwal et al., 2024) show that content can be optimized for LLM visibility. Small cognitive-bias edits such as social proof shift visibility and resist defensive prompts (Filandrianos et al., 2025). Indirect prompt injection can hijack LLM-integrated applications through retrieved content (Greshake et al., 2023).

### 5.3 Manipulation in the market

Review manipulation predates LLMs: promotional reviews are concentrated where incentives are strongest (Mayzlin, Dover & Chevalier, 2014), and a large market for fake reviews targets young products (He, Hollenbeck & Proserpio, 2022).

**Gap.** This literature documents attacks and biases, but proposes no defence that is *structural*. A matcher that can only recommend on entailed specification evidence is, by construction, unmoved by brand swaps and unverifiable marketing claims. Paper A should also note that bias-injection studies test what happens when misleading cues are *added*; prior licensing is about what happens when evidence is *missing*, which those studies do not measure.

## 6. Shopping benchmarks, needs and attributes

- **Shopping benchmarks.** ESCI (Reddy et al., 2022) labels query–product relevance. Shopping MMLU (Jin et al., 2024) tests LLMs on 57 shopping tasks. ShoppingComp (Tou et al., 2025) tests expert-curated multi-constraint tasks and finds very low retrieval F1 and susceptibility to promotional misinformation. These are small or expert-built, and none has an abstention metric or tests missing information.
- **Needs from reviews.** Machine learning can identify customer needs from online reviews as well as interviews do (Timoshenko & Hauser, 2019). Paper A mines fit and misfit statements ("too wide for my space") as need profiles.
- **Attribute extraction.** LLMs can extract product attribute values from listing text (Brinkmann, Shraga & Bizer, 2024), which supports the requirement parser and the spec-label pipeline.

## 7. Synthesis for Paper A

### 7.1 Closest work and the difference

| Work | What it does | What Paper A adds |
|---|---|---|
| Mohri & Hashimoto (2024); Rubin-Toles et al. (2025) | Conformal guarantee that retained *claims* are entailed | Guarantee on *decisions* over a *conjunction* of constraints, with recommend / reject / abstain |
| Yadkori et al. (2024); Geifman & El-Yaniv (2017) | Abstain with bounded error | Bound unsupported decisions; Separation result shows error bounds can miss them |
| Ravikumar (2026) | Confidence-based abstention fails for LLM recommenders | Support-based abstention instead of confidence |
| Longpre et al. (2021); Xu et al. (2024); Shi et al. (2024); Si et al. (2026) | Diagnose and reduce memory over context in QA | Recommendation setting; missing and vague evidence; abstention |
| EDDI (Ma et al., 2019); AFABench | Acquire features by information value | Stop on support, not confidence; VOI-blindness result |
| Shopping Companion (Yu et al., 2026); ShoppingComp | Name missing attribute verification as a failure; small expert benchmarks | Large counterfactual benchmark with post-launch validation |
| Chu & Hou (2026); BiasRecBench; Kumar & Lakkaraju (2024); Nestaas et al. (2025) | Brand, bias and manipulation sway LLM recommenders | Structural defence; tests *absent* evidence, not only injected cues |
| UniSRec, Recformer, TIGER, LLM2Rec; Wang et al. (2025) | Recommend or target new items by similarity | Evidence check per need; no similarity-based licensing |

### 7.2 Gap statement

> AI recommenders can place new products near similar items, follow edited context in QA, abstain with a bounded error rate, and guarantee that generated claims are supported. No work (i) shows whether recommenders license new-product matches on priors when listing evidence is missing, vague or edited, (ii) gives a matcher that recommends only when every checkable constraint of a need is entailed by inspected evidence and abstains otherwise, or (iii) bounds the rate of unsupported recommendation decisions and validates launch-time matches against post-launch reviews.

### 7.3 Draft related-work section (NeurIPS style, about 650 words)

**Cold-start and LLM recommendation.** Recommending items without interaction history has relied on content and hybrid models [Schein et al., 2002; Volkovs et al., 2017], text-based sequential models [Hou et al., 2022; Li et al., 2023; He et al., 2025] and generative retrieval [Rajput et al., 2023]. LLMs extend this to natural-language preferences [Sanner et al., 2023] and synthetic cold-start signals [Wang et al., 2024], and item-centric methods select users for new items [Wang et al., 2025]. All of these place a new item by similarity to known items, a prior; none checks whether the item's listing supports a specific need. Recent audits find that LLM recommenders memorise item transitions [Kim et al., 2026] and that cold-start gains are often unreachable in practice [Dong et al., 2026].

**Context versus parametric knowledge.** Models frequently answer from memory rather than context [Longpre et al., 2021; Xie et al., 2024; Xu et al., 2024]. Context-aware decoding [Shi et al., 2024] and faithfulness training [Si et al., 2026] improve context-following, and benchmarks test unanswerable and counterfactual contexts [Ming et al., 2024]. We study the recommendation analogue, where the dominant failure is *absent* rather than conflicting evidence, and require abstention rather than a best guess.

**Selective prediction and conformal risk control.** Abstention with bounded error is well studied [Chow, 1970; Geifman & El-Yaniv, 2017; Kamath et al., 2020], and conformal risk control and Learn-then-Test give finite-sample bounds on general risks [Bates et al., 2021; Angelopoulos et al., 2024; Angelopoulos et al., 2025]. For LLMs, conformal abstention bounds hallucination [Yadkori et al., 2024], and conformal factuality guarantees that retained claims are entailed [Mohri & Hashimoto, 2024; Rubin-Toles et al., 2025]. Our guarantee differs in its object (a recommendation decision over a conjunction of constraints), its output space (recommend, reject, abstain), and its target (support rather than correctness). We show that calibrated confidence does not imply support.

**Information acquisition.** Active feature acquisition chooses what to observe under cost [Ma et al., 2019; Schütz et al., 2025], with guarantees for adaptive greedy policies [Golovin & Krause, 2011] and classic results on testing series systems [Ünlüyurt, 2004]. LLM agents interleave reasoning and lookup [Yao et al., 2023] but struggle to seek missing information [Zhou et al., 2025] and to verify product attributes [Yu et al., 2026]. These methods stop on confidence; we stop on support and show that value-of-information stopping is blind when priors are strong.

**Bias and manipulation of LLM recommenders.** Brand cues, injected biases and strategic text shift LLM recommendations [Chu & Hou, 2026; Tang et al., 2026; Kumar & Lakkaraju, 2024; Nestaas et al., 2025; Aggarwal et al., 2024; Filandrianos et al., 2025]. These studies add misleading cues; we additionally test missing evidence, and our decision rule is invariant to cues that do not change the entailed evidence.

**Shopping benchmarks.** Existing benchmarks evaluate relevance [Reddy et al., 2022], broad shopping skills [Jin et al., 2024] and expert-curated multi-constraint tasks [Tou et al., 2025]. Ours adds counterfactual evidence variants on new products, an abstention metric, and validation against post-launch reviews from Amazon Reviews 2023 [Hou et al., 2026].

---

# Part II. Paper B: early-buyer fit, review trajectories and the liability of newness

*This part keeps the marketing and entrepreneurship review from the earlier version, now category-neutral. "Fit" means that the listing's evidence supports the buyer's checkable need, as measured by Paper A's pipeline.*

## 8. Marketing

### 8.1 Seeding: who should get the product first?

Diffusion research holds that products spread through innovators and imitators (Bass, 1969) and through adopter categories with different needs (Rogers, 2003). Seeding research asks which customers to activate first, and has mostly answered with **network position**: hubs adopt earlier and speed diffusion (Goldenberg et al., 2009), seeding hubs or bridges beats random seeding (Hinz et al., 2011), and seeding value splits into acceleration and expansion (Libai, Muller & Peres, 2013). Firm-created word of mouth works best from less loyal customers (Godes & Mayzlin, 2009). Haenlein and Libai (2017) synthesize these programmes. Cui, Hu, Cui and Xie (2018) are an exception that models negative word of mouth: in simulation, seeding customers with a high propensity to adopt beats seeding hubs, especially for lower-quality and niche products. Seeding research measures reach and speed, not the reviews that seeded customers write.

### 8.2 Early reviews and path dependence

Early opinions shape later ones. A single artificial up-vote produces lasting rating inflation (Muchnik, Aral & Taylor, 2013), and visible popularity makes outcomes unequal and unpredictable (Salganik, Dodds & Watts, 2006). Average ratings tend to fall as later, less well-matched buyers arrive (Godes & Silva, 2012), prior ratings shape later rating behaviour (Moe & Trusov, 2011), and early ratings are biased by the self-selection of early buyers (Li & Hitt, 2008; Hu, Pavlou & Zhang, 2017). Reviews affect sales (Chevalier & Mayzlin, 2006), and for new products negative reviews matter more (Cui, Lui & Guo, 2012). Park, Shin and Xie (2021) show that a product's first review affects its valence and volume up to 36 months later.

### 8.3 Firms managing early ratings

Kuksov and Xie (2010) show that a forward-looking firm should adjust price or give early customers extras to raise early ratings. Fainmesser, Lauga and Ofek (2021) show in theory that, when later consumers see average ratings, a firm advertises to a **narrower group of consumers** to raise the first generation's average rating. This is the theoretical precedent for fit-based early targeting, and Paper B tests it empirically. Product-testing programmes such as Amazon Vine do not reliably raise ratings (Garnefeld et al., 2021), incentivized reviews inflate ratings even when disclosed (Park, Shin & Xie, 2023), and reviewers' style changes after enrolment (Puranam & Cardie, 2014). Matching on evidence avoids the incentive problem.

### 8.4 Fit uncertainty, needs and targeting

Product fit uncertainty is distinct from quality uncertainty and harms satisfaction and returns (Hong & Pavlou, 2014). Customer needs can be mined from reviews (Timoshenko & Hauser, 2019; Netzer et al., 2012; Archak, Ghose & Ipeirotis, 2011). Popularity information shifts choices (Tucker & Zhang, 2011), which makes popularity targeting the natural baseline. Machine-learning targeting depends on data conditions (Simester, Timoshenko & Zoumpoulis, 2020), and targeting by predicted risk differs from targeting by predicted response (Ascarza, 2018; Gutierrez & Gérardy, 2017).

**Gap in marketing.** Early reviews matter, and in theory firms should target better-matched early buyers. No study measures first buyers' fit at the level of checkable needs and listing evidence, or tests whether it predicts the review trajectory.

## 9. Entrepreneurship

### 9.1 Liability of newness and legitimacy

New organizations fail more often because they lack roles, routines and ties with outsiders (Stinchcombe, 1965; Freeman, Carroll & Hannan, 1983). They lack cognitive and sociopolitical legitimacy (Aldrich & Fiol, 1994; Suchman, 1995), which they can actively build (Zimmerman & Zeitz, 2002), usually with costly signals (Connelly et al., 2011).

### 9.2 Reputation cold start on platforms

On marketplaces, legitimacy is largely the review record. A seller's first negative feedback sharply slows growth (Cabral & Hortaçsu, 2010). Giving newcomers a first transaction and public evaluation substantially improves their later outcomes (Pallais, 2014), intermediaries help newcomers land first jobs (Stanton & Thomas, 2016), and monitoring tools reduce employers' reliance on experience (Liang, Hong & Gu, 2025).

### 9.3 Early adopters and lean startup

Founders are told to start with early adopters whose problem the product solves (Ries, 2011; Blank, 2013; Eisenmann, Ries & Dillard, 2012), echoing lead users (von Hippel, 1986). Hypothesis-driven entrepreneurs perform better (Camuffo et al., 2020). The method is manual and does not link early-adopter choice to public reputation.

### 9.4 AI and entrepreneurship

AI is expected to reshape venture creation (Obschonka & Audretsch, 2020; Chalmers, MacKenzie & Carter, 2021), but evidence is mixed: generative-AI advice helped high-performing entrepreneurs and hurt low performers (Otis et al., 2024).

**Gap in entrepreneurship.** No study treats evidence-supported first-customer selection, or listing fixes that make a product matchable, as a cheap way for a new venture to build legitimacy, nor tests whether early fit matters more for small brands.

## 10. Hypotheses for Paper B (from the refined plan)

- **H1 (marketing).** Products whose early buyers' needs were evidence-supported by the listing have higher average ratings and review volume 6–12 months after launch, controlling for price, category, specs and brand size.
- **H2 (marketing).** Misfit statements in the first reviews ("too wide", "smaller than listed") predict lower later ratings more strongly than general negative sentiment.
- **H3 (entrepreneurship).** The H1 association is stronger for small or new brands.
- **H4 (AI / IS, shared with Paper A's RQ3).** At the same contact budget, evidence-grounded targeting reaches more post-launch-satisfied buyers and fewer misfit buyers than popularity or prior-based targeting.
- **H5 (AI-native operations).** Turning abstentions into seller listing fixes raises coverage without raising URR.

**Methodological cautions.** Self-selection is the main threat to H1 (Li & Hitt, 2008; Hu et al., 2017): good products may attract better-fit buyers. Use within-brand comparisons and controls for specs and price, and rely on misfit statements (H2) as a sharper signal. Historical purchases were shaped by Amazon's own recommendations (Chaney, Stewart & Engelhardt, 2018; Schnabel et al., 2016); state this as a limitation.

## 11. Draft related-work section for Paper B (PACIS / HICSS style, about 750 words)

**Seeding and the early-review problem.** Seeding research asks which customers a firm should activate first and has mostly answered with network position [Goldenberg et al., 2009; Hinz et al., 2011; Libai et al., 2013], judging seeding by reach and speed. A parallel stream shows that what early customers say has lasting effects: prior ratings bias later ones [Muchnik et al., 2013; Moe & Trusov, 2011], ratings drift as later buyers are less well matched [Godes & Silva, 2012], early ratings reflect early buyers' self-selection [Li & Hitt, 2008; Hu et al., 2017], and a product's first review alters its rating and volume for years [Park et al., 2021]. Analytical work concludes that firms should manage early ratings through price [Kuksov & Xie, 2010] or by targeting a narrower, better-matched first generation [Fainmesser et al., 2021]. Free-product testing does not reliably help [Garnefeld et al., 2021], and incentivized reviews mislead even when disclosed [Park et al., 2023]. The literature implies, but has not tested, that selecting first buyers whose needs the product verifiably meets protects its reputation.

**New ventures and the reputation cold start.** New ventures face a liability of newness [Stinchcombe, 1965; Freeman et al., 1983] because they lack legitimacy [Aldrich & Fiol, 1994; Suchman, 1995], which they usually buy with costly signals [Connelly et al., 2011] but can also build [Zimmerman & Zeitz, 2002]. On platforms, early negative feedback slows sellers' growth [Cabral & Hortaçsu, 2010], and a first transaction with a public evaluation improves newcomers' later outcomes [Pallais, 2014; Stanton & Thomas, 2016]. Practice advises founders to start with early adopters [Ries, 2011; Blank, 2013], without a scalable method and without linking that choice to reputation.

**AI matching of new products.** Recommenders place new items by similarity [Hou et al., 2022; Li et al., 2023] or select audiences for them [Wang et al., 2025], and LLM recommenders are swayed by brand and marketing cues [Chu & Hou, 2026; Kumar & Lakkaraju, 2024]. Evidence-grounded matching instead recommends a product only when its listing supports every checkable need, and tells the seller which specification to add when it cannot.

**Research gap.** Marketing shows that early reviews are consequential and, in theory, that firms should target better-matched early buyers, but has not measured first-buyer fit against listing evidence. Entrepreneurship identifies the reputation cold start as a core liability of new ventures, but has not examined evidence-based first-customer selection as a legitimacy strategy, nor whether it matters most for small brands. AI research matches new items by similarity and is vulnerable to brand priors. **This paper measures whether the evidence-supported fit of a new product's first buyers predicts its later rating and review volume, tests whether the effect is strongest for small brands, and shows how an AI-native launch process (target, exclude, or ask the seller for a missing specification) turns this into action.**

**Contribution statement.**

> To marketing, we provide an empirical test of fit-based early-buyer targeting, moving it from theory [Fainmesser et al., 2021] to evidence with need-level fit measured against listing specifications. To entrepreneurship, we show whether evidence-based first-customer selection matters most for small brands facing a liability of newness, and frame listing fixes as low-cost legitimacy building. To information systems, we show how an AI-native launch process built on evidence-grounded matching produces target, exclusion and listing-fix actions.

---

# Part III. Thesis framework

```
                      PAPER A (method)                                         PAPER B (outcome)
 Shopper need ─► requirement parser ─► checkable constraints ─┐
                                                              ├─► support verifier ─► recommend / reject / abstain (URR ≤ α)
 New listing ──► acquisition policy (reads fields by cost) ───┘          │                    │
     (brand, ratings hidden)                                             │                    ▼
                                                                         │      first buyers: supported vs misfit share
                                                                         ▼                    │
                                                 abstain ─► seller adds missing spec (H5)     ▼
                                                                                 early reviews ─► 6–12-month rating, volume (H1, H2)
                                                                                              ▲
                                                                     brand size (moderator, H3)
```

- **Why priors fail:** knowledge conflicts and shortcuts (§2), calibration ≠ support (§3), VOI blindness (§4), manipulation (§5).
- **Why fit matters after launch:** self-selection and rating dynamics (Li & Hitt, 2008; Godes & Silva, 2012), first-review persistence (Park et al., 2021).
- **Why it matters most for new ventures:** liability of newness and reputation cold start (Stinchcombe, 1965; Cabral & Hortaçsu, 2010; Pallais, 2014).

---

# Part IV. Citation fixes for the proposal

| Proposal citation | Status | Fix |
|---|---|---|
| "Faithfulness-QA (2026)" | **Not found.** | Replace with FaithEval (Ming et al., 2024) and/or CANOE (Si et al., 2026). Mo et al. (2026) is a 2026 counterfactual-faithfulness paper, but its dataset is MedCounterFact. |
| CANOE (2025) | Exists | Cite the AAAI-26 version (Si et al., 2026). |
| BLaIR (ACL 2026) | **Confirmed** | ACL 2026 long paper 2026.acl-long.147, with an extra author (Xiangjun Fu) compared with the 2024 arXiv version. Use the ACL citation everywhere. |
| Cui, Lui & Guo (2012) | Confirmed | *International Journal of Electronic Commerce*, 17(1), 39–58. |
| Fleder & Hosanagar | Confirmed | *Management Science*, 2009, 55(5). |
| He, Hollenbeck & Proserpio (2022) | Confirmed | *Marketing Science* (INFORMS press release); SSRN 3664992. |
| Conformal abstention (2024) | Confirmed | Yadkori et al., arXiv 2405.01563 (also NeurIPS 2024 workshop). |
| Missing | Add | Angelopoulos et al. (2024) conformal risk control; Angelopoulos et al. (2025) Learn then Test; Mohri & Hashimoto (2024); Rubin-Toles et al. (2025); Ravikumar (2026); Shopping Companion; ShoppingComp; Chu & Hou (2026); BiasRecBench; Wang et al. (2025); Park et al. (2021); Fainmesser et al. (2021). |
| "Never use `details` specs" | Too absolute | Write "we found no work that…". |

---

# Part V. Structured academic review of 20 core papers

*Added 17 October 2026 at yui's request: 10 recent papers from peer-reviewed conferences, plus 10 papers with more than 100 citations. 14 papers are AI and 6 are marketing (70 / 30). "Academic review" is read here as a structured appraisal of each paper, in the style of a referee report. It is not a simulated peer review of the proposal.*

**How to read the citation counts.**
- Google Scholar and the Semantic Scholar API both refused automated access, so the counts come from three other sources:
  - Liner review pages, which show a "Cited by" number that appears to come from Semantic Scholar, from an undated snapshot.
  - IDEAS/RePEc CitEc, which counts only citations from economics working papers and journals indexed in RePEc.
  - Scopus, via a university research portal.
- All three undercount compared with Google Scholar, so read each count as a **lower bound**. Counts from different sources are not comparable with each other.
- The conference set is chosen by venue and recency, so no citation count is required for it.
- Chevalier & Mayzlin (2006) was left out of the highly cited set because its journal-article count could not be verified, although it is almost certainly highly cited.
- Venue: confirmed against the publisher page, ACL Anthology, PMLR, dblp or ICLR/NeurIPS proceedings.

**Fields per paper:** the problem, the method, the key finding (from the abstract or main result), strengths, limitations from the thesis's point of view, and how the thesis uses or differs from the paper.

## V.1 Overview

| # | Paper | Venue | Set | Field | Citations (lower bound, source) | Used in |
|---|---|---|---|---|---|---|
| C1 | Mohri & Hashimoto, conformal factuality | ICML 2024 | Conference | AI | 56 (Liner) | A |
| C2 | Rubin-Toles et al., coherent factuality | ICLR 2025 | Conference | AI | — | A |
| C3 | Xie et al., knowledge conflicts | ICLR 2024 | Conference | AI | — | A |
| C4 | Shi et al., context-aware decoding | NAACL 2024 | Conference | AI | — | A |
| C5 | Si et al., CANOE | AAAI 2026 | Conference | AI | — | A |
| C6 | Sanner et al., LLMs as near cold-start recommenders | RecSys 2023 | Conference | AI | — | A |
| C7 | Rajput et al., TIGER | NeurIPS 2023 | Conference | AI | 107 (Liner) | A |
| C8 | Hou et al., BLaIR / Amazon Reviews 2023 | ACL 2026 | Conference | AI | — | A, B |
| C9 | Nestaas et al., adversarial SEO for LLMs | ICLR 2025 | Conference | AI | — | A |
| C10 | Filandrianos et al., cognitive biases in LLM product recs | EMNLP 2025 | Conference | AI | — | A |
| H1 | Geifman & El-Yaniv, selective classification | NeurIPS 2017 | >100 cites | AI | 543 (Liner) | A |
| H2 | Longpre et al., entity-based knowledge conflicts | EMNLP 2021 | >100 cites | AI | 278 (Liner) | A |
| H3 | Hou et al., UniSRec | KDD 2022 | >100 cites | AI | 242 (Liner) | A |
| H4 | Angelopoulos et al., conformal risk control | ICLR 2024 | >100 cites | AI | 151 (Liner) | A |
| H5 | Bass, new product growth model | *Management Science* 1969 | >100 cites | Marketing | 1,529 (CitEc) | B |
| H6 | Muchnik, Aral & Taylor, social influence bias | *Science* 2013 | >100 cites | Marketing | 736 (Scopus) | B |
| H7 | Li & Hitt, self-selection in reviews | *ISR* 2008 | >100 cites | Marketing / IS | 291 (CitEc) | B |
| H8 | Timoshenko & Hauser, customer needs from UGC | *Marketing Science* 2019 | >100 cites | Marketing | 111 (CitEc) | A, B |
| H9 | Hong & Pavlou, product fit uncertainty | *ISR* 2014 | >100 cites | Marketing / IS | 104 (CitEc) | A, B |
| H10 | Godes & Silva, dynamics of online opinion | *Marketing Science* 2012 | >100 cites | Marketing | 103 (CitEc) | B |

Liner sources: liner.com/review/{entitybased-knowledge-conflicts-in-question-answering, selective-classification-for-deep-neural-networks, recommender-systems-with-generative-retrieval, conformal-risk-control, language-models-with-conformal-factuality-guarantees}; UniSRec at liner.com/ko/review/towards-universal-sequence-representation-learning-for-recommender-systems. CitEc sources: ideas.repec.org/a/inm/ormnsc/v15y1969i5p215-227 (Bass), …/orisre/v19y2008i4p456-474 (Li & Hitt), …/ormksc/v38y2019i1p1-20 (Timoshenko & Hauser), …/orisre/v25y2014i2p328-344 (Hong & Pavlou), …/ormksc/v31y2012i3p448-473 (Godes & Silva). Scopus: cris.huji.ac.il (Muchnik et al.). All accessed 17 October 2026.

## V.2 Conference papers (AI)

**C1. Mohri & Hashimoto (2024), "Language models with conformal factuality guarantees", ICML.**
- *Problem.* LLM outputs mix true and false claims, and there is no guarantee on how many retained claims are correct.
- *Method.* Split an output into claims, score each one, and use conformal prediction to pick a threshold. Claims below the threshold are removed, so the retained output is entailed with probability ≥ 1 − α.
- *Key finding.* The guarantee holds in QA and reasoning tasks, and keeps most of the useful content at practical α.
- *Strengths.* Distribution-free; works with any scorer; simple.
- *Limitations for us.* It filters generated text. It does not make decisions, it has no notion of a conjunctive need, and it does not separate "contradicted" from "unresolved". The guarantee is on its calibration labels.
- *Use / differ.* This is the closest guarantee to Paper A's URR bound. Paper A moves the object from *claims* to *decisions* over a conjunction of constraints, adds reject/abstain, and validates against post-launch reviews.

**C2. Rubin-Toles, Gambhir, Ramji, Roth & Goel (2025), "Conformal language model reasoning with coherent factuality", ICLR.**
- *Problem.* For reasoning chains, a claim can be true but not deducible from the earlier steps.
- *Method.* Represent reasoning as a dependency graph and apply conformal filtering so that retained steps are coherent: each one follows from earlier ones.
- *Key finding.* Coherent factuality is achieved at the target level on math reasoning, while plain claim-wise filtering breaks chains.
- *Use / differ.* This supports the claim that "true" and "supported by what was shown" are different targets. Paper A's support status per constraint is the decision-level analogue.

**C3. Xie, Zhang, Chen, Lou & Su (2024), "Adaptive chameleon or stubborn sloth", ICLR.**
- *Problem.* How do LLMs behave when external evidence conflicts with their parametric memory?
- *Method.* Elicit each model's memory, then build coherent counter-memory evidence and test responses under single and mixed evidence.
- *Key finding.* LLMs accept coherent counter-memory evidence, but show strong confirmation bias toward memory when evidence is mixed.
- *Limitations for us.* QA only, and the evidence is always *present*.
- *Use / differ.* This is the template for Paper A's probe. Paper A adds *missing* and *vague* evidence, which is the realistic new-product case.

**C4. Shi, Han, Lewis, Tsvetkov, Zettlemoyer & Yih (2024), "Trusting your evidence: Hallucinate less with context-aware decoding", NAACL (short).**
- *Problem.* Models ignore context in favour of priors.
- *Method.* Contrastive decoding that amplifies the difference between output probabilities with and without the context.
- *Key finding.* Better faithfulness in summarization and knowledge-conflict tasks, with no training.
- *Use / differ.* A strong training-free baseline for Paper A. It pushes toward the context but cannot abstain when the context is silent.

**C5. Si et al. (2026), "Teaching large language models to maintain contextual faithfulness via synthetic tasks and reinforcement learning" (CANOE), AAAI.**
- *Problem.* Faithfulness training needs labelled data that is expensive to annotate.
- *Method.* Synthesize short-form QA tasks with verifiable answers, then train with rule-based RL rewards that transfer to long-form generation.
- *Key finding.* Faithfulness improves across many tasks, and the paper reports results above strong proprietary models.
- *Use / differ.* A training baseline for Paper A's verifier. Paper A's counterfactual evidence-sensitivity loss differs by targeting the *absence* of evidence and an abstain action.

**C6. Sanner, Balog, Radlinski, Wedin & Dixon (2023), "Large language models are competitive near cold-start recommenders…", RecSys.**
- *Problem.* Can LLMs recommend from natural-language preferences when interaction data is thin?
- *Method.* Collect item-based and language-based preferences, and compare LLM prompting with collaborative-filtering baselines.
- *Key finding.* LLMs are competitive in the near cold-start setting, especially with language-based preferences.
- *Limitations for us.* Movies, where the LLM may have memorized the items. Accuracy is measured, not support.
- *Use / differ.* This motivates using LLMs on new products. Paper A asks whether that competence comes from evidence or from memory.

**C7. Rajput et al. (2023), "Recommender systems with generative retrieval" (TIGER), NeurIPS.**
- *Problem.* Retrieval with item IDs cannot generalize to new items.
- *Method.* Give items semantic IDs made from quantized content embeddings, then generate the next item's ID with a sequence model.
- *Key finding.* Beats sequential baselines on Amazon data, with some ability to retrieve cold-start items.
- *Use / differ.* A representative similarity-based new-item method. A semantic ID places a new item near similar items, which is exactly a prior and not a check of the listing.

**C8. Hou et al. (2026), "Bridging language and items for retrieval and recommendation", ACL (arXiv 2024).**
- *Problem.* Text encoders do not capture the link between item metadata and the language people use about items.
- *Method.* Release Amazon Reviews 2023 (more than 570 million reviews across 33 categories) and pretrain BLaIR with contrastive learning on metadata–review pairs.
- *Key finding.* BLaIR improves retrieval and recommendation, including complex product search.
- *Use / differ.* This is Paper A's dataset and a strong encoder baseline. Paper A uses the `details` specifications as hidden ground truth and post-launch reviews as validation, which this paper does not.

**C9. Nestaas, Debenedetti & Tramèr (2025), "Adversarial search engine optimization for large language models", ICLR.**
- *Problem.* Third-party content that LLM search reads can be crafted to promote itself.
- *Method.* Preference-manipulation attacks on real LLM search and plug-in systems.
- *Key finding.* The attacks raise a product's selection, and they create a prisoner's dilemma in which every party has an incentive to attack.
- *Use / differ.* This motivates Paper A's invariance to marketing rewrites. An entailment-only decision rule is a structural defence, not a filter.

**C10. Filandrianos, Dimitriou, Lymperaiou, Thomas & Stamou (2025), "Bias beware", EMNLP.**
- *Problem.* Do cognitive-bias cues in product descriptions (for example social proof or scarcity) sway LLM recommenders?
- *Method.* Insert bias-framed edits into descriptions and measure the change in recommendation.
- *Key finding.* Small edits shift visibility, and defensive prompting does not reliably stop this.
- *Use / differ.* Evidence that LLM recommenders respond to cues that are not checkable evidence. Paper A's marketing-rewrite variant directly tests this.

## V.3 Highly cited papers (AI)

**H1. Geifman & El-Yaniv (2017), "Selective classification for deep neural networks", NeurIPS.** *(543+)*
- *Problem.* How to make a trained network abstain so that error on accepted inputs stays below a target.
- *Method.* Choose a confidence threshold on held-out data with a high-probability bound on selective risk.
- *Key finding.* A guaranteed risk level at the achieved coverage on ImageNet-scale models.
- *Use / differ.* This is the canonical abstention baseline. Paper A's Separation result shows that bounding *error* this way can still leave URR near 1, because a calibrated model can be confidently right for prior reasons.

**H2. Longpre et al. (2021), "Entity-based knowledge conflicts in question answering", EMNLP.** *(278+)*
- *Problem.* Do QA models read the passage or recall the answer?
- *Method.* Substitute answer entities in passages to create conflicts between context and memory.
- *Key finding.* Models often answer from memory and hallucinate the original answer; training with substituted data reduces this and improves generalization.
- *Use / differ.* This is the founding diagnosis of evidence vs memory. Paper A's edited and brand-swap variants extend entity substitution to product attributes.

**H3. Hou et al. (2022), "Towards universal sequence representation learning for recommender systems" (UniSRec), KDD.** *(242+)*
- *Problem.* ID-based sequential recommenders do not transfer across domains or to new items.
- *Method.* Represent items by their text through a parametric whitening and mixture-of-experts adaptor, then pretrain on multiple domains.
- *Key finding.* Strong transfer and inductive (new-item) performance.
- *Use / differ.* This is the text-based new-item baseline. It scores a new item by text similarity and never asks whether the text supports a specific need.

**H4. Angelopoulos, Bates, Fisch, Lei & Schuster (2024), "Conformal risk control", ICLR.** *(151+)*
- *Problem.* Conformal prediction controls coverage, but many tasks need control of other losses.
- *Method.* Generalize split conformal prediction to bound the expected value of any monotone loss.
- *Key finding.* Finite-sample control of losses such as false negative rate in vision and NLP tasks.
- *Use / differ.* This is the calibration machinery for Paper A's Theory result 4. URR is a monotone loss in the decision threshold; Learn-then-Test covers it if the acquisition policy makes it non-monotone.

## V.4 Highly cited papers (marketing)

**H5. Bass (1969), "A new product growth for model consumer durables", *Management Science*.** *(1,529+)*
- *Problem.* How do new products diffuse?
- *Method.* A model of first purchases driven by innovation (external influence) and imitation (prior adopters).
- *Key finding.* The model fits the sales curves of durables and forecasts the timing of peak sales.
- *Use / differ.* This is Paper B's diffusion backdrop: early adopters shape later adoption. Paper B adds that *who* the early adopters are, and whether the product fits them, shapes what they say to imitators.

**H6. Muchnik, Aral & Taylor (2013), "Social influence bias: A randomized experiment", *Science*.** *(736+)*
- *Problem.* Do prior ratings causally bias later ones?
- *Method.* A field experiment on a news site that randomly gave comments an up-vote, a down-vote or nothing.
- *Key finding.* One early up-vote raised the chance of further positive ratings and produced lasting inflation; negative manipulation was corrected by the crowd.
- *Use / differ.* This is causal evidence that early signals persist. Paper B's H1 and H2 rest on it, and the asymmetry it reports needs discussing for misfit reviews.

**H7. Li & Hitt (2008), "Self-selection and information role of online product reviews", *Information Systems Research*.** *(291+)*
- *Problem.* Are early reviews representative of what later buyers will experience?
- *Method.* A model and data from book reviews over time.
- *Key finding.* Early buyers self-select. Their preferences differ from later buyers', so early ratings are biased and then trend over time.
- *Use / differ.* This is the main identification threat for Paper B: good products may simply attract better-fit early buyers. It also gives the mechanism, since fit among early buyers shapes the early signal.

**H8. Timoshenko & Hauser (2019), "Identifying customer needs from user-generated content", *Marketing Science*.** *(111+)*
- *Problem.* Can reviews replace interviews for finding customer needs?
- *Method.* A CNN filters out uninformative content, and clustering removes repetition before human review.
- *Key finding.* UGC identifies needs at least as well as interviews, and more efficiently.
- *Use / differ.* This justifies mining fit and misfit statements from reviews as need profiles in both papers. Paper A goes further and turns needs into checkable constraints.

**H9. Hong & Pavlou (2014), "Product fit uncertainty in online markets", *Information Systems Research*.** *(104+)*
- *Problem.* Is uncertainty about fit different from uncertainty about quality?
- *Method.* Survey and transaction data on online purchases.
- *Key finding.* Fit uncertainty is distinct from quality uncertainty, and it raises returns and lowers satisfaction. Product descriptions and similar cues can reduce it.
- *Use / differ.* This is the business definition behind "fit" in both papers. Paper A operationalizes fit as entailed checkable constraints; Paper B measures its consequences in reviews.

**H10. Godes & Silva (2012), "Sequential and temporal dynamics of online opinion", *Marketing Science*.** *(103+)*
- *Problem.* Why do average ratings decline over time?
- *Method.* Separate the effect of time from the effect of review order in Amazon book reviews.
- *Key finding.* Ratings fall with the number of reviews, which the authors attribute to later buyers being less well matched to the product.
- *Use / differ.* This is direct support for Paper B's mechanism that mismatch lowers ratings. Paper B measures mismatch at the level of the need, instead of inferring it from the order of reviews.

## V.5 What the 20 papers add up to

1. **AI (14 papers).** Models prefer memory to evidence (H2, C3). Existing fixes push the model toward the context but cannot abstain (C4, C5). Abstention and conformal tools bound *error* or *unsupported text* (H1, H4, C1, C2). New-item recommenders rely on similarity (H3, C6, C7), and LLM recommenders are moved by cues that are not evidence (C9, C10). No paper bounds *unsupported decisions*, which is Paper A's opening.
2. **Marketing (6 papers).** Early adopters drive diffusion (H5), and early signals persist (H6). Early buyers self-select (H7), and mismatch lowers ratings (H10). Fit is a distinct uncertainty that can be measured from text (H8, H9). No paper links need-level fit among first buyers to the review trajectory, which is Paper B's opening.
3. **Read in full first.** C1, C3, H1, H7 and H10 set the bar that reviewers will compare against.

---

## Limitations of this review and remaining checks

1. **Abstract-level reading.** Read Mohri & Hashimoto (2024), Rubin-Toles et al. (2025), Shopping Companion, ShoppingComp, Chu & Hou (2026), Park et al. (2021) and Fainmesser et al. (2021) in full before the proposal defence.
2. **Fast-moving area.** Several closest papers are 2026 arXiv preprints. Re-run searches before submission: "conformal" AND "recommendation" AND "abstain"; "context faithfulness" AND "recommendation"; "LLM shopping agent" AND "verification"; "prior" OR "memorization" AND "LLM recommender".
3. **Unverified details** are marked **[check details]** below.

---

## References

*APA 7th edition. ✔ = existence and core details checked against the listed source. **[check details]** = existence verified, but the marked element was filled from memory.*

### A. Recommender systems and new items

- Abdollahpouri, H., Burke, R., & Mobasher, B. (2017). Controlling popularity bias in learning-to-rank recommendation. In *Proceedings of the 11th ACM Conference on Recommender Systems* (pp. 42–46). https://doi.org/10.1145/3109859.3109912 ✔ **[check details: pages]**
- Burke, R. (2002). Hybrid recommender systems: Survey and experiments. *User Modeling and User-Adapted Interaction, 12*(4), 331–370. ✔ **[check details: pages]**
- Chaney, A. J. B., Stewart, B. M., & Engelhardt, B. E. (2018). How algorithmic confounding in recommendation systems increases homogeneity and decreases utility. In *Proceedings of the 12th ACM Conference on Recommender Systems* (pp. 224–232). ✔ **[check details: pages]**
- Chen, L., Chen, G., & Wang, F. (2015). Recommender systems based on user reviews: The state of the art. *User Modeling and User-Adapted Interaction, 25*(2), 99–154. ✔ **[check details: pages]**
- Dong, Z., Qin, F., Shah, M., & Wang, Y. (2026). *Diagnosing and mitigating retrieval bottlenecks in LLM-based cold-start recommendation* (arXiv:2606.29947). ✔
- Fleder, D., & Hosanagar, K. (2009). Blockbuster culture's next rise or fall: The impact of recommender systems on sales diversity. *Management Science, 55*(5), 697–712. ✔ **[check details: pages]**
- Geng, S., Liu, S., Fu, Z., Ge, Y., & Zhang, Y. (2022). Recommendation as language processing (RLP): A unified pretrain, personalized prompt & predict paradigm (P5). In *Proceedings of the 16th ACM Conference on Recommender Systems*. ✔
- He, Y., Liu, X., Zhang, A., Ma, Y., & Chua, T.-S. (2025). *LLM2Rec: Large language models are powerful embedding models for sequential recommendation* (arXiv:2506.21579). ✔ (proposal lists KDD 2025) **[check details: venue]**
- Hou, Y., Li, J., Fu, X., He, Z., Yan, A., Chen, X., & McAuley, J. (2026). Bridging language and items for retrieval and recommendation: Benchmarking LLMs as semantic encoders. In *Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)* (pp. 3251–3265). ACL. ✔ (arXiv:2403.03952, 2024; introduces Amazon Reviews 2023 and BLaIR)
- Hou, Y., Mu, S., Zhao, W. X., Li, Y., Ding, B., & Wen, J.-R. (2022). Towards universal sequence representation learning for recommender systems. In *Proceedings of KDD 2022*. ✔ (arXiv:2206.05941)
- Hou, Y., Zhang, J., Lin, Z., Lu, H., Xie, R., McAuley, J., & Zhao, W. X. (2024b). Large language models are zero-shot rankers for recommender systems. In *Advances in Information Retrieval (ECIR 2024)*. Springer. ✔
- Kim, S., Lee, S., Ju, C. M., Loveland, D., Kumar, B., Shin, K., Shah, N., & Collins, L. (2026). *On the memorization behavior of LLMs in generative recommendation: Observations, implications, and training strategies* (arXiv:2606.17276). ✔
- Lan, Y.-T., Huo, Y., Shen, Y., Yang, X., & Liu, Z. (2025). *Next-user retrieval: Enhancing cold-start recommendations via generative next-user modeling* (arXiv:2506.15267). ✔
- Li, J., Wang, M., Li, J., Fu, J., Shen, X., Shang, J., & McAuley, J. (2023). Text is all you need: Learning language representations for sequential recommendation. In *Proceedings of KDD 2023*. ✔ (arXiv:2305.13731) **[check details: author list]**
- Liu, E., et al. (2025). Generative recommender with end-to-end learnable item tokenization (ETEGRec). In *Proceedings of SIGIR 2025*. ✔ (arXiv:2409.05546) **[check details: authors]**
- Ma, Q., Wen, M., Xia, Z., & Chen, D. (2016). A sub-linear, massive-scale look-alike audience extension system. *Proceedings of Machine Learning Research, 53*, 51–67. ✔
- McAuley, J., & Leskovec, J. (2013). Hidden factors and hidden topics: Understanding rating dimensions with review text. In *Proceedings of the 7th ACM Conference on Recommender Systems* (pp. 165–172). ✔ **[check details: pages]**
- Rajput, S., et al. (2023). Recommender systems with generative retrieval. In *Advances in Neural Information Processing Systems 36*. ✔ **[check details: author list]**
- Sanner, S., Balog, K., Radlinski, F., Wedin, B., & Dixon, L. (2023). Large language models are competitive near cold-start recommenders for language- and item-based preferences. In *Proceedings of the 17th ACM Conference on Recommender Systems*. ✔
- Schein, A. I., Popescul, A., Ungar, L. H., & Pennock, D. M. (2002). Methods and metrics for cold-start recommendations. In *Proceedings of the 25th Annual International ACM SIGIR Conference* (pp. 253–260). ✔ **[check details: pages]**
- Schnabel, T., Swaminathan, A., Singh, A., Chandak, N., & Joachims, T. (2016). Recommendations as treatments: Debiasing learning and evaluation. *Proceedings of Machine Learning Research, 48* (ICML 2016). ✔
- Volkovs, M., Yu, G., & Poutanen, T. (2017). DropoutNet: Addressing cold start in recommender systems. In *Advances in Neural Information Processing Systems 30*. ✔
- Wang, D., Jiao, J., Bhadury, A., Zhang, Y., Gao, M., & Dalal, O. (2025). *Item-centric exploration for cold start problem* (arXiv:2507.09423). ✔
- Wang, J., Lu, H., Caverlee, J., Chi, E., & Chen, M. (2024). *Large language models as data augmenters for cold-start item recommendation* (arXiv:2402.11724). ✔
- Wu, L., et al. (2024). A survey on large language models for recommendation. *World Wide Web, 27*. https://doi.org/10.1007/s11280-024-01291-2 ✔ **[check details: author list, article number]**
- Zheng, L., Noroozi, V., & Yu, P. S. (2017). Joint deep modeling of users and items using reviews for recommendation. In *Proceedings of WSDM 2017* (pp. 425–434). ✔ **[check details: pages]**

### B. Evidence versus memory, faithfulness and support

- Arjovsky, M., Bottou, L., Gulrajani, I., & Lopez-Paz, D. (2019). *Invariant risk minimization* (arXiv:1907.02893). ✔
- Gao, T., Yen, H., Yu, J., & Chen, D. (2023). Enabling large language models to generate text with citations. In *Proceedings of EMNLP 2023*. ✔
- Geirhos, R., Jacobsen, J.-H., Michaelis, C., Zemel, R., Brendel, W., Bethge, M., & Wichmann, F. A. (2020). Shortcut learning in deep neural networks. *Nature Machine Intelligence, 2*, 665–673. ✔ **[check details: author list, pages]**
- Kaushik, D., Hovy, E., & Lipton, Z. C. (2020). Learning the difference that makes a difference with counterfactually-augmented data. In *International Conference on Learning Representations*. ✔
- Longpre, S., Perisetla, K., Chen, A., Ramesh, N., DuBois, C., & Singh, S. (2021). Entity-based knowledge conflicts in question answering. In *Proceedings of EMNLP 2021*. ✔ **[check details: author list]**
- Ming, Y., Purushwalkam, S., Pandit, S., Ke, Z., Nguyen, X.-P., Xiong, C., & Joty, S. (2024). *FaithEval: Can your language model stay faithful to context, even if "the moon is made of marshmallows"* (arXiv:2410.03727). ✔ **[check details: published venue]**
- Mo, K., Venkatayogi, S., Shaib, C., Kouzy, R., Xu, W., Wallace, B. C., & Li, J. J. (2026). *Faithfulness vs. safety: Evaluating LLM behavior under counterfactual medical evidence* (arXiv:2601.11886). ✔
- Petroni, F., Rocktäschel, T., Lewis, P., Bakhtin, A., Wu, Y., Miller, A. H., & Riedel, S. (2019). Language models as knowledge bases? In *Proceedings of EMNLP-IJCNLP 2019*. ✔ **[check details: author list]**
- Rashkin, H., Nikolaev, V., Lamm, M., Aroyo, L., Collins, M., Das, D., Petrov, S., Tomar, G. S., Turc, I., & Reitter, D. (2023). Measuring attribution in natural language generation models. *Computational Linguistics, 49*(4). ✔ **[check details: author list, pages]**
- Shi, W., Han, X., Lewis, M., Tsvetkov, Y., Zettlemoyer, L., & Yih, W.-t. (2024). Trusting your evidence: Hallucinate less with context-aware decoding. In *Proceedings of NAACL 2024 (Short Papers)*. ✔
- Si, S., Zhao, H., Gao, C., Bai, Y., Wang, Z., Gao, B., Luo, K., Li, W., Huang, Y., Chen, G., Qi, F., Zhang, M., Chang, B., & Sun, M. (2026). Teaching large language models to maintain contextual faithfulness via synthetic tasks and reinforcement learning. *Proceedings of the AAAI Conference on Artificial Intelligence, 40*(39), 33001–33009. ✔
- Xie, J., Zhang, K., Chen, J., Lou, R., & Su, Y. (2024). Adaptive chameleon or stubborn sloth: Revealing the behavior of large language models in knowledge conflicts. In *International Conference on Learning Representations*. ✔
- Xu, R., et al. (2024). Knowledge conflicts for LLMs: A survey. In *Proceedings of EMNLP 2024*. ✔ (arXiv:2403.08319) **[check details: author list]**
- Zhou, W., Zhang, S., Poon, H., & Chen, M. (2023). Context-faithful prompting for large language models. In *Findings of EMNLP 2023*. ✔

### C. Abstention, calibration and conformal risk control

- Angelopoulos, A. N., & Bates, S. (2023). Conformal prediction: A gentle introduction. *Foundations and Trends in Machine Learning, 16*(4), 494–591. ✔ **[check details: volume/pages]**
- Angelopoulos, A. N., Bates, S., Candès, E. J., Jordan, M. I., & Lei, L. (2025). Learn then test: Calibrating predictive algorithms to achieve risk control. *Annals of Applied Statistics*. ✔ (arXiv:2110.01052, 2021) **[check details: journal volume and year]**
- Angelopoulos, A. N., Bates, S., Fisch, A., Lei, L., & Schuster, T. (2024). Conformal risk control. In *International Conference on Learning Representations*. ✔
- Bates, S., Angelopoulos, A., Lei, L., Malik, J., & Jordan, M. I. (2021). Distribution-free, risk-controlling prediction sets. *Journal of the ACM, 68*(6). ✔ (arXiv:2101.02703) **[check details: journal details]**
- Cherian, J. J., Gibbs, I., & Candès, E. J. (2024). Large language model validity via enhanced conformal prediction methods. In *Advances in Neural Information Processing Systems 37*. ✔
- Chow, C. K. (1970). On optimum recognition error and reject tradeoff. *IEEE Transactions on Information Theory, 16*(1), 41–46. ✔ **[check details: issue/pages]**
- Geifman, Y., & El-Yaniv, R. (2017). Selective classification for deep neural networks. In *Advances in Neural Information Processing Systems 30*. ✔
- Kadavath, S., et al. (2022). *Language models (mostly) know what they know* (arXiv:2207.05221). ✔
- Kamath, A., Jia, R., & Liang, P. (2020). Selective question answering under domain shift. In *Proceedings of ACL 2020*. ✔
- Mohri, C., & Hashimoto, T. (2024). Language models with conformal factuality guarantees. *Proceedings of Machine Learning Research, 235* (ICML 2024). ✔
- Rajpurkar, P., Jia, R., & Liang, P. (2018). Know what you don't know: Unanswerable questions for SQuAD. In *Proceedings of ACL 2018 (Short Papers)*. ✔
- Ravikumar, S. (2026). *Do LLM recommenders know when they're hallucinating? Auditing confidence calibration in catalog faithfulness* (arXiv:2608.10008). ✔
- Rubin-Toles, M., Gambhir, M., Ramji, K., Roth, A., & Goel, S. (2025). Conformal language model reasoning with coherent factuality. In *International Conference on Learning Representations*. ✔
- Yadkori, Y. A., et al. (2024). *Mitigating LLM hallucinations via conformal abstention* (arXiv:2405.01563). ✔ **[check details: author list]**

### D. Information acquisition and agents

- Golovin, D., & Krause, A. (2011). Adaptive submodularity: Theory and applications in active learning and stochastic optimization. *Journal of Artificial Intelligence Research, 42*, 427–486. ✔ **[check details: pages]**
- Howard, R. A. (1966). Information value theory. *IEEE Transactions on Systems Science and Cybernetics, 2*(1), 22–26. ✔ **[check details: issue/pages]**
- Ma, C., Tschiatschek, S., Palla, K., Hernández-Lobato, J. M., Nowozin, S., & Zhang, C. (2019). EDDI: Efficient dynamic discovery of high-value information with partial VAE. *Proceedings of Machine Learning Research, 97* (ICML 2019). ✔
- Schütz, V., Wu, H., Rezvan, R., Aronsson, L., & Chehreghani, M. H. (2025). *AFABench: A generic framework for benchmarking active feature acquisition* (arXiv:2508.14734). ✔
- Ünlüyurt, T. (2004). Sequential testing of complex systems: A review. *Discrete Applied Mathematics, 142*(1–3), 189–205. ✔ **[check details: volume/pages]**
- Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2023). ReAct: Synergizing reasoning and acting in language models. In *International Conference on Learning Representations*. ✔
- Yu, Z., Xiao, K., Zhao, H., Luo, T., & Zeng, X. (2026). *Shopping Companion: Benchmarking and training LLM agents for long-horizon preference-grounded e-commerce tasks* (arXiv:2603.14864). ✔ **[check details: year]**
- Zhou, Z., et al. (2025). From passive to active reasoning: Can large language models ask the right questions under incomplete information? *Proceedings of Machine Learning Research, 267* (ICML 2025). ✔ **[check details: author list]**

### E. Bias and manipulation in LLM recommenders and online reviews

- Aggarwal, P., Murahari, V., Rajpurohit, T., Kalyan, A., Narasimhan, K., & Deshpande, A. (2024). GEO: Generative engine optimization. In *Proceedings of KDD 2024*. ✔
- Chu, X., & Hou, Y. (2026). *Incumbent advantage: Brand bias and cognitive manipulation dynamics in LLM recommendation systems* (arXiv:2606.17443). ✔
- Filandrianos, G., Dimitriou, A., Lymperaiou, M., Thomas, K., & Stamou, G. (2025). Bias beware: The impact of cognitive biases on LLM-driven product recommendations. In *Proceedings of EMNLP 2025* (pp. 22397–22426). ✔
- Greshake, K., Abdelnabi, S., Mishra, S., Endres, C., Holz, T., & Fritz, M. (2023). Not what you've signed up for: Compromising real-world LLM-integrated applications with indirect prompt injection. In *Proceedings of the 16th ACM Workshop on Artificial Intelligence and Security*. ✔ **[check details: author list]**
- He, S., Hollenbeck, B., & Proserpio, D. (2022). The market for fake reviews. *Marketing Science, 41*(5), 896–921. ✔ **[check details: volume/pages]**
- Kumar, A., & Lakkaraju, H. (2024). *Manipulating large language models to increase product visibility* (arXiv:2404.07981). ✔
- Lichtenberg, J. M., Buchholz, A., & Schwöbel, P. (2024). *Large language models as recommender systems: A study of popularity bias* (arXiv:2406.01285). ✔
- Malthouse, E., Lee, K.-Y., Pal, S., Feng, X., & Yang, J. (2026). *Evaluating brand retrieval and ranking in large language model recommendations* (arXiv:2609.16304). ✔
- Mayzlin, D., Dover, Y., & Chevalier, J. (2014). Promotional reviews: An empirical investigation of online review manipulation. *American Economic Review, 104*(8), 2421–2455. ✔ **[check details: issue/pages]**
- Nestaas, F., Debenedetti, E., & Tramèr, F. (2025). Adversarial search engine optimization for large language models. In *International Conference on Learning Representations*. ✔
- Tang, Z., Zhang, Z., Wang, Q., Tang, Z., Li, B., & Chu, X. (2026). *Is your LLM-as-a-recommender agent trustable? LLMs' recommendation is easily hacked by biases (preferences)* (arXiv:2603.17417). ✔

### F. Shopping benchmarks, needs and attributes

- Brinkmann, A., Shraga, R., & Bizer, C. (2024). *ExtractGPT: Exploring the potential of large language models for product attribute value extraction* (arXiv:2310.12537). ✔ **[check details: published venue]**
- Jin, Y., et al. (2024). Shopping MMLU: A massive multi-task online shopping benchmark for large language models. In *NeurIPS 2024 Datasets and Benchmarks Track*. ✔
- Reddy, C. K., et al. (2022). *Shopping queries dataset: A large-scale ESCI benchmark for improving product search* (arXiv:2206.06588). ✔
- Timoshenko, A., & Hauser, J. R. (2019). Identifying customer needs from user-generated content. *Marketing Science, 38*(1), 1–20. https://doi.org/10.1287/mksc.2018.1123 ✔
- Tou, H., Zeng, Y., Ma, C., Li, M., Li, M., Yuan, W., Zhang, H., & Jia, K. (2025). *ShoppingComp: Are LLMs really ready for your shopping cart?* (arXiv:2511.22978). ✔

### G. Marketing (Paper B)

- Archak, N., Ghose, A., & Ipeirotis, P. G. (2011). Deriving the pricing power of product features by mining consumer reviews. *Management Science, 57*(8), 1485–1509. ✔ **[check details: pages]**
- Ascarza, E. (2018). Retention futility: Targeting high-risk customers might be ineffective. *Journal of Marketing Research, 55*(1), 80–98. ✔ **[check details: pages]**
- Bass, F. M. (1969). A new product growth for model consumer durables. *Management Science, 15*(5), 215–227. https://doi.org/10.1287/mnsc.15.5.215 ✔
- Chevalier, J. A., & Mayzlin, D. (2006). The effect of word of mouth on sales: Online book reviews. *Journal of Marketing Research, 43*(3), 345–354. ✔ **[check details: pages]**
- Cui, F., Hu, H.-h., Cui, W.-t., & Xie, Y. (2018). Seeding strategies for new product launch: The role of negative word-of-mouth. *PLOS ONE, 13*(11), e0206736. ✔
- Cui, G., Lui, H.-K., & Guo, X. (2012). The effect of online consumer reviews on new product sales. *International Journal of Electronic Commerce, 17*(1), 39–58. ✔
- Fainmesser, I. P., Lauga, D. O., & Ofek, E. (2021). Ratings, reviews, and the marketing of new products. *Management Science, 67*(11), 7023–7045. https://doi.org/10.1287/mnsc.2020.3848 ✔
- Garnefeld, I., Krah, T., Böhm, E., et al. (2021). Online reviews generated through product testing: Can more favorable reviews be enticed with free products? *Journal of the Academy of Marketing Science, 49*, 703–722. https://doi.org/10.1007/s11747-021-00770-6 ✔ **[check details: full author list]**
- Godes, D., & Mayzlin, D. (2009). Firm-created word-of-mouth communication: Evidence from a field test. *Marketing Science, 28*(4), 721–739. ✔
- Godes, D., & Silva, J. C. (2012). Sequential and temporal dynamics of online opinion. *Marketing Science, 31*(3), 448–473. ✔
- Goldenberg, J., Han, S., Lehmann, D. R., & Hong, J. W. (2009). The role of hubs in the adoption process. *Journal of Marketing, 73*(2), 1–13. ✔
- Gutierrez, P., & Gérardy, J.-Y. (2017). Causal inference and uplift modelling: A review of the literature. *Proceedings of Machine Learning Research, 67*, 1–13. ✔
- Haenlein, M., & Libai, B. (2017). Seeding, referral, and recommendation: Creating profitable word-of-mouth programs. *California Management Review, 59*(2), 68–91. ✔ **[check details: subtitle]**
- Hinz, O., Skiera, B., Barrot, C., & Becker, J. U. (2011). Seeding strategies for viral marketing: An empirical comparison. *Journal of Marketing, 75*(6), 55–71. ✔
- Hong, Y., & Pavlou, P. A. (2014). Product fit uncertainty in online markets: Nature, effects, and antecedents. *Information Systems Research, 25*(2), 328–344. ✔
- Hu, N., Pavlou, P. A., & Zhang, J. (2017). On self-selection biases in online product reviews. *MIS Quarterly, 41*(2), 449–471. ✔ **[check details: pages]**
- Kuksov, D., & Xie, Y. (2010). Pricing, frills, and customer ratings. *Marketing Science, 29*(5), 925–943. ✔
- Li, X., & Hitt, L. M. (2008). Self-selection and information role of online product reviews. *Information Systems Research, 19*(4), 456–474. ✔
- Libai, B., Muller, E., & Peres, R. (2013). Decomposing the value of word-of-mouth seeding programs: Acceleration versus expansion. *Journal of Marketing Research, 50*(2), 161–176. ✔
- Moe, W. W., & Trusov, M. (2011). The value of social dynamics in online product ratings forums. *Journal of Marketing Research, 48*(3), 444–456. ✔ **[check details: volume/pages]**
- Muchnik, L., Aral, S., & Taylor, S. J. (2013). Social influence bias: A randomized experiment. *Science, 341*(6146), 647–651. ✔ **[check details: pages]**
- Netzer, O., Feldman, R., Goldenberg, J., & Fresko, M. (2012). Mine your own business: Market-structure surveillance through text mining. *Marketing Science, 31*(3), 521–543. ✔ **[check details: pages]**
- Park, S., Shin, W., & Xie, J. (2021). The fateful first consumer review. *Marketing Science, 40*(3), 481–507. ✔
- Park, S., Shin, W., & Xie, J. (2023). Disclosure in incentivized reviews: Does it protect consumers? *Management Science*, 7009–7021. https://doi.org/10.1287/mnsc.2023.00930 ✔ **[check details: volume/issue]**
- Puranam, D., & Cardie, C. (2014). The enrollment effect: A study of Amazon's Vine program. In *Proceedings of the Joint Workshop on Social Dynamics and Personal Attributes in Social Media*. ACL. ✔
- Rogers, E. M. (2003). *Diffusion of innovations* (5th ed.). Free Press. ✔
- Salganik, M. J., Dodds, P. S., & Watts, D. J. (2006). Experimental study of inequality and unpredictability in an artificial cultural market. *Science, 311*(5762), 854–856. ✔ **[check details: pages]**
- Simester, D., Timoshenko, A., & Zoumpoulis, S. I. (2020). Targeting prospective customers: Robustness of machine-learning methods to typical data challenges. *Management Science, 66*(6), 2495–2522. ✔
- Tucker, C., & Zhang, J. (2011). How does popularity information affect choices? A field experiment. *Management Science, 57*(5), 828–842. ✔ **[check details: pages]**

### H. Entrepreneurship and platform reputation (Paper B)

- Aldrich, H. E., & Fiol, C. M. (1994). Fools rush in? The institutional context of industry creation. *Academy of Management Review, 19*(4), 645–670. ✔ **[check details: pages]**
- Blank, S. (2013). Why the lean start-up changes everything. *Harvard Business Review, 91*(5), 63–72. ✔ **[check details: pages]**
- Cabral, L., & Hortaçsu, A. (2010). The dynamics of seller reputation: Evidence from eBay. *Journal of Industrial Economics, 58*(1), 54–78. ✔ **[check details: volume/pages]**
- Camuffo, A., Cordova, A., Gambardella, A., & Spina, C. (2020). A scientific approach to entrepreneurial decision making: Evidence from a randomized control trial. *Management Science, 66*(2), 564–586. ✔ **[check details: pages]**
- Chalmers, D., MacKenzie, N. G., & Carter, S. (2021). Artificial intelligence and entrepreneurship: Implications for venture creation in the fourth industrial revolution. *Entrepreneurship Theory and Practice, 45*(5), 1028–1053. ✔
- Connelly, B. L., Certo, S. T., Ireland, R. D., & Reutzel, C. R. (2011). Signaling theory: A review and assessment. *Journal of Management, 37*(1), 39–67. ✔ **[check details: pages]**
- Eisenmann, T. R., Ries, E., & Dillard, S. (2012). *Hypothesis-driven entrepreneurship: The lean startup* (Background Note 812-095). Harvard Business School. ✔
- Freeman, J., Carroll, G. R., & Hannan, M. T. (1983). The liability of newness: Age dependence in organizational death rates. *American Sociological Review, 48*(5), 692–710. ✔ **[check details: pages]**
- Liang, C., Hong, Y., & Gu, B. (2025). Monitoring and the cold start problem in digital platforms: Theory and evidence from online labor markets. *Information Systems Research, 36*(1), 600–620. ✔
- Obschonka, M., & Audretsch, D. B. (2020). Artificial intelligence and big data in entrepreneurship: A new era has begun. *Small Business Economics, 55*(3), 529–539. ✔ **[check details: pages]**
- Otis, N., Clarke, R., Delecourt, S., Holtz, D., & Koning, R. (2024). *The uneven impact of generative AI on entrepreneurial performance* (Harvard Business School Working Paper). ✔ A version appears in *Management Science* (DOI 10.1287/mnsc.2024.06909). **[check details: published version]**
- Pallais, A. (2014). Inefficient hiring in entry-level labor markets. *American Economic Review, 104*(11), 3565–3599. ✔ **[check details: pages]**
- Ries, E. (2011). *The lean startup*. Crown Business. ✔
- Stanton, C. T., & Thomas, C. (2016). Landing the first job: The value of intermediaries in online hiring. *Review of Economic Studies, 83*(2), 810–854. ✔
- Stinchcombe, A. L. (1965). Social structure and organizations. In J. G. March (Ed.), *Handbook of organizations* (pp. 142–193). Rand McNally. ✔ **[check details: pages]**
- Suchman, M. C. (1995). Managing legitimacy: Strategic and institutional approaches. *Academy of Management Review, 20*(3), 571–610. ✔ **[check details: pages]**
- von Hippel, E. (1986). Lead users: A source of novel product concepts. *Management Science, 32*(7), 791–805. ✔
- Zimmerman, M. A., & Zeitz, G. J. (2002). Beyond survival: Achieving new venture growth by building legitimacy. *Academy of Management Review, 27*(3), 414–431. ✔ **[check details: pages]**
