# InfiAgent-DABench: Evaluating agents on data analysis tasks

| | |
|---|---|
| **Set** | Market research agent · AI |
| **Citations** | not checked |
| **Original** | [https://arxiv.org/abs/2401.05507](https://arxiv.org/abs/2401.05507) · local stub: [`raw/hu-2024-infiagent-dabench-data-analysis-agents.md`](../raw/hu-2024-infiagent-dabench-data-analysis-agents.md) |

**APA:** Hu, X., Zhao, Z., Wei, S., Chai, Z., Ma, Q., Wang, G., Wang, X., Su, J., Xu, J., Zhu, M., Cheng, Y., Yuan, J., Li, J., Kuang, K., Yang, Y., Yang, H., & Wu, F. (2024). InfiAgent-DABench: Evaluating agents on data analysis tasks. In *Proceedings of the 41st International Conference on Machine Learning* (PMLR 235). **[check details: author list]**

## 1. Research question
How can data-analysis agents be evaluated automatically and reliably on realistic CSV tasks?

## 2. Limitation of existing methods
Open-ended analysis questions are hard to grade automatically, so earlier evaluations relied on humans or loose matching.

## 3. Contributions
DAEval, a set of questions over CSV files reformatted into closed-form answers ('format prompting'), an agent framework, and the DAAgent model.

## 4. Proposed methods
Questions are generated and reviewed, then converted so answers can be checked exactly; agents run code in a sandbox and are scored by exact match.

## 5. Key findings
Benchmarked many LLMs and showed current models still fail many realistic analysis tasks; a tuned open model (DAAgent) improves over its base.

## 6. Limitations
Closed-form answers favour calculation questions over interpretation; tasks are single-file.

## 7. Author names
Xueyu Hu, Ziyu Zhao, Shuang Wei, Ziwei Chai, Qianli Ma, Guoyin Wang, Xuwu Wang, Jing Su, Jingjing Xu, Ming Zhu, Yao Cheng, Jianbo Yuan, Jiwei Li, Kun Kuang, Yang Yang, Hongxia Yang, Fei Wu

## 8. Publish year
2024

## 9. Proceedings or journal name
Proceedings of the 41st International Conference on Machine Learning

---

**Relevance to the Beauty Market Research Agent:** Evidence for the design choice that Python computes the counts and the LLM interprets. Its exact-match checking is the way to grade the brief's 'calculated counts'.

*Extracted 2026-10-25 from the abstract, venue page and main results; not a full-text reading. Check numbers against the original before quoting.*
