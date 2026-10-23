# Is conformal factuality for RAG-based LLMs robust? Novel metrics and systematic insights

| | |
|---|---|
| **Set** | 2025–2026 field check |
| **Citations** | not required |
| **Original** | [https://arxiv.org/abs/2603.16817](https://arxiv.org/abs/2603.16817) · local stub: [`raw/chen-2026-conformal-factuality-rag-robustness.md`](../raw/chen-2026-conformal-factuality-rag-robustness.md) |

**APA:** Chen, Y., Chen, D., Chikodikar, S. M., Yin, C. H., & Vinayak, R. K. (2026). *Is conformal factuality for RAG-based LLMs robust? Novel metrics and systematic insights* (arXiv:2603.16817). arXiv.

## 1. Research question
How reliable and useful is conformal factuality filtering for retrieval-augmented LLMs?

## 2. Limitation of existing methods
Conformal factuality papers report validity but not how much useful content survives, nor robustness to shift and distractors.

## 3. Contributions
A systematic study across generation, claim scoring, calibration, robustness and efficiency, with informativeness-aware metrics.

## 4. Proposed methods
Apply conformal factuality to RAG outputs on three benchmarks and several model families; vary shift and distractors; compare LLM confidence scorers with lightweight entailment (NLI) verifiers.

## 5. Key findings
High factuality levels often leave low-usefulness outputs; guarantees break under shift and distractors; NLI verifiers match or beat LLM confidence scorers at over 100× fewer FLOPs.

## 6. Limitations
Three benchmarks; conclusions imply calibration data must match deployment.

## 7. Author names
Yi Chen, Daiwei Chen, Sukrut Madhav Chikodikar, Caitlyn Heqi Yin, Ramya Korlakai Vinayak

## 8. Publish year
2026

## 9. Proceedings or journal name
arXiv preprint arXiv:2603.16817

---

**Relevance to the thesis:** Names the **vacuity** risk the pilot shows (certified URR ≈ 4% at coverage ≈ 13%). The thesis must report informativeness (coverage, recall of supported) next to URR, and run an NLI verifier baseline.

*Extracted 2026-10-21 from the arXiv abstract page or HTML (fetched that day), for the repositioning after the 2026 field check (`team-opinion/field-check-2026.md` in the project files); not a full-text reading. Check numbers against the original before quoting.*
