# Shopping Companion: Benchmarking and training LLM agents for long-horizon preference-grounded e-commerce tasks

| | |
|---|---|
| **Set** | 2025–2026 field check |
| **Citations** | not required |
| **Original** | [https://arxiv.org/abs/2603.14864](https://arxiv.org/abs/2603.14864) · local stub: [`raw/yu-2026-shopping-companion-preference-grounded.md`](../raw/yu-2026-shopping-companion-preference-grounded.md) |

**APA:** Yu, Z., Xiao, K., Zhao, H., Luo, T., & Zeng, X. (2026). *Shopping Companion: Benchmarking and training LLM agents for long-horizon preference-grounded e-commerce tasks* (arXiv:2603.14864). arXiv.

## 1. Research question
How can LLM shopping agents be evaluated and trained on long-horizon tasks that need cross-session preference memory?

## 2. Limitation of existing methods
Shopping benchmarks are single-session and do not test preference memory.

## 3. Contributions
Shopping Companion Bench over 1.2M real items, and annotation-free tool-wise rewards.

## 4. Proposed methods
Two long-horizon tasks; reward each tool call; fine-tune a 4B model.

## 5. Key findings
GPT-5 stays under 70% success; failures come mainly from preference hallucination and **insufficient verification of product attributes against user requirements**.

## 6. Limitations
No abstention or missing-attribute scoring described.

## 7. Author names
Zijian Yu, Kejun Xiao, Huaipeng Zhao, Tao Luo, Xiaoyi Zeng

## 8. Publish year
2026

## 9. Proceedings or journal name
arXiv preprint arXiv:2603.14864

---

**Relevance to the thesis:** Names the thesis's failure mode (unverified attributes) as a top agent error, without a benchmark that isolates it. Supports the benchmark contribution.

*Extracted 2026-10-21 from the arXiv abstract page or HTML (fetched that day), for the repositioning after the 2026 field check (`team-opinion/field-check-2026.md` in the project files); not a full-text reading. Check numbers against the original before quoting.*
