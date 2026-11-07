"""Offline EDA -> evidence -> 5 Whys -> provisional Good Question Cards.
Run from any directory with the project's .venv Python. No model/API calls.
"""
from pathlib import Path
import base64
import hashlib
import html
import importlib.metadata
import json
import os

os.environ.setdefault('MPLBACKEND', 'Agg')
os.environ.setdefault('MPLCONFIGDIR', '/private/tmp/beauty-research-mpl')
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/beauty_research_workflow'


def save_json(path, obj):
    path.write_text(json.dumps(obj, indent=2, default=str) + '\n')


def load_data():
    """Reuse full-file profiles, and recompute the evidence from those rows."""
    OUT.mkdir(parents=True, exist_ok=True)
    paths = {
        'catalog': ROOT / 'output/beauty_eda/products_profile.csv',
        'reviews': ROOT / 'output/beauty_reviews/reviews_with_catalog.parquet',
        'products': ROOT / 'output/beauty_reviews/product_review_profile.csv',
        'histories': ROOT / 'output/beauty_reviews/reviewer_history_profile.parquet',
    }
    for path in paths.values():
        if not path.exists():
            raise FileNotFoundError(f'{path}: first run scripts/beauty_eda.py and scripts/add_beauty_reviews.py')
    catalog = pd.read_csv(paths['catalog'])
    columns = ['parent_asin', 'asin', 'review_rating', 'text_chars', 'helpful_vote',
               'verified_purchase', 'exact_duplicate', 'catalog_match', 'review_image_count']
    reviews = pd.read_parquet(paths['reviews'], columns=columns)
    histories = pd.read_parquet(paths['histories'])
    assert catalog.parent_asin.is_unique and catalog.parent_asin.notna().all()
    assert reviews.catalog_match.all(), 'Investigate unmatched records before proceeding'
    clean = reviews.loc[~reviews.exact_duplicate].copy()
    provenance = {name: {'path': str(path), 'sha256': hashlib.file_digest(path.open('rb'), 'sha256').hexdigest()}
                  for name, path in paths.items()}
    provenance['source_manifest'] = json.loads((ROOT / 'data/beauty_sources.json').read_text())
    provenance['versions'] = {name: importlib.metadata.version(name) for name in
                              ['ai-data-science-team', 'pandas', 'pytimetk', 'sweetviz', 'nbformat']}
    provenance['scope'] = 'Local catalog/review snapshots; review deduplication uses exact record hashes.'
    save_json(OUT / 'provenance.json', provenance)
    return {'catalog': catalog, 'reviews': reviews, 'clean': clean, 'histories': histories}


