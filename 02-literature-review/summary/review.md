# Literature Review (Narrative)

*Stage 2 of [WORKFLOW.md](../../WORKFLOW.md). Narrative summary with APA citations covering every file in [`../wiki/`](../wiki/) (40 papers, listed in [`../index.md`](../index.md)). Update whenever a paper is added to `raw/` or `wiki/`. Last updated 2026-10-17.*

**Scope.** This review supports the thesis *Before the First Review*:
- **Paper A** (NeurIPS 2027) asks whether AI recommenders match new products to customers on listing **evidence** or on **priors**. It proposes a matcher that recommends only when every checkable constraint of a need is entailed by inspected evidence, abstains otherwise, and bounds the unsupported recommendation rate (URR).
- **Paper B** (PACIS/HICSS) asks whether evidence-supported fit among a new product's first buyers shapes its review trajectory.

**Corpus.** The wiki holds 40 papers, chosen as yui asked:
- 10 recent papers from peer-reviewed conferences.
- 20 papers with more than 100 verified citations: 14 AI and 6 marketing (70/30).
- 10 surveys.

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

## 8. Gap

Across the 40 papers, prior work does five things:
- places new items by similarity (Hou et al., 2022; Rajput et al., 2023; Sanner et al., 2023);
- shows that models prefer memory to context (Longpre et al., 2021; Xie et al., 2024);
- bounds error or the support of generated text (Geifman & El-Yaniv, 2017; Mohri & Hashimoto, 2024; Rubin-Toles et al., 2025);
- documents manipulation (Filandrianos et al., 2025; Nestaas et al., 2025);
- shows that early, well-matched reviews matter (Godes & Silva, 2012; Li & Hitt, 2008; Muchnik et al., 2013).

No paper does any of the following:
- tests whether recommenders license new-product matches on priors when listing evidence is missing, vague or edited;
- recommends only when every checkable constraint is entailed, and abstains otherwise;
- bounds the rate of unsupported recommendation decisions;
- links the evidence-supported fit of a product's first buyers to its review trajectory.

## References

