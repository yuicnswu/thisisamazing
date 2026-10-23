# Brainstorm

*Living document. Stage 1 of [WORKFLOW.md](../WORKFLOW.md). Update it whenever stages 02–05 surface a new problem, constraint or changed hypothesis.*

Starting inputs: `is-topic/research_proposal.md`, `is-topic/topic-comparison.md`, `is-topic/refined-thesis-plan.md`, `is-topic/neurips-mock-review.md`, and the beauty GMV dataset below.

**Updated 2026-10-21 (repositioning).** The RQ1 pilot (`05-report/report.md`), the 2025–2026 field check and the role-by-role team opinion (both in the project files under `team-opinion/`) changed what the work can claim. The sections below are rewritten around that. What was retired, and why, is in "Claims retired".

## Perspectives by role
*Condensed from the 2026-10-21 team opinion (`team-opinion/team-opinion.md` in the project files), which applied each brief in `.agents/` to the pilot and the field check.*

| Role | What they see | What they want changed |
|---|---|---|
| PI (`research-principal-investigator`) | The question is open; the pitch's version isn't. Brand bias and the URR template are published; a strict prompt gets URR to 5–10%. The pilot's accidental result is the paper: confidence and prompting can't be **certified**, a quote-checked verifier can. | Re-centre the claim on certifiable grounding. |
| Researcher | Novelty is in the combination and the benchmark. Seven must-cite papers were missing (now in stage 02, plus a semi-supervised risk-control paper found 2026-10-21). | 2026 baseline set; evaluate where strict prompting fails (k ≥ 2, paraphrase, usage-text distractors). |
| Domain expert | Beauty needs are mostly experiential; ~5–6% of early reviews state a checkable one. Listings are badly incomplete: `details` carries skin/hair type six times as often as the visible text. | Scope claims to checkable needs; stop selling missing attributes as the reason new brands fail. |
| NeurIPS reviewer (`neurips-2026-standard`) | Main track reject-leaning today (routine LTT, overlapping diagnosis, one small category, Claude-only models and judge). | Gold-set true-risk bound, non-vacuity, ≥ 10× scale, ≥ 2 categories, open-weight models. |
| Data scientist | The certified result is real at α = 0.10; n is the binding constraint at α = 0.05. | Bigger category; test the new-vs-established gap (Theorem 4). |
| AI engineer | Blocked on the Mac run (BLaIR, open-weight). Paraphrase recall (0–2%) is the verifier's weak spot. | Quote-only NLI typed check; open-weight judge. |
| Product manager | G0 failed on All_Beauty; stage files were spread over five PRs. | Consolidate PRs; decide the category before the 30 Nov gate. |
| Paper writer | "The honest paper is smaller and stronger than the pitch." | Retire four claims (below); lead with what the evidence supports. |
| Data engineer / analyst | Both review files and the pilot listings are in hand; the metadata for any larger category is not reachable from the cloud or the Mac sandbox (403). | Count G0 on the Mac host itself. |
| UX / full-stack | The merchant loop is the only part a seller sees. | Design the disclosure request as a verification task ("does this apply?"), never auto-filled text. |

## Novelty, audience, methodology and evaluation check (PI + researcher)

**Novelty after the field check (2026-10-21).**
- *Published by others:* brand bias in LLM product recommendation on skincare (Chu & Hou, 2026); conformal risk control on a recommender threshold (De Toni et al., 2025); conformal factuality and its conditional and abstention variants (Mohri & Hashimoto, 2024; Cherian et al., 2024; Abbasi-Yadkori et al., 2024); semi-supervised risk control that combines a small labelled set with model-imputed labels (Einbinder et al., 2024); review-mined preferences on Amazon Beauty (Paischer et al., 2024).
- *Still open (no paper found):* (1) a shopping benchmark that scores **abstaining when the listing is silent**; (2) evidence that a recommender's **groundedness can be certified with checkable quotes when its confidence cannot**, on the same items and α (Ravikumar, 2026, supports this from the confidence side); (3) turning abstentions into **demand-ranked, truthful disclosure requests**, the counter-position to GEO rewriting (Bagga et al., 2025; Allouah et al., 2025); (4) a selective, conjunctive risk guarantee for **newly launched** items under one-sided label noise.

**Audience.** Primary: NeurIPS Evaluations & Datasets track (the 2026 name of Datasets & Benchmarks), RecSys 2027 or SIGIR 2027 (resource / reproducibility or full paper). Secondary: an IS paper on seller disclosure and new-entrant exposure (design science, or with an experiment). NeurIPS main track is a stretch goal with a specific bar (project-spec.md, "Venue bar").

