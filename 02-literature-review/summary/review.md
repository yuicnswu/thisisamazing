# Literature Review (Narrative)

*Stage 2 of [WORKFLOW.md](../../WORKFLOW.md). Narrative summary with APA citations covering every file in [`../wiki/`](../wiki/) (87 papers, listed in [`../index.md`](../index.md)). Update whenever a paper is added to `raw/` or `wiki/`. Last updated 2026-10-25 (section 10 added for the Beauty Market Research Agent; earlier: section 8 and the gap in section 9 for the repositioning, 2026-10-21).*

**Scope.** This review supports the thesis *Before the First Review*:
- **Paper A** (NeurIPS 2027) asks whether AI recommenders match new products to customers on listing **evidence** or on **priors**. It proposes a matcher that recommends only when every checkable constraint of a need is entailed by inspected evidence, abstains otherwise, and bounds the unsupported recommendation rate (URR).
- **Paper B** (PACIS/HICSS) asks whether evidence-supported fit among a new product's first buyers shapes its review trajectory.

**Corpus.** The wiki holds 87 papers. The first 40 were chosen as yui asked:
- 10 recent papers from peer-reviewed conferences.
- 20 papers with more than 100 verified citations: 14 AI and 6 marketing (70/30).
- 10 surveys.

Thirteen more were added on 2026-10-21 from the 2025–2026 field check, because they change what the thesis can claim (section 8). Thirty-four more were added on 2026-10-25 for the Beauty Market Research Agent plan (section 10).

The fuller positioning, including 2026 preprints that are not in this corpus, is in [`is-topic/literature-review.md`](../../is-topic/literature-review.md).

## 1. Maps of the field

Two surveys organize LLM-based recommendation:
- Zhao et al. (2024) group methods by pre-training, fine-tuning and prompting.
- Wu et al. (2024) split them into discriminative and generative paradigms.

Both flag hallucination and trustworthiness as open problems, but neither asks whether a recommendation is supported by what the item's listing says.

W. Zhang et al. (2025) trace cold-start recommendation from content features to the "world knowledge" of LLMs. They present that knowledge as a solution, which is exactly the prior that Paper A puts under test.

The closest survey is Wang et al. (2026). It reviews more than 200 studies on trustworthy LLM recommendation and treats factuality (grounding, hallucinated items) and robustness (poisoning, textual attacks) as central risks. In the parts we could read, it does not discuss abstention or any guarantee on support.

Three general surveys complete the map:
- Xu et al. (2024) classify knowledge conflicts.
- Y. Zhang et al. (2025) classify hallucination.
- Wen et al. (2025) review when LLMs should abstain.

Campos et al. (2024) review conformal prediction in NLP. **No survey in the corpus covers recommendation decisions for new products that must be supported by listing evidence, with abstention and a bound on unsupported decisions.**

## 2. How recommenders handle new products

History-based recommenders disadvantage new products. Fleder and Hosanagar (2009) show that common recommender designs can reduce aggregate sales diversity, because they lean on past sales.

Later work places new items by content. UniSRec represents items by their text so that representations transfer across domains and to unseen items (Hou et al., 2022). TIGER gives items semantic IDs built from content embeddings and generates the next item's ID (Rajput et al., 2023). P5 recasts many recommendation tasks as text-to-text language processing (Geng et al., 2022).

LLMs are competitive near cold start when preferences are stated in language (Sanner et al., 2023). Amazon Reviews 2023 and the BLaIR encoders link item metadata with review language at scale (Hou et al., 2026).

All of these methods place a new item **by similarity** to what is already known. A semantic ID, a text embedding or an LLM's recollection of similar products is a prior. None of them checks whether the new listing actually supports a specific need, and none abstains when it does not. Paper A builds on Hou et al. (2026) for data, and uses the `details` specification fields as hidden ground truth.

## 3. Evidence versus memory

Language models store a great deal of relational knowledge in their parameters (Petroni et al., 2019). When the context contradicts that memory, QA models often answer from memory instead (Longpre et al., 2021). When the counter-evidence is coherent, LLMs are receptive to it, but they show confirmation bias toward memory once evidence is mixed (Xie et al., 2024).

Three kinds of fix push models toward the context:
- **Decoding:** context-aware decoding contrasts outputs with and without the context (Shi et al., 2024).
- **Training:** CANOE trains faithfulness with synthetic tasks and reinforcement learning (Si et al., 2026).
- **Data:** counterfactually augmented data teaches models the features that actually determine a label (Kaushik et al., 2020). Paper A borrows this idea for its evidence-sensitivity loss, but generates the variants automatically from specifications instead of with human editors.

Support can also be scored automatically. ALCE uses entailment to check whether citations support generated statements (Gao et al., 2023).

This literature has two gaps for Paper A. First, it is almost entirely about QA and generation. Second, it treats evidence as *present but conflicting*. The typical new-product failure is evidence that is **missing** or **vague**: a listing that never states its width.

## 4. Abstention and distribution-free guarantees

The closest classic analogue to "the listing does not say" is SQuAD 2.0, which adds unanswerable questions and showed that strong readers could not reliably detect missing answers (Rajpurkar et al., 2018).

