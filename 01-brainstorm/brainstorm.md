# Brainstorm

*Living document. Stage 1 of [WORKFLOW.md](../WORKFLOW.md). Update it whenever stages 02–05 surface a new problem, constraint or changed hypothesis.*

Starting inputs: `is-topic/research_proposal.md`, `is-topic/topic-comparison.md`, `is-topic/refined-thesis-plan.md`, `is-topic/neurips-mock-review.md`, and the beauty GMV dataset below.

## Perspectives by role
_To be filled._

## Novelty, audience, methodology and evaluation check (PI + researcher)
_To be filled._

## Core problems
_To be filled._

## Testable hypotheses
_To be filled._

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
- **D1. Category: decided, Beauty is the main category** (yui, 2026-10-17: "let's do beauty"). Reason: the thesis uses the same dataset as BLaIR (Hou et al., ACL 2026), which released Amazon Reviews 2023 and evaluates on All Beauty. It is not a follow-up to BLaIR's method; BLaIR's released encoders become a zero-shot baseline and an RQ1 probe, and its Amazon-C4 recipe a source of need statements (plan §12.0). The cohort shows listing evidence is sparse (`skin_type` 16%, `product_benefits` 13%, `active_ingredients` 2.4% present) while priors are always present. Consequences, detailed in `is-topic/refined-thesis-plan.md` §12:
  - Scope is limited to **checkable** beauty attributes: skin type, hair type, scent / fragrance-free, item form, free-from claims, volume, SPF, count, and ingredients when a list exists. Experiential needs ("won't break me out") are out of scope and should trigger abstention.
  - Expect higher abstention, a harder spec parser (vague words like "gentle") and noisier misfit labels than in Home & Kitchen.
  - Gate G0 (by 31 Oct) counts, on the full Beauty_and_Personal_Care metadata, products whose visible text and hidden `details` agree on ≥2 attributes (target ≥20,000) and the share of early verified reviews with a checkable need. If G0 fails, Beauty keeps RQ1 and the hackathon, and RQ2's benchmark moves back to Home & Kitchen.
- **D2. "GMV" is a proxy.** `order_gmv` equals list price (one unit per review); satisfied/regret GMV are price × 1[rating ≥ 4] / 1[rating ≤ 2]. Any revenue-effect claim for the hackathon brief must say it is rating-weighted list price over reviews, not observed sales.
- **D3. Snapshot leakage.** `meta_rating_number` and `meta_average_rating` are 2023 crawl values (median 11× the reviews existing at purchase). Usable as popularity cues in RQ1 prompts; never as launch-time features for RQ3 or H1.
- **D4. Dedup first.** The shared CSV is pre-dedup (487 repeat user–product pairs); without dedup a user's history can contain the target product.
- **D5. Promotional seeding at launch.** 26–30% of reviews on products with 1–9 prior reviews are unverified vs 5% for established products; outcome metrics use `verified_purchase == True`.
- **D6. Thin trajectories.** Median product has one row and 985 products have both a cold-start and a later row, so H1 (6–12-month review trajectories) needs the full category files, not this cut.
- **D7. Small effects so far.** The report's satisfaction/regret gaps are 1–7 pp on cells of 172–772 rows without confidence intervals; treat them as hypotheses for the G1 pilot, not findings.
