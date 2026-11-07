# Conformal language model reasoning with coherent factuality

| | |
|---|---|
| **Set** | Conference · AI |
| **Citations** | not required (conference set) |
| **Original** | [https://openreview.net/forum?id=AJpUZd8Clb](https://openreview.net/forum?id=AJpUZd8Clb) · local stub: [`raw/rubin-toles-2025-conformal-reasoning-coherent-factuality.md`](../raw/rubin-toles-2025-conformal-reasoning-coherent-factuality.md) |

**APA:** Rubin-Toles, M., Gambhir, M., Ramji, K., Roth, A., & Goel, S. (2025). Conformal language model reasoning with coherent factuality. In *International Conference on Learning Representations*.

## 1. Research question
How can conformal guarantees be extended from independent claims to reasoning chains, where each step must follow from earlier steps?

## 2. Limitation of existing methods
Claim-wise conformal filtering treats claims as independent, so it can keep a true step whose premises were removed, breaking the chain.

## 3. Contributions
Defines coherent factuality; a conformal procedure over a deducibility graph of reasoning steps with a finite-sample guarantee.

## 4. Proposed methods
Build a graph of which steps depend on which, score sub-graphs, and calibrate a threshold so retained steps are both correct and deducible from retained predecessors.

## 5. Key findings
On mathematical reasoning tasks the method reaches the target coherent-factuality level while plain claim-wise filtering does not.

## 6. Limitations
Needs a dependency graph, which is itself produced by a model; evaluated on math reasoning, not decisions.

## 7. Author names
Maxon Rubin-Toles, Maya Gambhir, Keshav Ramji, Aaron Roth, Surbhi Goel

## 8. Publish year
2025

## 9. Proceedings or journal name
International Conference on Learning Representations (ICLR 2025)

---

**Relevance to the thesis:** Supports Paper A's distinction between 'true' and 'supported by what was shown'. Paper A's per-constraint support status is the decision-level analogue.

*Extracted 2026-10-17 from the abstract and main results; not a full-text reading. Check numbers against the original before quoting.*
