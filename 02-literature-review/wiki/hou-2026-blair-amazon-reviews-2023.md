# Bridging language and items for retrieval and recommendation: Benchmarking LLMs as semantic encoders

| | |
|---|---|
| **Set** | Conference · AI |
| **Citations** | not required (conference set) |
| **Original** | [https://arxiv.org/abs/2403.03952](https://arxiv.org/abs/2403.03952) · local stub: [`raw/hou-2026-blair-amazon-reviews-2023.md`](../raw/hou-2026-blair-amazon-reviews-2023.md) |

**APA:** Hou, Y., Li, J., Fu, X., He, Z., Yan, A., Chen, X., & McAuley, J. (2026). Bridging language and items for retrieval and recommendation: Benchmarking LLMs as semantic encoders. In *Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)* (pp. 3251–3265).

## 1. Research question
How can text encoders connect item metadata with the language people use about items, for retrieval and recommendation?

## 2. Limitation of existing methods
General-purpose sentence encoders are not trained on the link between product metadata and review language, and earlier Amazon datasets are dated.

## 3. Contributions
Amazon Reviews 2023 (over 570 million reviews, 48 million items, 33 categories) and BLaIR, encoders pretrained on metadata–review pairs; complex product search benchmark.

## 4. Proposed methods
Contrastive pretraining that pulls item metadata and the item's reviews together, evaluated on retrieval, sequential recommendation and complex product search.

## 5. Key findings
BLaIR improves over general encoders on retrieval and recommendation, including complex language-based product search.

## 6. Limitations
Optimizes semantic similarity; does not test whether a listing supports a specific need. The arXiv (2024) and ACL (2026) versions differ in author list.

## 7. Author names
Yupeng Hou, Jiacheng Li, Xiangjun Fu, Zhankui He, An Yan, Xiusi Chen, Julian McAuley

## 8. Publish year
2026

## 9. Proceedings or journal name
Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (ACL 2026), Volume 1: Long Papers, pp. 3251–3265

---

**Relevance to the thesis:** Paper A's dataset and an encoder baseline. Paper A uses the `details` specs as hidden ground truth and post-launch reviews as validation, which this paper does not.

*Extracted 2026-10-17 from the abstract and main results; not a full-text reading. Check numbers against the original before quoting.*
