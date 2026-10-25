# InsightBench: Evaluating business analytics agents through multi-step insight generation

| | |
|---|---|
| **Set** | Market research agent · AI |
| **Citations** | not checked |
| **Original** | [https://proceedings.iclr.cc/paper_files/paper/2025/hash/0dfe31d6e703e138d46a7d2fced38b7c-Abstract-Conference.html](https://proceedings.iclr.cc/paper_files/paper/2025/hash/0dfe31d6e703e138d46a7d2fced38b7c-Abstract-Conference.html) · local stub: [`raw/sahu-2025-insightbench-business-analytics-agents.md`](../raw/sahu-2025-insightbench-business-analytics-agents.md) |

**APA:** Sahu, G., Puri, A., Rodriguez, J. A., Abaskohi, A., Chegini, M., Drouin, A., Taslakian, P., Zantedeschi, V., Lacoste, A., Vazquez, D., Chapados, N., Pal, C., Rajeswar, S., & Laradji, I. (2025). InsightBench: Evaluating business analytics agents through multi-step insight generation. In *International Conference on Learning Representations*.

## 1. Research question
Can LLM agents carry out a full business-analytics workflow, from posing questions to summarising insights and recommended actions, rather than answering one query at a time?

## 2. Limitation of existing methods
Data-analysis benchmarks score single queries (one table, one answer), so they miss whether an agent finds the insights that matter in a dataset.

## 3. Contributions
A benchmark of 100 business datasets (finance, incident management and others) with planted insights, an LLaMA-3 based two-way evaluator, and the AgentPoirot baseline agent.

## 4. Proposed methods
Each dataset carries curated ground-truth insights. An agent plans questions, runs code, interprets outputs and writes a summary; the evaluator matches generated insights to the planted ones.

## 5. Key findings
AgentPoirot, which plans multi-step analyses, beats single-query tools such as the Pandas Agent. Results vary across open and closed LLMs and across evaluation strategies.

## 6. Limitations
Insights are planted in synthetic data, so the benchmark measures recovery of known patterns, not discovery in messy real data. Evaluation leans on an LLM judge.

## 7. Author names
Gaurav Sahu, Abhay Puri, Juan A. Rodriguez, Amirhossein Abaskohi, Mohammad Chegini, Alexandre Drouin, Perouz Taslakian, Valentina Zantedeschi, Alexandre Lacoste, David Vazquez, Nicolas Chapados, Christopher Pal, Sai Rajeswar, Issam Laradji

## 8. Publish year
2025

## 9. Proceedings or journal name
International Conference on Learning Representations

---

**Relevance to the Beauty Market Research Agent:** The closest benchmark to the merchant brief. Its planted-insight design is a template for scoring evidence accuracy and coverage on the Sephora moisturizer database, and AgentPoirot is a natural adaptive baseline.

*Extracted 2026-10-25 from the abstract, venue page and main results; not a full-text reading. Check numbers against the original before quoting.*
