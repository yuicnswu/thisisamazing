# Mock NeurIPS review: "Before the First Review"

*Mock review of the planned NeurIPS 2027 main-track paper, 17 Oct 2026. Reviewed material: yui's proposal (uploaded 17 Oct), `refined-thesis-plan.md` (incl. §9 strategic sellers / two-sided guarantee, §10 NeurIPS plan, §11 no-annotator labels) and `literature-review.md`. Neither source file was changed.*

## How to read this

- **What is scored.** There is no paper yet, so each reviewer scores *the paper this plan would produce if every step works as described*. Scores reflect the design, the claims and the positioning, not results.
- **What can't be scored yet.** The size of the prior-licensing gap (RQ1), whether URR ≤ α holds empirically, method vs. baselines, the proofs (only statements exist), feasibility counts (how many products have parseable specs), and the post-launch signal (RQ3). Any of these can move a score by one or two points either way.
- **Scales.** The 2026 Reviewer Guidelines page doesn't publish the scales, so these use the NeurIPS 2025 form: **Overall** 1–6 (6 strong accept, 5 accept, 4 borderline accept, 3 borderline reject, 2 reject, 1 strong reject); **Quality / Clarity / Significance / Originality** 1–4 (4 excellent, 3 good, 2 fair, 1 poor); **Confidence** 1–5. Check against the 2027 form when it's out.
- **Tone.** The reviewers were asked to be the critical reviewers the paper will actually meet, so read this as a stress test rather than a prediction.

## Score summary

| Reviewer | Expertise | Overall | Quality | Clarity | Significance | Originality | Confidence |
|---|---|---|---|---|---|---|---|
| R1 | Conformal prediction, learning theory | **3** | 2 | 3 | 2 | 2 | 4 |
| R2 | LLM recommenders, cold start | **3** | 2 | 3 | 3 | 3 | 4 |
| R3 | Evaluation and benchmarks | **4** | 3 | 3 | 3 | 3 | 3 |
| R4 | NLP faithfulness and grounding | **3** | 2 | 2 | 2 | 2 | 3 |
| **Mean** | | **3.25** | 2.25 | 2.75 | 2.5 | 2.5 | |

**Verdict as planned: borderline reject at the main track** (typical accepts average around 4.5 or higher). Realistic ceiling with the fixes in the meta-review: **4–5**. As an Evaluations & Datasets submission (diagnosis + benchmark), the same design would sit at about **4**.

---

## Reviewer 1: conformal prediction and learning theory

**Summary.** The paper defines the unsupported recommendation rate (URR), a recommend / reject / abstain rule over a conjunction of checkable constraints, and calibrates the verifier with conformal risk control or Learn-then-Test so that URR ≤ α. Supporting theory: calibration ≠ groundedness (Thm 1), myopic VOI stopping is blind under strong priors (Thm 2), outcome training learns priors (Thm 3), the finite-sample bound (Thm 4), plus a two-risk version with an exposure gap ≤ β and a disclosure result.

**Strengths.**
- The *support vs. accuracy* distinction is stated crisply, and "a correct but unsupported recommendation passes an error guarantee and fails ours" is a good line.
- The plan is honest that the guarantee is relative to labels (§11.2), which many papers aren't.
- The two-risk calibration (URR and exposure gap) is a sensible use of Learn-then-Test.

