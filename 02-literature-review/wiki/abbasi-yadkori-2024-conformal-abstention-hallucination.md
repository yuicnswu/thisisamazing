# Mitigating LLM hallucinations via conformal abstention

| | |
|---|---|
| **Set** | 2025–2026 field check |
| **Citations** | not required |
| **Original** | [https://arxiv.org/abs/2405.01563](https://arxiv.org/abs/2405.01563) · local stub: [`raw/abbasi-yadkori-2024-conformal-abstention-hallucination.md`](../raw/abbasi-yadkori-2024-conformal-abstention-hallucination.md) |

**APA:** Abbasi-Yadkori, Y., Kuzborskij, I., Stutz, D., György, A., Fisch, A., Doucet, A., Beloshapka, I., Weng, W.-H., Yang, Y.-Y., Szepesvári, C., Cemgil, A. T., & Tomasev, N. (2024). *Mitigating LLM hallucinations via conformal abstention* (arXiv:2405.01563). arXiv.

## 1. Research question
Can an LLM abstain when it is likely to hallucinate, with a statistical guarantee on its error rate?

## 2. Limitation of existing methods
Log-probability abstention has no guarantee and works poorly on long-form answers.

## 3. Contributions
Self-consistency-based abstention calibrated with conformal risk control and high-probability (RCPS-style) bounds.

## 4. Proposed methods
Sample several answers, have the model judge their agreement, abstain on low agreement; pick the threshold on a labelled calibration set.

## 5. Key findings
Test error stays near the target with less abstention than log-probability baselines on long answers (TriviaQA, Temporal Sequences, Gemini Pro).

## 6. Limitations
Two QA datasets, one model, exchangeability, manual labels to calibrate the matching threshold.

## 7. Author names
Yasin Abbasi-Yadkori, Ilja Kuzborskij, David Stutz, András György, Adam Fisch, Arnaud Doucet, Iuliya Beloshapka, Wei-Hung Weng, Yao-Yuan Yang, Csaba Szepesvári, Ali Taylan Cemgil, Nenad Tomasev

## 8. Publish year
2024

## 9. Proceedings or journal name
arXiv preprint arXiv:2405.01563

---

**Relevance to the thesis:** Conformal abstention for LLMs in both CRC and (α, δ) forms already exists. The thesis's abstention is triggered by **missing evidence**, not by self-agreement, which is the point Ravikumar (2026) supports empirically.

*Extracted 2026-10-21 from the arXiv abstract page or HTML (fetched that day), for the repositioning after the 2026 field check (`team-opinion/field-check-2026.md` in the project files); not a full-text reading. Check numbers against the original before quoting.*
