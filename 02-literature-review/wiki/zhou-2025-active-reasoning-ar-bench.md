# From passive to active reasoning: Can large language models ask the right questions under incomplete information?

| | |
|---|---|
| **Set** | Conference · AI |
| **Citations** | not required (conference set) |
| **Original** | [https://proceedings.mlr.press/v267/zhou25e.html](https://proceedings.mlr.press/v267/zhou25e.html) · local stub: [`raw/zhou-2025-active-reasoning-ar-bench.md`](../raw/zhou-2025-active-reasoning-ar-bench.md) |

**APA:** Zhou, Z., Feng, X., Zhu, Z., Yao, J., Koyejo, S., & Han, B. (2025). From passive to active reasoning: Can large language models ask the right questions under incomplete information? In *Proceedings of the 42nd International Conference on Machine Learning* (PMLR 267, pp. 78714–78758).

## 1. Research question
Can LLMs actively gather missing information through interaction, rather than reasoning only over complete inputs?

## 2. Limitation of existing methods
Reasoning benchmarks give all information up front, so they cannot test whether a model knows what it is missing.

## 3. Contributions
AR-Bench, covering detective cases, situation puzzles and number guessing (commonsense, logical and symbolic reasoning).

## 4. Proposed methods
Evaluate LLMs that must ask questions to obtain hidden facts; test prompting, tree search and post-training.

## 5. Key findings
Current LLMs often fail to obtain or use the information they need; tree search and post-training give only modest gains.

## 6. Limitations
Puzzle domains; no cost model for questions and no guarantee on when to stop.

## 7. Author names
Zhanke Zhou, Xiao Feng, Zhaocheng Zhu, Jiangchao Yao, Sanmi Koyejo, Bo Han

## 8. Publish year
2025

## 9. Proceedings or journal name
Proceedings of the 42nd International Conference on Machine Learning (ICML), PMLR 267, pp. 78714–78758

---

**Relevance to the thesis:** Motivates Paper A's acquisition policy. Paper A stops on support rather than confidence, and gives a cost-ordered fallback for inspecting listing fields.

*Extracted 2026-10-17 from the abstract and main results; not a full-text reading. Check numbers against the original before quoting.*