- Angelopoulos, A. N., Bates, S., Fisch, A., Lei, L., & Schuster, T. (2024). Conformal risk control. In *International Conference on Learning Representations*.
- Archak, N., Ghose, A., & Ipeirotis, P. G. (2011). Deriving the pricing power of product features by mining consumer reviews. *Management Science, 57*(8), 1485–1509. https://doi.org/10.1287/mnsc.1110.1370
- Babić Rosario, A., Sotgiu, F., De Valck, K., & Bijmolt, T. H. A. (2016). The effect of electronic word of mouth on sales: A meta-analytic review of platform, product, and metric factors. *Journal of Marketing Research, 53*(3), 297–318. https://doi.org/10.1509/jmr.14.0380
- Bass, F. M. (1969). A new product growth for model consumer durables. *Management Science, 15*(5), 215–227. https://doi.org/10.1287/mnsc.15.5.215
- Campos, M., Farinhas, A., Zerva, C., Figueiredo, M. A. T., & Martins, A. F. T. (2024). Conformal prediction for natural language processing: A survey. *Transactions of the Association for Computational Linguistics, 12*, 1497–1516. https://doi.org/10.1162/tacl_a_00715
- Filandrianos, G., Dimitriou, A., Lymperaiou, M., Thomas, K., & Stamou, G. (2025). Bias beware: The impact of cognitive biases on LLM-driven product recommendations. In *Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing* (pp. 22397–22426).
- Fleder, D., & Hosanagar, K. (2009). Blockbuster culture's next rise or fall: The impact of recommender systems on sales diversity. *Management Science, 55*(5), 697–712.
- Gao, T., Yen, H., Yu, J., & Chen, D. (2023). Enabling large language models to generate text with citations. In *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing*.
- Geifman, Y., & El-Yaniv, R. (2017). Selective classification for deep neural networks. In *Advances in Neural Information Processing Systems 30*.
- Geng, S., Liu, S., Fu, Z., Ge, Y., & Zhang, Y. (2022). Recommendation as language processing (RLP): A unified pretrain, personalized prompt & predict paradigm (P5). In *Proceedings of the 16th ACM Conference on Recommender Systems*.
- Godes, D., & Silva, J. C. (2012). Sequential and temporal dynamics of online opinion. *Marketing Science, 31*(3), 448–473.
- Haenlein, M., & Libai, B. (2017). Seeding, referral, and recommendation: Creating profitable word-of-mouth programs. *California Management Review, 59*(2), 68–91.
- Hong, Y., & Pavlou, P. A. (2014). Product fit uncertainty in online markets: Nature, effects, and antecedents. *Information Systems Research, 25*(2), 328–344.
- Hou, Y., Li, J., Fu, X., He, Z., Yan, A., Chen, X., & McAuley, J. (2026). Bridging language and items for retrieval and recommendation: Benchmarking LLMs as semantic encoders. In *Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)* (pp. 3251–3265).
- Hou, Y., Mu, S., Zhao, W. X., Li, Y., Ding, B., & Wen, J.-R. (2022). Towards universal sequence representation learning for recommender systems. In *Proceedings of the 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining*.
- Kaushik, D., Hovy, E., & Lipton, Z. C. (2020). Learning the difference that makes a difference with counterfactually-augmented data. In *International Conference on Learning Representations*.
- Li, X., & Hitt, L. M. (2008). Self-selection and information role of online product reviews. *Information Systems Research, 19*(4), 456–474.
- Longpre, S., Perisetla, K., Chen, A., Ramesh, N., DuBois, C., & Singh, S. (2021). Entity-based knowledge conflicts in question answering. In *Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing*.
- Ma, C., Tschiatschek, S., Palla, K., Hernández-Lobato, J. M., Nowozin, S., & Zhang, C. (2019). EDDI: Efficient dynamic discovery of high-value information with partial VAE. In *Proceedings of the 36th International Conference on Machine Learning* (PMLR 97).
- Mohri, C., & Hashimoto, T. (2024). Language models with conformal factuality guarantees. In *Proceedings of the 41st International Conference on Machine Learning* (PMLR 235).
- Muchnik, L., Aral, S., & Taylor, S. J. (2013). Social influence bias: A randomized experiment. *Science, 341*(6146), 647–651.
- Nestaas, F., Debenedetti, E., & Tramèr, F. (2025). Adversarial search engine optimization for large language models. In *International Conference on Learning Representations*.
- Petroni, F., Rocktäschel, T., Lewis, P., Bakhtin, A., Wu, Y., Miller, A. H., & Riedel, S. (2019). Language models as knowledge bases? In *Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing*.
- Rajpurkar, P., Jia, R., & Liang, P. (2018). Know what you don't know: Unanswerable questions for SQuAD. In *Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers)*.
- Rajput, S., Mehta, N., Singh, A., Keshavan, R. H., Vu, T., Heldt, L., Hong, L., Tay, Y., Tran, V. Q., Samost, J., Kula, M., Chi, E. H., & Sathiamoorthy, M. (2023). Recommender systems with generative retrieval. In *Advances in Neural Information Processing Systems 36*. **[check details: author list]**
- Rubin-Toles, M., Gambhir, M., Ramji, K., Roth, A., & Goel, S. (2025). Conformal language model reasoning with coherent factuality. In *International Conference on Learning Representations*.
- Sanner, S., Balog, K., Radlinski, F., Wedin, B., & Dixon, L. (2023). Large language models are competitive near cold-start recommenders for language- and item-based preferences. In *Proceedings of the 17th ACM Conference on Recommender Systems*. https://doi.org/10.1145/3604915.3608845
- Shi, W., Han, X., Lewis, M., Tsvetkov, Y., Zettlemoyer, L., & Yih, W.-t. (2024). Trusting your evidence: Hallucinate less with context-aware decoding. In *Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics (Volume 2: Short Papers)*.
- Si, S., Zhao, H., Gao, C., Bai, Y., Wang, Z., Gao, B., Luo, K., Li, W., Huang, Y., Chen, G., Qi, F., Zhang, M., Chang, B., & Sun, M. (2026). Teaching large language models to maintain contextual faithfulness via synthetic tasks and reinforcement learning. *Proceedings of the AAAI Conference on Artificial Intelligence, 40*(39), 33001–33009.
- Timoshenko, A., & Hauser, J. R. (2019). Identifying customer needs from user-generated content. *Marketing Science, 38*(1), 1–20. https://doi.org/10.1287/mksc.2018.1123
- Wang, B., Cui, Y., Xu, Z., Zhao, J., Fan, C., Zhang, J., Yang, W., Zhang, S., Chen, S., Zhang, Y., Zhao, X., Wang, W., Gao, C., Feng, F., He, X., & Chen, J. (2026). *Trustworthy recommendation in the era of large language models: Opportunities and challenges* (arXiv:2606.00540).
- Wen, B., Yao, J., Feng, S., Xu, C., Tsvetkov, Y., Howe, B., & Wang, L. L. (2025). Know your limits: A survey of abstention in large language models. *Transactions of the Association for Computational Linguistics, 13*, 529–556.
- Wu, L., Zheng, Z., Qiu, Z., Wang, H., Gu, H., Shen, T., Qin, C., Zhu, C., Zhu, H., Liu, Q., Xiong, H., & Chen, E. (2024). A survey on large language models for recommendation. *World Wide Web, 27*. https://doi.org/10.1007/s11280-024-01291-2 **[check details: author list]**
- Xie, J., Zhang, K., Chen, J., Lou, R., & Su, Y. (2024). Adaptive chameleon or stubborn sloth: Revealing the behavior of large language models in knowledge conflicts. In *International Conference on Learning Representations*.
- Xu, R., Qi, Z., Guo, Z., Wang, C., Wang, H., Zhang, Y., & Xu, W. (2024). Knowledge conflicts for LLMs: A survey. In *Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing*. **[check details: author list]**
- Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2023). ReAct: Synergizing reasoning and acting in language models. In *International Conference on Learning Representations*.
- Zhang, W., Bei, Y., Yang, L., Zou, H. P., Zhou, P., Liu, A., Li, Y., Chen, H., Wang, J., Wang, Y., Huang, F., Zhou, S., Bu, J., Lin, A., Caverlee, J., Karray, F., King, I., & Yu, P. S. (2025). *Cold-start recommendation towards the era of large language models (LLMs): A comprehensive survey and roadmap* (arXiv:2501.01945).
- Zhang, Y., Li, Y., Cui, L., Cai, D., Liu, L., Fu, T., Huang, X., Zhao, E., Zhang, Y., Chen, Y., Wang, L., Luu, A. T., Bi, W., Shi, F., & Shi, S. (2025). Siren's song in the AI ocean: A survey on hallucination in large language models. *Computational Linguistics, 51*(4), 1374–1404. https://doi.org/10.1162/COLI.a.16
- Zhao, Z., Fan, W., Li, J., Liu, Y., Mei, X., Wang, Y., Wen, Z., Wang, F., Zhao, X., Tang, J., & Li, Q. (2024). Recommender systems in the era of large language models (LLMs). *IEEE Transactions on Knowledge and Data Engineering, 36*(11), 6889–6907.
- Zhou, Z., Feng, X., Zhu, Z., Yao, J., Koyejo, S., & Han, B. (2025). From passive to active reasoning: Can large language models ask the right questions under incomplete information? In *Proceedings of the 42nd International Conference on Machine Learning* (PMLR 267, pp. 78714–78758).
