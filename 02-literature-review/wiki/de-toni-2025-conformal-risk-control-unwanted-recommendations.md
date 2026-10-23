# You don't bring me flowers: Mitigating unwanted recommendations through conformal risk control

| | |
|---|---|
| **Set** | 2025–2026 field check |
| **Citations** | not required |
| **Original** | [https://arxiv.org/abs/2507.16829](https://arxiv.org/abs/2507.16829) · local stub: [`raw/de-toni-2025-conformal-risk-control-unwanted-recommendations.md`](../raw/de-toni-2025-conformal-risk-control-unwanted-recommendations.md) |

**APA:** De Toni, G., Purificato, E., Gomez, E., Lepri, B., Passerini, A., & Consonni, C. (2025). You don't bring me flowers: Mitigating unwanted recommendations through conformal risk control. In *Proceedings of the 19th ACM Conference on Recommender Systems*. ACM.

## 1. Research question
Can the share of unwanted items in personalised recommendations be provably bounded using only binary "do not recommend" feedback, without retraining the recommender?

## 2. Limitation of existing methods
Recommenders filter harmful or unwanted content heuristically, with no guarantee on how much gets through.

## 3. Contributions
A post-hoc, model-agnostic conformal risk control layer for recommendation, with a replacement strategy that keeps list quality.

## 4. Proposed methods
Calibrate a global score threshold on held-out feedback with conformal risk control so expected unwanted share ≤ α; replace filtered items with previously watched, unflagged ones.

## 5. Key findings
On KuaiRand the unwanted share meets the target and replacement keeps nDCG better than removal; the global threshold is driven by heavy reporters.

## 6. Limitations
One dataset; global threshold; guarantee in expectation only (a high-probability version is listed as future work); assumes re-exposed items are not re-reported.

## 7. Author names
Giovanni De Toni, Erasmo Purificato, Emilia Gomez, Bruno Lepri, Andrea Passerini, Cristian Consonni

## 8. Publish year
2025

## 9. Proceedings or journal name
Proceedings of the 19th ACM Conference on Recommender Systems (RecSys 2025)

---

**Relevance to the thesis:** **Makes "URR ≤ α for recommendations" a known template.** The thesis's calibration (Learn-then-Test, high-probability, selective ratio risk, three-way decision) is a rigour difference, not a headline. Cite it as the closest recommendation-side precedent and demote C2 to method.

*Extracted 2026-10-21 from the arXiv abstract page or HTML (fetched that day), for the repositioning after the 2026 field check (`team-opinion/field-check-2026.md` in the project files); not a full-text reading. Check numbers against the original before quoting.*
