# Agentless: Demystifying LLM-based software engineering agents

| | |
|---|---|
| **Set** | Market research agent · AI |
| **Citations** | not checked |
| **Original** | [https://arxiv.org/abs/2407.01489](https://arxiv.org/abs/2407.01489) · local stub: [`raw/xia-2025-agentless-software-engineering-agents.md`](../raw/xia-2025-agentless-software-engineering-agents.md) |

**APA:** Xia, C. S., Deng, Y., Dunn, S., & Zhang, L. (2025). Agentless: Demystifying LLM-based software engineering agents. *Proceedings of the ACM on Software Engineering, 2*(FSE).

## 1. Research question
Do autonomous agents that decide their own next actions actually beat a simple fixed pipeline?

## 2. Limitation of existing methods
Agent systems are complex, costly and hard to analyse, and few studies test them against a strong fixed workflow.

## 3. Contributions
Agentless, a fixed three-phase pipeline (localise, repair, validate) with no agent deciding future actions, plus a cleaned benchmark subset.

## 4. Proposed methods
A predetermined sequence of LLM calls and tests, compared with open-source and commercial agents on SWE-bench Lite.

## 5. Key findings
The fixed pipeline reached the best open-source result at the time (32% on SWE-bench Lite) at a low cost per issue (about $0.70), beating many agents.

## 6. Limitations
Software repair has fast executable feedback; results may not carry over to open-ended analysis where the right next step is less obvious.

## 7. Author names
Chunqiu Steven Xia, Yinlin Deng, Soren Dunn, Lingming Zhang

## 8. Publish year
2025

## 9. Proceedings or journal name
Proceedings of the ACM on Software Engineering (FSE 2025)

---

**Relevance to the Beauty Market Research Agent:** The strongest published case for the null hypothesis in the RQ. The fixed analytical workflow baseline must be built as carefully as Agentless, or the comparison will flatter the agent.

*Extracted 2026-10-25 from the abstract, venue page and main results; not a full-text reading. Check numbers against the original before quoting.*