def run_eda(data):
    """Call the original notebook's real tools directly, without LLM orchestration."""
    from ai_data_science_team.tools.eda import describe_dataset, visualize_missing, generate_correlation_funnel, generate_sweetviz_report
    catalog, clean = data['catalog'], data['clean']
    numeric_catalog = catalog[['average_rating', 'rating_number', 'price', 'title_chars', 'description_chars', 'feature_chars']]
    numeric_reviews = clean[['review_rating', 'text_chars', 'helpful_vote', 'review_image_count']]
    status = {}
    for name, frame in [('catalog', numeric_catalog), ('reviews', numeric_reviews)]:
        _, artifact = describe_dataset.func(data_raw=frame.to_dict())
        pd.DataFrame(artifact['describe_df']).to_csv(OUT / f'{name}_tool_description.csv', index=False)
        status[f'describe_{name}'] = {'rows': len(frame), 'scope': 'full population in derived profile'}
    sample = numeric_catalog.sample(n=min(2000, len(catalog)), random_state=42).reset_index(drop=True)
    _, missing = visualize_missing.func(data_raw=sample.to_dict(), n_sample=len(sample))
    for key, value in missing.items():
        if not isinstance(value, str):
            raise RuntimeError(f'Missingness plot failed: {key}: {value}')
        (OUT / f'{key}.png').write_bytes(base64.b64decode(value))
    status['missingness'] = {'sample_rows': len(sample), 'seed': 42, 'scope': 'uniform catalog sample; use ledger for exact counts'}
    # A missingness diagnostic, not a customer-fit or causal model. Avoid price
    # itself and other direct price encodings as predictors of its availability.
    diagnostic = pd.DataFrame({
        'price_available': catalog.has_price.map({True: 'Yes', False: 'No'}),
        'description_available': catalog.has_description.map({True: 'Yes', False: 'No'}),
        'features_available': catalog.has_features.map({True: 'Yes', False: 'No'}),
        'rating_count': catalog.rating_number,
        'title_chars': catalog.title_chars,
    }).dropna().sample(n=5000, random_state=42).reset_index(drop=True)
    assert diagnostic.price_available.eq('Yes').any() and not diagnostic.isna().any().any()
    _, funnel = generate_correlation_funnel.func(data_raw=diagnostic.to_dict(), target='price_available', target_bin_index='Yes')
    pd.DataFrame(funnel['correlation_data']).to_csv(OUT / 'availability_correlations.csv', index=False)
    for key in ['plot_image', 'plotly_figure']:
        if isinstance(funnel[key], dict) and 'error' in funnel[key]:
            raise RuntimeError(f'Correlation rendering failed: {funnel[key]}')
    (OUT / 'availability_funnel.png').write_bytes(base64.b64decode(funnel['plot_image']))
    save_json(OUT / 'availability_funnel_plotly.json', funnel['plotly_figure'])
    status['correlation_funnel'] = {'sample_rows': len(diagnostic), 'seed': 42, 'target': 'price_available=Yes',
                                  'interpretation': 'Binned Pearson associations; exploratory, no causal inference or significance claim.'}
    _, sweet = generate_sweetviz_report.func(data_raw=sample.to_dict(), report_name='sweetviz.html', report_directory=str(OUT), open_browser=False)
    assert (OUT / 'sweetviz.html').is_file(), sweet
    status['sweetviz'] = {'sample_rows': len(sample), 'seed': 42, 'target': None}
    save_json(OUT / 'tool_execution.json', status)
    return status


def build_evidence(data):
    c, r, clean, h = (data[k] for k in ['catalog', 'reviews', 'clean', 'histories'])
    mixed = clean.assign(low=clean.review_rating.le(2), high=clean.review_rating.ge(4)).groupby('parent_asin').agg(
        n=('review_rating', 'size'), low=('low', 'sum'), high=('high', 'sum'))
    records = []
    def add(key, claim, numerator, denominator, source, boundary):
        records.append(dict(id=key, claim=claim, numerator=int(numerator), denominator=int(denominator),
                            percent=100 * numerator / denominator, source=source, boundary=boundary, status='observed'))
    add('E1', 'Products with observed price', c.has_price.sum(), len(c), 'catalog.has_price', 'Missing price does not mean unavailable or free.')
    add('E2', 'Products retained by price + description + features filter', (c.has_price & c.has_description & c.has_features).sum(), len(c), 'catalog.has_*', 'Eligibility changes are measurable; conversion effects are unknown.')
    add('E3', 'Exact duplicate excess review records', r.exact_duplicate.sum(), len(r), 'reviews.exact_duplicate', 'Exact records only; repeated short phrases are not evidence of fraud.')
    add('E4', 'Review records matched to catalog', r.catalog_match.sum(), len(r), 'reviews.catalog_match', 'Parent-level match does not establish variant-level attribute agreement.')
    add('E5', 'Reviewers with one distinct observed product', h.distinct_products.eq(1).sum(), len(h), 'histories.distinct_products', 'Category-specific observed reviews are not complete purchase histories.')
    add('E6', 'Reviewers with at least five distinct observed products', h.distinct_products.ge(5).sum(), len(h), 'histories.distinct_products', 'Earlier eligible histories after a temporal split will be fewer.')
    add('E7', 'Products with >=20 deduplicated reviews and >=3 low and >=3 high ratings', ((mixed.n >= 20) & (mixed.low >= 3) & (mixed.high >= 3)).sum(), len(mixed), 'clean reviews grouped by parent_asin', 'Candidate pool only; neither preference conflicts nor customer fit are validated.')
    add('E8', 'Raw reviews with variant ASIN different from parent ASIN', r.asin.ne(r.parent_asin).sum(), len(r), 'reviews.asin,parent_asin', 'Identifier difference alone is not a join error.')
    five = c.average_rating.eq(5)
    add('E9', 'Five-star products supported by fewer than five catalog ratings', (five & c.rating_number.lt(5)).sum(), five.sum(), 'catalog.average_rating,rating_number', 'Catalog ratings and collected reviews have different scopes.')
    ledger = pd.DataFrame(records)
    ledger.to_csv(OUT / 'evidence_ledger.csv', index=False)
    save_json(OUT / 'evidence_ledger.json', records)
    return records


