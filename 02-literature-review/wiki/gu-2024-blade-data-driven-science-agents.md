# BLADE: Benchmarking language model agents for data-driven science

| | |
|---|---|
| **Set** | Market research agent · AI |
| **Citations** | not checked |
| **Original** | [https://aclanthology.org/2024.findings-emnlp.815](https://aclanthology.org/2024.findings-emnlp.815) · local stub: [`raw/gu-2024-blade-data-driven-science-agents.md`](../raw/gu-2024-blade-data-driven-science-agents.md) |

**APA:** Gu, K., Shang, R., Jiang, R., Kuang, K., Lin, R.-J., Lyu, D., Mao, Y., Pan, Y., Wu, T., Yu, J., Zhang, Y., Zhang, T. M., Zhu, L., Merrill, M. A., Heer, J., & Althoff, T. (2024). BLADE: Benchmarking language model agents for data-driven science. In *Findings of the Association for Computational Linguistics: EMNLP 2024*.

## 1. Research question
How well do LLM agents make the many justifiable analysis decisions (variables, transformations, models) that open-ended research questions require?

## 2. Limitation of existing methods
Analyses have many valid paths, so single-answer benchmarks cannot judge whether an agent's analytic choices are sound.

## 3. Contributions
A benchmark of 12 datasets and research questions with analyses collected independently from expert data scientists, plus automatic matching of agent decisions to the space of expert decisions.

## 4. Proposed methods
Agents produce conceptual variables, transformations and statistical models; these are matched against expert choices to score accuracy and diversity.

## 5. Key findings
Models without data access produce mostly basic analyses; agents that interact with the data produce more diverse and more expert-like analysis decisions, though still incomplete.

## 6. Limitations
Small set of datasets from the social and health sciences; matching to expert choices does not cover every valid analysis.

## 7. Author names
Ken Gu, Ruoxi Shang, Ruien Jiang, Keying Kuang, Richard-John Lin, Donghe Lyu, Yue Mao, Youran Pan, Teng Wu, Jiaqian Yu, Yikun Zhang, Tianmai M. Zhang, Lanyi Zhu, Mike A. Merrill, Jeffrey Heer, Tim Althoff

## 8. Publish year
2024

## 9. Proceedings or journal name
Findings of the Association for Computational Linguistics: EMNLP 2024

---

**Relevance to the Beauty Market Research Agent:** Directly relevant to 'investigation coverage': it shows how to score which analyses an agent chose against a set of expert analyses, a fair way to compare adaptive and fixed pipelines.

*Extracted 2026-10-25 from the abstract, venue page and main results; not a full-text reading. Check numbers against the original before quoting.*
