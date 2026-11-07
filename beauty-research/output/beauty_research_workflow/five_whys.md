# Evidence-backed 5 Whys

Chains stop when evidence runs out; the number of links is not a quality target.

## W1: A complete-listing filter excludes most products from a shopping study.

Evidence: E1, E2.

- **Why are products excluded?** The rule requires observed price, description and features simultaneously. [verified rule consequence]

- **Why are these fields absent?** The local snapshot contains missing fields; source omission, extraction, and availability timing are competing explanations. [unknown; stop]

**Root Cause:** Verified exclusion mechanism: conjunction of three availability requirements. Origin of missingness is unresolved.

**Countermeasure:** Report all-product and eligible-product results separately; audit missing fields against independently obtained source records.

**Reverse Check:** Removing the filter restores eligibility by construction; improved fit or revenue must be tested separately.

**Confidence:** High for exclusion mechanism; unknown for upstream origin.

## W2: Most observed reviewers cannot support a multi-product history experiment.

Evidence: E5, E6.

- **Why is multi-product history scarce?** Most user IDs have only one distinct reviewed product in this category snapshot. [observed constraint]

- **Why do they have only one?** Sparse reviewing, category restrictions and collection scope are possible explanations. Purchases outside the snapshot are unobserved. [unknown; stop]

**Root Cause:** The snapshot lacks enough observed within-user history for most users; its behavioral origin is unresolved.

**Countermeasure:** Begin with explicit context annotation; report the size and selection of any eligible history subset after temporal splitting.

**Reverse Check:** More earlier reviews could enlarge eligibility; they would not establish that personalization improves customer fit.

**Confidence:** High for data limitation; low for behavioral explanations.

## W3: Opposing ratings cannot by themselves identify customer-specific product fit.

Evidence: E7, E8, E9.

- **Why are opposing ratings insufficient?** A single score does not identify the aspect, user need, product variant or reason for dissatisfaction. [measurement limitation]

- **What could explain disagreement?** Preferences, performance differences, variant mismatch, defects, shipping or authenticity concerns are rival hypotheses. [untested hypotheses]

- **Which explanation is supported?** No adjudicated aspect/context labels or prospective shopper outcomes are available in this workflow. [unresolved; stop]

**Root Cause:** The desired construct (customer fit) has not been independently measured; there is no established cause of rating disagreement.

**Countermeasure:** Annotate context, aspect, preference, defect, logistics and uncertainty with quoted spans; collect real shopper judgments before fit claims.

**Reverse Check:** Better annotations may distinguish explanations; only held-out validation can show the distinction is reliable.

**Confidence:** High for measurement gap; causal explanation unresolved.
