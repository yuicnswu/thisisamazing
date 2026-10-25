# MiniCheck: Efficient fact-checking of LLMs on grounding documents

| | |
|---|---|
| **Set** | Market research agent · AI |
| **Citations** | not checked |
| **Original** | [https://aclanthology.org/2024.emnlp-main.499](https://aclanthology.org/2024.emnlp-main.499) · local stub: [`raw/tang-2024-minicheck-grounding-fact-checking.md`](../raw/tang-2024-minicheck-grounding-fact-checking.md) |

**APA:** Tang, L., Laban, P., & Durrett, G. (2024). MiniCheck: Efficient fact-checking of LLMs on grounding documents. In *Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing* (pp. 8818–8847).

## 1. Research question
Can a small model check whether LLM output is grounded in documents as well as GPT-4, at much lower cost?

## 2. Limitation of existing methods
Grounding checks with large LLMs are accurate but expensive; small checkers were weaker.

## 3. Contributions
Small fact-checkers trained on synthetic data that requires multi-sentence reasoning, and the LLM-AggreFact benchmark.

## 4. Proposed methods
Synthetic claim-document pairs for training; evaluation across many grounding datasets.

## 5. Key findings
MiniCheck models reach GPT-4-level accuracy on LLM-AggreFact at a small fraction of the cost (the paper reports about 400 times cheaper).

## 6. Limitations
Sentence-level checks; does not judge whether a claim is relevant or important.

## 7. Author names
Liyan Tang, Philippe Laban, Greg Durrett

## 8. Publish year
2024

## 9. Proceedings or journal name
Proceedings of EMNLP 2024

---

**Relevance to the Beauty Market Research Agent:** A cheap verifier for the 'check evidence' step that fits the free-tier budget, and a baseline the earlier Chen et al. (2026) entry already recommends.

*Extracted 2026-10-25 from the abstract, venue page and main results; not a full-text reading. Check numbers against the original before quoting.*
