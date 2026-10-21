# Large language model validity via enhanced conformal prediction methods

| | |
|---|---|
| **Set** | 2025–2026 field check |
| **Citations** | not required |
| **Original** | [https://arxiv.org/abs/2406.09714](https://arxiv.org/abs/2406.09714) · local stub: [`raw/cherian-2024-llm-validity-conformal-conditional.md`](../raw/cherian-2024-llm-validity-conformal-conditional.md) |

**APA:** Cherian, J. J., Gibbs, I., & Candès, E. J. (2024). *Large language model validity via enhanced conformal prediction methods* (arXiv:2406.09714). arXiv.

## 1. Research question
Can LLM outputs carry validity guarantees that hold conditionally on the prompt, without filtering so much that the output becomes useless?

## 2. Limitation of existing methods
Conformal factuality (Mohri & Hashimoto, 2024) gives marginal guarantees and can remove most claims.

## 3. Contributions
Group-conditional conformal factuality via the conditional conformal method of Gibbs et al., and conditional boosting to learn better claim scorers.

## 4. Proposed methods
Adaptive, prompt-dependent thresholds with group-conditional coverage; differentiate through the procedure to train scores.

## 5. Key findings
Boosted scores retain more claims (mean 39% vs 24%) with calibrated, group-conditional validity on medical QA and biographies.

## 6. Limitations
Exact conditional guarantees are impossible without assumptions; needs an annotated calibration set.

## 7. Author names
John J. Cherian, Isaac Gibbs, Emmanuel J. Candès

## 8. Publish year
2024

## 9. Proceedings or journal name
arXiv preprint arXiv:2406.09714 (the field check lists NeurIPS 2024; confirm the proceedings entry before citing)

---

**Relevance to the thesis:** Shows group-conditional guarantees are standard, so the **two-sided (new vs established) guarantee** is novel as an object, not as machinery. Also the reference for informativeness-preserving calibration.

*Extracted 2026-10-21 from the arXiv abstract page or HTML (fetched that day), for the repositioning after the 2026 field check (`team-opinion/field-check-2026.md` in the project files); not a full-text reading. Check numbers against the original before quoting.*
