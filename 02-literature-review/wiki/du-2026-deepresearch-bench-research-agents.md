# DeepResearch Bench: A comprehensive benchmark for deep research agents

| | |
|---|---|
| **Set** | Market research agent · AI |
| **Citations** | not checked |
| **Original** | [https://arxiv.org/abs/2506.11763](https://arxiv.org/abs/2506.11763) · local stub: [`raw/du-2026-deepresearch-bench-research-agents.md`](../raw/du-2026-deepresearch-bench-research-agents.md) |

**APA:** Du, M., Xu, B., Zhu, C., Wang, X., & Mao, Z. (2026). DeepResearch Bench: A comprehensive benchmark for deep research agents. In *International Conference on Learning Representations*.

## 1. Research question
How should agents that search and write cited research reports be evaluated?

## 2. Limitation of existing methods
No benchmark scored both the quality of a research report and whether its citations support its statements.

## 3. Contributions
100 expert-written PhD-level tasks across 22 fields, plus RACE (reference-based report quality) and FACT (citation accuracy and effective citations).

## 4. Proposed methods
RACE has a judge model weight comprehensiveness, depth, instruction following and readability against a reference report; FACT extracts statement-URL pairs and checks support.

## 5. Key findings
Commercial deep-research agents differ on quality and citations (e.g., citation accuracy from about 78% to 90%); RACE agrees with humans about as often as humans agree with each other.

## 6. Limitations
Web-research tasks, not analysis of a private database; LLM judges introduce their own biases.

## 7. Author names
Mingxuan Du, Benfeng Xu, Chiwei Zhu, Xiaorui Wang, Zhendong Mao

## 8. Publish year
2026

## 9. Proceedings or journal name
International Conference on Learning Representations

---

**Relevance to the Beauty Market Research Agent:** FACT is almost exactly the 'evidence accuracy' metric for the merchant brief (does each quoted review support its finding?), and RACE is a template for scoring usefulness.

*Extracted 2026-10-25 from the abstract, venue page and main results; not a full-text reading. Check numbers against the original before quoting.*