**Weaknesses.**
1. **The theorems look like observations.** Thm 1 (a calibrated confidence threshold can have URR → 1 when the prior is strong and evidence absent) follows almost from the definitions: calibration is about the label, support is about the evidence. Thm 2 is the definition of myopic stopping restated. Thm 4 is a direct application of LTT. Reviewers with my background will say "there is no technical theory contribution", and the plan currently makes the theory a main pillar of originality (§8 verdict).
2. **URR is a conditional ratio, and the plan doesn't say how it is controlled.** URR = P(unsupported | recommend). Conformal risk control bounds an expected loss, not a ratio conditioned on the selection the threshold itself makes. This is a selective-risk / FDR-type quantity: LTT can handle it, but the statement, the p-values and the validity argument need to be written out, and coverage can collapse at small α.
3. **The α + ε corollary is wrong as stated.** If the parser mislabels a fraction ε of *all* items, the errors can concentrate in the recommended set, so the true URR is bounded by roughly α + ε / P(recommend), not α + ε. At 30% coverage that is a 3× inflation. The estimate of ε also needs to be on the *recommended, labelled-entailed* items, which is where the errors that matter live.
4. **Exchangeability is assumed exactly where it breaks.** Calibration on constructed edits (L1) and testing on natural listings (L2) is a distribution shift. So is the strategic-seller setting in §9A, which is performative by definition, and CRC/LTT don't cover it without a shift model. The plan's claim that the rule is "robust by construction" to rewrites is true only for an oracle verifier: an actual LLM verifier can be fooled by "fits most under-60 cm spaces". The guarantee is on the verifier, and the verifier is what the attacker targets.
5. **The disclosure theorem is the classic unravelling result.** Applying Grossman/Milgrom to an AI matcher is a nice remark, but it isn't a new theorem unless it handles something the classic model doesn't (noisy verifier, costly disclosure, partial conjunctions).

**Questions.** What exactly is calibrated: one threshold on the verifier's entailment score, per-constraint thresholds, or a joint parameter? How is the conjunction's dependence between constraints handled in the bound? Is the exposure-gap constraint ever infeasible together with URR ≤ α, and what happens then?

**Scores.** Overall 3 · Quality 2 · Clarity 3 · Significance 2 · Originality 2 · Confidence 4.

---

## Reviewer 2: LLM recommenders and cold start

**Summary.** Diagnoses "prior licensing" (LLM recommenders recommend new products when the listing doesn't support the need), proposes an evidence-seeking verifier-plus-abstention matcher, and validates against post-launch reviews on Amazon Reviews 2023.

**Strengths.**
- The running example (no width listed → "cannot tell yet: add a width") is clear and memorable.
- Testing *missing* and *vague* evidence, not only injected bias, is a real gap next to BiasRecBench and Chu & Hou (2026).
- The plan already knows its closest neighbours (Mohri & Hashimoto, Wang et al. 2025, Shopping Companion, ShoppingComp).

**Weaknesses.**
1. **The deterministic label pipeline may be the solution.** L2 items are kept only when a rule-based parser finds the value in visible text and agrees with `details`; L1 edits (spec removed, replaced by "compact", value changed) are exactly the edits a parser detects. So on the evaluation set, *extract-then-compare with rules* is close to optimal by construction. The plan treats this as an empirical risk ("if the regex baseline already reaches low URR the story changes", §10.3); it's actually structural. Unless there is a subset where support is decidable but rules fail, the LLM matcher has no room to win.
2. **The obvious strong baseline is missing:** a frontier model with a carefully written "recommend only if every constraint is explicitly stated; otherwise say what's missing" prompt, and an LLM-extract-then-rule pipeline. I'd expect both to do well on checkable specs. The diagnosis must show frontier models fail *with* this prompt, not just with a generic recommendation prompt.
3. **Recformer and UniSRec aren't comparable baselines.** They score items for a user's interaction sequence, not for a stated need. Including them invites an apples-to-oranges objection; either define a fair adaptation or drop them.
4. **Contamination.** Products launched in 2022–2023 are likely in the pretraining data of every frontier model. The memorisation probe helps, but the post-cutoff listing set is "optional" in the plan. For a paper whose thesis is "models use memory, not evidence", it should be mandatory.
5. **Coverage and usefulness.** A support-only rule abstains whenever a spec is missing, and many real listings omit specs. If coverage on natural new listings is low, reviewers will ask whether this is a recommender or a spec checker. Seller feedback ("add a width") is claimed as the remedy but isn't evaluated beyond a simulation (H5).

**Questions.** What share of new Home & Kitchen listings state a width in visible text? What's the URR and coverage of the strong-prompt baseline in the pilot?

**Scores.** Overall 3 · Quality 2 · Clarity 3 · Significance 3 · Originality 3 · Confidence 4.

---

## Reviewer 3: evaluation and benchmarks

**Summary.** The most concrete contribution is a large benchmark of counterfactual evidence variants (missing / vague / edited / conflicting / brand swap / marketing rewrite) on real new-product listings, with exact labels by construction and validation against post-launch reviews.

**Strengths.**
- Labels by construction (L1) are a clean answer to "no human annotators", and the rule that the evaluated model never makes its own calibration labels is right.
- Minimal edits of real listings keep the variants realistic.
- Splits by launch date and unseen brands, plus a held-out category, are well chosen.
- The never-cut list and gates (G1–G4) show good research management.

**Weaknesses.**
1. **Construction artefacts.** Removing a spec or substituting "compact" leaves textual traces (odd phrasing, missing units). A fine-tuned verifier can learn the edit signature rather than support. Needs an artefact check (e.g. a classifier that tries to tell edited from natural listings) and results on natural L2 items reported as the headline, not the constructed ones.
2. **RQ3 is weaker than it looks.** The `details` metadata is a 2023 snapshot, so the *launch-time* listing isn't observed: sellers may have added the width after misfit reviews. Reviewers' needs are inferred from their own reviews, which are written *after* the fit outcome, so the validation is endogenous. Fit/misfit statements will be sparse. This can support "signal exists", not "launch-time decisions predict satisfaction".
3. **Narrow scope.** Dimensions, capacity, weight, material and colour from controlled vocabularies is a small slice of shopping needs. It's defensible (it's what makes support decidable), but significance for the broader NeurIPS audience needs an argument beyond shopping, e.g. "checkable-constraint grounding" as a general agent-safety problem.
4. **The benchmark sizes are targets, not counts.** 20–40K products and 300K pairs depend on the October feasibility count.

