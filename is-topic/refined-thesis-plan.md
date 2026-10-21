# Refined thesis plan: Before the First Review

Merges yui's proposal *"Before the First Review: Evidence-Grounded Matching of New Products to the Customers They Genuinely Serve"* (17 Oct 2026) with the earlier project plan (`project-plan.md`) and the literature review (`literature-review.md`). **This file supersedes `project-plan.md`.** **Category switched to Beauty on 17 Oct 2026 (yui: "let's do beauty"); §12 holds the Beauty scope, data and costs, and the sections below are updated to match.** yui's proposal is treated as the main statement of intent; the earlier plan supplies the business and entrepreneurship side.

## 1. One-paragraph summary

New products have no reviews, so AI recommenders match them on **priors** (category, brand, memorised products, persuasive wording) rather than on the **evidence in the listing**. Wrong early matches hurt the new product itself: misfit first buyers return it and leave bad first reviews, and first reviews persist (Park, Shin & Xie 2021). The thesis (a) shows that current AI recommenders license matches on priors; (b) builds an evidence-seeking matcher that recommends only when every checkable need is supported by the listing, abstains otherwise, and bounds the unsupported recommendation rate (URR ≤ α); and (c) shows that evidence-supported first buyers predict a healthier review trajectory, especially for small, unknown brands. Every abstention becomes a specific listing fix for the seller.

## 2. Decisions where the two plans conflicted