Selective classification gives deep networks a reject option with guaranteed risk at the achieved coverage (Geifman & El-Yaniv, 2017). Conformal risk control generalizes split conformal prediction to bound the expected value of any monotone loss (Angelopoulos et al., 2024).

For LLMs, two papers move from *error* to *support*:
- Conformal factuality removes claims until the retained output is entailed with probability at least 1 − α (Mohri & Hashimoto, 2024).
- Coherent factuality extends this to reasoning chains, where each retained step must follow from earlier ones (Rubin-Toles et al., 2025).

These are the theoretical anchors for Paper A, and also its main novelty threat. Paper A's guarantee differs in three ways:
- **Object:** a recommendation decision over a conjunction of constraints, not a set of generated claims.
- **Output space:** recommend, reject or abstain.
- **Labels:** because the project uses no human annotators, Paper A calibrates on automatic spec labels and post-launch review labels, and states its guarantee relative to them.

## 5. Acquiring missing information

When evidence is missing, a matcher can look for it. EDDI chooses the next feature to acquire by expected information gain (Ma et al., 2019). ReAct interleaves reasoning with lookups, and was tested on a web-shopping task (Yao et al., 2023). AR-Bench shows that current LLMs often fail to ask for the information they need, and that search and post-training give only modest gains (Zhou et al., 2025).

These methods stop when confidence is high enough. Paper A's argument is that strong priors make confidence high before any evidence is read, so a matcher should stop on **support** instead.

## 6. Manipulation of LLM recommenders

Third-party content can steer LLM search and product selection (Nestaas et al., 2025). Small cognitive-bias edits to product descriptions, such as social proof or scarcity, shift LLM recommendations, and defensive prompts do not reliably stop this (Filandrianos et al., 2025).

Both studies add misleading cues. Paper A also tests *absent* evidence. Its decision rule cannot be licensed by unverifiable marketing claims, which makes it a structural defence rather than a filter.

## 7. Why early fit matters for a new product (Paper B)

Diffusion research holds that early adopters drive later adoption through imitation (Bass, 1969). Early signals persist: a single randomized up-vote produced lasting rating inflation (Muchnik et al., 2013). Electronic word of mouth correlates with sales, and volume matters more than valence (Babić Rosario et al., 2016).

Early reviews are not neutral, though:
- Early buyers self-select, so early ratings are biased and then drift (Li & Hitt, 2008).
- Ratings tend to fall as later buyers turn out to be less well matched (Godes & Silva, 2012).

Fit is a distinct uncertainty from quality. It raises returns and lowers satisfaction, and product information can reduce it (Hong & Pavlou, 2014). Customer needs can be mined from reviews as well as from interviews (Timoshenko & Hauser, 2019). Feature-level opinions in reviews also affect demand (Archak et al., 2011).

Seeding programmes are usually judged by reach rather than by the reviews that seeded customers write (Haenlein & Libai, 2017). Together these studies imply, but do not test, that choosing first buyers whose needs a product verifiably meets protects its early reputation. That is Paper B's question.

## 8. 2025–2026 work that moved the field

Thirteen recent papers change what Paper A can claim. Most are preprints.

**The brand-bias diagnosis is published.** Chu and Hou (2026) show that, on skincare, GPT-4o-mini, Claude Sonnet and Gemini 3 Flash recommend the well-known brand every time when specifications are identical. A rating edge under 0.1 stars, or authority-style copy including fabricated clinical claims, breaks that dominance. Hou is BLaIR's first author, so this sits on the thesis's own category and data lineage. Paper A's pilot found something different in a different task: when the model accepts or rejects one listing for one need, brand-plus-hype swaps moved decisions both ways about equally, and the operative prior was product type. RQ1 can therefore be a reconciliation of the two designs, not a discovery of brand bias.

**Risk-controlled recommendation is a known template.** De Toni et al. (2025) calibrate a recommender's threshold with conformal risk control so that the expected share of unwanted items stays at or below a target. Conformal abstention for LLM hallucination exists in expectation and high-probability forms (Abbasi-Yadkori et al., 2024), and group-conditional conformal factuality is standard machinery (Cherian et al., 2024). Combined with Mohri and Hashimoto (2024), this makes "URR ≤ α" a method component of Paper A rather than its contribution. Even the natural upgrade, a bound on the *true* error rate that combines a small gold set with many proxy labels, has a general form already: semi-supervised risk control via prediction-powered inference gives finite-sample (α, δ) control whatever the quality of the imputed labels (Einbinder et al., 2024). It is stated for i.i.d. data and does not give a general theory for ratio-type selective risks.

**Confidence does not certify grounding.** Ravikumar (2026) audits four LLM recommenders, one on Amazon Reviews 2023. Verbalised confidence stays at 67–86 while catalog-hit rates range from 39% to 99%, and conformal abstention on that confidence reduces hallucination by at most 1.65 points. Chen et al. (2026) find that conformal factuality filtering often leaves little useful content at high factuality, breaks under shift and distractors, and that small entailment verifiers match LLM confidence scorers at over 100× lower cost. Together these papers support the pilot's central finding (confidence and strict prompting certify nothing at α = 0.10, while a quote-checked verifier does) and set two obligations: report informativeness next to the risk, and compare against an entailment verifier.

