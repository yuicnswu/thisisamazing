# Large language models are competitive near cold-start recommenders for language- and item-based preferences

| | |
|---|---|
| **Set** | Conference · AI |
| **Citations** | not required (conference set) |
| **Original** | [https://doi.org/10.1145/3604915.3608845](https://doi.org/10.1145/3604915.3608845) · local stub: [`raw/sanner-2023-llm-near-cold-start-recommenders.md`](../raw/sanner-2023-llm-near-cold-start-recommenders.md) |

**APA:** Sanner, S., Balog, K., Radlinski, F., Wedin, B., & Dixon, L. (2023). Large language models are competitive near cold-start recommenders for language- and item-based preferences. In *Proceedings of the 17th ACM Conference on Recommender Systems*. https://doi.org/10.1145/3604915.3608845

## 1. Research question
Can LLMs recommend well from natural-language preferences when interaction data is scarce?

## 2. Limitation of existing methods
Collaborative filtering needs interaction history; item-based preferences are hard for users to express and do not explain why.

## 3. Contributions
A new dataset of item-based and language-based preferences; a comparison of LLM prompting with collaborative-filtering baselines.

## 4. Proposed methods
Zero- and few-shot prompting of LLMs with language or item preferences, compared with item-based CF.

## 5. Key findings
LLMs are competitive with item-based CF in the near cold-start setting, especially from language-based preferences.

## 6. Limitations
Movie domain, where items are likely memorized by the LLM; accuracy measured, not whether recommendations are supported.

## 7. Author names
Scott Sanner, Krisztian Balog, Filip Radlinski, Ben Wedin, Lucas Dixon

## 8. Publish year
2023

## 9. Proceedings or journal name
Proceedings of the 17th ACM Conference on Recommender Systems (RecSys 2023)

---

**Relevance to the thesis:** Motivates using LLMs for new products. Paper A asks whether such competence comes from item evidence or from memorized priors.

*Extracted 2026-10-17 from the abstract and main results; not a full-text reading. Check numbers against the original before quoting.*