def build_whys(evidence):
    """Method-guided analysis: chain links are not automatically causal findings."""
    chains = [
        dict(id='W1', problem='A complete-listing filter excludes most products from a shopping study.', evidence=['E1', 'E2'],
             steps=[{'why': 'Why are products excluded?', 'answer': 'The rule requires observed price, description and features simultaneously.', 'status': 'verified rule consequence'},
                    {'why': 'Why are these fields absent?', 'answer': 'The local snapshot contains missing fields; source omission, extraction, and availability timing are competing explanations.', 'status': 'unknown; stop'}],
             root_cause='Verified exclusion mechanism: conjunction of three availability requirements. Origin of missingness is unresolved.',
             countermeasure='Report all-product and eligible-product results separately; audit missing fields against independently obtained source records.',
             reverse_check='Removing the filter restores eligibility by construction; improved fit or revenue must be tested separately.', confidence='High for exclusion mechanism; unknown for upstream origin.'),
        dict(id='W2', problem='Most observed reviewers cannot support a multi-product history experiment.', evidence=['E5', 'E6'],
             steps=[{'why': 'Why is multi-product history scarce?', 'answer': 'Most user IDs have only one distinct reviewed product in this category snapshot.', 'status': 'observed constraint'},
                    {'why': 'Why do they have only one?', 'answer': 'Sparse reviewing, category restrictions and collection scope are possible explanations. Purchases outside the snapshot are unobserved.', 'status': 'unknown; stop'}],
             root_cause='The snapshot lacks enough observed within-user history for most users; its behavioral origin is unresolved.',
             countermeasure='Begin with explicit context annotation; report the size and selection of any eligible history subset after temporal splitting.',
             reverse_check='More earlier reviews could enlarge eligibility; they would not establish that personalization improves customer fit.', confidence='High for data limitation; low for behavioral explanations.'),
        dict(id='W3', problem='Opposing ratings cannot by themselves identify customer-specific product fit.', evidence=['E7', 'E8', 'E9'],
             steps=[{'why': 'Why are opposing ratings insufficient?', 'answer': 'A single score does not identify the aspect, user need, product variant or reason for dissatisfaction.', 'status': 'measurement limitation'},
                    {'why': 'What could explain disagreement?', 'answer': 'Preferences, performance differences, variant mismatch, defects, shipping or authenticity concerns are rival hypotheses.', 'status': 'untested hypotheses'},
                    {'why': 'Which explanation is supported?', 'answer': 'No adjudicated aspect/context labels or prospective shopper outcomes are available in this workflow.', 'status': 'unresolved; stop'}],
             root_cause='The desired construct (customer fit) has not been independently measured; there is no established cause of rating disagreement.',
             countermeasure='Annotate context, aspect, preference, defect, logistics and uncertainty with quoted spans; collect real shopper judgments before fit claims.',
             reverse_check='Better annotations may distinguish explanations; only held-out validation can show the distinction is reliable.', confidence='High for measurement gap; causal explanation unresolved.')]
    save_json(OUT / 'five_whys.json', chains)
    text = '# Evidence-backed 5 Whys\n\nChains stop when evidence runs out; the number of links is not a quality target.\n'
    for chain in chains:
        text += f"\n## {chain['id']}: {chain['problem']}\n\nEvidence: {', '.join(chain['evidence'])}.\n"
        for step in chain['steps']:
            text += f"\n- **{step['why']}** {step['answer']} [{step['status']}]\n"
        for key in ['root_cause', 'countermeasure', 'reverse_check', 'confidence']:
            text += f"\n**{key.replace('_', ' ').title()}:** {chain[key]}\n"
    (OUT / 'five_whys.md').write_text(text)
    return chains


