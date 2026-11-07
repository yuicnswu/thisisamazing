# Know what you don't know: Unanswerable questions for SQuAD

| | |
|---|---|
| **Set** | Highly cited · AI |
| **Citations** | 2,913 (Liner, read 2026-10-17; lower bound) |
| **Original** | [https://arxiv.org/abs/1806.03822](https://arxiv.org/abs/1806.03822) · local stub: [`raw/rajpurkar-2018-unanswerable-questions-squad.md`](../raw/rajpurkar-2018-unanswerable-questions-squad.md) |

**APA:** Rajpurkar, P., Jia, R., & Liang, P. (2018). Know what you don't know: Unanswerable questions for SQuAD. In *Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers)*.

## 1. Research question
Can reading-comprehension systems tell when a passage does not contain the answer?

## 2. Limitation of existing methods
QA datasets guaranteed an answer in the passage, so models learned to always guess a plausible span.

## 3. Contributions
SQuAD 2.0, adding over 50,000 adversarial unanswerable questions written to look answerable.

## 4. Proposed methods
Crowdworkers write questions relevant to a passage but unanswerable from it; models must answer or abstain.

## 5. Key findings
Strong models lost much of their accuracy, showing they could not reliably detect missing answers.

## 6. Limitations
Extractive QA; abstention evaluated without any guarantee.

## 7. Author names
Pranav Rajpurkar, Robin Jia, Percy Liang

## 8. Publish year
2018

## 9. Proceedings or journal name
Proceedings of ACL 2018 (Volume 2: Short Papers)

---

**Relevance to the thesis:** Closest classic analogue to Paper A's 'unresolved' status: the evidence does not contain what is needed, so the right output is to abstain.

*Extracted 2026-10-17 from the abstract and main results; not a full-text reading. Check numbers against the original before quoting.*