**Scores.** Overall 4 (conditional on a hard natural subset and the artefact check) · Quality 3 · Clarity 3 · Significance 3 · Originality 3 · Confidence 3.

---

## Reviewer 4: NLP faithfulness and grounding

**Summary.** Applies context-faithfulness and attribution ideas to recommendation decisions, with abstention.

**Strengths.**
- Correctly identifies that the failure here is *absent* evidence, which differs from knowledge-conflict work.
- The four support statuses (entailed / contradicted / unresolved / conflicting) are a useful refinement of binary AIS.

**Weaknesses.**
1. **"Prior licensing" on missing evidence is the unanswerable-question problem.** SQuAD 2.0, FaithEval's unanswerable contexts and conformal abstention all study models answering without support. The novelty is the domain plus conjunctions. The paper needs to show something that doesn't transfer from those results, e.g. that the *conjunction* structure makes it worse (models check one constraint and license the rest), or that popularity/brand predicts licensing.
2. **The motivation and the metric pull in different directions.** The intro argues that wrong matches create misfit returns and bad first reviews: that's an *accuracy* harm. The metric penalises *unsupported* matches, including correct ones. The paper needs to show why unsupported-but-correct recommendations are harmful (manipulability, accountability, unfair exposure), or reviewers will ask why not just bound error.
3. **Clarity across the documents is uneven.** The proposal lets the model see `details`; plan §11 hides it. The proposal has a human gold set; the plan drops it. The literature review §3.3 says calibration uses post-launch review labels; plan §11.1 says post-launch labels are never used for calibration. The headline also grew (§9: strategic robustness, disclosure, two-sided guarantee) to more than 9 pages can carry. A reader can't tell what the single main claim is.
4. **Verifier robustness isn't evaluated adversarially.** Marketing rewrites are "persuasive, unverifiable claims", but the threat that matters is *pseudo-evidence* ("fits standard 24-inch spaces", "slim 55-ish cm design"). That's where a support verifier fails.

