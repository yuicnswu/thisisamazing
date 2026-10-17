# Selective classification for deep neural networks

| | |
|---|---|
| **Set** | Highly cited · AI |
| **Citations** | 543 (Liner, undated snapshot; lower bound) |
| **Original** | [https://arxiv.org/abs/1705.08500](https://arxiv.org/abs/1705.08500) · local stub: [`raw/geifman-2017-selective-classification.md`](../raw/geifman-2017-selective-classification.md) |

**APA:** Geifman, Y., & El-Yaniv, R. (2017). Selective classification for deep neural networks. In *Advances in Neural Information Processing Systems 30*.

## 1. Research question
How can a trained deep network abstain so that error on the inputs it accepts stays below a user-chosen level?

## 2. Limitation of existing methods
Reject-option theory existed (Chow, 1970), but there was no practical method with a guarantee for modern deep networks.

## 3. Contributions
A selection-with-guaranteed-risk algorithm for any trained network, using softmax response or MC-dropout as confidence.

## 4. Proposed methods
Pick a confidence threshold on held-out data by binary search with a high-probability bound on selective risk.

## 5. Key findings
Achieves guaranteed risk at the obtained coverage on CIFAR and ImageNet, e.g. low top-5 error with high coverage.

## 6. Limitations
Guarantees error, not whether a prediction is supported by evidence; relies on confidence that may be high for the wrong reasons.

## 7. Author names
Yonatan Geifman, Ran El-Yaniv

## 8. Publish year
2017

## 9. Proceedings or journal name
Advances in Neural Information Processing Systems 30 (NeurIPS 2017)

---

**Relevance to the thesis:** Canonical abstention baseline. Paper A's Separation result shows a calibrated, error-controlled policy can still have URR near 1.

*Extracted 2026-10-17 from the abstract and main results; not a full-text reading. Check numbers against the original before quoting.*