**Methodology.** Counterfactual edits of real listings with labels from hidden `details`, two independent extractors, and the NeSy certificate; Learn-then-Test on one item per product; product-cluster bootstrap CIs. Changes: needs with k ≥ 2 constraints and paraphrased evidence become first-class cells; a brand-mask control and a Chu & Hou choice-set replication sit next to the single-listing protocol; ≥ 2 categories; open-weight matchers and an open-weight judge.

**Evaluation.** URR with informativeness (coverage, recall of supported) always reported together; certifiability (does LTT certify anything at α); conjunctive URR by k; disclosure yield and entrant exposure for the merchant loop.

## Core problems
1. **P1. Confidence is not certifiable groundedness.** Shopping assistants decide from priors and self-reported confidence. Neither separates supported from unsupported recommendations well enough to certify a risk level (pilot: confidence and strict-prompt scores certify nothing at α = 0.10; quote-certified scores certify in 100% of splits).
2. **P2. Benchmarks never ask the model to say "the listing doesn't say".** Every 2025–2026 shopping benchmark found assumes the needed information exists.
3. **P3. Listings are silently incomplete, and sellers are told to persuade rather than disclose.** 37% of 6,503 All_Beauty listings have at least one checkable attribute recorded in the hidden `details` field but absent from the text shoppers see (29% excluding item form). GEO work rewrites for rank without checking truth.
4. **P4. Strict prompting looks sufficient only on easy items.** One constraint, stated in the parser's words, is where the 5–10% URR was measured. Real needs are conjunctions, and real evidence is paraphrased or mixed with usage text.
5. **P5. Data scale.** At the pilot's coverage, α = 0.10 needs about 1,000–2,200 independent products; α = 0.05 needs about 5,000 if the verifier's true URR is 2%, and about 12,600 if it is 3% (`04-implementation/category_check`). All_Beauty has about 2,200 usable ones.

## Testable hypotheses
| | Hypothesis | Falsified if |
|---|---|---|
| H-A (certifiability) | On the same items and α, LTT certifies a quote-certified verifier but not confidence-based or strict-prompt scores; the gap holds for open-weight models and dense encoders. | An uncertified score family certifies at α = 0.10 with comparable recall in ≥ 80% of splits. |
| H-B (hard split) | A strict prompt's URR rises above α = 0.10 on two-constraint needs where one constraint is missing or vague, and its recall falls on paraphrased evidence, while per-constraint verification keeps URR ≤ α. | Strict-prompt conjunctive URR stays ≤ 0.10 (CI) and paraphrase recall stays ≥ 80%. |
| H-C (reconciliation with Chu & Hou) | Brand drives choice between identical-spec items but not single-listing accept/reject; product type is the operative prior in the latter. | Brand-mask vs famous-brand changes single-listing decisions by ≥ 5 pp, same direction, CI excluding 0. |
| H-D (disclosure) | Truthful disclosure of the attribute that caused an abstention raises certified coverage without raising URR, more for new products than for established ones, while GEO rewriting raises rank but introduces unverifiable or false claims. | Disclosure yield ≈ 0, or URR rises above α after disclosure. |
| H-E (entrant exposure) | Under the certified matcher, the coverage gap between zero-review and established products is explained by missing evidence; disclosure closes most of it. | The gap persists after disclosure at equal evidence. |

Paper B's H1–H3 (early-buyer fit and review trajectories) stay as written in `is-topic/refined-thesis-plan.md` §3, as a separate IS paper.

## Claims retired (2026-10-21)
| Retired claim | Why | Replaced by |
|---|---|---|
| "AI recommenders are biased by brand" | Published on skincare (Chu & Hou, 2026); our pilot found no brand effect in single-listing checks | H-C, a reconciliation |
| "First support guarantee" / "URR ≤ α" as a headline | Template exists (De Toni et al., 2025; Mohri & Hashimoto, 2024) | URR control as method; certifiability (H-A) as the finding |
| "Regret prevented" / 22.4% vs 14.9% as an effect | Keyword-detected association, no returns data | Motivation only, labelled as association |
| "Robust by construction to strategic rewrites" | Fails for a learned verifier (`theory.md` Prop 12); fabricated claims persuade models | Disclosure requests are verification tasks; adversarial evaluation |
| "LLMs license matches on priors" as the main finding | Strict prompting fixes it on easy items | H-B on the hard split |

