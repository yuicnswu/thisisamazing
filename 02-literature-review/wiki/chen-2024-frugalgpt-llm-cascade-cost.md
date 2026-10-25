# FrugalGPT: How to use large language models while reducing cost and improving performance

| | |
|---|---|
| **Set** | Market research agent · AI |
| **Citations** | not checked |
| **Original** | [https://arxiv.org/abs/2305.05176](https://arxiv.org/abs/2305.05176) · local stub: [`raw/chen-2024-frugalgpt-llm-cascade-cost.md`](../raw/chen-2024-frugalgpt-llm-cascade-cost.md) |

**APA:** Chen, L., Zaharia, M., & Zou, J. (2024). FrugalGPT: How to use large language models while reducing cost and improving performance. *Transactions on Machine Learning Research*.

## 1. Research question
How can applications cut LLM API costs without losing accuracy?

## 2. Limitation of existing methods
Applications send every query to one large model, although prices differ by orders of magnitude across models.

## 3. Contributions
Three cost-saving strategies (prompt adaptation, approximation, cascades) and an LLM cascade that learns when a cheaper model's answer is good enough.

## 4. Proposed methods
A scorer judges each answer; queries escalate to more expensive models only when needed.

## 5. Key findings
The cascade matched the best single model's accuracy with large cost reductions (up to 98% in reported settings).

## 6. Limitations
Prices and models have changed since; tested on classification-style tasks.

## 7. Author names
Lingjiao Chen, Matei Zaharia, James Zou

## 8. Publish year
2024

## 9. Proceedings or journal name
Transactions on Machine Learning Research

---

**Relevance to the Beauty Market Research Agent:** Relevant to the Groq free tier and Ollama plan: a cascade (small model first, larger model on hard steps) is a cost lever to report alongside accuracy.

*Extracted 2026-10-25 from the abstract, venue page and main results; not a full-text reading. Check numbers against the original before quoting.*
