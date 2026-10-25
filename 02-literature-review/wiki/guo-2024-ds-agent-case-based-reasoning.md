# DS-Agent: Automated data science by empowering large language models with case-based reasoning

| | |
|---|---|
| **Set** | Market research agent · AI |
| **Citations** | not checked |
| **Original** | [https://arxiv.org/abs/2402.17453](https://arxiv.org/abs/2402.17453) · local stub: [`raw/guo-2024-ds-agent-case-based-reasoning.md`](../raw/guo-2024-ds-agent-case-based-reasoning.md) |

**APA:** Guo, S., Deng, C., Wen, Y., Chen, H., Chang, Y., & Wang, J. (2024). DS-Agent: Automated data science by empowering large language models with case-based reasoning. In *Proceedings of the 41st International Conference on Machine Learning* (PMLR 235).

## 1. Research question
Can reusing expert solutions from past cases make LLM agents reliable and cheap at data-science tasks?

## 2. Limitation of existing methods
LLM agents plan poorly from scratch on data-science tasks and are costly to run repeatedly.

## 3. Contributions
An agent that retrieves and adapts past human solutions (from Kaggle) in a development stage, and reuses its own successful cases in a cheap deployment stage.

## 4. Proposed methods
Case-based reasoning loop: retrieve, reuse, execute, revise with feedback; deployment uses a simplified retrieve-and-reuse step.

## 5. Key findings
High task success with GPT-4 in development and lower cost per run in deployment than full agent loops, while also helping open-source models.

## 6. Limitations
Depends on a library of similar past cases; mostly machine-learning tasks rather than exploratory analysis.

## 7. Author names
Siyuan Guo, Cheng Deng, Ying Wen, Hechang Chen, Yi Chang, Jun Wang

## 8. Publish year
2024

## 9. Proceedings or journal name
Proceedings of the 41st International Conference on Machine Learning

---

**Relevance to the Beauty Market Research Agent:** Suggests a middle path between adaptive and fixed workflows: reuse vetted investigation plans for recurring merchant questions, which can cut time and compute cost.

*Extracted 2026-10-25 from the abstract, venue page and main results; not a full-text reading. Check numbers against the original before quoting.*
