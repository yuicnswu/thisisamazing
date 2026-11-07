# EDDI: Efficient dynamic discovery of high-value information with partial VAE

| | |
|---|---|
| **Set** | Highly cited · AI |
| **Citations** | 136 (Liner, read 2026-10-17; lower bound) |
| **Original** | [https://arxiv.org/abs/1809.11142](https://arxiv.org/abs/1809.11142) · local stub: [`raw/ma-2019-eddi-active-feature-acquisition.md`](../raw/ma-2019-eddi-active-feature-acquisition.md) |

**APA:** Ma, C., Tschiatschek, S., Palla, K., Hernández-Lobato, J. M., Nowozin, S., & Zhang, C. (2019). EDDI: Efficient dynamic discovery of high-value information with partial VAE. In *Proceedings of the 36th International Conference on Machine Learning* (PMLR 97).

## 1. Research question
How can a system decide which missing feature to acquire next for each individual, at low cost?

## 2. Limitation of existing methods
Acquisition methods needed fully observed training data or were too slow to choose features per instance.

## 3. Contributions
A partial VAE that handles missing data, plus an information-theoretic acquisition function.

## 4. Proposed methods
Estimate the expected information gain of each unobserved feature with the partial VAE and acquire the best one sequentially.

## 5. Key findings
Acquires high-value information efficiently on health and education data, beating baselines.

## 6. Limitations
Stops on predictive confidence or budget, not on whether the decision is supported.

## 7. Author names
Chao Ma, Sebastian Tschiatschek, Konstantina Palla, José Miguel Hernández-Lobato, Sebastian Nowozin, Cheng Zhang

## 8. Publish year
2019

## 9. Proceedings or journal name
Proceedings of the 36th International Conference on Machine Learning (ICML), PMLR 97

---

**Relevance to the thesis:** Acquisition baseline for Paper A. Paper A's VOI-blindness result shows confidence-based stopping never looks when priors are strong.

*Extracted 2026-10-17 from the abstract and main results; not a full-text reading. Check numbers against the original before quoting.*