**Shopping benchmarks assume the information exists.** ShoppingBench scores GPT-4.1 at 48.2% success on intent-grounded tasks (J. Wang et al., 2025). Shopping Companion finds GPT-5 below 70% and names insufficient checking of product attributes against requirements as a main failure (Yu et al., 2026). ShopSimulator penalises buying without confirming details but scores each instruction against one gold product (P. Wang et al., 2026). None of the three has an outcome for "the listing does not say", which is the label Paper A's benchmark is built on.

**Sellers will optimise for AI shoppers, and nobody checks truth.** In randomised audits, simple query-specific description edits raise a seller's market share with AI shopping agents (Allouah et al., 2025). E-GEO rewrites Amazon listings to climb LLM rerankers, with gains of about half a rank position for the best rewriters, and does not check whether the rewrites stay faithful to the product (Bagga et al., 2025). This is the opening for the merchant-fix loop: an abstention becomes a request to *disclose* a checkable fact, which the verifier then rewards only if the listing states it.

**Needs mined from reviews are not new.** Mender conditions a generative recommender on preferences mined from users' reviews, including on Amazon Beauty (Paischer et al., 2024). Paper A's difference is the next step: each mined need is checked against the listing, and can come back unresolved.

## 9. Gap (revised 2026-10-21)

Across the 53 papers, prior work does six things:
- places new items by similarity (Hou et al., 2022; Rajput et al., 2023; Sanner et al., 2023);
- shows that models prefer memory to context and known brands to unknown ones (Chu & Hou, 2026; Longpre et al., 2021; Xie et al., 2024);
- bounds error, unwanted items or the support of generated text, including with proxy labels (Angelopoulos et al., 2024; De Toni et al., 2025; Einbinder et al., 2024; Mohri & Hashimoto, 2024);
- shows that confidence-based abstention barely helps LLM recommenders (Ravikumar, 2026);
- documents seller manipulation of LLM rankers without checking truth (Allouah et al., 2025; Bagga et al., 2025; Nestaas et al., 2025);
- shows that early, well-matched reviews matter (Godes & Silva, 2012; Li & Hitt, 2008; Muchnik et al., 2013).

No paper found does any of the following:
- a benchmark that scores **abstaining when the listing is silent** on a need, with counterfactual edits of real listings (missing, vague, paraphrased, contradicted) and multi-constraint needs;
- shows that a recommender's **groundedness can be certified** by checkable quoted evidence when its confidence cannot, at the same α and on the same items;
- turns abstentions into **demand-ranked, truthful disclosure requests** to sellers and measures what disclosure does to coverage, risk and new-product exposure;
- a risk guarantee for **selective conjunctive** recommendation decisions on newly launched items, with one-sided label noise;
- links the evidence-supported fit of a product's first buyers to its review trajectory.

## 10. Related work for the Beauty Market Research Agent (added 2026-10-25)

The agent turns Sephora (then Amazon All Beauty) reviews and listings into a merchant research brief, and asks whether adaptive investigation beats a fixed analytical workflow on evidence accuracy, unsupported claims, coverage, time and cost. Thirty-four papers were added for this plan. They fall into six groups.

**Review mining is an old marketing-research idea; LLMs are the new step.** Feature-based review summarisation, with counts of positive and negative opinions per feature, goes back to Hu and Liu (2004). Marketing adopted it as automated market research: Lee and Bradlow (2011) derive attributes and market structure from review text, Netzer et al. (2012) map brands and associations from forum posts, and Tirunillai and Tellis (2014) extract quality dimensions with LDA. Berger et al. (2020) set the validity standards that text-derived marketing measures must meet. Timoshenko and Hauser (2019) showed that reviews can replace interviews for needs discovery, and their follow-up finds that fine-tuned LLMs formulate customer needs as well as professional analysts (Timoshenko et al., 2025). The brief's "findings with calculated counts and quotations" is therefore aspect-based opinion summarisation with traceable evidence, an established output with a new way of producing it.

**LLMs in market research: accepted when validated, doubted as synthetic respondents.** Marketing journals now publish LLM-based research when it is checked against human data. LLM perceptual maps agree with survey maps (Li et al., 2024), and AI-human hybrids raise efficiency across research stages (Arora et al., 2025). Synthetic respondents are less reliable: LLM willingness-to-pay looks plausible but generalises poorly to new features (Brand et al., 2023), LLM time preferences differ from humans' (Goli & Singh, 2024), and silicon samples suit pretesting rather than final inference (Sarstedt et al., 2024). The agent sidesteps this debate because it analyses real customer text, but it inherits the validation duty, and Goli and Singh (2024) are a reason to keep the LLM's own priors out of the counts.

