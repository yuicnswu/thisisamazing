# Why do multi-agent LLM systems fail?

| | |
|---|---|
| **Set** | Multi-agent and self-evolving systems (added 2026-11-07 for the beauty orchestrator paper) |
| **Citations** | not required |
| **Original** | [https://arxiv.org/abs/2503.13657](https://arxiv.org/abs/2503.13657) · local stub: [`raw/cemri-2025-why-multi-agent-llm-systems-fail.md`](../raw/cemri-2025-why-multi-agent-llm-systems-fail.md) |

**APA:** Cemri, M., Pan, M. Z., Yang, S., Agrawal, L. A., Chopra, B., Tiwari, R., Keutzer, K., Parameswaran, A., Klein, D., Ramchandran, K., Zaharia, M., Gonzalez, J. E., & Stoica, I. (2025). *Why do multi-agent LLM systems fail?* (arXiv:2503.13657).

## 1. Research question
Why do multi-agent LLM systems often show small or no gains over single-agent baselines?

## 2. Limitation of existing methods
Gains of multi-agent systems are reported on benchmarks without a systematic account of how they fail.

## 3. Contributions
MAST, a taxonomy of multi-agent system failures built from annotated execution traces of several popular frameworks, with an LLM-as-judge annotation pipeline.

## 4. Proposed methods
Grounded-theory analysis of traces from several multi-agent frameworks, inter-annotator agreement studies, and case studies of interventions.

## 5. Key findings
Failures cluster into specification and system design, inter-agent misalignment, and task verification and termination; simple fixes such as better role specification help only partly.

## 6. Limitations
Preprint; frameworks and tasks are mostly software and general QA, not analytics; the taxonomy is descriptive.

## 7. Author names
Mert Cemri, Melissa Z. Pan, Shuyi Yang, Lakshya A. Agrawal, Bhavya Chopra, Rishabh Tiwari, Kurt Keutzer, Aditya Parameswaran, Dan Klein, Kannan Ramchandran, Matei Zaharia, Joseph E. Gonzalez, Ion Stoica

## 8. Publish year
2025

## 9. Proceedings or journal name
arXiv preprint arXiv:2503.13657

**Relevance to this project:** motivates DP5/DP6 and arm M+ in `beauty-research/proposals/agentic_beauty_market_research.md` §2.4 and §5.4: evolution must run on a small interpretable policy space, be selected on development templates only, and pay for its own cost.
