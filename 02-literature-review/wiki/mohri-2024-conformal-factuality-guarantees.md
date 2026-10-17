# Language models with conformal factuality guarantees

| | |
|---|---|
| **Set** | Conference · AI |
| **Citations** | 56 (Liner, undated snapshot; lower bound) |
| **Original** | [https://arxiv.org/abs/2402.10978](https://arxiv.org/abs/2402.10978) · local stub: [`raw/mohri-2024-conformal-factuality-guarantees.md`](../raw/mohri-2024-conformal-factuality-guarantees.md) |

**APA:** Mohri, C., & Hashimoto, T. (2024). Language models with conformal factuality guarantees. In *Proceedings of the 41st International Conference on Machine Learning* (PMLR 235).

## 1. Research question
Can we guarantee that the claims an LLM outputs are correct with a user-chosen probability, without retraining the model?

## 2. Limitation of existing methods
LLM outputs mix true and false claims, and existing uncertainty methods give scores without any guarantee on what is finally shown to the user.

## 3. Contributions
Links conformal prediction to factuality by treating an LLM output as a set of claims; a back-off procedure that removes claims until the remaining output is entailed with probability at least 1 − α.

## 4. Proposed methods
Split the output into sub-claims, score each with a confidence function, calibrate a threshold on labelled data with split conformal prediction, and drop claims below the threshold.

## 5. Key findings
The target factuality level is met on closed-book QA and reasoning tasks while keeping most of the useful content at practical α.

## 6. Limitations
Filters generated text; it does not make decisions. The guarantee is relative to the calibration labels, assumes exchangeability, and the output can lose content as α falls.

## 7. Author names
Christopher Mohri, Tatsunori Hashimoto

## 8. Publish year
2024

## 9. Proceedings or journal name
Proceedings of the 41st International Conference on Machine Learning (ICML), PMLR 235

---

**Relevance to the thesis:** Closest guarantee to Paper A. Paper A moves the object from claims to recommendation decisions over a conjunction of constraints, adds recommend/reject/abstain, and validates against post-launch reviews.

*Extracted 2026-10-17 from the abstract and main results; not a full-text reading. Check numbers against the original before quoting.*
