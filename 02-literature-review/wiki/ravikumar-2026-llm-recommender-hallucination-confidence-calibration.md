# Do LLM recommenders know when they're hallucinating? Auditing confidence calibration in catalog faithfulness

| | |
|---|---|
| **Set** | 2025–2026 field check |
| **Citations** | not required |
| **Original** | [https://arxiv.org/abs/2608.10008](https://arxiv.org/abs/2608.10008) · local stub: [`raw/ravikumar-2026-llm-recommender-hallucination-confidence-calibration.md`](../raw/ravikumar-2026-llm-recommender-hallucination-confidence-calibration.md) |

**APA:** Ravikumar, S. (2026). Do LLM recommenders know when they're hallucinating? Auditing confidence calibration in catalog faithfulness. In *Proceedings of the 35th ACM International Conference on Information and Knowledge Management (CIKM 2026)*. ACM. (arXiv:2608.10008)

## 1. Research question
Does an LLM recommender's verbalised confidence track whether the item it recommends is actually in the catalog?

## 2. Limitation of existing methods
Hallucinated (out-of-catalog) recommendations are measured, but whether models know when they hallucinate, and whether confidence-based abstention helps, was untested.

## 3. Contributions
An audit of four zero-shot LLMs across three catalogs, including Amazon Reviews 2023 Toys, with a validated matcher and a conformal abstention test.

## 4. Proposed methods
Elicit recommendations and verbalised confidence from Mistral Large, Llama-3.3-70B, GPT-OSS-120B and Claude Sonnet 4.6 on MovieLens-25M, Amazon Toys and Yelp; match to catalogs; calibrate a conformal abstention threshold on confidence.

## 5. Key findings
Out-of-catalog rates range 0.6–2.7% (MovieLens) to 49–61% (Amazon Toys). Mean confidence stays at about 67–86 while catalog-hit rates span 39–99%. Conformal abstention on confidence cuts hallucination by at most 1.65 points (median about 0.02).

## 6. Limitations
One human annotator; residual matcher error up to 0.22 on Amazon; judge from the same vendor as one generator; zero-shot frontier models and verbalised confidence only.

## 7. Author names
Srijith Ravikumar

## 8. Publish year
2026

## 9. Proceedings or journal name
Listed for the 35th ACM International Conference on Information and Knowledge Management (CIKM 2026); acceptance not independently confirmed

---

**Relevance to the thesis:** **Independent support for the thesis's central claim**: abstaining on confidence does not certify grounding; abstaining on checkable evidence can. It is also a required baseline (confidence-based abstention, same protocol).

*Extracted 2026-10-21 from the arXiv abstract page or HTML (fetched that day), for the repositioning after the 2026 field check (`team-opinion/field-check-2026.md` in the project files); not a full-text reading. Check numbers against the original before quoting.*
