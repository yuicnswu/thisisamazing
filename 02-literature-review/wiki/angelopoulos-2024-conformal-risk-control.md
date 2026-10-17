# Conformal risk control

| | |
|---|---|
| **Set** | Highly cited · AI |
| **Citations** | 151 (Liner, undated snapshot; lower bound) |
| **Original** | [https://arxiv.org/abs/2208.02814](https://arxiv.org/abs/2208.02814) · local stub: [`raw/angelopoulos-2024-conformal-risk-control.md`](../raw/angelopoulos-2024-conformal-risk-control.md) |

**APA:** Angelopoulos, A. N., Bates, S., Fisch, A., Lei, L., & Schuster, T. (2024). Conformal risk control. In *International Conference on Learning Representations*.

## 1. Research question
Can conformal prediction control the expected value of losses other than miscoverage?

## 2. Limitation of existing methods
Split conformal prediction controls coverage only; earlier risk-control methods gave high-probability bounds that are more conservative.

## 3. Contributions
Conformal risk control: a finite-sample bound on the expected value of any bounded monotone loss, with tightness results.

## 4. Proposed methods
Choose the smallest threshold whose adjusted empirical risk on calibration data is below α.

## 5. Key findings
Controls losses such as false negative rate in segmentation, tumour detection and multilabel classification, with near-exact control.

## 6. Limitations
Needs a loss that is monotone in the threshold and exchangeable data; the guarantee is in expectation.

## 7. Author names
Anastasios N. Angelopoulos, Stephen Bates, Adam Fisch, Lihua Lei, Tal Schuster

## 8. Publish year
2024

## 9. Proceedings or journal name
International Conference on Learning Representations (ICLR 2024)

---

**Relevance to the thesis:** Calibration machinery for Paper A's URR bound (Theory result 4). Learn-then-Test covers the case where acquisition makes URR non-monotone.

*Extracted 2026-10-17 from the abstract and main results; not a full-text reading. Check numbers against the original before quoting.*