| Question | Earlier plan | yui's proposal | **Decision** | Why |
|---|---|---|---|---|
| Core contribution | Fit-first seeding of first buyers (business-led) | Evidence-grounded matching with abstention and a URR guarantee (AI method) | **yui's method is the core.** Fit-first seeding becomes the business and entrepreneurship outcome built on top of it. | The method gives a sharper, testable novelty claim (*support, not accuracy*) that the literature review didn't cover; seeding alone overlaps with Fainmesser et al. 2021 and Wang et al. 2025. |
| Category | Skincare (Beauty_and_Personal_Care) | Appliances (dev), Home & Kitchen, Tools & Home Improvement | **Beauty is the main category** (yui, 17 Oct: "let's do beauty"; this reverses the earlier choice of yui's proposal categories). Dev: All_Beauty. Main: Beauty_and_Personal_Care, skin care. Held-out: Beauty_and_Personal_Care, hair care. Appliances is an optional cross-domain transfer test. See §12. | Beauty is where yui's data, the hackathon brief and the business case already are, and it is the category where prior licensing should be strongest (heavily marketed, brand-driven, well known to LLMs). The method still needs checkable constraints, so **scope is limited to attributes a listing can state and a parser can check**: skin type, hair type, scent / fragrance-free, item form, "free-from" claims, volume, SPF, count, and ingredient presence when an ingredient list exists. Experiential needs ("won't break me out", "feels light") stay out of scope. The cost is sparser evidence and noisier labels (§12.4). |
| Venue | PACIS / HICSS (IS) | NeurIPS 2027 main track | **NeurIPS 2027 main track is the primary target for the whole thesis** (updated 17 Oct, yui: "aim at NeurIPS track"). Fallback: NeurIPS Evaluations & Datasets track. Paper B (business outcome) is an optional follow-up after submission. See §10. | yui's explicit choice. The IS thesis document is built around the NeurIPS paper, with Paper B as an extra chapter if time allows. |
| Commercial action (Reinvent Commerce brief) | Target list, message, promotion, do-not-target | Recommend / reject / abstain with cited evidence; seller feedback | **Both, in one loop:** supported matches → launch target list; contradicted → do-not-target; abstain → "add this spec" fix for the seller. | This meets the brief's "useful commercial action" and "measurable effect" criteria without changing the method. |
| Forecasting rule (brief: no LLM-only prediction) | LLM extracts, logistic regression predicts | LLM verifier + conformal calibration | **Keep yui's design.** The decision rule is a logical conjunction over verified support labels, calibrated with conformal risk control; the trajectory analysis (H1–H3) uses regression. | Neither part is "LLM-only forecasting". State this explicitly in the brief write-up. |

## 3. Research questions and hypotheses

**Main question:** How can a new product find the customers it genuinely serves before it has reviews, popularity or an established brand?

| | Question / hypothesis | Paper |
|---|---|---|
| **RQ1 (diagnosis)** | Do AI recommenders match new products on listing evidence or on priors, brands and persuasive wording? | A |
| **RQ2 (method)** | Can an agent match on evidence alone, abstain when evidence is missing, and guarantee URR ≤ α? | A |
| **RQ3 (validation)** | Do evidence-based matches at launch predict which customers were satisfied after launch? | A |
| **H1 (marketing)** | Beauty products whose early verified buyers' checkable needs (skin type, hair type, scent, form, free-from, size) were evidence-supported by the listing have higher average ratings and verified review volume 6–12 months after launch, controlling for price, subcategory, listed attributes and brand size. Tested on the full Beauty_and_Personal_Care files, not the hackathon cohort (§12.2). | B |
| **H2 (marketing)** | Attribute-misfit statements in the first verified reviews ("too oily for my combination skin", "says unscented but smells strong", "smaller bottle than I expected", "not for curly hair") predict lower later ratings, more strongly than general negative sentiment (first-review persistence, Park et al. 2021). | B |
| **H3 (entrepreneurship)** | The H1 association is stronger for small or new brands (liability of newness). | B |
| **H4 (AI / IS)** | At the same contact budget, evidence-grounded targeting reaches more post-launch-satisfied buyers and fewer misfit buyers than popularity or prior-based (LLM / Recformer) targeting. | A (RQ3) + B |
| **H5 (AI-native operations)** | Turning abstentions into seller listing fixes raises coverage (more matchable customers) without raising URR. Simulate it by restoring hidden specs. | A |

H1–H5 replace the earlier skincare versions in `literature-review.md` §5.3; after the 17 Oct switch they are Beauty hypotheses again, now limited to checkable attributes (the literature review itself is maintained in its own thread). The theory anchors are unchanged: Li & Hitt 2008, Godes & Silva 2012, Muchnik et al. 2013, Park et al. 2021, Stinchcombe 1965, Zimmerman & Zeitz 2002.

## 4. Method (from yui's proposal, unchanged)

Need = conjunction of checkable constraints. Policy inspects listing fields, labels each constraint *entailed / contradicted / unresolved / conflicting*, and recommends only if all are entailed, rejects if any is contradicted, and abstains otherwise. The verifier is trained with counterfactual edits (evidence-sensitivity loss) and brand/popularity/marketing swaps (invariance loss). Acquisition is via RL, with a cost-ordered fallback. The URR bound comes from conformal risk control or Learn-then-Test. Base model: 7–8B open-weight + LoRA; frontier APIs as baselines. The theory, benchmark, baselines and ablations are as in the proposal.

**Added for Paper B (light):** for each new product, compute the share of its first *k* reviewers whose mined need is entailed / contradicted by the listing, and regress the 6–12-month rating and volume on it (H1–H3), with brand fixed effects and the sales-event natural experiment from `project-plan.md`.

## 5. Novelty statement (merged)

> AI recommenders can place new products near similar known items (UniSRec, Recformer, TIGER), select audiences for new items (Wang et al. 2025), and abstain with a bounded *error* rate (conformal abstention). Marketing research shows first reviews persist (Park et al. 2021) and that targeting well-matched early buyers helps in theory (Fainmesser et al. 2021). No work bounds the rate of recommendations that are not *supported* by listing evidence, shows that current recommenders license new-product matches on priors, or links evidence-supported early matching to the new product's review trajectory and to the liability of newness. This thesis does all three.

By field: **AI**: high (support guarantee and prior-licensing diagnosis). **Marketing**: moderate to high (empirical test of fit-based early targeting). **Entrepreneurship**: high (H3; seller feedback as cheap legitimacy-building).

## 6. Timeline (one project, two papers)

_Superseded by §10.5 (NeurIPS-first timeline with gates)._

| When | Work | Gate |
|---|---|---|
| Oct 2026 | Setup, feasibility count of parseable specs, EDA | |
| Nov 2026 | RQ1 pilot (2,000 products, 500 needs) | **Go / no-go 30 Nov** |
| Nov 2026–Jan 2027 | Theory drafts; benchmark and automatic labels (§11); mine misfit statements | |
| Feb–Mar 2027 | Method, guarantee, baselines; **Paper B regressions (H1–H3)** in parallel, reusing the mined needs | |
| Apr 2027 | Ablations, RQ3, H4–H5; write Paper A | |
| early May 2027 | NeurIPS 2027 submission (date to confirm when the call is out) | |
| after May | Paper B for PACIS or HICSS (check deadlines); thesis write-up combines both | |

If the pilot is a no-go, Paper B still stands on its own (H1–H3 need no new method), so the thesis is safe either way.

## 7. Citation check of the proposal

Checked against `literature-review.md` and quick web searches (titles and abstracts only).

**Confirmed:** Nestaas et al., *Adversarial Search Engine Optimization for LLMs*, ICLR 2025 ([ICLR](https://iclr.cc/virtual/2025/poster/28746)); CANOE, *Teaching LLMs to Maintain Contextual Faithfulness via Synthetic Tasks and RL* ([arXiv:2505.16483](https://arxiv.org/abs/2505.16483)); the "Cold-Start Retrieval Bottlenecks" paper exists as *Diagnosing and Mitigating Retrieval Bottlenecks in LLM-Based Cold-Start Recommendation* ([arXiv:2606.29947](https://arxiv.org/abs/2606.29947)); Timoshenko & Hauser 2019; Chevalier & Mayzlin 2006; Fleder & Hosanagar.

**Fix before sharing:**
1. **Missing closest work.** The proposal doesn't cite the three papers the literature review flagged as closest: Fainmesser, Lauga & Ofek 2021 (Management Science), Park, Shin & Xie 2021 (Marketing Science), and especially **Wang et al. 2025, *Item-centric Exploration for Cold Start Problem*** ([arXiv:2507.09423](https://arxiv.org/abs/2507.09423)), which selects users for new items. Add Wang et al. to the "New items" row and state the difference (support guarantee and evidence, not engagement).
2. **Missing guarantee citations.** The guarantee relies on conformal risk control and Learn-then-Test (Angelopoulos et al.), which aren't cited. Add them.
3. **The guarantee is only as good as its labels.** URR ≤ α holds against the labels used for calibration. If those come from the LLM verifier, the bound is on the verifier's judgement (see §11 for the no-annotator label design), not the truth. With no human annotators (§11), calibrate on labels known by construction plus deterministic spec labels, and bound the label error separately in Theory result 4.
4. **CANOE year.** The arXiv version is 2025; there appears to be an AAAI version. Cite the venue version.
5. **BLaIR venue.** The proposal says ACL 2026, but the literature review cites arXiv 2024 (Hou et al.). Confirm the ACL 2026 version and use one citation consistently in both files.
6. **"Never use `details` specs or post-launch reviews"** about Amazon Reviews 2023 users is too absolute. Write "we found no work that…".
7. **Fleder & Hosanagar** has no year: Management Science 2009.
8. **Unverified:** "Faithfulness-QA (2026)" and Cui, Lui & Guo 2012's venue (likely *International Journal of Electronic Commerce*). Confirm both.
9. **Not in the literature review yet:** He, Hollenbeck & Proserpio 2022; Kumar & Lakkaraju 2024; Nestaas et al.; UniSRec, Recformer, TIGER. The literature-review thread should add them so both documents cite the same set.

## 8. Novelty check per contribution (17 Oct 2026)

Based on web searches and abstract-level reading. Ratings: low / moderate / high.

| Contribution | Closest prior work (checked) | What's already done | What stays new | Rating |
|---|---|---|---|---|
| **C1. Prior-licensing diagnosis (RQ1)** | *Is Your LLM-as-a-Recommender Agent Trustable?* BiasRecBench ([arXiv:2603.17417](https://arxiv.org/abs/2603.17417)); Nestaas et al. ICLR 2025 ([link](https://iclr.cc/virtual/2025/poster/28746)); Lichtenberg et al., LLM popularity bias ([arXiv:2406.01285](https://arxiv.org/abs/2406.01285)); memorisation in generative recommenders ([arXiv:2606.17276](https://arxiv.org/abs/2606.17276)) | Injected brand, popularity and marketing cues already flip LLM recommender choices (BiasRecBench shows drops of up to 38 points). Memorisation in LLM recommenders is documented. | Testing what happens when evidence is **missing or vague** (does the model still recommend?), conjunctive checkable specs, **new products**, and a memorisation probe on Amazon listings. The bias-injection part alone isn't new. | **Moderate** (high if the missing/vague-evidence result is large) |
| **C2. Guarantee on support, not accuracy (URR ≤ α)** | Mohri & Hashimoto, *Language Models with Conformal Factuality Guarantees*, ICML 2024 ([PMLR](https://proceedings.mlr.press/v235/mohri24a.html)); Rubin-Toles et al., *Conformal LM Reasoning with Coherent Factuality*, ICLR 2025 ([PDF](https://proceedings.iclr.cc/paper_files/paper/2025/file/679fcceef65c3d855aa885bd024542c1-Paper-Conference.pdf)); Ravikumar, *Do LLM Recommenders Know When They're Hallucinating?* ([arXiv:2608.10008](https://arxiv.org/abs/2608.10008)) | **Conformal guarantees that retained claims are *entailed/supported* already exist for generated text.** Conformal abstention on confidence has been tried for LLM recommenders (catalog hallucination), and it barely helped (≤1.65 pp). | Applying support guarantees to **recommendation decisions** over a **conjunction** of constraints with a three-way recommend / reject / abstain rule, plus the separation result (calibrated ≠ grounded). Ravikumar's negative result is useful motivation. | **Moderate.** The proposal's line "our guarantee is on support, not accuracy" must cite Mohri & Hashimoto and say how it differs, or reviewers will. |
| **C3. Evidence-seeking acquisition policy** | EDDI (ICML 2019); AFABench ([arXiv:2508.14734](https://arxiv.org/abs/2508.14734)); *Shopping Companion* ([arXiv:2603.14864](https://arxiv.org/abs/2603.14864)), which rewards verifying product attributes against requirements | Cost-aware feature acquisition is a mature area. Shopping agents trained to check attributes exist, and "insufficient attribute verification" is already named as a failure mode. | Stopping on **support** rather than confidence, and the **VOI-blindness** theorem (myopic VOI never looks when the prior is strong). The theory is what carries this. | **Low to moderate** on method; **moderate** with Theorems 1–2 |
| **C4. Benchmark validated against post-launch reviews** | *ShoppingComp* ([arXiv:2511.22978](https://arxiv.org/abs/2511.22978)), 145 expert-curated instances with multi-constraint verification; Shopping MMLU ([arXiv:2410.20745](https://arxiv.org/abs/2410.20745)); ESCI shopping queries ([Amazon Science](https://www.amazon.science/code-and-datasets/shopping-queries-dataset-a-large-scale-esci-benchmark-for-improving-product-search)) | Multi-constraint shopping verification benchmarks exist, but they're small and expert-built, with no abstention metric or missing-info tests. | Large-scale **counterfactual evidence variants** (missing / vague / edited / conflicting / brand swap / marketing rewrite) on **new products**, with **post-launch review validation**. None of the found work does this. | **High**: the strongest contribution |
| **C5. Paper B: early-buyer fit → review trajectory** | Fainmesser, Lauga & Ofek 2021; Park, Shin & Xie 2021; Wang et al. 2025 ([arXiv:2507.09423](https://arxiv.org/abs/2507.09423)) (see `literature-review.md`) | Theory of targeting well-matched early buyers; first-review persistence; selecting users for new items. | An empirical test using spec-level fit/misfit, plus the small-brand moderation (H3). | **Moderate to high** (marketing); **high** (entrepreneurship) |

### Overall verdict
- **The combination is novel**; most individual pieces have close neighbours. For the NeurIPS main track, novelty will rest on **C4 (benchmark)** plus **Theorems 1–2** (calibration ≠ groundedness; VOI blindness). C2 needs careful positioning against conformal factuality.
- **Backup venue:** the **NeurIPS Datasets & Benchmarks track** fits C1 + C4 well if the method results are modest.
- **Must-add citations:** Mohri & Hashimoto 2024; Rubin-Toles et al. 2025; BiasRecBench; Shopping Companion; ShoppingComp; Ravikumar 2026; Wang et al. 2025; Fainmesser et al. 2021; Park et al. 2021.
- **Reword the claims:**
  - Not "first guarantee on support", but "first support guarantee for conjunctive recommendation decisions with abstention."
  - Not "AI recommenders are biased by brand", but "AI recommenders recommend new products *without evidence* (prior licensing), which bias-injection studies don't measure."

## 9. Raising the AI method's novelty to high

The current method pieces rate moderate (support guarantee) and low-to-moderate (acquisition) because of conformal factuality (Mohri & Hashimoto 2024) and attribute-verifying shopping agents. Two additions would make the method itself high-novelty. Both grow out of the new-product setting, so they don't change the dataset.

### A. Strategic sellers: a guarantee that holds when listings are written to game it
- **The gap:** existing support guarantees assume the evidence is fixed. Sellers aren't fixed: once a matcher is deployed, they rewrite listings (marketing rewrites, generative engine optimisation, vague words like "compact"). Prior work documents these attacks (Nestaas et al. 2025; Kumar & Lakkaraju 2024) but offers no defence with a guarantee.
- **The method:** show that the support-only decision rule is **robust by construction** to rewrites that add no checkable evidence. Persuasive text can't turn an *unresolved* constraint into *entailed*, so URR ≤ α survives a class of strategic edits. Formalise this as a guarantee under **strategic (performative) distribution shift**: calibrate on listings plus adversarially rewritten variants, and bound URR for any rewrite within the "no new evidence" class.
- **Disclosure result (theory):** under the abstain-unless-supported rule, a seller of a genuinely matching product maximises matches by **disclosing** the spec. Hiding or blurring it only causes abstention. This is the classic disclosure-unravelling logic (Grossman 1981; Milgrom 1981) applied to an AI matcher: the matcher makes honest, complete listings the seller's best response. It's a clean theorem connecting ML, economics and the seller-feedback loop.

### B. Two-sided guarantee: protect shoppers *and* new products
- **The gap:** abstention methods bound one risk (wrong or unsupported answers). For new products, too much abstention is also harmful, because a genuinely matching unfamiliar product never reaches its customers. That is the cold-start unfairness the thesis is about.
- **The method:** control two risks at once with multi-risk Learn-then-Test calibration:
  1. URR ≤ α (shopper protection), and
  2. the **exposure gap** (the difference in coverage of genuinely matching products between unfamiliar and established products) ≤ β (new-product protection).
- **Why it's novel:** it's a guarantee that the matcher doesn't systematically abstain more on small or new brands. That turns the entrepreneurship claim (H3) into a **formal method property**, which no recommender or abstention paper we found offers.

### Effect on the paper
- New headline: *"An evidence-grounded matcher with a support guarantee that is robust to strategic listings, induces truthful disclosure, and provably does not disadvantage new products."*
- AI method novelty: **moderate → high**. The C2 overlap with conformal factuality becomes background, not the contribution.
- Cost: two extra theory results (A: robustness + disclosure; B: two-risk calibration). B is a direct application of Learn-then-Test with two risks, so it's cheap. A's disclosure theorem is short. A's robustness bound needs a clean definition of the "no new evidence" rewrite class.
- Cut order: if time is short, keep B and A's disclosure theorem, and drop A's general robustness bound.

### Citations to add
Grossman 1981 (*JLE*, disclosure); Milgrom 1981 (*Bell J. Econ.*, "Good news and bad news"); Hardt et al. 2016 (strategic classification); Perdomo et al. 2020 (performative prediction); Angelopoulos et al. (Learn-then-Test; conformal risk control). These are well-known works; confirm the exact details when writing.

## 10. NeurIPS 2027 main-track plan (aligned with `.agents/neurips-2026-standard.md`)

NeurIPS 2026 rules are used as the quality bar. The 2027 call isn't out yet, so re-check the CfP and Handbook when they appear (deadlines, tracks and checklist change every year). The 2026 deadlines were 4 May (abstract) and 6 May (full paper), so plan for **early May 2027**. Meeting this standard raises the paper's rigour; it doesn't guarantee acceptance.

### 10.1 Track and contribution type
- **Track:** main track. **Contribution type: General.** It's a method with theory and experiments. "Theory" would drop the benchmark's weight, and "Use-Inspired" would shift reviewers to the commerce use case rather than the guarantee. Lock this in by the go/no-go gate (30 Nov); it can't be changed after submission.
- **Fallback:** Evaluations & Datasets track (that's its 2026 name; the proposal called it "Datasets & Benchmarks"). Use it if the method results are weak but the diagnosis + benchmark are strong. Only one track per paper, so decide at the March gate (§10.5).
- **Paper B** (seeding, H1–H3) and the business framing are **out of the NeurIPS paper**. They stay as a thesis chapter or a later IS/marketing paper. One sentence of motivation in the intro is enough.

### 10.2 What goes in the 9 pages
| Section | Content | Pages |
|---|---|---|
| Intro + running example | Prior licensing on a famous-brand moisturiser vs an unknown one; "cannot tell yet: state whether it is fragrance-free" | 1.0 |
| Problem setup | Conjunctive needs, support status, URR, two-sided objective | 1.0 |
| Diagnosis (RQ1) | Evidence ablations and counterfactual edits on frontier + open models; memorisation probe | 1.5 |
| Method | Verifier (counterfactual + invariance training), acquisition (fixed-order fallback allowed), decision rule, two-risk calibration | 1.5 |
| Theory | Thm 1 separation (calibrated ≠ grounded); Thm 2 VOI blindness; Thm 4 finite-sample URR + exposure-gap bound. Statements in the main text, proofs in the appendix | 1.0 |
| Experiments (RQ2, RQ3) | Main table vs. baselines, risk–coverage curves, ablations, post-launch validation, unfamiliar-vs-established split | 2.5 |
| Related work + limitations | Must cite conformal factuality, BiasRecBench, Shopping Companion, ShoppingComp, Wang et al. 2025 | 0.5 |

**Moved to the appendix:** Thm 3 (outcome training learns priors), the disclosure theorem (§9A), dataset card, label-construction protocol, full baseline tuning, compute ledger, extra categories.
**Cut from the NeurIPS paper:** §9A's general strategic-robustness bound, optional Thm 5, images, Boonthavorn data, market simulation, and Paper B.

### 10.3 Evidence the standard requires (team minimums, §4 of the standard)
- **Baselines:** the strongest published (Recformer/UniSRec; conformal abstention; context-aware decoding; CANOE-style faithfulness fine-tune; frontier LLM + ReAct agent) **plus a strong simple non-LLM baseline:** a regex/structured spec parser with rule-based matching. If this simple baseline already reaches low URR, the paper's story changes, so run it in the November pilot. Every baseline gets the **same tuning budget**.
- **Statistics:** mean ± std over **≥5 seeds** for trained parts; **bootstrap 95% CI** for API-model runs (state why). Use paired tests with multiple-comparison correction, and report effect sizes. Never write "significantly" without a test.
- **Ablations:** every claimed component (counterfactual loss, invariance loss, acquisition policy, conformal layer, exposure-gap constraint). Run sensitivity to α and β.
- **Generalisation:** All_Beauty (dev) → Beauty_and_Personal_Care skin care (main) → Beauty_and_Personal_Care hair care (held-out). Appliances as an optional cross-domain transfer test (shows the method is not beauty-specific).
- **Theory:** all assumptions stated, full proofs, and **an independent proof checker** (not the proof's author).
- **Failure cases:** a named error analysis (e.g. unit-conversion errors, conflicting title/spec, verifier misreads).
- **Efficiency:** inspection cost, latency, GPU-hours, API cost on the same setup; total project compute including failed runs.

### 10.4 Checklist items that need early action
| Item | Action | When |
|---|---|---|
| Licences (existing assets) | Confirm Amazon Reviews 2023 terms; release IDs, scripts and own labels only, never raw text | Oct |
| Human subjects / IRB | **N/A: no human annotators or participants** (yui, 17 Oct). Answer the crowdsourcing and IRB checklist items "N/A", with one line explaining that all labels are automatic (§11). Check with your university that using public review data needs no ethics approval | Oct |
| New assets | Dataset card, persistent ID, licence for the benchmark | Jan–Feb |
| LLM usage declaration | Log which models and agents produced which parts of the method; LLMs can't be authors | Ongoing |
| Double-blind | Anonymised code repo, no names or paths in code or git history | Apr |
| Reproducibility | One command from raw data to every table; a dry-run by someone else on a clean machine | Apr |
| Citations | Every reference checked by hand (the Handbook warns about hallucinated citations) | Apr |

### 10.5 Timeline with gates
| Dates | Work | Gate |
|---|---|---|
| 17–31 Oct 2026 | Beauty feasibility count on the full Beauty_and_Personal_Care metadata (§12.3 thresholds), EDA, licence check, choose contribution type | G0: Beauty data is feasible, or fall back to Home & Kitchen (§12.5) |
| Nov 2026 | RQ1 pilot (2,000 products, 500 needs; 1 open + 1 frontier model) **including the regex baseline** and the label-noise audit (§11.4) | **G1, 30 Nov: go / no-go** |
| Nov 2026–Jan 2027 | Theory drafts (Thms 1, 2, 4 + two-risk version); benchmark build; automatic label construction (§11) | G2, 31 Jan: benchmark frozen, theorem statements fixed |
| Feb–Mar 2027 | Verifier training, calibration, all baselines, ablations | **G3, 31 Mar: main results exist → decide main vs. Evaluations & Datasets track** |
| Apr 2027 | RQ3 post-launch validation, held-out category, writing, 2 internal mock reviews, proof check, reproducibility dry-run | G4, ~25 Apr: draft passes mock review |
| Early May 2027 | Abstract, then full paper (confirm 2027 dates) | Submit |
| After submission | Paper B (H1–H3) and the thesis chapter | |

### 10.6 Cut order if behind schedule
1. Market simulation, images, Boonthavorn data (already out)
2. The disclosure theorem → future work
3. RL acquisition → fixed cost-ordered inspection (the guarantee still holds)
4. Appliances cross-domain transfer test
5. Thm 3 → appendix sketch only
6. Hair-care held-out split → report All_Beauty + skin care only (state this as a limitation)

**Never cut:** the diagnosis (RQ1), the URR guarantee with its proof, the regex and conformal baselines, ≥5 seeds/CIs, the constructed-label calibration set with its noise audit (§11), and the post-launch validation. Without these, a main-track submission isn't credible.

### 10.7 What must be true by the deadline for a credible main-track submission
1. **The gap is real and large.** The pilot shows frontier LLMs often recommend when evidence is missing or vague, and the **regex baseline doesn't already solve the problem**.
2. **The guarantee holds empirically:** URR ≤ α on the held-out test set across seeds, calibrated on **constructed and deterministic** support labels, never on the LLM verifier's own labels (§11).
3. **The method beats the strongest baselines** on the risk–coverage frontier, with CIs that don't overlap at the main operating point, and without much higher abstention on unfamiliar products (exposure gap ≤ β).
4. **Theorems 1, 2 and 4 are proved** and independently checked.
5. **Post-launch validation shows signal:** launch-time decisions agree with later fit/misfit reviews better than the baselines' decisions do.
6. **Positioning is clean:** the paper explicitly distinguishes itself from conformal factuality (Mohri & Hashimoto 2024) and item-centric cold start (Wang et al. 2025).
7. **Submission hygiene:** 9 pages, anonymised code, checklist complete (human-subjects items N/A), every citation verified.

If 1 fails at G1, reframe (e.g. a negative-results or evaluation paper). If 2–3 fail at G3, switch to the Evaluations & Datasets track with the diagnosis + benchmark.

## 11. Labels without human annotators (decision 17 Oct: no human annotators)

The proposal's human gold set (500–1,000 pairs, 2–3 annotators) is **dropped**, and so is the IRB step. All labels are produced automatically. The URR guarantee stays valid, but **relative to these labels**, and the plan must say so plainly.

### 11.1 Three label sources, and what each is used for
| Label source | How it's made | Accuracy | Used for |
|---|---|---|---|
| **L1. Constructed labels (exact)** | Each benchmark item is *built* from a complete listing whose true spec comes from the hidden `details` field. The support status is known **by construction**: attribute removed → *unresolved*; "fragrance-free" replaced by "gentle" → *unresolved*; Skin Type edited to "Oily" against a "for dry skin" need → *contradicted*; volume edited to 1.7 fl oz against a "≥ 3 fl oz" need → *contradicted*; attribute inserted with its true value → *entailed* or *contradicted* by controlled-vocabulary or numeric comparison; title says "unscented" while the scent field says "Lavender" → *conflicting*. | Exact for the item as constructed. No judgement involved. | **Primary calibration set for URR**, plus training and main evaluation |
| **L2. Deterministic spec labels (natural listings)** | On unmodified listings, a rule-based parser reads the visible text (title, bullets, description), normalises units, and compares it with the need. The item is kept only when the visible text and the hidden `details` agree within tolerance, or when the spec is clearly absent from the visible text. Ambiguous items are dropped. | High but not perfect (parser errors). The error rate is estimated in §11.4. | Second calibration set; tests that results carry over from constructed to natural listings |
| **L3. Post-launch review labels (noisy)** | An LLM extracts attribute fit/misfit statements from later verified reviews of new products ("perfect for my dry skin", "smells strong for an unscented cream"). | Noisy and sparse. | **RQ3 validation only, never calibration** |

**Key rule:** the model being evaluated never produces its own calibration labels. The LLM verifier is the thing being calibrated, so its outputs can't also be the ground truth.

**Information hiding:** the matcher sees only the title, bullets and description. The `details` field stays hidden, because it's the source of truth for L1 and L2. This also stops a trivial "just read the details table" solution.

### 11.2 What the guarantee then covers (state this in the paper)
- **On constructed items (L1):** URR ≤ α holds exactly, with the usual finite-sample conformal / Learn-then-Test guarantee, for test items drawn from the same construction process. Assumption: calibration and test items are exchangeable.
- **On natural listings (L2):** the bound holds against parser labels. Because URR is a selective conditional risk, if parser errors occur at marginal rate ε, the **true URR is bounded by α + ε_rec(λ) ≤ α + ε / P(recommend)** (or bounded directly by evaluating ε on the selected/recommended subset). State this as a corollary of Theorem 4, report URR across values of ε, and condition calibration on minimum selection counts N_rec(λ) ≥ n_min to prevent coverage collapse.
- **On post-launch outcomes (L3):** no guarantee; these give correlational evidence only.

So the paper's claim becomes: *"a finite-sample guarantee on unsupported recommendations for constructed evidence variants, which transfers to natural listings up to the measured selective label-error rate ε_rec."* That's honest, mathematically sound, and addresses the selective-risk critique directly.

### 11.3 Making ε small and measurable without humans
- **Agreement filter:** keep a natural item only if (a) the parser finds the value in the visible text, (b) it matches `details` within tolerance, and (c) units are consistent. Drop the rest.
- **Two independent extractors:** run the rule-based parser and a separate LLM extractor (a different model family from the verifier). Their disagreement rate on kept items is an **estimate of ε** (and an upper bound if their errors are independent; state that assumption).
- **Consistency checks:** cross-check the same spec stated in two places (title vs. bullets), and cross-check physical plausibility (e.g. a 40 fl oz eye cream or SPF 150 is a parse error).
- **Post-launch check:** for products L2 marks as "entailed: fragrance-free", count how often later verified reviews say "strong smell / scented". A high rate signals parser or listing errors.
- **Optional author spot-check:** the authors themselves read ~100 random items to sanity-check the parser. This is normal debugging, not human-subjects research, so it needs no IRB. Report it as a sanity check, not as gold labels. Skip it if yui prefers zero manual reading.

### 11.4 Where reviewers will push back, and the answers
| Likely reviewer objection | Answer in the paper |
|---|---|
| "The guarantee only holds on synthetic variants." | It's exact there **by design**: constructed items are the controlled setting where support is unambiguous. The corollary extends it to natural listings with the measured ε, and RQ3 adds real outcomes. |
| "The parser labels may be wrong." | ε is estimated with two independent extractors plus consistency checks; results are reported across a range of ε, and the bound α + ε / P(recommend) is stated explicitly. |
| "The constructed variants don't look like real listings." | Variants are minimal edits of *real* listings (one spec removed or changed), not generated from scratch. Report results on natural L2 items separately, so reviewers can see any gap. |
| "Without human labels, how do you know 'entailed' means what a person would think?" | For checkable attributes from controlled vocabularies (skin type, hair type, scent, item form, free-from claims) and numbers (volume, SPF, count), entailment is a deterministic comparison, not a judgement call. That's exactly why the scope excludes experience attributes like "non-greasy" or "won't break me out". |
| "Beauty needs are mostly experiential, so the in-scope set is small." | Report the share of real early-review needs that are checkable (§12.3) and present the scope honestly. Abstaining on experiential needs is the intended behaviour, not a failure. |
| "Post-launch labels are LLM-extracted and noisy." | They're used only for validation, never for the guarantee, and the claim is correlational. |

### 11.5 What changes in the plan
- **Benchmark:** constructed variants (L1) become the core of the benchmark, which suits the NeurIPS evaluation angle well.
- **Scope gets tighter:** only constraints whose support can be decided deterministically: skin type, hair type, scent / fragrance-free, item form, free-from claims and certifications (from controlled vocabularies), volume, SPF and count (numeric), and ingredient presence or absence when an ingredient list is present. See §12.1.
- **Timeline:** no IRB wait. The time saved goes to the label-noise audit (§11.3) in the November pilot.
- **Checklist:** crowdsourcing and IRB items are "N/A: no human subjects; all labels are derived automatically from public data". The licence item still applies (Amazon Reviews 2023 terms).
- **Never-cut list:** replace "human gold set" with "L1 calibration set + ε audit".

## 12. Beauty as the main category (decision 17 Oct 2026)

yui chose Beauty ("let's do beauty"). NeurIPS 2027 main track and the no-annotator label design (§11) are unchanged. This section replaces the Appliances / Home & Kitchen / Tools scope everywhere in the plan.

### 12.0 Why Beauty: the same dataset as BLaIR
yui's reason for choosing Beauty (17 Oct): the thesis uses **the same dataset as BLaIR** (yui: "not a follow up but base on the same data set"). It is not a follow-up to BLaIR's method. BLaIR (Hou, Li, Fu, He, Yan, Chen & McAuley, *Bridging Language and Items for Retrieval and Recommendation*, ACL 2026; arXiv:2403.03952, 2024) is the paper that released Amazon Reviews 2023, and it also evaluates on All Beauty.

**What BLaIR does.** It pretrains RoBERTa-based sentence encoders (BLaIR-base 123M, BLaIR-large 354M, released) with a contrastive loss that pairs each review with its item's metadata, so a user's language and an item's listing text land in one embedding space. It evaluates on sequential recommendation (the arXiv text names **All Beauty**, Video Games and Office Products as domains, though its tables report Beauty, Games and Baby, so check which split to reuse), conventional product search (ESCI), and a new task, *complex product search*, with **Amazon-C4**: 21,223 queries written by ChatGPT from 5-star reviews of at least 100 characters, each paired with the reviewed item as ground truth, over a 1.06M-item pool. The ACL 2026 version adds a benchmark of 11 LLMs as semantic encoders. It doesn't study new-item cold start, evidence support or abstention.

**How the thesis differs.** BLaIR asks *"does the embedding retrieve the item this user liked?"* The thesis asks *"does this listing actually **support** this customer's need, and can the system abstain and bound the rate at which it doesn't?"* Three concrete differences:
1. **From similarity to support.** BLaIR scores a need–listing pair by cosine similarity, which rises with topical overlap even when the deciding attribute (fragrance-free, oily skin) is missing or contradicted. That is the prior-licensing failure RQ1 measures.
2. **From the reviewed item to the evidenced item.** Amazon-C4 treats the item the reviewer bought as the correct answer. The thesis labels support from the hidden `details` field instead (§11), so a match is correct only if the listing states the evidence.
3. **From ranking to a decision with a guarantee.** BLaIR always returns a ranked list. The thesis adds recommend / reject / abstain and the URR ≤ α guarantee.

**How BLaIR is used in the experiments.**
- **Baseline:** BLaIR-base/large as a zero-shot dense retriever over listing text (it embeds new items from metadata alone, so it applies at launch), with a similarity threshold for a "recommend" decision. Add a conformal threshold on BLaIR similarity as a second baseline, so the comparison isolates *support* vs *confidence*.
- **RQ1 probe:** run the evidence ablations (remove, blur, edit, brand-swap) on BLaIR scores as well as on LLMs. If BLaIR's similarity barely moves when the deciding attribute is removed, that is direct evidence for the diagnosis.
- **Need source:** reuse Amazon-C4's review-to-query recipe for Beauty, keeping only queries with at least one checkable constraint (§12.1), and compare against C4's original "reviewed item" labels. Check at G0 whether C4's item pool already covers Beauty.
- **Comparability:** use BLaIR's All_Beauty split and preprocessing where possible, so reviewers can match numbers to a published paper.

**Does this strengthen the case for Beauty against the costs in §12.4?** Partly. It adds a published, well-known starting point (an ACL 2026 paper from the dataset's own lab), released models as ready baselines, and an existing Beauty split. Reviewers will recognise the data and the baselines. It doesn't fix sparse listing evidence or noisy labels, because BLaIR never needed checkable attributes. The G0 thresholds and the fallback (§12.5) stay. One caution: BLaIR is a representation-learning paper and this is a guarantee paper, so the paper should say "uses the Amazon Reviews 2023 data released with BLaIR, and BLaIR as a baseline", not "extends BLaIR". The novelty claim stays the support guarantee, which also keeps the paper a NeurIPS paper rather than a retrieval-venue follow-up.

### 12.1 What a "checkable need" is in Beauty
A need is still a conjunction of constraints, but every constraint must come from this list. Anything else is out of scope and the matcher should abstain on it.

| Constraint type | Examples of a need | Where the listing states it | How support is decided |
|---|---|---|---|
| Skin type | "for oily skin", "safe for sensitive skin" | `details`: Skin Type; title, bullets | Controlled vocabulary (dry, oily, combination, normal, sensitive, all). "All skin types" entails any single skin type; record this rule in the dataset card |
| Hair type | "for curly hair", "fine hair" | `details`: Hair Type | Controlled vocabulary |
| Scent | "fragrance-free", "unscented", "lavender" | `details`: Scent; title | Vocabulary; "fragrance-free" is contradicted by any named scent |
| Item form | "a gel, not a cream", "spray" | `details`: Item Form | Vocabulary |
| Free-from and certifications | "paraben-free", "sulfate-free", "vegan", "cruelty-free" | `details`: Material Type Free; bullets | Vocabulary; absence of the claim is *unresolved*, never *contradicted* |
| Size and count | "at least 3 fl oz", "travel size", "pack of 2" | `details`: Item Volume, Unit Count; title | Numeric with unit normalisation (fl oz ↔ ml) |
| SPF | "SPF 30 or higher" | title, bullets | Numeric |
| Ingredients | "contains niacinamide", "no alcohol" | `details`: Active Ingredients / ingredient list (when present) | String match on a normalised INCI list; *unresolved* if no list |

The matcher sees only title, bullets and description; `details` stays hidden as the source of truth for L1 and L2 (§11.1).

### 12.2 Data
| Source | Role | Notes |
|---|---|---|
| Amazon Reviews 2023 **All_Beauty** (reviews + metadata) | Dev set and RQ1 pilot | Small category. The reviews file is already in the shared folder (`All_Beauty.jsonl`); the metadata file still has to be downloaded |
| Amazon Reviews 2023 **Beauty_and_Personal_Care** (reviews + metadata) | Main benchmark (skin care), held-out split (hair care), RQ3 post-launch validation, Paper B (H1–H3) | Very large; stream it rather than load it. Use the raw (0-core) files, never 5-core, so new products are kept. Split by subcategory path |
| **Hackathon cohort** `data/hackathon_beauty_gmv.csv` (see `data/README.md`) | Hackathon demo and a sanity check of the pipeline; not the thesis benchmark | 15,606 rows after dedup on (user_id, parent_asin). Too thin for H1: median product has one row, only 985 products have both a cold-start and a later row |
| Amazon Reviews 2023 **Appliances** | Optional cross-domain transfer test | Already in the shared folder (`Appliances.jsonl.gz`) |

Data rules carried over from `data/README.md`: dedup first; outcome metrics use `verified_purchase == True` only; `meta_rating_number` and `meta_average_rating` are 2023 snapshots and must never be launch-time features (usable only as popularity cues in RQ1 prompts); "GMV" in the cohort is rating-weighted list price, not observed sales.

### 12.3 G0 feasibility count (by 31 Oct)
On the full Beauty_and_Personal_Care metadata, count:
1. Products whose **visible** text and hidden `details` both state at least one in-scope attribute and agree (the L2 pool). Proceed if there are **≥ 20,000** such products with at least two attributes, enough for a 2,000-product pilot, a frozen benchmark and a held-out split.
2. The share of early verified reviews (first 10 per product) that state at least one **checkable** need or misfit. If it is under ~10%, RQ3 and H2 will be underpowered; report it either way, since reviewers will ask.
3. Per-attribute coverage, to fix which attributes go into the benchmark. In the hackathon cohort, coverage was: skin type 16%, scent 17%, hair type 17%, item form 48%, product benefits 13%, free-from 4%, active ingredients 2.4%. These are shares of a large category, so the absolute counts in the full file should still be large; G0 checks that.

### 12.4 What the switch costs
| Cost | Effect on the paper | Mitigation |
|---|---|---|
| **Sparse listing evidence** (most listings state few checkable attributes) | Higher abstention and lower coverage at a given α; the risk–coverage curves will look worse than in Home & Kitchen | Report coverage honestly. The abstain → "add this attribute" fix becomes the stronger part of the story (H5). Build L1 variants only from listings that state the attribute |
| **Experiential needs dominate real reviews** ("broke me out", "too greasy") | The in-scope share of real needs is smaller; RQ3 and H2 have fewer usable reviews | Measure the share at G0. Keep experiential needs as an explicit abstention class in the benchmark |
| **Vaguer vocabulary** ("gentle", "clean", "suitable for most skin") | The L2 parser is harder to get right, so ε is likely higher than for centimetres and litres | Controlled vocabularies, a "vague" class that maps to *unresolved*, and the two-extractor ε estimate (§11.3) |
| **Noisier misfit labels** (skin reactions have many causes) | L3 labels are noisier; post-launch validation is weaker | L3 is validation only; restrict to attribute-linked misfits (scent, size, skin type stated in the review) |
| **Promotional seeding at launch** (26–30% of early reviews are unverified vs 5% later) | Early-review outcomes are biased | Verified purchases only; report the unverified share as a descriptive result |
| **Health-adjacent claims** (SPF, acne, sensitive skin) | Ethics and broader-impact questions from reviewers | Treat SPF and "for sensitive skin" as listing claims being checked, not medical advice; say so in limitations |
| **One more download and a large file** | More preprocessing time in October | Stream the files; subcategory splits reduce working size |

**What the switch gains:** it puts the thesis directly on BLaIR's data, Beauty split and released models (§12.0). RQ1 should also show a bigger effect, because beauty is brand-driven, heavily marketed and well known to LLMs, so prior licensing has more room to show. The strategic-seller angle (§9A) fits better, since beauty listings are written to persuade. The thesis, the hackathon demo and Paper B now share one category and one data pipeline, and the entrepreneurship story (indie beauty brands against famous ones) is easy for readers to follow.

### 12.5 Fallback
If G0 fails (too few products with agreeing attributes, or almost no checkable needs in early reviews), keep Beauty for RQ1 (the diagnosis) and the hackathon, and move the benchmark and guarantee (RQ2) to Home & Kitchen, the previous main category. Decide this at G0, before the pilot, so the November go/no-go still tests the final setup.
