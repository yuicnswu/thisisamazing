# E-GEO: A testbed for generative engine optimization in e-commerce

| | |
|---|---|
| **Set** | 2025–2026 field check |
| **Citations** | not required |
| **Original** | [https://arxiv.org/abs/2511.20867](https://arxiv.org/abs/2511.20867) · local stub: [`raw/bagga-2025-e-geo-generative-engine-optimization-ecommerce.md`](../raw/bagga-2025-e-geo-generative-engine-optimization-ecommerce.md) |

**APA:** Bagga, P. S., Farias, V. F., Korkotashvili, T., Peng, T., & Wu, Y. (2025). *E-GEO: A testbed for generative engine optimization in e-commerce* (arXiv:2511.20867). arXiv.

## 1. Research question
What makes a generative shopping engine rank a listing higher, and how can sellers rewrite listings to climb?

## 2. Limitation of existing methods
GEO had been studied on web search, not on product listings with LLM rerankers.

## 3. Contributions
E-GEO: 13,747 Reddit-derived product queries, each with 10 Amazon listings; seven LLM rewriters, fifteen heuristic prompts and a prompt meta-optimiser; adversarial red-teaming.

## 4. Proposed methods
Model the engine as an LLM reranker over five models; rewrite the target listing; measure rank change.

## 5. Key findings
Rewrites move ranks: GPT-5 and Claude rewriters gain about +0.56 to +0.57 mean rank positions, and the meta-optimiser beats the heuristics.

## 6. Limitations
One query source and retrieval depth; reranking stage only; one target listing per query; rewrites are not checked for factual faithfulness to the product (only an in-prompt defence against questionable content).

## 7. Author names
Puneet S. Bagga, Vivek F. Farias, Tamar Korkotashvili, Tianyi Peng, Yuhang Wu

## 8. Publish year
2025

## 9. Proceedings or journal name
arXiv preprint arXiv:2511.20867 (cs.IR)

---

**Relevance to the thesis:** The **opposite stance to the merchant-fix loop**: GEO rewrites for rank without checking truth; EvidenceGuard asks for disclosure of checkable facts and only rewards what the listing states. E-GEO rewriting is a required seller-side baseline, and the faithfulness gap is the opening for "truthful listing optimisation".

*Extracted 2026-10-21 from the arXiv abstract page or HTML (fetched that day), for the repositioning after the 2026 field check (`team-opinion/field-check-2026.md` in the project files); not a full-text reading. Check numbers against the original before quoting.*
