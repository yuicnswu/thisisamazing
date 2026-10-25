# ShoppingBench: A real-world intent-grounded shopping benchmark for LLM-based agents

| | |
|---|---|
| **Set** | 2025–2026 field check |
| **Citations** | not required |
| **Original** | [https://arxiv.org/abs/2508.04266](https://arxiv.org/abs/2508.04266) · local stub: [`raw/wang-2025-shoppingbench-intent-grounded-shopping-agents.md`](../raw/wang-2025-shoppingbench-intent-grounded-shopping-agents.md) |

**APA:** Wang, J., Xiao, K., Sun, Q., Zhao, H., Luo, T., Zhang, J. D., & Zeng, X. (2025). *ShoppingBench: A real-world intent-grounded shopping benchmark for LLM-based agents* (arXiv:2508.04266). arXiv.

## 1. Research question
Can LLM agents handle realistic shopping goals beyond finding one product (coupons, budgets, one seller for several items)?

## 2. Limitation of existing methods
Earlier shopping benchmarks test simple search-and-buy.

## 3. Contributions
3,310 intent-grounded instructions over four intents in a 2.5M-product sandbox with six tools; absolute success and relevance metrics.

## 4. Proposed methods
Agent trajectories scored against gold products and constraints; SFT + RL training of a small model.

## 5. Key findings
GPT-4.1 reaches 48.2% average success (30.4% on Coupon & Budget); a trained Qwen3-4B reaches 48.7%.

## 6. Limitations
No abstention metric; failure analysis covers 60 trajectories.

## 7. Author names
Jiangyuan Wang, Kejun Xiao, Qi Sun, Huaipeng Zhao, Tao Luo, Jian Dong Zhang, Xiaoyi Zeng

## 8. Publish year
2025

## 9. Proceedings or journal name
arXiv preprint arXiv:2508.04266

---

**Relevance to the thesis:** Representative of 2025–2026 shopping benchmarks: they assume the needed information exists. **None scores abstaining when the listing is silent**, which is the benchmark gap the thesis fills.

*Extracted 2026-10-21 from the arXiv abstract page or HTML (fetched that day), for the repositioning after the 2026 field check (`team-opinion/field-check-2026.md` in the project files); not a full-text reading. Check numbers against the original before quoting.*
