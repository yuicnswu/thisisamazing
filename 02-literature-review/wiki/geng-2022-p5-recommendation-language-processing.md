# Recommendation as language processing (RLP): A unified pretrain, personalized prompt & predict paradigm (P5)

| | |
|---|---|
| **Set** | Highly cited · AI |
| **Citations** | 545 (Liner, read 2026-10-17; lower bound) |
| **Original** | [https://arxiv.org/abs/2203.13366](https://arxiv.org/abs/2203.13366) · local stub: [`raw/geng-2022-p5-recommendation-language-processing.md`](../raw/geng-2022-p5-recommendation-language-processing.md) |

**APA:** Geng, S., Liu, S., Fu, Z., Ge, Y., & Zhang, Y. (2022). Recommendation as language processing (RLP): A unified pretrain, personalized prompt & predict paradigm (P5). In *Proceedings of the 16th ACM Conference on Recommender Systems*.

## 1. Research question
Can many recommendation tasks be unified as text-to-text language processing?

## 2. Limitation of existing methods
Each recommendation task needed its own model and features.

## 3. Contributions
P5: one text-to-text model trained with personalized prompts for rating, sequential, explanation, review and direct recommendation.

## 4. Proposed methods
Convert user–item data into natural-language prompts and train an encoder–decoder language model on all tasks.

## 5. Key findings
P5 matches or beats task-specific baselines and shows some zero-shot transfer to new prompts and items.

## 6. Limitations
Uses item IDs as tokens, so new items are hard; outputs are not checked against item evidence.

## 7. Author names
Shijie Geng, Shuchang Liu, Zuohui Fu, Yingqiang Ge, Yongfeng Zhang

## 8. Publish year
2022

## 9. Proceedings or journal name
Proceedings of the 16th ACM Conference on Recommender Systems (RecSys 2022)

---

**Relevance to the thesis:** Early LLM-recommender baseline; illustrates recommending from learned associations rather than listing evidence.

*Extracted 2026-10-17 from the abstract and main results; not a full-text reading. Check numbers against the original before quoting.*
