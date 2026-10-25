# Preference discerning with LLM-enhanced generative retrieval

| | |
|---|---|
| **Set** | 2025–2026 field check |
| **Citations** | not required |
| **Original** | [https://arxiv.org/abs/2412.08604](https://arxiv.org/abs/2412.08604) · local stub: [`raw/paischer-2024-mender-preference-discerning-generative-retrieval.md`](../raw/paischer-2024-mender-preference-discerning-generative-retrieval.md) |

**APA:** Paischer, F., Yang, L., Liu, L., Shao, S., Hassani, K., Li, J., Chen, R., Li, Z. G., Gao, X., Shao, W., Feng, X., Noorshams, N., Park, S., Long, B., & Eghbalzadeh, H. (2024). *Preference discerning with LLM-enhanced generative retrieval* (arXiv:2412.08604). arXiv.

## 1. Research question
Can a sequential recommender be conditioned on user preferences written in natural language, so it follows changing preferences rather than only interaction history?

## 2. Limitation of existing methods
Existing methods use approximated preferences only in training and rely on interaction history.

## 3. Contributions
The "preference discerning" task and benchmark (including preference steering and sentiment following), and Mender, a generative recommender that takes preferences in context; preferences are mined from users' past reviews (Amazon Beauty among the datasets).

## 4. Proposed methods
LLM-generated preference statements from review history, fed in context to a generative-retrieval recommender.

## 5. Key findings
Current state of the art adapts poorly to evolving preferences; Mender reaches state of the art and follows preferences unseen in training.

## 6. Limitations
No limitations section on the page; preferences are LLM-mined and not checked against item evidence.

## 7. Author names
Fabian Paischer, Liu Yang, Linfeng Liu, Shuai Shao, Kaveh Hassani, Jiacheng Li, Ricky Chen, Zhang Gabriel Li, Xiaoli Gao, Wei Shao, Xue Feng, Nima Noorshams, Sem Park, Bo Long, Hamid Eghbalzadeh

## 8. Publish year
2024

## 9. Proceedings or journal name
arXiv preprint arXiv:2412.08604 (the field check lists TMLR 2025; venue not confirmed on the arXiv page)

---

**Relevance to the thesis:** Makes "needs mined from review history" **not new**. The thesis's difference is what happens next: each mined need is checked against the listing and can be unresolved. Mender is a required preference-conditioned baseline.

*Extracted 2026-10-21 from the arXiv abstract page or HTML (fetched that day), for the repositioning after the 2026 field check (`team-opinion/field-check-2026.md` in the project files); not a full-text reading. Check numbers against the original before quoting.*
