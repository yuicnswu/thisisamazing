# Supervisor brief: Agentic AI for Beauty Product Development and Go-to-Market Research

## Proposed study

Develop an evidence-grounded agentic AI copilot that helps beauty merchants investigate customer needs, compare competitors and turn review evidence into product-development and go-to-market hypotheses. The practical demo will recommend an evidence-supported product-page clarification and a concrete positioning test, with supporting and conflicting evidence.

## Evidence already available

- Amazon All Beauty: 112,590 catalog products and 694,253 deduplicated reviews.
- Sephora: 8,494 catalog products and 1,094,187 deduplicated reviews, covering 2,351 products.
- Sephora supplies 926,314 existing recommendation labels; 412,406 labeled reviews have strictly earlier other-product customer history.
- Amazon has sparse reviewer histories and incomplete listings; a price/description/features filter retains only 3.85% of its catalog.

These findings favor Sephora for customer-context experiments and Amazon as a separate coverage/robustness domain. No cross-retailer identity mapping is assumed.

## Research contribution

Can a self-evolving, budget-aware multi-agent orchestrator improve the accuracy-cost trade-off of evidence-backed beauty market research? Compare a strong fixed workflow, a single adaptive agent, a fixed-policy multi-agent orchestrator and the same orchestrator after bounded self-evolution on development templates only, with the same model and tools at matched budgets, on 120 held-out tasks including trap tasks with known confounds. The verbatim-quote evidence check is already tested on 2,182 real products (certified unsupported rate ≤ 10%, 88–90% recall). Use executable analytical task oracles and held-out recommendation outcomes without creating new human review annotations.

## Business value and limits

Target faster research, concept comparison, positioning and launch-test preparation. Measure system correctness, runtime and cost first. A future merchant workflow study can measure staff effort and time to approved decisions; actual sales impact requires controlled deployment. A proposed 30–50% effort reduction is an unvalidated pilot target. An illustrative scenario gives $2,250/month in capacity value, not observed savings, assuming 10 briefs, 6 hours saved each, $40/hour labor and $150/month AI cost.

## Academic positioning

Intended venue: ICIS 2027 or HICSS-61, framed as design science research (five design principles, a staged FEDS evaluation). The ISMS Marketing Science framing of the 24 October draft is retired. The study leads with a marketing problem and tests whether agentic control adds value; it does not claim to discover proven market demand, validate formulation safety, or guarantee launch success. If fixed workflows match the agent, that boundary condition is a valid outcome.

## Proposed deliverables

A merchant demo; audited EDA and source registries; an executable task suite; matched-budget comparisons and ablations; a separate existing-label outcome experiment; and an eight-week research plan. Paid model experiments have not yet run.

[Full proposal](agentic_beauty_market_research.md)
