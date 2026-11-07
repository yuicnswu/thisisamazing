# Teaching large language models to maintain contextual faithfulness via synthetic tasks and reinforcement learning

| | |
|---|---|
| **Set** | Conference · AI |
| **Citations** | not required (conference set) |
| **Original** | [https://scholar.google.com/scholar?q=%22Teaching+large+language+models+to+maintain+contextual+faithfulness%22](https://scholar.google.com/scholar?q=%22Teaching+large+language+models+to+maintain+contextual+faithfulness%22) · local stub: [`raw/si-2026-canoe-contextual-faithfulness-rl.md`](../raw/si-2026-canoe-contextual-faithfulness-rl.md) |

**APA:** Si, S., Zhao, H., Gao, C., Bai, Y., Wang, Z., Gao, B., Luo, K., Li, W., Huang, Y., Chen, G., Qi, F., Zhang, M., Chang, B., & Sun, M. (2026). Teaching large language models to maintain contextual faithfulness via synthetic tasks and reinforcement learning. *Proceedings of the AAAI Conference on Artificial Intelligence, 40*(39), 33001–33009.

## 1. Research question
Can contextual faithfulness be trained without human-annotated data, in both short- and long-form generation?

## 2. Limitation of existing methods
Faithfulness training needs costly annotation, and methods tuned for short answers do not transfer to long-form generation.

## 3. Contributions
CANOE: synthetic short-form QA with verifiable answers plus rule-based RL rewards (Dual-GRPO) that transfer to long-form tasks.

## 4. Proposed methods
Synthesize QA from knowledge triples, then train with rewards for answer accuracy and for long-form proxies, without human labels.

## 5. Key findings
Improves faithfulness across many downstream tasks; the paper reports results above strong proprietary models.

## 6. Limitations
Optimizes following the context, not recognizing when the context is insufficient.

## 7. Author names
Shuzheng Si, Haozhe Zhao, Cheng Gao, Yuzhuo Bai, Zhitong Wang, Bofei Gao, Kangyang Luo, Wenhao Li, Yufei Huang, Gang Chen, Fanchao Qi, Minjia Zhang, Baobao Chang, Maosong Sun

## 8. Publish year
2026

## 9. Proceedings or journal name
Proceedings of the AAAI Conference on Artificial Intelligence, 40(39), 33001–33009

---

**Relevance to the thesis:** Training baseline for Paper A's verifier. Paper A's counterfactual evidence-sensitivity loss targets the absence of evidence and an abstain action.

*Extracted 2026-10-17 from the abstract and main results; not a full-text reading. Check numbers against the original before quoting.*
