# AFlow: Automating agentic workflow generation

| | |
|---|---|
| **Set** | Multi-agent and self-evolving systems (added 2026-11-07 for the beauty orchestrator paper) |
| **Citations** | not required |
| **Original** | [https://arxiv.org/abs/2410.10762](https://arxiv.org/abs/2410.10762) · local stub: [`raw/zhang-2025-aflow-agentic-workflow-generation.md`](../raw/zhang-2025-aflow-agentic-workflow-generation.md) |

**APA:** Zhang, J., Xiang, J., Yu, Z., Teng, F., Chen, X., Chen, J., Zhuge, M., Cheng, X., Hong, S., Wang, J., Zheng, B., Liu, B., Luo, Y., & Wu, C. (2025). AFlow: Automating agentic workflow generation. In *International Conference on Learning Representations*.

## 1. Research question
Can the workflow of LLM calls for a task be generated and optimised automatically?

## 2. Limitation of existing methods
Workflows are built by experts; earlier automatic methods optimise prompts or need a hand-fixed workflow skeleton.

## 3. Contributions
Formulates workflow optimisation as search over code-represented workflows; uses Monte Carlo tree search with LLM-proposed modifications and execution feedback.

## 4. Proposed methods
MCTS over workflows composed of operators (generate, ensemble, review and revise), expanding by LLM-written code changes and scoring by execution on a validation split.

## 5. Key findings
Improved over manual and automated baselines on QA, code and math benchmarks, and let smaller models match larger ones at a fraction of the inference cost.

## 6. Limitations
Optimises against a validation split of each benchmark; optimisation cost is reported but not amortised in the comparison; tasks have exact answers, unlike open research briefs.

## 7. Author names
Jiayi Zhang, Jinyu Xiang, Zhaoyang Yu, Fengwei Teng, Xionghui Chen, Jiaqi Chen, Mingchen Zhuge, Xin Cheng, Sirui Hong, Jinlin Wang, Bingnan Zheng, Bang Liu, Yuyu Luo, Chenglin Wu

## 8. Publish year
2025

## 9. Proceedings or journal name
International Conference on Learning Representations (ICLR 2025)

**Relevance to this project:** motivates DP5/DP6 and arm M+ in `beauty-research/proposals/agentic_beauty_market_research.md` §2.4 and §5.4: evolution must run on a small interpretable policy space, be selected on development templates only, and pay for its own cost.
