# Recommender systems with generative retrieval

| | |
|---|---|
| **Set** | Highly cited · AI |
| **Citations** | 107 (Liner, undated snapshot; lower bound) |
| **Original** | [https://arxiv.org/abs/2305.05065](https://arxiv.org/abs/2305.05065) · local stub: [`raw/rajput-2023-generative-retrieval-tiger.md`](../raw/rajput-2023-generative-retrieval-tiger.md) |

**APA:** Rajput, S., Mehta, N., Singh, A., Keshavan, R. H., Vu, T., Heldt, L., Hong, L., Tay, Y., Tran, V. Q., Samost, J., Kula, M., Chi, E. H., & Sathiamoorthy, M. (2023). Recommender systems with generative retrieval. In *Advances in Neural Information Processing Systems 36*. **[check details: author list]**

## 1. Research question
Can a recommender generate the identifier of the next item directly, instead of retrieving by embedding similarity?

## 2. Limitation of existing methods
Dual-encoder retrieval with random item IDs cannot generalize to new items and needs large embedding tables.

## 3. Contributions
TIGER: semantic IDs from quantized content embeddings and a sequence-to-sequence model that generates them.

## 4. Proposed methods
Quantize item content embeddings with an RQ-VAE into tuples of codewords, then train a Transformer to generate the next item's semantic ID.

## 5. Key findings
Beats sequential baselines on Amazon datasets and shows some ability to retrieve cold-start items.

## 6. Limitations
New items are placed by content similarity to known items; no check of whether the listing supports the need.

## 7. Author names
Shashank Rajput, Nikhil Mehta, Anima Singh, Raghunandan H. Keshavan, Trung Vu, Lukasz Heldt, Lichan Hong, Yi Tay, Vinh Q. Tran, Jonah Samost, Maciej Kula, Ed H. Chi, Maheswaran Sathiamoorthy

## 8. Publish year
2023

## 9. Proceedings or journal name
Advances in Neural Information Processing Systems 36 (NeurIPS 2023)

---

**Relevance to the thesis:** Representative similarity-based new-item method for Paper A; a semantic ID is a learned prior.

*Extracted 2026-10-17 from the abstract and main results; not a full-text reading. Check numbers against the original before quoting.*