**Data-analysis agents exist, but are scored on known answers.** Benchmarks test agents on CSV questions with exact answers (Hu et al., 2024), on discovery tasks drawn from published analyses (Majumder et al., 2025), on the space of expert analysis decisions (Gu et al., 2024) and, closest to the brief, on end-to-end business analytics with planted insights (Sahu et al., 2025). Agent designs re-plan as results arrive (Hong et al., 2025) or reuse past expert cases to cut cost (Guo et al., 2024). Two lessons transfer. Agents that interact with data choose more varied, expert-like analyses (Gu et al., 2024), which supports the adaptive arm; and the best systems still solve only a minority of open discovery tasks (Majumder et al., 2025), which supports keeping calculation in Python.

**Adaptive is not obviously better than fixed.** A fixed three-step pipeline beat many autonomous software agents at low cost (Xia et al., 2025), and simple baselines matched state-of-the-art agents once cost was counted (Kapoor et al., 2025). Adaptive routing between strategies by question complexity improves the accuracy-efficiency trade-off (Jeong et al., 2024), workflows can be optimised offline (Zhang et al., 2025), and model cascades cut cost sharply (Chen et al., 2024). For the RQ this means three things: the fixed workflow must be a strong, carefully built baseline; results must be reported as a cost-accuracy frontier on held-out merchant questions; and a router that chooses between fixed and adaptive investigation is a natural third arm.

**Evidence accuracy and unsupported claims have standard measures.** Attribution to identified sources gives a definition of a supported statement (Rashkin et al., 2023). Long outputs can be split into atomic facts and scored for precision (Min et al., 2023), and citations can be scored for recall and precision (Liu et al., 2023), which revealed that fluent, useful-looking answers are often poorly supported. Small checkers match GPT-4 at grounding checks at a fraction of the cost (Tang et al., 2024). For whole reports, STORM researches before writing and shows typical failures such as over-associating unrelated facts (Shao et al., 2024), and DeepResearch Bench scores report quality and citation accuracy separately (Du et al., 2026). LLM judges agree with humans about as often as humans agree with each other, but prefer longer answers (Zheng et al., 2023), a bias that would favour the adaptive arm.

**Design science and human-AI evidence frame the IS contribution.** IS venues expect the agent to be presented as a design science artifact with rigorous evaluation (Hevner et al., 2004), following a problem-to-evaluation process (Peffers et al., 2007), and positioned by its knowledge contribution; a working demo alone is routine design (Gregor & Hevner, 2013). Field evidence on generative AI at work sets expectations for the later merchant study: gains are large inside the AI's capability frontier and negative outside it (Dell'Acqua et al., 2023), and largest for less experienced workers (Brynjolfsson et al., 2025).

**Gap for the agent.** None of the papers found does the following:
- compare adaptive and fixed investigation for **marketing research from customer reviews**, on evidence accuracy, unsupported claims, coverage and cost together;
- score a merchant research brief at the level of **atomic findings backed by computed counts and quoted reviews, including opposing quotations**;
- validate review-derived findings on a **second retailer** (Sephora to Amazon All Beauty);
- test whether a traceable brief changes a product or marketing manager's decision, rather than only their speed.

## References

