# Entity-based knowledge conflicts in question answering

| | |
|---|---|
| **Set** | Highly cited · AI |
| **Citations** | 278 (Liner, undated snapshot; lower bound) |
| **Original** | [https://aclanthology.org/2021.emnlp-main.565](https://aclanthology.org/2021.emnlp-main.565) · local stub: [`raw/longpre-2021-entity-based-knowledge-conflicts.md`](../raw/longpre-2021-entity-based-knowledge-conflicts.md) |

**APA:** Longpre, S., Perisetla, K., Chen, A., Ramesh, N., DuBois, C., & Singh, S. (2021). Entity-based knowledge conflicts in question answering. In *Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing*.

## 1. Research question
When the passage contradicts what a QA model memorized, does the model read the passage or recall its memory?

## 2. Limitation of existing methods
QA evaluation assumed models read the passage; reliance on memory was invisible because passage and memory usually agree.

## 3. Contributions
Formalizes knowledge conflicts; an entity-substitution framework; a training fix.

## 4. Proposed methods
Replace the answer entity in passages with another entity of the same type and measure whether models output the substituted or the original answer.

## 5. Key findings
Models often over-rely on parametric knowledge and hallucinate the memorized answer; training with substituted examples reduces this and improves out-of-distribution generalization.

## 6. Limitations
Substitutions can be incoherent; only extractive/generative QA.

## 7. Author names
Shayne Longpre, Kartik Perisetla, Anthony Chen, Nikhil Ramesh, Chris DuBois, Sameer Singh

## 8. Publish year
2021

## 9. Proceedings or journal name
Proceedings of EMNLP 2021

---

**Relevance to the thesis:** Founding diagnosis of evidence versus memory. Paper A's edited and brand-swap variants extend entity substitution to product attributes.

*Extracted 2026-10-17 from the abstract and main results; not a full-text reading. Check numbers against the original before quoting.*
