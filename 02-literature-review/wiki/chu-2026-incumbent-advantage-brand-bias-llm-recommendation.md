# Incumbent advantage: Brand bias and cognitive manipulation dynamics in LLM recommendation systems

| | |
|---|---|
| **Set** | 2025–2026 field check |
| **Citations** | not required |
| **Original** | [https://arxiv.org/abs/2606.17443](https://arxiv.org/abs/2606.17443) · local stub: [`raw/chu-2026-incumbent-advantage-brand-bias-llm-recommendation.md`](../raw/chu-2026-incumbent-advantage-brand-bias-llm-recommendation.md) |

**APA:** Chu, X., & Hou, Y. (2026). *Incumbent advantage: Brand bias and cognitive manipulation dynamics in LLM recommendation systems* (arXiv:2606.17443). arXiv.

## 1. Research question
How do brands compete when shoppers ask an LLM to choose a product, in skincare, where quality is hard to judge before buying?

## 2. Limitation of existing methods
Brand-bias work on LLM recommenders had shown that injected cues move rankings, but not how known brands, ratings and authority-style copy trade off in a credence-good category, or what happens when every brand optimises.

## 3. Contributions
Three experiments on GPT-4o-mini, Claude Sonnet and Gemini 3 Flash: brand recognition with identical specifications, rating gaps, authority claims (including fabricated clinical evidence), and multi-brand optimisation, with a search-good robustness check.

## 4. Proposed methods
Controlled choice sets of products with identical specifications; vary brand familiarity, rating, and marketing language; measure which product each model recommends.

## 5. Key findings
With identical specifications the known brand is recommended every time. A rival rating edge under 0.1 stars ends that dominance, and authority-style language (fabricated clinical claims included) can too, with models responding differently. When every brand adopts the same optimisation, the individual gain disappears and non-participants get no recommendations.

## 6. Limitations
Skincare and three commercial models only; payoff is a recommendation-share proxy, not sales; no explicit limitations section.

## 7. Author names
Xi Chu, Yupeng Hou

## 8. Publish year
2026

## 9. Proceedings or journal name
arXiv preprint arXiv:2606.17443 (cs.AI)

---

**Relevance to the thesis:** **Scoops the brand-bias headline** (C1 in the plan), on our category, by BLaIR's first author. The thesis must cite it and position RQ1 as a reconciliation: in single-listing need-checking our pilot found the operative prior is product type, not brand (brand + hype swaps moved Claude both ways equally). Its finding that fabricated clinical claims persuade models is also the strongest argument that a verifier must check *stated* evidence and that merchant fixes must be requests to verify, not text to paste.

*Extracted 2026-10-21 from the arXiv abstract page or HTML (fetched that day), for the repositioning after the 2026 field check (`team-opinion/field-check-2026.md` in the project files); not a full-text reading. Check numbers against the original before quoting.*
