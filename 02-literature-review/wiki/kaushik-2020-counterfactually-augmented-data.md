# Learning the difference that makes a difference with counterfactually-augmented data

| | |
|---|---|
| **Set** | Highly cited · AI |
| **Citations** | 581 (Liner, read 2026-10-17; lower bound) |
| **Original** | [https://arxiv.org/abs/1909.12434](https://arxiv.org/abs/1909.12434) · local stub: [`raw/kaushik-2020-counterfactually-augmented-data.md`](../raw/kaushik-2020-counterfactually-augmented-data.md) |

**APA:** Kaushik, D., Hovy, E., & Lipton, Z. C. (2020). Learning the difference that makes a difference with counterfactually-augmented data. In *International Conference on Learning Representations*.

## 1. Research question
Can minimally edited counterfactual examples teach models to rely on features that actually determine the label?

## 2. Limitation of existing methods
Models trained on observational data pick up spurious correlations that break under distribution shift.

## 3. Contributions
A human-in-the-loop protocol for counterfactually revising documents so the label flips; counterfactually augmented datasets for sentiment and NLI.

## 4. Proposed methods
Annotators make minimal edits that change the label; models are trained on original plus revised data and tested on both.

## 5. Key findings
Models trained on combined data rely less on spurious features and generalize better across domains.

## 6. Limitations
Needs human editing; small datasets.

## 7. Author names
Divyansh Kaushik, Eduard Hovy, Zachary C. Lipton

## 8. Publish year
2020

## 9. Proceedings or journal name
International Conference on Learning Representations (ICLR 2020)

---

**Relevance to the thesis:** Basis for Paper A's evidence-sensitivity loss. Paper A generates counterfactual listing variants automatically from specs, with no human annotators.

*Extracted 2026-10-17 from the abstract and main results; not a full-text reading. Check numbers against the original before quoting.*
