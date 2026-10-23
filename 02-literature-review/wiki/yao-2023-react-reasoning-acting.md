# ReAct: Synergizing reasoning and acting in language models

| | |
|---|---|
| **Set** | Highly cited · AI |
| **Citations** | 3,479 (Liner, read 2026-10-17; lower bound) |
| **Original** | [https://arxiv.org/abs/2210.03629](https://arxiv.org/abs/2210.03629) · local stub: [`raw/yao-2023-react-reasoning-acting.md`](../raw/yao-2023-react-reasoning-acting.md) |

**APA:** Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2023). ReAct: Synergizing reasoning and acting in language models. In *International Conference on Learning Representations*.

## 1. Research question
Can LLMs interleave reasoning traces with actions such as lookups to solve tasks more reliably?

## 2. Limitation of existing methods
Chain-of-thought reasons without grounding and hallucinates; action-only agents act without planning.

## 3. Contributions
ReAct prompting that alternates thoughts and actions, including on a web-shopping environment.

## 4. Proposed methods
Few-shot prompts with interleaved Thought/Action/Observation steps, evaluated on HotpotQA, FEVER, ALFWorld and WebShop.

## 5. Key findings
Reduces hallucination in QA and fact checking and improves success on interactive tasks, including WebShop.

## 6. Limitations
No principled stopping rule or guarantee; performance depends on prompts.

## 7. Author names
Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao

## 8. Publish year
2023

## 9. Proceedings or journal name
International Conference on Learning Representations (ICLR 2023)

---

**Relevance to the thesis:** Baseline agent pattern for Paper A's acquisition policy (read a listing field, reason, decide). Paper A adds support-based stopping and a URR guarantee.

*Extracted 2026-10-17 from the abstract and main results; not a full-text reading. Check numbers against the original before quoting.*
