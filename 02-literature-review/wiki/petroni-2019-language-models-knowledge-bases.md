# Language models as knowledge bases?

| | |
|---|---|
| **Set** | Highly cited · AI |
| **Citations** | 2,753 (Liner, read 2026-10-17; lower bound) |
| **Original** | [https://arxiv.org/abs/1909.01066](https://arxiv.org/abs/1909.01066) · local stub: [`raw/petroni-2019-language-models-knowledge-bases.md`](../raw/petroni-2019-language-models-knowledge-bases.md) |

**APA:** Petroni, F., Rocktäschel, T., Lewis, P., Bakhtin, A., Wu, Y., Miller, A. H., & Riedel, S. (2019). Language models as knowledge bases? In *Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing*.

## 1. Research question
How much relational and factual knowledge do pretrained language models store, without fine-tuning?

## 2. Limitation of existing methods
Knowledge bases need schema engineering and supervision; it was unknown how much knowledge LMs absorb from raw text.

## 3. Contributions
The LAMA probe: cloze-style queries for facts from several knowledge sources.

## 4. Proposed methods
Convert knowledge-base triples into fill-in-the-blank statements and test whether pretrained LMs rank the correct object first.

## 5. Key findings
BERT recalls relational knowledge competitively with knowledge bases built by traditional methods, without supervision.

## 6. Limitations
Cloze probes are sensitive to wording; recall is not reliability.

## 7. Author names
Fabio Petroni, Tim Rocktäschel, Patrick Lewis, Anton Bakhtin, Yuxiang Wu, Alexander H. Miller, Sebastian Riedel

## 8. Publish year
2019

## 9. Proceedings or journal name
Proceedings of EMNLP-IJCNLP 2019

---

**Relevance to the thesis:** Shows that models carry strong priors about entities and products; Paper A tests when those priors license recommendations without listing evidence.

*Extracted 2026-10-17 from the abstract and main results; not a full-text reading. Check numbers against the original before quoting.*