**Scores.** Overall 3 · Quality 2 · Clarity 2 · Significance 2 · Originality 2 · Confidence 3.

---

## Meta-review

**Consensus.** The problem is well motivated, the running example is excellent, the evaluation design (constructed labels, temporal and brand splits, gates) is careful, and the positioning against the closest work is already better than most first submissions. All four reviewers converge on the same three doubts:

1. **Is there room for a learned method?** The scope that makes support decidable without humans also makes rules nearly sufficient, and the label pipeline is itself a rule-based matcher (R2, R3).
2. **Is the theory a contribution?** The headline theorems read as definitions or direct applications, and two details are currently wrong or missing: how a conditional ratio (URR) is calibrated, and the α + ε corollary (R1).
3. **Is support the right target?** The harm described is about accuracy, the metric is about support, and coverage on real listings may be low (R2, R4).

**Recommendation as planned:** borderline reject at the main track (mean 3.25). **The diagnosis + benchmark half is the strongest part**; the method and theory half is where the score is lost.

## The changes that would raise the score most (in order)

1. **Build a "hard but decidable" natural subset and make it the headline.** Support is still decidable from `details`, but rules fail: evidence in prose ("fits a standard 30-inch range opening"), unit conversion and composite specs ("18 x 24 in"), title/bullet conflicts, multi-field reasoning. Report the regex baseline, LLM-extract-then-rule, and a strong abstain-prompt frontier model on it **in the November pilot**. If rules win everywhere, reframe the paper around the diagnosis and the benchmark (E&D track) early rather than in March. *Fixes R2.1, R2.2, R3.1. Likely +1 overall.*
2. **Fix the guarantee and reposition the theory.** Write URR control as selective-risk control with LTT, with explicit p-values. Correct the corollary to α + ε / P(recommend) and estimate ε on the recommended set. State plainly that robustness to rewrites holds only up to the verifier's invariance, and test it with pseudo-evidence attacks. Then either find one non-obvious result (e.g. how conjunction length k drives URR for constraint-by-constraint verifiers, or a lower bound showing any confidence-based rule needs evidence acquisition) or present Thms 1–2 as "propositions" that motivate the design. *Fixes R1.1–R1.4.*
3. **Show why support matters, with numbers.** Measure how often unsupported recommendations are *wrong* on natural new listings (via `details`), how much a GEO-style rewrite moves prior-based matchers vs. yours, and coverage on real listings. One table that makes "unsupported is harmful even when sometimes right" undeniable resolves R4.2 and R2.5.
4. **Make contamination control mandatory.** Use post-cutoff listings (scraped after the evaluated models' training cutoffs, or newest-launched items) for the RQ1 diagnosis, not as an option.
5. **Narrow the headline to one claim.** Keep: diagnosis, support-guaranteed matcher, benchmark. Move the disclosure theorem and the general strategic-robustness bound to the appendix or future work (the plan's cut order already allows this). Keep the exposure-gap constraint only if it is evaluated, not just stated.
6. **Clean up baselines and documents.** Drop or properly adapt Recformer/UniSRec. Reconcile the three documents: `details` hidden (plan §11) vs. visible (proposal); no human gold set; and correct `literature-review.md` §3.3, which says post-launch labels are used for calibration (plan §11.1 says never). Downgrade RQ3's claim to "post-launch signal is consistent with" and list the 2023-snapshot problem as a limitation.

## One note beyond NeurIPS

The plan now makes the NeurIPS paper the whole IS thesis and leaves Paper B (H1–H3, the marketing and entrepreneurship outcome) as optional. For an IS committee, that's the part that makes it an IS thesis rather than an ML paper. Worth confirming with your supervisor that a thesis with Paper B as "if time allows" will satisfy the programme.
