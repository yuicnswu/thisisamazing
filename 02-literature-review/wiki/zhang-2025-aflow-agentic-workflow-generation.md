# AFlow: Automating agentic workflow generation

| | |
|---|---|
| **Set** | Market research agent · AI |
| **Citations** | not checked |
| **Original** | [https://proceedings.iclr.cc/paper_files/paper/2025/hash/5492ecbce4439401798dcd2c90be94cd-Abstract-Conference.html](https://proceedings.iclr.cc/paper_files/paper/2025/hash/5492ecbce4439401798dcd2c90be94cd-Abstract-Conference.html) · local stub: [`raw/zhang-2025-aflow-agentic-workflow-generation.md`](../raw/zhang-2025-aflow-agentic-workflow-generation.md) |

**APA:** Zhang, J., Xiang, J., Yu, Z., Teng, F., Chen, X., Chen, J., Zhuge, M., Cheng, X., Hong, S., Wang, J., Zheng, B., Liu, B., Luo, Y., & Wu, C. (2025). AFlow: Automating agentic workflow generation. In *International Conference on Learning Representations*.

## 1. Research question
Can effective agent workflows be found automatically instead of hand-designed?

## 2. Limitation of existing methods
Workflows are built by hand, and earlier automatic methods search a narrow space.

## 3. Contributions
Treats workflow design as search over code-represented graphs of LLM calls and uses Monte Carlo tree search with execution feedback.

## 4. Proposed methods
MCTS expands and refines workflows using reusable operators and evaluates them on a validation set.

## 5. Key findings
Reported 5.7% average improvement over hand-designed baselines across six benchmarks, and lets smaller models beat GPT-4o on some tasks at a small fraction of its inference cost.

## 6. Limitations
Needs a scored validation set per task family; search itself is costly.

## 7. Author names
Jiayi Zhang, Jinyu Xiang, Zhaoyang Yu, Fengwei Teng, Xionghui Chen, Jiaqi Chen, Mingchen Zhuge, Xin Cheng, Sirui Hong, Jinlin Wang, Bingnan Zheng, Bang Liu, Yuyu Luo, Chenglin Wu

## 8. Publish year
2025

## 9. Proceedings or journal name
International Conference on Learning Representations

---

**Relevance to the Beauty Market Research Agent:** Blurs the adaptive-versus-fixed line: a fixed workflow can be optimised offline. The RQ should say whether the fixed baseline is hand-built or optimised.

*Extracted 2026-10-25 from the abstract, venue page and main results; not a full-text reading. Check numbers against the original before quoting.*
