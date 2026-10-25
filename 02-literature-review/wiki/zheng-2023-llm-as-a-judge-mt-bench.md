# Judging LLM-as-a-judge with MT-Bench and Chatbot Arena

| | |
|---|---|
| **Set** | Market research agent · AI |
| **Citations** | not checked |
| **Original** | [https://arxiv.org/abs/2306.05685](https://arxiv.org/abs/2306.05685) · local stub: [`raw/zheng-2023-llm-as-a-judge-mt-bench.md`](../raw/zheng-2023-llm-as-a-judge-mt-bench.md) |

**APA:** Zheng, L., Chiang, W.-L., Sheng, Y., Zhuang, S., Wu, Z., Zhuang, Y., Lin, Z., Li, Z., Li, D., Xing, E. P., Zhang, H., Gonzalez, J. E., & Stoica, I. (2023). Judging LLM-as-a-judge with MT-Bench and Chatbot Arena. In *Advances in Neural Information Processing Systems 36* (Datasets and Benchmarks Track).

## 1. Research question
Can strong LLMs stand in for human judges of open-ended answers?

## 2. Limitation of existing methods
Human evaluation of open-ended outputs is slow and costly; automatic metrics miss quality.

## 3. Contributions
MT-Bench, Chatbot Arena, and an analysis of LLM-judge biases (position, verbosity, self-enhancement) with mitigations.

## 4. Proposed methods
Compared GPT-4 judgements with expert and crowd preferences.

## 5. Key findings
GPT-4 as judge agreed with humans over 80% of the time, about as often as humans agree with each other, but showed systematic biases.

## 6. Limitations
Chat tasks; judge biases remain; agreement is not accuracy on factual questions.

## 7. Author names
Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric P. Xing, Hao Zhang, Joseph E. Gonzalez, Ion Stoica

## 8. Publish year
2023

## 9. Proceedings or journal name
Advances in Neural Information Processing Systems 36 (Datasets and Benchmarks Track)

---

**Relevance to the Beauty Market Research Agent:** If brief usefulness is scored by an LLM judge before the merchant study, these biases (especially verbosity) must be controlled, since adaptive agents write longer briefs.

*Extracted 2026-10-25 from the abstract, venue page and main results; not a full-text reading. Check numbers against the original before quoting.*
