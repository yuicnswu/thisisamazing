# Automated design of agentic systems

| | |
|---|---|
| **Set** | Multi-agent and self-evolving systems (added 2026-11-07 for the beauty orchestrator paper) |
| **Citations** | not required |
| **Original** | [https://arxiv.org/abs/2408.08435](https://arxiv.org/abs/2408.08435) · local stub: [`raw/hu-2025-automated-design-agentic-systems.md`](../raw/hu-2025-automated-design-agentic-systems.md) |

**APA:** Hu, S., Lu, C., & Clune, J. (2025). Automated design of agentic systems. In *International Conference on Learning Representations*.

## 1. Research question
Can agentic systems be designed automatically, by a meta agent that writes new agents in code, instead of by hand?

## 2. Limitation of existing methods
Hand-designed agent building blocks (chain-of-thought, self-reflection, role assignment) are combined manually; earlier automation searched only prompts or fixed graph structures.

## 3. Contributions
Defines the research area ADAS; proposes Meta Agent Search, in which a meta agent iteratively programs new agents in Python and keeps an archive of discoveries.

## 4. Proposed methods
Meta Agent Search: an LLM proposes a new agent as code, it is evaluated on a validation set, and the result and code are added to an archive that conditions the next proposal.

## 5. Key findings
Discovered agents outperformed hand-designed baselines on reading comprehension, math and science QA, and transferred across domains and models.

## 6. Limitations
Selection uses performance on the benchmark's own validation data; the search cost is large and is not charged against the gains; the search space (arbitrary code) makes discovered agents hard to interpret or audit.

## 7. Author names
Shengran Hu, Cong Lu, Jeff Clune

## 8. Publish year
2025

## 9. Proceedings or journal name
International Conference on Learning Representations (ICLR 2025)

**Relevance to this project:** motivates DP5/DP6 and arm M+ in `beauty-research/proposals/agentic_beauty_market_research.md` §2.4 and §5.4: evolution must run on a small interpretable policy space, be selected on development templates only, and pay for its own cost.
