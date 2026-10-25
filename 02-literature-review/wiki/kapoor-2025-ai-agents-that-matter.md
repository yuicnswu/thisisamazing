# AI agents that matter

| | |
|---|---|
| **Set** | Market research agent · AI |
| **Citations** | not checked |
| **Original** | [https://arxiv.org/abs/2407.01502](https://arxiv.org/abs/2407.01502) · local stub: [`raw/kapoor-2025-ai-agents-that-matter.md`](../raw/kapoor-2025-ai-agents-that-matter.md) |

**APA:** Kapoor, S., Stroebl, B., Siegel, Z. S., Nadgir, N., & Narayanan, A. (2025). AI agents that matter. *Transactions on Machine Learning Research*.

## 1. Research question
Are current agent benchmarks and evaluation practices good enough to tell whether agents are useful in the real world?

## 2. Limitation of existing methods
Agent papers report accuracy without cost, overfit to benchmarks, lack holdout sets and mix up model and downstream evaluation.

## 3. Contributions
Shows that simple baselines can match complex agents, argues for joint cost-accuracy (Pareto) evaluation, and gives a framework against shortcuts and overfitting.

## 4. Proposed methods
Re-evaluation of published agents on benchmarks such as HumanEval with cost tracking, plus a review of benchmark practices.

## 5. Key findings
Simple baselines (retrying, escalating model size) matched state-of-the-art agents at much lower cost; many benchmarks allow shortcuts.

## 6. Limitations
Mostly coding and web benchmarks; cost estimates depend on API prices at the time.

## 7. Author names
Sayash Kapoor, Benedikt Stroebl, Zachary S. Siegel, Nitya Nadgir, Arvind Narayanan

## 8. Publish year
2025

## 9. Proceedings or journal name
Transactions on Machine Learning Research

---

**Relevance to the Beauty Market Research Agent:** Defines how the RQ's 'acceptable time and compute cost' must be reported: as a cost-accuracy frontier against simple baselines, with a held-out set of merchant questions.

*Extracted 2026-10-25 from the abstract, venue page and main results; not a full-text reading. Check numbers against the original before quoting.*
