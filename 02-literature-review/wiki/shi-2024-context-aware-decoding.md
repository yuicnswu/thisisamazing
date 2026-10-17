# Trusting your evidence: Hallucinate less with context-aware decoding

| | |
|---|---|
| **Set** | Conference · AI |
| **Citations** | not required (conference set) |
| **Original** | [https://aclanthology.org/2024.naacl-short.69](https://aclanthology.org/2024.naacl-short.69) · local stub: [`raw/shi-2024-context-aware-decoding.md`](../raw/shi-2024-context-aware-decoding.md) |

**APA:** Shi, W., Han, X., Lewis, M., Tsvetkov, Y., Zettlemoyer, L., & Yih, W.-t. (2024). Trusting your evidence: Hallucinate less with context-aware decoding. In *Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics (Volume 2: Short Papers)*.

## 1. Research question
Can decoding alone make LMs pay more attention to the given context and less to their priors?

## 2. Limitation of existing methods
Models often ignore input context in favour of prior knowledge, especially when the two conflict; fixes usually need retraining.

## 3. Contributions
Context-aware decoding (CAD), a training-free contrastive decoding rule.

## 4. Proposed methods
Amplify the difference between output probabilities computed with and without the context.

## 5. Key findings
Improves faithfulness in summarization and knowledge-conflict tasks across model families, with large gains when context contradicts memory.

## 6. Limitations
Always produces an answer; cannot abstain when the context is silent. Adds a second forward pass.

## 7. Author names
Weijia Shi, Xiaochuang Han, Mike Lewis, Yulia Tsvetkov, Luke Zettlemoyer, Wen-tau Yih

## 8. Publish year
2024

## 9. Proceedings or journal name
Proceedings of NAACL 2024 (Volume 2: Short Papers)

---

**Relevance to the thesis:** Training-free baseline for Paper A's verifier. Paper A shows why pushing toward the context is not enough when the context lacks the needed attribute.

*Extracted 2026-10-17 from the abstract and main results; not a full-text reading. Check numbers against the original before quoting.*
