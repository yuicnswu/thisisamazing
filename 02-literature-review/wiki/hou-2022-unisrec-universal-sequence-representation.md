# Towards universal sequence representation learning for recommender systems

| | |
|---|---|
| **Set** | Highly cited · AI |
| **Citations** | 242 (Liner, undated snapshot; lower bound) |
| **Original** | [https://arxiv.org/abs/2206.05941](https://arxiv.org/abs/2206.05941) · local stub: [`raw/hou-2022-unisrec-universal-sequence-representation.md`](../raw/hou-2022-unisrec-universal-sequence-representation.md) |

**APA:** Hou, Y., Mu, S., Zhao, W. X., Li, Y., Ding, B., & Wen, J.-R. (2022). Towards universal sequence representation learning for recommender systems. In *Proceedings of the 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining*.

## 1. Research question
Can sequential recommenders learn item representations that transfer across domains and to new items?

## 2. Limitation of existing methods
ID-based sequential recommenders cannot represent unseen items or transfer between domains.

## 3. Contributions
UniSRec: text-based item representations with parametric whitening and a mixture-of-experts adaptor; multi-domain pretraining.

## 4. Proposed methods
Encode item text with a frozen language model, adapt with whitening and MoE, and pretrain with sequence–item and sequence–sequence contrastive tasks.

## 5. Key findings
Strong cross-domain and cross-platform transfer, including in inductive settings without item IDs.

## 6. Limitations
Scores new items by text similarity; does not check whether the text supports a particular need.

## 7. Author names
Yupeng Hou, Shanlei Mu, Wayne Xin Zhao, Yaliang Li, Bolin Ding, Ji-Rong Wen

## 8. Publish year
2022

## 9. Proceedings or journal name
Proceedings of the 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining (KDD 2022)

---

**Relevance to the thesis:** Text-based new-item baseline for Paper A; an example of similarity-based licensing.

*Extracted 2026-10-17 from the abstract and main results; not a full-text reading. Check numbers against the original before quoting.*
