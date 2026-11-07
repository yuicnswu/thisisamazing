# Multi-agent architecture search via agentic supernet

| | |
|---|---|
| **Set** | Multi-agent and self-evolving systems (added 2026-11-07 for the beauty orchestrator paper) |
| **Citations** | not required |
| **Original** | [https://arxiv.org/abs/2502.04180](https://arxiv.org/abs/2502.04180) · local stub: [`raw/zhang-2025-maas-multi-agent-architecture-search.md`](../raw/zhang-2025-maas-multi-agent-architecture-search.md) |

**APA:** Zhang, G., Niu, L., Fang, J., Wang, K., Bai, L., & Wang, X. (2025). Multi-agent architecture search via agentic supernet. In *Proceedings of the 42nd International Conference on Machine Learning*.

## 1. Research question
Can one search produce multi-agent systems that adapt to each query's difficulty and budget, instead of one fixed architecture for all queries?

## 2. Limitation of existing methods
Automated multi-agent design returns a single complex system for every query, which wastes compute on easy queries.

## 3. Contributions
An agentic supernet: a distribution over multi-agent architectures from which a controller samples a query-dependent system, trained with performance and cost together.

## 4. Proposed methods
Supernet of agentic operators with a learned, query-conditioned sampler optimised on task performance and inference cost.

## 5. Key findings
Reports higher accuracy than prior automated systems with a fraction of their inference and training cost, and transfer across datasets and models.

## 6. Limitations
Cost-aware, but optimisation and evaluation use the same benchmarks; no evidence ledger or claim-level verification; exact-answer tasks only.

## 7. Author names
Guibin Zhang, Luyang Niu, Junfeng Fang, Kun Wang, Lei Bai, Xiang Wang

## 8. Publish year
2025

## 9. Proceedings or journal name
Proceedings of the 42nd International Conference on Machine Learning (ICML 2025)

**Relevance to this project:** motivates DP5/DP6 and arm M+ in `beauty-research/proposals/agentic_beauty_market_research.md` §2.4 and §5.4: evolution must run on a small interpretable policy space, be selected on development templates only, and pay for its own cost.