def build_questions():
    # Scores are transparent planning judgments, not empirical research results.
    specs = [
        ('Q1', 'Can an LLM distinguish explicit preference mismatch from product defects and delivery complaints?', 'Review text contains enough explicit evidence for humans to distinguish these explanations.', ['E7', 'E8'], 'W3', [5, 4, 5, 5, 5], 'pilot'),
        ('Q2', 'Does explicit usage context improve customer–product fit judgments beyond product ratings?', 'Independent shoppers can supply needs and compare plausible products.', ['E5', 'E7'], 'W2', [5, 2, 5, 3, 5], 'park pending shopper labels'),
        ('Q3', 'Do LLM conclusions remain stable when irrelevant brand and rating cues are masked?', 'Human validators can confirm that edits preserve relevant product information.', ['E9'], 'W3', [4, 4, 5, 4, 4], 'secondary pilot'),
        ('Q4', 'Does variant-aware review retrieval improve aspect interpretation?', 'Variant identity and corresponding listing attributes can be verified independently.', ['E8'], 'W3', [4, 2, 4, 3, 4], 'park pending variant mapping'),
        ('Q5', 'Do earlier reviewer histories improve fit judgments over explicit current needs?', 'Enough time-valid multi-product histories and independent fit labels exist.', ['E5', 'E6'], 'W2', [4, 1, 4, 2, 4], 'park pending history audit'),
        ('Q6', 'Does evaluation only on complete listings overstate LLM interpretation performance?', 'Human labels can be sampled across completeness strata.', ['E1', 'E2'], 'W1', [4, 4, 5, 5, 4], 'secondary pilot'),
    ]
    names = ['importance', 'feasibility', 'falsifiability', 'evidence_leverage', 'downside_learning']
    questions = [dict(id=q, question=text, hidden_assumption=a, evidence=e, why_chain=w,
                      scores=dict(zip(names, scores)), planning_total=sum(scores), originality=None,
                      originality_status='[Unresolved Gap] Literature audit required; no novelty or conference-readiness claim.', decision=d)
                 for q, text, a, e, w, scores, d in specs]
    questions.sort(key=lambda q: -q['planning_total'])
    save_json(OUT / 'questions.json', questions)
    cards = []
    for qid, title, stake, hypotheses, test, falsifier, pilot, resources, objection, action in [
        ('Q1', 'Distinguishing preference mismatch from product failure',
         'A merchant needs different actions for unsuitable targeting, a defective product and delivery problems.',
         ['H1: Explicit context and aspect spans improve preference-mismatch classification.',
          'H2: Sentiment and complaint keywords explain apparent gains without context reasoning.',
          'H3: Humans cannot reliably separate these causes from available text.'],
         'Compare majority/keyword baselines, text-only LLM and context/aspect-guided LLM under an equal model budget. Use two independent annotators plus adjudication; allow unclear and multiple labels. Split by parent product and remove exact duplicates; exclude listing aggregate ratings and reviewer identifiers. Report macro-F1, per-class recall, span F1, uncertainty coverage, product-cluster bootstrap intervals, cost and latency.',
         'No reliable human agreement, or no held-out improvement over the strongest baseline after controlling for sentiment and review length. Treat inconclusive intervals as inconclusive.',
         'Days 1–3: refine schema on 50 reviews. Days 4–7: independently label 300 additional reviews across rating and completeness strata, including mixed-rating products and controls. Days 8–10: freeze schema and product-disjoint split; lock prompts on development data. Days 11–14: evaluate baselines and context ablation on untouched test products. Use pilot variance to plan a powered follow-up.',
         'Two annotators, one adjudicator, local review text, annotation budget; model access and cost approval before running LLM experiments.',
         'This may be ordinary complaint classification; no independently verified customer fit or demonstrated novelty.',
         'Review the 200-row annotation seed, extend it beyond rating-balanced sampling, and label the first 50 with uncertainty.'),
        ('Q6', 'Selection effects from listing completeness',
         'A shopping assistant evaluated only on complete listings may leave most of a merchant catalog untested.',
         ['H1: Restricting to complete listings changes measured LLM performance.',
          'H2: Differences reflect review length, product type or review volume rather than completeness.',
          'H3: Performance is stable across completeness strata.'],
         'Sample independently labeled reviews in complete and incomplete product strata. Keep test products disjoint from development. Compare the same frozen model; report within-stratum macro-F1 and catalog-weighted estimates. Match or stratify on observable review length and volume; validate product types manually. Report residual confounding and do not interpret a stratum difference as a causal effect of missingness.',
         'No meaningful stratum difference, or the difference disappears under observable controls; either result limits the selection-bias claim.',
         'Week 1: cross-tab eligibility and design a 300-review stratified annotation sample. Week 2: adjudicate, freeze prompts, evaluate a single fixed model and reweight to known catalog proportions. Report uncertainty and strata with insufficient labels.',
         'Same annotators and frozen model as Q1; extra labels may be necessary for sparse strata.',
         'Observed groups are confounded, listing timestamps are unknown, and the pilot may be underpowered.',
         'Audit the eligibility table and preregister the strata and estimand before looking at model scores.')]:
        question = next(q for q in questions if q['id'] == qid)
        cards.append(dict(id=qid, working_title=title, research_question=question['question'], stake=stake,
                          hidden_assumption=question['hidden_assumption'], competing_hypotheses=hypotheses,
                          discriminating_test=test, falsifier=falsifier, two_week_pilot=pilot,
                          minimum_resources=resources, strongest_reviewer_objection=objection,
                          next_action=action, status='Provisional design; no experiment has been run.'))
    save_json(OUT / 'question_cards.json', cards)
    md = '# Provisional research questions\n\nScores (1–5) are planning judgments. Originality is unscored pending a literature audit. No LLM evaluation or causal experiment has been run.\n'
    for q in questions:
        md += f"\n- **{q['id']} ({q['planning_total']}/25; {q['decision']}):** {q['question']} Evidence: {', '.join(q['evidence'])}; chain: {q['why_chain']}. Assumption: {q['hidden_assumption']}\n"
    for card in cards:
        md += f"\n## {card['id']}: {card['working_title']}\n"
        for key, value in card.items():
            if key not in ['id', 'working_title']:
                rendered = '\n'.join('- ' + s for s in value) if isinstance(value, list) else value
                md += f"\n**{key.replace('_', ' ').title()}:**\n\n{rendered}\n"
    md += '\n## Claims to verify before a paper claim\n\n- Audit current literature for equivalent complaint/context benchmarks and methods.\n- Establish annotation agreement and construct validity independently of model outputs.\n- Obtain prospective shopper needs and judgments before claiming customer–product fit.\n- Obtain merchant action/outcome data or run an experiment before claiming conversion, margin or retention gains.\n'
    (OUT / 'research_questions.md').write_text(md)
    return questions, cards


