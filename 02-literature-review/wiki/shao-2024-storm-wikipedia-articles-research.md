# Assisting in writing Wikipedia-like articles from scratch with large language models

| | |
|---|---|
| **Set** | Market research agent · AI |
| **Citations** | not checked |
| **Original** | [https://aclanthology.org/2024.naacl-long.347](https://aclanthology.org/2024.naacl-long.347) · local stub: [`raw/shao-2024-storm-wikipedia-articles-research.md`](../raw/shao-2024-storm-wikipedia-articles-research.md) |

**APA:** Shao, Y., Jiang, Y., Kanell, T. A., Xu, P., Khattab, O., & Lam, M. S. (2024). Assisting in writing Wikipedia-like articles from scratch with large language models. In *Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics (Volume 1: Long Papers)* (pp. 6252–6278).

## 1. Research question
How can an LLM research a topic and write a grounded, well-organised long-form article?

## 2. Limitation of existing methods
Generation work assumed outlines or sources were given; pre-writing research was not modelled.

## 3. Contributions
STORM, which discovers perspectives, simulates multi-perspective question asking against sources, and builds an outline before writing; plus the FreshWiki dataset.

## 4. Proposed methods
Perspective-guided conversations retrieve and synthesise sources; outline then article with citations; evaluated automatically and by Wikipedia editors.

## 5. Key findings
Articles were judged more organised and broader than a retrieval-augmented baseline; editors flagged source bias transfer and over-association of unrelated facts.

## 6. Limitations
Wikipedia-style topics; citation quality still imperfect.

## 7. Author names
Yijia Shao, Yucheng Jiang, Theodore A. Kanell, Peter Xu, Omar Khattab, Monica S. Lam

## 8. Publish year
2024

## 9. Proceedings or journal name
Proceedings of NAACL 2024

---

**Relevance to the Beauty Market Research Agent:** The closest design to 'investigate, then write a brief'. Its perspective step maps to investigating counterexamples, and its failure modes (over-association, source bias) belong in the unsupported-claims audit.

*Extracted 2026-10-25 from the abstract, venue page and main results; not a full-text reading. Check numbers against the original before quoting.*