- Abbasi-Yadkori, Y., Kuzborskij, I., Stutz, D., György, A., Fisch, A., Doucet, A., Beloshapka, I., Weng, W.-H., Yang, Y.-Y., Szepesvári, C., Cemgil, A. T., & Tomasev, N. (2024). *Mitigating LLM hallucinations via conformal abstention* (arXiv:2405.01563). arXiv.
- Allouah, A., Besbes, O., Figueroa, J. D., Kanoria, Y., & Kumar, A. (2025). *What is your AI agent buying? Evaluation, biases, model dependence, & emerging implications for agentic e-commerce* (arXiv:2508.02630). arXiv.
- Angelopoulos, A. N., Bates, S., Fisch, A., Lei, L., & Schuster, T. (2024). Conformal risk control. In *International Conference on Learning Representations*.
- Archak, N., Ghose, A., & Ipeirotis, P. G. (2011). Deriving the pricing power of product features by mining consumer reviews. *Management Science, 57*(8), 1485–1509. https://doi.org/10.1287/mnsc.1110.1370
- Arora, N., Chakraborty, I., & Nishimura, Y. (2025). AI-human hybrids for marketing research: Leveraging large language models (LLMs) as collaborators. *Journal of Marketing, 89*(2), 43–70. https://doi.org/10.1177/00222429241276529
- Babić Rosario, A., Sotgiu, F., De Valck, K., & Bijmolt, T. H. A. (2016). The effect of electronic word of mouth on sales: A meta-analytic review of platform, product, and metric factors. *Journal of Marketing Research, 53*(3), 297–318. https://doi.org/10.1509/jmr.14.0380
- Bagga, P. S., Farias, V. F., Korkotashvili, T., Peng, T., & Wu, Y. (2025). *E-GEO: A testbed for generative engine optimization in e-commerce* (arXiv:2511.20867). arXiv.
- Bass, F. M. (1969). A new product growth for model consumer durables. *Management Science, 15*(5), 215–227. https://doi.org/10.1287/mnsc.15.5.215
- Berger, J., Humphreys, A., Ludwig, S., Moe, W. W., Netzer, O., & Schweidel, D. A. (2020). Uniting the tribes: Using text for marketing insight. *Journal of Marketing, 84*(1), 1–25. https://doi.org/10.1177/0022242919873106
- Brand, J., Israeli, A., & Ngwe, D. (2023). *Using LLMs for market research* (Harvard Business School Working Paper No. 23-062). https://papers.ssrn.com/abstract=4395751
- Brynjolfsson, E., Li, D., & Raymond, L. (2025). Generative AI at work. *The Quarterly Journal of Economics, 140*(2), 889–942. https://doi.org/10.1093/qje/qjae044
- Campos, M., Farinhas, A., Zerva, C., Figueiredo, M. A. T., & Martins, A. F. T. (2024). Conformal prediction for natural language processing: A survey. *Transactions of the Association for Computational Linguistics, 12*, 1497–1516. https://doi.org/10.1162/tacl_a_00715
- Chen, L., Zaharia, M., & Zou, J. (2024). FrugalGPT: How to use large language models while reducing cost and improving performance. *Transactions on Machine Learning Research*.
- Chen, Y., Chen, D., Chikodikar, S. M., Yin, C. H., & Vinayak, R. K. (2026). *Is conformal factuality for RAG-based LLMs robust? Novel metrics and systematic insights* (arXiv:2603.16817). arXiv.
- Cherian, J. J., Gibbs, I., & Candès, E. J. (2024). *Large language model validity via enhanced conformal prediction methods* (arXiv:2406.09714). arXiv.
- Chu, X., & Hou, Y. (2026). *Incumbent advantage: Brand bias and cognitive manipulation dynamics in LLM recommendation systems* (arXiv:2606.17443). arXiv.
- De Toni, G., Purificato, E., Gomez, E., Lepri, B., Passerini, A., & Consonni, C. (2025). You don't bring me flowers: Mitigating unwanted recommendations through conformal risk control. In *Proceedings of the 19th ACM Conference on Recommender Systems*.
- Dell'Acqua, F., McFowland, E., III, Mollick, E. R., Lifshitz-Assaf, H., Kellogg, K., Rajendran, S., Krayer, L., Candelon, F., & Lakhani, K. R. (2023). *Navigating the jagged technological frontier: Field experimental evidence of the effects of AI on knowledge worker productivity and quality* (Harvard Business School Working Paper No. 24-013). https://doi.org/10.2139/ssrn.4573321
- Du, M., Xu, B., Zhu, C., Wang, X., & Mao, Z. (2026). DeepResearch Bench: A comprehensive benchmark for deep research agents. In *International Conference on Learning Representations*.
- Einbinder, B.-S., Ringel, L., & Romano, Y. (2024). *Semi-supervised risk control via prediction-powered inference* (arXiv:2412.11174). arXiv.
- Filandrianos, G., Dimitriou, A., Lymperaiou, M., Thomas, K., & Stamou, G. (2025). Bias beware: The impact of cognitive biases on LLM-driven product recommendations. In *Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing* (pp. 22397–22426).
- Fleder, D., & Hosanagar, K. (2009). Blockbuster culture's next rise or fall: The impact of recommender systems on sales diversity. *Management Science, 55*(5), 697–712.
- Gao, T., Yen, H., Yu, J., & Chen, D. (2023). Enabling large language models to generate text with citations. In *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing*.
- Geifman, Y., & El-Yaniv, R. (2017). Selective classification for deep neural networks. In *Advances in Neural Information Processing Systems 30*.
- Geng, S., Liu, S., Fu, Z., Ge, Y., & Zhang, Y. (2022). Recommendation as language processing (RLP): A unified pretrain, personalized prompt & predict paradigm (P5). In *Proceedings of the 16th ACM Conference on Recommender Systems*.
- Godes, D., & Silva, J. C. (2012). Sequential and temporal dynamics of online opinion. *Marketing Science, 31*(3), 448–473.
- Goli, A., & Singh, A. (2024). Frontiers: Can large language models capture human preferences? *Marketing Science, 43*(4), 709–722. https://doi.org/10.1287/mksc.2023.0306
- Gregor, S., & Hevner, A. R. (2013). Positioning and presenting design science research for maximum impact. *MIS Quarterly, 37*(2), 337–355. https://doi.org/10.25300/MISQ/2013/37.2.01
- Gu, K., Shang, R., Jiang, R., Kuang, K., Lin, R.-J., Lyu, D., Mao, Y., Pan, Y., Wu, T., Yu, J., Zhang, Y., Zhang, T. M., Zhu, L., Merrill, M. A., Heer, J., & Althoff, T. (2024). BLADE: Benchmarking language model agents for data-driven science. In *Findings of the Association for Computational Linguistics: EMNLP 2024*.
- Guo, S., Deng, C., Wen, Y., Chen, H., Chang, Y., & Wang, J. (2024). DS-Agent: Automated data science by empowering large language models with case-based reasoning. In *Proceedings of the 41st International Conference on Machine Learning* (PMLR 235).
- Haenlein, M., & Libai, B. (2017). Seeding, referral, and recommendation: Creating profitable word-of-mouth programs. *California Management Review, 59*(2), 68–91.
- Hevner, A. R., March, S. T., Park, J., & Ram, S. (2004). Design science in information systems research. *MIS Quarterly, 28*(1), 75–105. https://doi.org/10.2307/25148625
- Hong, S., Lin, Y., Liu, B., Liu, B., Wu, B., Zhang, C., Li, D., Chen, J., Zhang, J., Wang, J., Zhang, L., Zhang, L., Yang, M., Zhuge, M., Guo, T., Zhou, T., Tao, W., Tang, X., Lu, X., Zheng, X., Liang, X., Fei, Y., Cheng, Y., Wang, Y., Gou, Z., Xu, Z., & Wu, C. (2025). Data Interpreter: An LLM agent for data science. In *Findings of the Association for Computational Linguistics: ACL 2025*.
- Hong, Y., & Pavlou, P. A. (2014). Product fit uncertainty in online markets: Nature, effects, and antecedents. *Information Systems Research, 25*(2), 328–344.
- Hou, Y., Li, J., Fu, X., He, Z., Yan, A., Chen, X., & McAuley, J. (2026). Bridging language and items for retrieval and recommendation: Benchmarking LLMs as semantic encoders. In *Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)* (pp. 3251–3265).
- Hou, Y., Mu, S., Zhao, W. X., Li, Y., Ding, B., & Wen, J.-R. (2022). Towards universal sequence representation learning for recommender systems. In *Proceedings of the 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining*.
- Hu, M., & Liu, B. (2004). Mining and summarizing customer reviews. In *Proceedings of the 10th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining* (pp. 168–177). https://doi.org/10.1145/1014052.1014073
- Hu, X., Zhao, Z., Wei, S., Chai, Z., Ma, Q., Wang, G., Wang, X., Su, J., Xu, J., Zhu, M., Cheng, Y., Yuan, J., Li, J., Kuang, K., Yang, Y., Yang, H., & Wu, F. (2024). InfiAgent-DABench: Evaluating agents on data analysis tasks. In *Proceedings of the 41st International Conference on Machine Learning* (PMLR 235). **[check details: author list]**
- Jeong, S., Baek, J., Cho, S., Hwang, S. J., & Park, J. C. (2024). Adaptive-RAG: Learning to adapt retrieval-augmented large language models through question complexity. In *Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics (Volume 1: Long Papers)* (pp. 7036–7050).
- Kapoor, S., Stroebl, B., Siegel, Z. S., Nadgir, N., & Narayanan, A. (2025). AI agents that matter. *Transactions on Machine Learning Research*.
- Kaushik, D., Hovy, E., & Lipton, Z. C. (2020). Learning the difference that makes a difference with counterfactually-augmented data. In *International Conference on Learning Representations*.
- Lee, T. Y., & Bradlow, E. T. (2011). Automated marketing research using online customer reviews. *Journal of Marketing Research, 48*(5), 881–894. https://doi.org/10.1509/jmkr.48.5.881
- Li, P., Castelo, N., Katona, Z., & Sarvary, M. (2024). Frontiers: Determining the validity of large language models for automated perceptual analysis. *Marketing Science, 43*(2), 254–266. https://doi.org/10.1287/mksc.2023.0454
- Li, X., & Hitt, L. M. (2008). Self-selection and information role of online product reviews. *Information Systems Research, 19*(4), 456–474.
- Liu, N. F., Zhang, T., & Liang, P. (2023). Evaluating verifiability in generative search engines. In *Findings of the Association for Computational Linguistics: EMNLP 2023* (pp. 7001–7025).
- Longpre, S., Perisetla, K., Chen, A., Ramesh, N., DuBois, C., & Singh, S. (2021). Entity-based knowledge conflicts in question answering. In *Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing*.
- Ma, C., Tschiatschek, S., Palla, K., Hernández-Lobato, J. M., Nowozin, S., & Zhang, C. (2019). EDDI: Efficient dynamic discovery of high-value information with partial VAE. In *Proceedings of the 36th International Conference on Machine Learning* (PMLR 97).
- Majumder, B. P., Surana, H., Agarwal, D., Dalvi Mishra, B., Meena, A., Prakhar, A., Vora, T., Khot, T., Sabharwal, A., & Clark, P. (2025). DiscoveryBench: Towards data-driven discovery with large language models. In *International Conference on Learning Representations*.
- Min, S., Krishna, K., Lyu, X., Lewis, M., Yih, W.-t., Koh, P. W., Iyyer, M., Zettlemoyer, L., & Hajishirzi, H. (2023). FActScore: Fine-grained atomic evaluation of factual precision in long form text generation. In *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing* (pp. 12076–12100).
- Mohri, C., & Hashimoto, T. (2024). Language models with conformal factuality guarantees. In *Proceedings of the 41st International Conference on Machine Learning* (PMLR 235).
- Muchnik, L., Aral, S., & Taylor, S. J. (2013). Social influence bias: A randomized experiment. *Science, 341*(6146), 647–651.
- Nestaas, F., Debenedetti, E., & Tramèr, F. (2025). Adversarial search engine optimization for large language models. In *International Conference on Learning Representations*.
- Netzer, O., Feldman, R., Goldenberg, J., & Fresko, M. (2012). Mine your own business: Market-structure surveillance through text mining. *Marketing Science, 31*(3), 521–543. https://doi.org/10.1287/mksc.1120.0713
- Paischer, F., Yang, L., Liu, L., Shao, S., Hassani, K., Li, J., Chen, R., Li, Z. G., Gao, X., Shao, W., Feng, X., Noorshams, N., Park, S., Long, B., & Eghbalzadeh, H. (2024). *Preference discerning with LLM-enhanced generative retrieval* (arXiv:2412.08604). arXiv.
- Peffers, K., Tuunanen, T., Rothenberger, M. A., & Chatterjee, S. (2007). A design science research methodology for information systems research. *Journal of Management Information Systems, 24*(3), 45–77. https://doi.org/10.2753/MIS0742-1222240302
- Petroni, F., Rocktäschel, T., Lewis, P., Bakhtin, A., Wu, Y., Miller, A. H., & Riedel, S. (2019). Language models as knowledge bases? In *Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing*.
- Rajpurkar, P., Jia, R., & Liang, P. (2018). Know what you don't know: Unanswerable questions for SQuAD. In *Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers)*.
- Rajput, S., Mehta, N., Singh, A., Keshavan, R. H., Vu, T., Heldt, L., Hong, L., Tay, Y., Tran, V. Q., Samost, J., Kula, M., Chi, E. H., & Sathiamoorthy, M. (2023). Recommender systems with generative retrieval. In *Advances in Neural Information Processing Systems 36*. **[check details: author list]**
- Rashkin, H., Nikolaev, V., Lamm, M., Aroyo, L., Collins, M., Das, D., Petrov, S., Tomar, G. S., Turc, I., & Reitter, D. (2023). Measuring attribution in natural language generation models. *Computational Linguistics, 49*(4), 777–840. https://doi.org/10.1162/coli_a_00486
- Ravikumar, S. (2026). Do LLM recommenders know when they're hallucinating? Auditing confidence calibration in catalog faithfulness. In *Proceedings of the 35th ACM International Conference on Information and Knowledge Management*. (arXiv:2608.10008)
- Rubin-Toles, M., Gambhir, M., Ramji, K., Roth, A., & Goel, S. (2025). Conformal language model reasoning with coherent factuality. In *International Conference on Learning Representations*.
- Sahu, G., Puri, A., Rodriguez, J. A., Abaskohi, A., Chegini, M., Drouin, A., Taslakian, P., Zantedeschi, V., Lacoste, A., Vazquez, D., Chapados, N., Pal, C., Rajeswar, S., & Laradji, I. (2025). InsightBench: Evaluating business analytics agents through multi-step insight generation. In *International Conference on Learning Representations*.
- Sanner, S., Balog, K., Radlinski, F., Wedin, B., & Dixon, L. (2023). Large language models are competitive near cold-start recommenders for language- and item-based preferences. In *Proceedings of the 17th ACM Conference on Recommender Systems*. https://doi.org/10.1145/3604915.3608845
- Sarstedt, M., Adler, S. J., Rau, L., & Schmitt, B. (2024). Using large language models to generate silicon samples in consumer and marketing research: Challenges, opportunities, and guidelines. *Psychology & Marketing, 41*(6), 1254–1270. https://doi.org/10.1002/mar.21982
- Shao, Y., Jiang, Y., Kanell, T. A., Xu, P., Khattab, O., & Lam, M. S. (2024). Assisting in writing Wikipedia-like articles from scratch with large language models. In *Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics (Volume 1: Long Papers)* (pp. 6252–6278).
- Shi, W., Han, X., Lewis, M., Tsvetkov, Y., Zettlemoyer, L., & Yih, W.-t. (2024). Trusting your evidence: Hallucinate less with context-aware decoding. In *Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics (Volume 2: Short Papers)*.
- Si, S., Zhao, H., Gao, C., Bai, Y., Wang, Z., Gao, B., Luo, K., Li, W., Huang, Y., Chen, G., Qi, F., Zhang, M., Chang, B., & Sun, M. (2026). Teaching large language models to maintain contextual faithfulness via synthetic tasks and reinforcement learning. *Proceedings of the AAAI Conference on Artificial Intelligence, 40*(39), 33001–33009.
- Tang, L., Laban, P., & Durrett, G. (2024). MiniCheck: Efficient fact-checking of LLMs on grounding documents. In *Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing* (pp. 8818–8847).
- Timoshenko, A., & Hauser, J. R. (2019). Identifying customer needs from user-generated content. *Marketing Science, 38*(1), 1–20. https://doi.org/10.1287/mksc.2018.1123
- Timoshenko, A., Mao, C., & Hauser, J. R. (2025). *Transforming the voice of the customer: Large language models for identifying customer needs* (arXiv:2503.01870). arXiv.
- Tirunillai, S., & Tellis, G. J. (2014). Mining marketing meaning from online chatter: Strategic brand analysis of big data using latent Dirichlet allocation. *Journal of Marketing Research, 51*(4), 463–479. https://doi.org/10.1509/jmr.12.0106
- Wang, B., Cui, Y., Xu, Z., Zhao, J., Fan, C., Zhang, J., Yang, W., Zhang, S., Chen, S., Zhang, Y., Zhao, X., Wang, W., Gao, C., Feng, F., He, X., & Chen, J. (2026). *Trustworthy recommendation in the era of large language models: Opportunities and challenges* (arXiv:2606.00540).
- Wang, J., Xiao, K., Sun, Q., Zhao, H., Luo, T., Zhang, J. D., & Zeng, X. (2025). *ShoppingBench: A real-world intent-grounded shopping benchmark for LLM-based agents* (arXiv:2508.04266). arXiv.
- Wang, P., Wu, Y., Song, X., Wang, W., Chen, G., Li, Z., Yan, K., Deng, K., Liu, Q., Zhao, S., Xiong, S., Liu, X., Chen, X., Deng, W., Su, W., & Zheng, B. (2026). *ShopSimulator: Evaluating and exploring RL-driven LLM agent for shopping assistants* (arXiv:2601.18225). arXiv.
- Wen, B., Yao, J., Feng, S., Xu, C., Tsvetkov, Y., Howe, B., & Wang, L. L. (2025). Know your limits: A survey of abstention in large language models. *Transactions of the Association for Computational Linguistics, 13*, 529–556.
- Wu, L., Zheng, Z., Qiu, Z., Wang, H., Gu, H., Shen, T., Qin, C., Zhu, C., Zhu, H., Liu, Q., Xiong, H., & Chen, E. (2024). A survey on large language models for recommendation. *World Wide Web, 27*. https://doi.org/10.1007/s11280-024-01291-2 **[check details: author list]**
- Xia, C. S., Deng, Y., Dunn, S., & Zhang, L. (2025). Agentless: Demystifying LLM-based software engineering agents. *Proceedings of the ACM on Software Engineering, 2*(FSE).
- Xie, J., Zhang, K., Chen, J., Lou, R., & Su, Y. (2024). Adaptive chameleon or stubborn sloth: Revealing the behavior of large language models in knowledge conflicts. In *International Conference on Learning Representations*.
- Xu, R., Qi, Z., Guo, Z., Wang, C., Wang, H., Zhang, Y., & Xu, W. (2024). Knowledge conflicts for LLMs: A survey. In *Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing*. **[check details: author list]**
- Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2023). ReAct: Synergizing reasoning and acting in language models. In *International Conference on Learning Representations*.
- Yu, Z., Xiao, K., Zhao, H., Luo, T., & Zeng, X. (2026). *Shopping Companion: Benchmarking and training LLM agents for long-horizon preference-grounded e-commerce tasks* (arXiv:2603.14864). arXiv.
- Zhang, J., Xiang, J., Yu, Z., Teng, F., Chen, X., Chen, J., Zhuge, M., Cheng, X., Hong, S., Wang, J., Zheng, B., Liu, B., Luo, Y., & Wu, C. (2025). AFlow: Automating agentic workflow generation. In *International Conference on Learning Representations*.
- Zhang, W., Bei, Y., Yang, L., Zou, H. P., Zhou, P., Liu, A., Li, Y., Chen, H., Wang, J., Wang, Y., Huang, F., Zhou, S., Bu, J., Lin, A., Caverlee, J., Karray, F., King, I., & Yu, P. S. (2025). *Cold-start recommendation towards the era of large language models (LLMs): A comprehensive survey and roadmap* (arXiv:2501.01945).
- Zhang, Y., Li, Y., Cui, L., Cai, D., Liu, L., Fu, T., Huang, X., Zhao, E., Zhang, Y., Chen, Y., Wang, L., Luu, A. T., Bi, W., Shi, F., & Shi, S. (2025). Siren's song in the AI ocean: A survey on hallucination in large language models. *Computational Linguistics, 51*(4), 1374–1404. https://doi.org/10.1162/COLI.a.16
- Zhao, Z., Fan, W., Li, J., Liu, Y., Mei, X., Wang, Y., Wen, Z., Wang, F., Zhao, X., Tang, J., & Li, Q. (2024). Recommender systems in the era of large language models (LLMs). *IEEE Transactions on Knowledge and Data Engineering, 36*(11), 6889–6907.
- Zheng, L., Chiang, W.-L., Sheng, Y., Zhuang, S., Wu, Z., Zhuang, Y., Lin, Z., Li, Z., Li, D., Xing, E. P., Zhang, H., Gonzalez, J. E., & Stoica, I. (2023). Judging LLM-as-a-judge with MT-Bench and Chatbot Arena. In *Advances in Neural Information Processing Systems 36* (Datasets and Benchmarks Track).
- Zhou, Z., Feng, X., Zhu, Z., Yao, J., Koyejo, S., & Han, B. (2025). From passive to active reasoning: Can large language models ask the right questions under incomplete information? In *Proceedings of the 42nd International Conference on Machine Learning* (PMLR 267, pp. 78714–78758).