def write_report(evidence, chains, questions, cards):
    esc = lambda x: html.escape(str(x))
    ledger = pd.DataFrame(evidence)[['id', 'claim', 'numerator', 'denominator', 'percent', 'boundary']].copy()
    ledger['percent'] = ledger['percent'].map(lambda x: f'{x:.2f}%')
    parts = ['''<!doctype html><html><head><meta charset="utf-8"><title>Beauty: evidence to research</title>
<style>body{font:16px/1.6 system-ui;max-width:1150px;margin:45px auto;padding:0 24px;color:#182b3a;background:#fafbfd}h1,h2{line-height:1.2}section{background:white;padding:25px;margin:22px 0;border:1px solid #dbe3eb;border-radius:12px}table{border-collapse:collapse;width:100%;font-size:13px}td,th{text-align:left;border-bottom:1px solid #dde4ea;padding:9px;vertical-align:top}img{max-width:100%}a{color:#175fc0}.note{background:#eef4fc;padding:16px}code{overflow-wrap:anywhere}</style></head><body>
<h1>Beauty: from evidence to a testable research question</h1>
<p>EDA tools → evidence ledger → 5 Whys → provisional Good Question Cards → pilot decision.</p>
<p><a href="../sephora/report.html">Sephora integration and evaluation without new annotation</a></p>
<p class="note">Executed locally without LLM/API calls. Statistics are observations; 5 Whys explanations stop at unknowns; proposed model experiments have not been run. Customer fit and commercial uplift remain unmeasured.</p>
<section><h2>1. EDA and provenance</h2><p>Full-file descriptive summaries; seeded samples for expensive visual tools. No customer demographic or fit labels are inferred from ratings.</p>
<p><a href="../beauty_eda/report.html">Catalog EDA</a> · <a href="../beauty_reviews/report.html">Review EDA</a> · <a href="sweetviz.html">Sweetviz (2,000 products)</a> · <a href="tool_execution.json">Tool execution scopes</a> · <a href="provenance.json">Input hashes and versions</a></p>
<img src="matrix_plot.png" alt="Missingness in a uniform sample of 2000 products"><p>Sample visualization; the ledger below contains exact population counts.</p>
<img src="availability_funnel.png" alt="Exploratory correlation funnel for price availability"><p>Availability correlations are descriptive and cannot identify why fields are missing.</p></section>
<section><h2>2. Evidence ledger</h2>''', ledger.to_html(index=False, escape=True), '</section><section><h2>3. Evidence-backed 5 Whys</h2>']
    for chain in chains:
        parts.append(f"<h3>{esc(chain['id'])}: {esc(chain['problem'])}</h3><p>Evidence: {esc(', '.join(chain['evidence']))}</p><ol>")
        for step in chain['steps']:
            parts.append(f"<li><b>{esc(step['why'])}</b> {esc(step['answer'])} <i>[{esc(step['status'])}]</i></li>")
        parts.append('</ol>')
        for key in ['root_cause', 'countermeasure', 'reverse_check', 'confidence']:
            parts.append(f"<p><b>{esc(key.replace('_',' ').title())}:</b> {esc(chain[key])}</p>")
    parts.append('</section><section><h2>4. Ranked question candidates</h2><p>Planning scores only: importance, feasibility, falsifiability, evidence leverage and downside learning, each 1–5. Originality is unresolved; these are provisional data-grounded designs.</p>')
    parts.append(pd.DataFrame([{'ID': q['id'], 'Question': q['question'], **q['scores'], 'Total /25': q['planning_total'], 'Decision': q['decision']} for q in questions]).to_html(index=False))
    parts.append('</section><section><h2>5. Good Question Cards and two-week pilots</h2>')
    for card in cards:
        parts.append(f"<h3>{esc(card['id'])}: {esc(card['working_title'])}</h3>")
        for key, value in card.items():
            if key not in ['id', 'working_title']:
                rendered = '<ul>' + ''.join(f'<li>{esc(s)}</li>' for s in value) + '</ul>' if isinstance(value, list) else esc(value)
                parts.append(f"<p><b>{esc(key.replace('_',' ').title())}:</b> {rendered}</p>")
    parts.append('''</section><section><h2>6. What is needed next</h2><ol><li>Human annotation and agreement checks for explicit context, aspects, preference mismatch, defects and logistics.</li><li>A literature audit before claiming novelty.</li><li>Prospective shopper needs and independent fit judgments before evaluating customer–product fit.</li><li>Merchant actions and outcomes to measure conversion, margin or service impact.</li></ol><p>A target review must never be both the source of a purported pre-purchase need and independent ground truth for its own prediction. Keep product families, duplicates and development/test data separated. Validate variant mappings and avoid future listing aggregates in historical prediction.</p></section>
<p><a href="evidence_ledger.csv">Evidence CSV</a> · <a href="five_whys.md">5 Whys Markdown</a> · <a href="research_questions.md">Questions and pilots Markdown</a></p></body></html>''')
    (OUT / 'report.html').write_text('\n'.join(parts))
    return OUT / 'report.html'


def main():
    data = load_data()
    run_eda(data)
    evidence = build_evidence(data)
    chains = build_whys(evidence)
    questions, cards = build_questions()
    report = write_report(evidence, chains, questions, cards)
    print(f'Created {report}')


if __name__ == '__main__':
    main()
