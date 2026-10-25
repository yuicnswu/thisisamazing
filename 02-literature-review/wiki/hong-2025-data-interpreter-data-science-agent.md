# Data Interpreter: An LLM agent for data science

| | |
|---|---|
| **Set** | Market research agent · AI |
| **Citations** | not checked |
| **Original** | [https://aclanthology.org/2025.findings-acl.1016/](https://aclanthology.org/2025.findings-acl.1016/) · local stub: [`raw/hong-2025-data-interpreter-data-science-agent.md`](../raw/hong-2025-data-interpreter-data-science-agent.md) |

**APA:** Hong, S., Lin, Y., Liu, B., Liu, B., Wu, B., Zhang, C., Li, D., Chen, J., Zhang, J., Wang, J., Zhang, L., Zhang, L., Yang, M., Zhuge, M., Guo, T., Zhou, T., Tao, W., Tang, X., Lu, X., Zheng, X., Liang, X., Fei, Y., Cheng, Y., Wang, Y., Gou, Z., Xu, Z., & Wu, C. (2025). Data Interpreter: An LLM agent for data science. In *Findings of the Association for Computational Linguistics: ACL 2025*.

## 1. Research question
How can an LLM agent handle long, interdependent data-science tasks whose plan must change as intermediate results arrive?

## 2. Limitation of existing methods
Earlier agents follow linear plans and struggle when a step's output should change later steps.

## 3. Contributions
An agent that models a task as a hierarchical graph of sub-tasks and regenerates parts of the graph as data and results change.

## 4. Proposed methods
Hierarchical graph modelling of the task, programmable node generation with code execution, and iterative refinement of the graph after each result.

## 5. Key findings
Large gains over open-source baselines on data-analysis benchmarks, including InfiAgent-DABench (reported 75.9% to 94.9%) and machine-learning tasks.

## 6. Limitations
Benchmarks are mostly well-posed tasks with known answers; cost and failure analysis of re-planning are limited.

## 7. Author names
Sirui Hong, Yizhang Lin, Bang Liu, Bangbang Liu, Binhao Wu, Ceyao Zhang, Danyang Li, Jiaqi Chen, Jiayi Zhang, Jinlin Wang, Li Zhang, Lingyao Zhang, Min Yang, Mingchen Zhuge, Taicheng Guo, Tuo Zhou, Wei Tao, Xiangru Tang, Xiangtao Lu, Xiawu Zheng, Xinbing Liang, Yaying Fei, Yuheng Cheng, Yunfei Wang, Zhibin Gou, Zongze Xu, Chenglin Wu

## 8. Publish year
2025

## 9. Proceedings or journal name
Findings of the Association for Computational Linguistics: ACL 2025

---

**Relevance to the Beauty Market Research Agent:** A concrete design for 'choose follow-up analyses based on what it discovers'. Its graph re-planning is close to what LangGraph will implement and is a strong adaptive comparator.

*Extracted 2026-10-25 from the abstract, venue page and main results; not a full-text reading. Check numbers against the original before quoting.*
