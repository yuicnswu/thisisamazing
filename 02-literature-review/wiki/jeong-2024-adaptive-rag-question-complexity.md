# Adaptive-RAG: Learning to adapt retrieval-augmented large language models through question complexity

| | |
|---|---|
| **Set** | Market research agent · AI |
| **Citations** | not checked |
| **Original** | [https://aclanthology.org/2024.naacl-long.389](https://aclanthology.org/2024.naacl-long.389) · local stub: [`raw/jeong-2024-adaptive-rag-question-complexity.md`](../raw/jeong-2024-adaptive-rag-question-complexity.md) |

**APA:** Jeong, S., Baek, J., Cho, S., Hwang, S. J., & Park, J. C. (2024). Adaptive-RAG: Learning to adapt retrieval-augmented large language models through question complexity. In *Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics (Volume 1: Long Papers)* (pp. 7036–7050).

## 1. Research question
Can a system pick how much retrieval and reasoning a question needs, instead of using one fixed strategy for all?

## 2. Limitation of existing methods
Single-step retrieval fails on complex questions; multi-step retrieval wastes compute on simple ones.

## 3. Contributions
A small classifier that predicts question complexity and routes each question to no retrieval, single-step or multi-step retrieval.

## 4. Proposed methods
Classifier trained on automatically labelled complexity; evaluated on single-hop and multi-hop QA for accuracy and efficiency.

## 5. Key findings
Adaptive routing improves the accuracy-efficiency trade-off over fixed strategies.

## 6. Limitations
QA only; complexity labels are derived automatically and only three strategies are considered.

## 7. Author names
Soyeong Jeong, Jinheon Baek, Sukmin Cho, Sung Ju Hwang, Jong C. Park

## 8. Publish year
2024

## 9. Proceedings or journal name
Proceedings of NAACL 2024

---

**Relevance to the Beauty Market Research Agent:** Suggests a third arm for the experiment: a router that decides when a merchant question needs the full adaptive investigation and when a fixed workflow is enough.

*Extracted 2026-10-25 from the abstract, venue page and main results; not a full-text reading. Check numbers against the original before quoting.*
