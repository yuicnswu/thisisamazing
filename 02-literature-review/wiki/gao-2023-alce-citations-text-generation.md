# Enabling large language models to generate text with citations

| | |
|---|---|
| **Set** | Highly cited · AI |
| **Citations** | 395 (Liner, read 2026-10-17; lower bound) |
| **Original** | [https://arxiv.org/abs/2305.14627](https://arxiv.org/abs/2305.14627) · local stub: [`raw/gao-2023-alce-citations-text-generation.md`](../raw/gao-2023-alce-citations-text-generation.md) |

**APA:** Gao, T., Yen, H., Yu, J., & Chen, D. (2023). Enabling large language models to generate text with citations. In *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing*.

## 1. Research question
Can LLMs generate answers whose citations actually support each statement, and how should this be measured?

## 2. Limitation of existing methods
No reproducible benchmark measured whether LLM citations support the generated text.

## 3. Contributions
ALCE benchmark with automatic metrics for fluency, correctness and citation quality (recall and precision via NLI).

## 4. Proposed methods
Retrieve passages, prompt LLMs to answer with citations, and score support with an NLI model.

## 5. Key findings
Even the best models lacked complete citation support for a large share of answers.

## 6. Limitations
NLI-based support judgement is itself imperfect; generation, not decisions.

## 7. Author names
Tianyu Gao, Howard Yen, Jiatong Yu, Danqi Chen

## 8. Publish year
2023

## 9. Proceedings or journal name
Proceedings of EMNLP 2023

---

**Relevance to the thesis:** Shows support can be scored automatically with entailment, as Paper A's verifier does; Paper A applies support to decisions over constraints.

*Extracted 2026-10-17 from the abstract and main results; not a full-text reading. Check numbers against the original before quoting.*
