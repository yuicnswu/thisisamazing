# Sephora: evaluation without new human annotation

Question: Does customer context improve prediction of an existing reviewer recommendation beyond popularity, history and non-LLM text baselines?

1. Use only observed binary `is_recommended` labels; never impute missing labels from ratings. Report selection and class balance.
2. Freeze a chronological development/test cutoff after inspecting coverage, with all same-day reviews on the same side. For history, use strictly earlier dates and exclude target-product histories in the stricter condition. Temporal eligibility counts are not final test sizes.
3. Hide the target review text, title, rating, recommendation and feedback fields. Inputs may include product descriptions and earlier review evidence. Audit prior text duplicates across splits. Current customer profiles may not have been recorded before the target: disclose that limitation or omit them from prospective claims.
4. Exclude listing aggregate rating/review/loves counts from historical prediction. Price, ingredients and product highlights are undated snapshot attributes: test their removal and avoid asserting fully time-valid evaluation.
5. Compare training-period majority/popularity, structured customer/product and text-embedding baselines against the same LLM with no profile, observed profile and shuffled profile. Keep labels and target reviews out of prompts.
6. Report AUROC, PR-AUC with positive-class convention, balanced accuracy, macro-F1, log loss/calibration, customer-cluster bootstrap intervals, cost and latency. Lock thresholds/prompts on development data. Test held-out products separately from chronological known-product evaluation.
7. Claim prediction of reported recommendations only. Missing exposure sets mean unreviewed products are not negatives. No causal customer-fit, safety, revenue or conversion claim follows from this audit.

No model experiment has been run. Existing reviews and labels supply evaluation outcomes; no human annotation is requested.