## Datasets
*Added 2026-10-17 when yui shared `hackathon_beauty_gmv.csv` and its EDA report (both in the project's shared folder under `data/`, with a full profile in `data/README.md`; not committed here because of size and the Amazon Reviews 2023 licence).*

| Dataset | Source | Size | Planned role |
|---|---|---|---|
| Amazon Reviews 2023: All_Beauty | McAuley Lab | full category files (reviews + metadata) | Thesis dev set and RQ1 pilot |
| Amazon Reviews 2023: Beauty_and_Personal_Care | McAuley Lab | full category files, raw (0-core) | Thesis main data: skin care = main benchmark, hair care = held-out split; RQ3 validation and Paper B (H1–H3) |
| Amazon Reviews 2023: Appliances | McAuley Lab | full category file | Optional cross-domain transfer test |
| Beauty GMV cohort | Cut from Amazon Reviews 2023 beauty; one row per review event | 16,093 rows raw, 15,606 after dedup; 12,935 verified; 5,233 verified cold-start (0–9 prior reviews) | Hackathon demo and pipeline sanity check; not the thesis benchmark (too thin, see D6) |

The EDA report's counts reproduce exactly from the CSV after deduplicating on `(user_id, parent_asin)`.

## Constraints from the data
- **D1. Category: Beauty is the main category** (yui, 2026-10-17: "let's do beauty"). *Update 2026-10-21:* G0 failed on All_Beauty (3.7% of listings with ≥ 2 agreeing attributes, ~6% of early reviews with a checkable need), and the repositioned benchmark needs ≥ 2 categories anyway. The recommendation is to count G0 on both Beauty_and_Personal_Care and Home_and_Kitchen and use both (`03-solution-design/project-spec.md`, "Categories"). This is yui's decision. Reason: the thesis uses the same dataset as BLaIR (Hou et al., ACL 2026), which released Amazon Reviews 2023 and evaluates on All Beauty. It is not a follow-up to BLaIR's method; BLaIR's released encoders become a zero-shot baseline and an RQ1 probe, and its Amazon-C4 recipe a source of need statements (plan §12.0). The cohort shows listing evidence is sparse (`skin_type` 16%, `product_benefits` 13%, `active_ingredients` 2.4% present) while priors are always present. Consequences, detailed in `is-topic/refined-thesis-plan.md` §12:
  - Scope is limited to **checkable** beauty attributes: skin type, hair type, scent / fragrance-free, item form, free-from claims, volume, SPF, count, and ingredients when a list exists. Experiential needs ("won't break me out") are out of scope and should trigger abstention.
  - Expect higher abstention, a harder spec parser (vague words like "gentle") and noisier misfit labels than in Home & Kitchen.
  - Gate G0 (by 31 Oct) counts, on the full Beauty_and_Personal_Care metadata, products whose visible text and hidden `details` agree on ≥2 attributes (target ≥20,000) and the share of early verified reviews with a checkable need. If G0 fails, Beauty keeps RQ1 and the hackathon, and RQ2's benchmark moves back to Home & Kitchen.
- **D2. "GMV" is a proxy.** `order_gmv` equals list price (one unit per review); satisfied/regret GMV are price × 1[rating ≥ 4] / 1[rating ≤ 2]. Any revenue-effect claim for the hackathon brief must say it is rating-weighted list price over reviews, not observed sales.
- **D3. Snapshot leakage.** `meta_rating_number` and `meta_average_rating` are 2023 crawl values (median 11× the reviews existing at purchase). Usable as popularity cues in RQ1 prompts; never as launch-time features for RQ3 or H1.
- **D4. Dedup first.** The shared CSV is pre-dedup (487 repeat user–product pairs); without dedup a user's history can contain the target product.
- **D5. Promotional seeding at launch.** 26–30% of reviews on products with 1–9 prior reviews are unverified vs 5% for established products; outcome metrics use `verified_purchase == True`.
- **D6. Thin trajectories.** Median product has one row and 985 products have both a cold-start and a later row, so H1 (6–12-month review trajectories) needs the full category files, not this cut.
- **D7. Small effects so far.** The report's satisfaction/regret gaps are 1–7 pp on cells of 172–772 rows without confidence intervals; treat them as hypotheses for the G1 pilot, not findings.
- **D8. Review-side need rate is low in both available categories (2026-10-21).** On the full review files, a rule proxy finds a checkable attribute in 5.2% of early verified All_Beauty reviews (17,776 of 343,706) and 8.6% of early verified Appliances reviews (34,201 of 396,393), most of the latter being fit/compatibility with a named appliance. Neither clears the plan's 10% bar on its own; Appliances products are also better reviewed (25% have ≥ 10 verified reviews vs 11%). Source: `04-implementation/category_check`.
- **D9. Disclosure inventory.** 2,435 of 6,503 All_Beauty listings (37%) have a checkable attribute in `details` that the visible text never states. This is the natural test bed for the merchant-fix loop: `details` plays the truthful seller.
