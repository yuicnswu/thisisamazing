# Semi-supervised risk control via prediction-powered inference

| | |
|---|---|
| **Set** | 2025–2026 field check |
| **Citations** | not required |
| **Original** | [https://arxiv.org/abs/2412.11174](https://arxiv.org/abs/2412.11174) · local stub: [`raw/einbinder-2024-semi-supervised-risk-control-ppi.md`](../raw/einbinder-2024-semi-supervised-risk-control-ppi.md) |

**APA:** Einbinder, B.-S., Ringel, L., & Romano, Y. (2024). *Semi-supervised risk control via prediction-powered inference* (arXiv:2412.11174). arXiv.

## 1. Research question
Can unlabelled data with model-imputed labels tighten risk-controlling calibration without losing finite-sample validity?

## 2. Limitation of existing methods
Risk-controlling prediction sets (RCPS, Learn-then-Test) need many labelled calibration points; small labelled sets give conservative thresholds.

## 3. Contributions
Combines prediction-powered inference with RCPS: a small labelled set plus a large imputed set give finite-sample (α, δ) risk control whatever the imputation quality.

## 4. Proposed methods
Decompose the PPI risk estimate into i.i.d. terms with a Waudby-Smith–Ramdas bound; for binary losses, Clopper–Pearson bounds with the error budget split between labelled and unlabelled data. Covers non-monotone risks and one conditional-risk case.

## 5. Key findings
Valid risk control with lower conservatism when imputations are accurate; ImageNet and early time-series classification with an LLM.

## 6. Limitations
i.i.d. only (shift left to future work); no general theory for ratio-type selective risks; can be conservative with small labelled sets.

## 7. Author names
Bat-Sheva Einbinder, Liran Ringel, Yaniv Romano

## 8. Publish year
2024

## 9. Proceedings or journal name
arXiv preprint arXiv:2412.11174 (venue not stated on the page; check before citing)

---

**Relevance to the thesis:** **Changes the main-track plan.** The team opinion's proposed "true-risk bound from a small gold set plus many proxy labels" is this method in general form. What stays open is the extension to the thesis's *selective, conjunctive ratio risk* (URR = P(unsupported | recommend)) with one-sided proxy errors and launch-time shift. Cite it as the base and claim only that extension.

*Extracted 2026-10-21 from the arXiv abstract page or HTML (fetched that day), for the repositioning after the 2026 field check (`team-opinion/field-check-2026.md` in the project files); not a full-text reading. Check numbers against the original before quoting.*
