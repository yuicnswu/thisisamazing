# DSPy: Compiling declarative language model calls into self-improving pipelines

| | |
|---|---|
| **Set** | Multi-agent and self-evolving systems (added 2026-11-07 for the beauty orchestrator paper) |
| **Citations** | not required |
| **Original** | [https://arxiv.org/abs/2310.03714](https://arxiv.org/abs/2310.03714) · local stub: [`raw/khattab-2024-dspy-self-improving-pipelines.md`](../raw/khattab-2024-dspy-self-improving-pipelines.md) |

**APA:** Khattab, O., Singhvi, A., Maheshwari, P., Zhang, Z., Santhanam, K., Vardhamanan, S., Haq, S., Sharma, A., Joshi, T. T., Moazam, H., Miller, H., Zaharia, M., & Potts, C. (2024). DSPy: Compiling declarative language model calls into self-improving pipelines. In *International Conference on Learning Representations*.

## 1. Research question
Can LM pipelines be written as declarative modules and optimised automatically instead of by hand-crafted prompts?

## 2. Limitation of existing methods
Pipelines depend on long hand-written prompt templates that are brittle and do not transfer between models.

## 3. Contributions
A programming model of parameterised modules with signatures, and a compiler (teleprompters) that bootstraps demonstrations and optimises prompts to maximise a metric.

## 4. Proposed methods
Modules (Predict, ChainOfThought, ReAct) composed in Python; optimisers bootstrap and select few-shot demonstrations and instructions against a user metric on training data.

## 5. Key findings
Compiled pipelines beat few-shot prompting and expert-written prompt chains on math word problems and multi-hop QA, including with small open models.

## 6. Limitations
Needs a metric and training examples; optimising on the same small set can overfit; optimises prompts and demonstrations, not control or stopping policy.

## 7. Author names
Omar Khattab, Arnav Singhvi, Paridhi Maheshwari, Zhiyuan Zhang, Keshav Santhanam, Sri Vardhamanan, Saiful Haq, Ashutosh Sharma, Thomas T. Joshi, Hanna Moazam, Heather Miller, Matei Zaharia, Christopher Potts

## 8. Publish year
2024

## 9. Proceedings or journal name
International Conference on Learning Representations (ICLR 2024)

**Relevance to this project:** motivates DP5/DP6 and arm M+ in `beauty-research/proposals/agentic_beauty_market_research.md` §2.4 and §5.4: evolution must run on a small interpretable policy space, be selected on development templates only, and pay for its own cost.
