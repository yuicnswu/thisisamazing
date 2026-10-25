# FActScore: Fine-grained atomic evaluation of factual precision in long form text generation

| | |
|---|---|
| **Set** | Market research agent · AI |
| **Citations** | not checked |
| **Original** | [https://aclanthology.org/2023.emnlp-main.741](https://aclanthology.org/2023.emnlp-main.741) · local stub: [`raw/min-2023-factscore-atomic-factual-precision.md`](../raw/min-2023-factscore-atomic-factual-precision.md) |

**APA:** Min, S., Krishna, K., Lyu, X., Lewis, M., Yih, W.-t., Koh, P. W., Iyyer, M., Zettlemoyer, L., & Hajishirzi, H. (2023). FActScore: Fine-grained atomic evaluation of factual precision in long form text generation. In *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing* (pp. 12076–12100).

## 1. Research question
How can the factual precision of long generated text be measured when it mixes true and false statements?

## 2. Limitation of existing methods
Binary judgements of whole outputs hide how much of a long text is wrong.

## 3. Contributions
FActScore: split text into atomic facts and compute the share supported by a knowledge source, plus an automatic estimator.

## 4. Proposed methods
Human and model-based decomposition into atomic facts, each checked against Wikipedia; tested on people biographies.

## 5. Key findings
Commercial models had low factual precision on biographies (ChatGPT about 58%); the automatic estimator tracked human scores closely.

## 6. Limitations
Measures precision, not recall; needs a trusted knowledge source; biographies only.

## 7. Author names
Sewon Min, Kalpesh Krishna, Xinxi Lyu, Mike Lewis, Wen-tau Yih, Pang Wei Koh, Mohit Iyyer, Luke Zettlemoyer, Hannaneh Hajishirzi

## 8. Publish year
2023

## 9. Proceedings or journal name
Proceedings of EMNLP 2023

---

**Relevance to the Beauty Market Research Agent:** The unit of analysis for the brief's evidence check: decompose each finding into atomic claims and verify each against the SQLite reviews and listings.

*Extracted 2026-10-25 from the abstract, venue page and main results; not a full-text reading. Check numbers against the original before quoting.*
