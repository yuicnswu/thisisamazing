# GPTSwarm: Language agents as optimizable graphs

| | |
|---|---|
| **Set** | Multi-agent and self-evolving systems (added 2026-11-07 for the beauty orchestrator paper) |
| **Citations** | not required |
| **Original** | [https://arxiv.org/abs/2402.16823](https://arxiv.org/abs/2402.16823) · local stub: [`raw/zhuge-2024-gptswarm-language-agents-optimizable-graphs.md`](../raw/zhuge-2024-gptswarm-language-agents-optimizable-graphs.md) |

**APA:** Zhuge, M., Wang, W., Kirsch, L., Faccio, F., Khizbullin, D., & Schmidhuber, J. (2024). GPTSwarm: Language agents as optimizable graphs. In *Proceedings of the 41st International Conference on Machine Learning*.

## 1. Research question
Can language-agent systems be represented as computational graphs whose nodes and connections are optimised automatically?

## 2. Limitation of existing methods
Agent frameworks are hand-wired; prompt engineering and orchestration are tuned separately and manually.

## 3. Contributions
Represents agents as graphs of LLM operations; optimises node prompts and edge connectivity (which agent talks to which).

## 4. Proposed methods
Node-level prompt optimisation and edge-level optimisation of the connection distribution with policy gradients against a task utility.

## 5. Key findings
Optimised graphs improved over hand-designed swarms on several benchmarks, and edge optimisation could learn to ignore adversarial agents.

## 6. Limitations
Utility is measured on the target benchmark; cost of optimisation is secondary; graph search spaces still need a designer.

## 7. Author names
Mingchen Zhuge, Wenyi Wang, Louis Kirsch, Francesco Faccio, Dmitrii Khizbullin, Jürgen Schmidhuber

## 8. Publish year
2024

## 9. Proceedings or journal name
Proceedings of the 41st International Conference on Machine Learning (ICML 2024)

**Relevance to this project:** motivates DP5/DP6 and arm M+ in `beauty-research/proposals/agentic_beauty_market_research.md` §2.4 and §5.4: evolution must run on a small interpretable policy space, be selected on development templates only, and pay for its own cost.
