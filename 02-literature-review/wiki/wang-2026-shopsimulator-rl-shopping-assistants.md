# ShopSimulator: Evaluating and exploring RL-driven LLM agent for shopping assistants

| | |
|---|---|
| **Set** | 2025–2026 field check |
| **Citations** | not required |
| **Original** | [https://arxiv.org/abs/2601.18225](https://arxiv.org/abs/2601.18225) · local stub: [`raw/wang-2026-shopsimulator-rl-shopping-assistants.md`](../raw/wang-2026-shopsimulator-rl-shopping-assistants.md) |

**APA:** Wang, P., Wu, Y., Song, X., Wang, W., Chen, G., Li, Z., Yan, K., Deng, K., Liu, Q., Zhao, S., Xiong, S., Liu, X., Chen, X., Deng, W., Su, W., & Zheng, B. (2026). *ShopSimulator: Evaluating and exploring RL-driven LLM agent for shopping assistants* (arXiv:2601.18225). arXiv.

## 1. Research question
How well do LLM shopping assistants do in a realistic, multi-turn, personalised simulator, and can RL improve them?

## 2. Limitation of existing methods
Prior environments are small or single-turn.

## 3. Contributions
A Chinese shopping environment from about 1.3M Taobao products in 12 domains, four scenarios, and loose / strict / success rewards; RL exploration.

## 4. Proposed methods
LLM-simulated shoppers; reward by match of the purchased item to one gold target on category, attributes, options and price.

## 5. Key findings
GPT-5 reaches 32.65% full success; SFT + RL lifts Qwen3-8B single-turn success from 14.1% to 38.9%. Failing to ask for missing information is 9.4% of AskShopper errors.

## 6. Limitations
One gold item per instruction; no task where no listing matches; abstention not scored.

## 7. Author names
Pei Wang, Yanan Wu, Xiaoshuai Song, Weixun Wang, Gengru Chen, Zhongwen Li, Kezhong Yan, Ken Deng, Qi Liu, Shuaibing Zhao, Shaopan Xiong, Xuepeng Liu, Xuefeng Chen, Wanxi Deng, Wenbo Su, Bo Zheng

## 8. Publish year
2026

## 9. Proceedings or journal name
arXiv preprint arXiv:2601.18225

---

**Relevance to the thesis:** Even the environment that penalises acting without confirming details has **no "listing is silent" outcome**. Supports the benchmark gap.

*Extracted 2026-10-21 from the arXiv abstract page or HTML (fetched that day), for the repositioning after the 2026 field check (`team-opinion/field-check-2026.md` in the project files); not a full-text reading. Check numbers against the original before quoting.*
