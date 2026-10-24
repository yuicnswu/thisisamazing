"""Join full Beauty reviews to the existing catalog profile; no API requests."""
import argparse
import collections
import hashlib
import html
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd


def is_empty(value):
    return value is None or (isinstance(value, str) and not value.strip()) or (isinstance(value, (list, dict)) and not value)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--reviews', default=str(Path.home()/'Downloads/All_Beauty.jsonl'))
    parser.add_argument('--catalog', default='output/beauty_eda/products_profile.csv')
    parser.add_argument('--output', default='output/beauty_reviews')
    args = parser.parse_args()
    source, catalog_path, out = Path(args.reviews), Path(args.catalog), Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    fields = collections.defaultdict(lambda: {'present': 0, 'null': 0, 'empty': 0, 'types': collections.Counter()})
    rows, errors, blank_lines = [], [], 0
    digest = hashlib.sha256()
    canonical_hashes = collections.Counter()
    for lineno, line in enumerate(source.open('rb'), 1):
        digest.update(line)
        if not line.strip():
            blank_lines += 1
            continue
        try:
            record = json.loads(line)
            if not isinstance(record, dict):
                raise ValueError('Record is not a JSON object')
        except Exception as exc:
            errors.append({'source_line': lineno, 'error': str(exc)})
            continue
        for key, value in record.items():
            field = fields[key]
            field['present'] += 1
            field['types'][type(value).__name__] += 1
            if value is None:
                field['null'] += 1
            elif is_empty(value):
                field['empty'] += 1
        fingerprint = hashlib.sha256(json.dumps(record, sort_keys=True).encode()).hexdigest()
        canonical_hashes[fingerprint] += 1
        text = record.get('text') or ''
        rows.append({
            'review_source_line': lineno,
            'parent_asin': record.get('parent_asin'),
            'asin': record.get('asin'),
            'user_id': record.get('user_id'),
            'review_rating': record.get('rating'),
            'review_title': record.get('title'),
            'review_text': text,
            'timestamp_ms': record.get('timestamp'),
            'helpful_vote': record.get('helpful_vote'),
            'verified_purchase': record.get('verified_purchase'),
            'review_image_count': len(record.get('images') or []),
            'text_chars': len(text),
            'record_sha256': fingerprint,
        })
    frame = pd.DataFrame(rows)
    del rows
    n = len(frame)
    for col in ['review_rating', 'timestamp_ms', 'helpful_vote']:
        frame[col] = pd.to_numeric(frame[col], errors='coerce')
    frame['review_datetime_utc'] = pd.to_datetime(frame.timestamp_ms, unit='ms', utc=True, errors='coerce')
    frame['exact_duplicate'] = frame.duplicated('record_sha256', keep='first')
    frame['has_text'] = frame.review_text.str.strip().ne('')
    # These are text-screening flags, never inferred needs, traits or fit labels.
    frame['context_phrase_flag'] = frame.review_text.str.contains(r'\b(?:i have|i wanted|i needed|i was looking|for my|my hair|my skin)\b', case=False, regex=True)
    frame['tradeoff_phrase_flag'] = frame.review_text.str.contains(r'\b(?:but|however|although|except|wish|prefer)\b', case=False, regex=True)
    catalog = pd.read_csv(catalog_path)
    if catalog.parent_asin.isna().any() or not catalog.parent_asin.is_unique:
        raise ValueError('Catalog parent_asin must be nonmissing and unique for a many-to-one join')
    selected = ['parent_asin', 'title', 'brand', 'store', 'price', 'average_rating', 'rating_number', 'segment_heuristic', 'has_description', 'has_features', 'details_count', 'image_count']
    catalog = catalog[selected].rename(columns={c: 'listing_' + c for c in selected if c != 'parent_asin'})
    joined = frame.merge(catalog, on='parent_asin', how='left', validate='many_to_one', indicator='catalog_join', sort=False)
    assert len(joined) == n, 'Join inflated the review table'
    joined['catalog_match'] = joined.catalog_join.eq('both')
    joined = joined.drop(columns='catalog_join')
    joined.to_parquet(out / 'reviews_with_catalog.parquet', index=False, compression='zstd')
    clean = joined.loc[~joined.exact_duplicate].copy()
    users = clean.dropna(subset=['user_id']).groupby('user_id').agg(
        collected_reviews=('parent_asin', 'size'), distinct_products=('parent_asin', 'nunique'),
        mean_observed_rating=('review_rating', 'mean'), first_review_utc=('review_datetime_utc', 'min'),
        last_review_utc=('review_datetime_utc', 'max'))
    users.to_parquet(out / 'reviewer_history_profile.parquet', compression='zstd')
    products = clean.dropna(subset=['parent_asin']).groupby('parent_asin').agg(
        collected_reviews=('review_rating', 'size'), unique_reviewers=('user_id', 'nunique'),
        collected_mean_rating=('review_rating', 'mean'), collected_median_rating=('review_rating', 'median'),
        low_rating_reviews=('review_rating', lambda x: int(x.le(2).sum())),
        high_rating_reviews=('review_rating', lambda x: int(x.ge(4).sum())),
        nonempty_text_reviews=('has_text', 'sum'), median_text_chars=('text_chars', 'median'),
        verified_purchase_fraction=('verified_purchase', 'mean'), first_review_utc=('review_datetime_utc', 'min'),
        last_review_utc=('review_datetime_utc', 'max'))
    products = catalog.merge(products.reset_index(), on='parent_asin', how='outer', validate='one_to_one')
    products.to_csv(out / 'product_review_profile.csv', index=False)
    candidates = products.loc[products.collected_reviews.ge(20) & products.low_rating_reviews.ge(3) & products.high_rating_reviews.ge(3)].sort_values('collected_reviews', ascending=False)
    candidates.to_csv(out / 'mixed_experience_product_candidates.csv', index=False)
    unmatched = joined.loc[~joined.catalog_match, ['parent_asin']].value_counts().rename('reviews').reset_index()
    unmatched.to_csv(out / 'unmatched_product_ids.csv', index=False)
    pd.DataFrame(errors, columns=['source_line', 'error']).to_csv(out / 'parse_errors.csv', index=False)
    quality = pd.DataFrame([{'field': key, 'present': data['present'], 'absent': n-data['present'], 'null': data['null'], 'empty_non_null': data['empty'], 'usable_pct': (data['present']-data['null']-data['empty'])/n*100, 'types': json.dumps(data['types'])} for key, data in fields.items()])
    quality.to_csv(out / 'review_field_quality.csv', index=False)
    clean[['review_rating','helpful_vote','text_chars','review_image_count']].describe(percentiles=[.01,.25,.5,.75,.9,.95,.99]).T.to_csv(out / 'review_numeric_summary.csv')
    rating_table = clean.groupby('review_rating', dropna=False).agg(reviews=('parent_asin','size'), median_text_chars=('text_chars','median'), verified_purchase_fraction=('verified_purchase','mean'))
    rating_table.to_csv(out / 'rating_distribution.csv')
    monthly = clean.dropna(subset=['review_datetime_utc']).groupby(clean.review_datetime_utc.dt.strftime('%Y-%m')).agg(reviews=('parent_asin', 'size'), mean_rating=('review_rating', 'mean'))
    monthly.to_csv(out / 'monthly_review_activity.csv')
    user_distribution = users.distinct_products.value_counts().sort_index().rename_axis('distinct_products').reset_index(name='reviewers')
    user_distribution.to_csv(out / 'reviewer_history_distribution.csv', index=False)
    text_norm = clean.loc[clean.has_text, 'review_text'].str.casefold().str.replace(r'\s+', ' ', regex=True).str.strip()
    repeated = text_norm.value_counts()
    pd.DataFrame({'normalized_review_text': repeated[repeated.gt(1)].index, 'records': repeated[repeated.gt(1)].values}).head(100).to_csv(out / 'repeated_text_examples.csv', index=False)
    # Balanced annotation seed is a convenience sample, not a representative test set.
    eligible = clean.loc[clean.catalog_match & clean.text_chars.ge(80)]
    sample = pd.concat([group.sample(min(40, len(group)), random_state=42) for _, group in eligible.groupby('review_rating')]).sort_values(['review_rating', 'review_source_line'])
    sample = sample[['review_source_line','parent_asin','asin','review_rating','listing_title','review_title','review_text','context_phrase_flag','tradeoff_phrase_flag']].copy()
    for col in ['annotated_use_case_span','annotated_requirement_span','annotated_preference_span','annotated_positive_aspect_span','annotated_negative_aspect_span','annotation_uncertainty']:
        sample[col] = ''
    sample.to_csv(out / 'annotation_seed_200.csv', index=False)
    matched_parent_ids = clean.loc[clean.catalog_match, 'parent_asin'].nunique()
    pair_sizes = clean.groupby(['user_id', 'parent_asin'], dropna=False).size()
    summary = {
        'review_source': str(source.resolve()), 'review_source_bytes': source.stat().st_size,
        'review_source_sha256': digest.hexdigest(), 'catalog_profile_source': str(catalog_path.resolve()),
        'catalog_profile_sha256': hashlib.sha256(catalog_path.read_bytes()).hexdigest(),
        'raw_review_rows': n, 'blank_lines': blank_lines, 'parse_errors': len(errors),
        'exact_duplicate_excess': int(frame.exact_duplicate.sum()), 'deduplicated_reviews': len(clean),
        'joined_review_rows': len(joined), 'catalog_matched_review_rows': int(joined.catalog_match.sum()),
        'catalog_match_pct': float(joined.catalog_match.mean()*100),
        'unique_reviewed_parent_products': int(clean.parent_asin.nunique()), 'catalog_products': len(catalog),
        'matched_catalog_products_with_reviews': int(matched_parent_ids),
        'catalog_products_without_reviews': int(len(catalog)-matched_parent_ids),
        'unique_reviewers': len(users), 'reviewers_one_distinct_product': int(users.distinct_products.eq(1).sum()),
        'reviewers_at_least_2_distinct_products': int(users.distinct_products.ge(2).sum()),
        'reviewers_at_least_5_distinct_products': int(users.distinct_products.ge(5).sum()),
        'median_distinct_products_per_reviewer': float(users.distinct_products.median()),
        'repeated_user_parent_pairs': int(pair_sizes.gt(1).sum()),
        'distinct_variant_asins': int(clean.asin.nunique()),
        'variant_asin_differs_from_parent_rows': int((clean.asin != clean.parent_asin).sum()),
        'invalid_or_missing_review_rating': int((~clean.review_rating.between(1,5)).sum()),
        'noninteger_review_rating': int(clean.review_rating.mod(1).ne(0).sum()),
        'missing_user_ids': int(clean.user_id.isna().sum()), 'missing_parent_ids': int(clean.parent_asin.isna().sum()),
        'invalid_or_missing_timestamp': int(clean.review_datetime_utc.isna().sum()),
        'verified_purchase_pct': float(clean.verified_purchase.mean()*100),
        'nonempty_review_text_pct': float(clean.has_text.mean()*100),
        'median_review_text_chars': float(clean.text_chars.median()),
        'mean_review_rating': float(clean.review_rating.mean()),
        'reviews_with_images': int(clean.review_image_count.gt(0).sum()),
        'reviews_with_helpful_votes': int(clean.helpful_vote.gt(0).sum()),
        'review_date_min_utc': str(clean.review_datetime_utc.min()), 'review_date_max_utc': str(clean.review_datetime_utc.max()),
        'repeated_normalized_nonempty_text_groups': int(repeated.gt(1).sum()),
        'repeated_normalized_nonempty_text_excess': int((repeated-1).clip(lower=0).sum()),
        'context_phrase_flag_rows': int(clean.context_phrase_flag.sum()),
        'tradeoff_phrase_flag_rows': int(clean.tradeoff_phrase_flag.sum()),
        'mixed_experience_product_candidates': len(candidates), 'annotation_seed_rows': len(sample),
    }
    (out / 'summary.json').write_text(json.dumps(summary, indent=2))
    write_report(out, summary, quality, rating_table, users, products, candidates, monthly)
    print(json.dumps(summary, indent=2))


def write_report(out, s, quality, ratings, users, products, candidates, monthly):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'figure.dpi':140,'axes.spines.top':False,'axes.spines.right':False})
    charts=[]
    def save(name,title,draw,caption):
        fig,ax=plt.subplots(figsize=(10,5)); draw(ax); ax.set_title(title,loc='left',fontweight='bold',pad=14); fig.tight_layout(); fig.savefig(out/f'{name}.png'); plt.close(fig); charts.append((name,title,caption))
    save('01_ratings','Ratings in the collected review file',lambda ax: (ax.bar(ratings.index,ratings.reviews,color='#287b8e'),ax.set_xlabel('Review rating'),ax.set_ylabel('Reviews')),'Exact duplicate records removed. This distribution is not the complete Amazon ratings population.')
    def hist(ax):
        values=users.distinct_products.clip(upper=6).value_counts().sort_index(); ax.bar(values.index,values,color='#287b8e'); ax.set_xticks(range(1,7),['1','2','3','4','5','6+']); ax.set_yscale('log'); ax.set_xlabel('Distinct products reviewed within this file'); ax.set_ylabel('Reviewers (log scale)')
    save('02_histories','Available reviewer histories are sparse',hist,'Counts are restricted to this category and this collection; one product here does not mean one Amazon purchase overall.')
    def exposure(ax):
        vals=products.collected_reviews.dropna(); ax.hist(np.log10(1+vals),bins=40,color='#287b8e'); ax.set_xlabel('log10(1 + collected reviews per product)'); ax.set_ylabel('Products')
    save('03_product_review_counts','Collected review counts per product',exposure,'Counts are calculated from this file, independently of listing rating_number. They are not sales or exposure measures.')
    def activity(ax):
        yearly=monthly.copy(); yearly['year']=yearly.index.str[:4]; yearly=yearly.groupby('year').reviews.sum(); ax.bar(yearly.index,yearly.values,color='#287b8e'); ax.tick_params(axis='x',rotation=60); ax.set_xlabel('Review year (UTC)'); ax.set_ylabel('Collected reviews')
    save('04_activity','Review activity by year',activity,'Historical review timestamps do not date the listing snapshot and do not establish sales trends.')
    def complete(ax):
        v=quality.set_index('field').usable_pct.sort_values(); ax.barh(v.index,v.values,color='#287b8e'); ax.set_xlabel('Nonempty records (%)')
    save('05_review_coverage','Review field coverage',complete,'Nulls, blank strings and empty image lists are unavailable. Numeric zeros and False remain valid values.')
    def html_table(df): return df.to_html(border=0,float_format=lambda x:f'{x:,.3f}',escape=True)
    one=100*s['reviewers_one_distinct_product']/s['unique_reviewers']
    overview=f'''<ul><li><strong>{s['raw_review_rows']:,} review records</strong> and {s['unique_reviewers']:,} distinct reviewers.</li><li>{s['catalog_match_pct']:.2f}% of review rows join to the catalog on parent_asin without row multiplication.</li><li>{s['matched_catalog_products_with_reviews']:,} catalog products have collected reviews; {s['catalog_products_without_reviews']:,} have none.</li><li>{one:.1f}% of reviewers have only one distinct product in this file. Only {s['reviewers_at_least_5_distinct_products']:,} have at least five.</li><li>{s['verified_purchase_pct']:.1f}% of collected reviews are marked verified purchase; that flag is not a guarantee of review truthfulness.</li><li>{s['mixed_experience_product_candidates']:,} products have at least 20 collected reviews, including at least 3 low (1-2) and 3 high (4-5) ratings. These are candidates for manual investigation, not proven preference conflicts.</li></ul>'''
    sources=f'''<p>Reviews: {html.escape(s['review_source'])}<br>SHA-256: <code>{s['review_source_sha256']}</code><br>Catalog profile: {html.escape(s['catalog_profile_source'])}</p><p>The original files remain unchanged. The joined Parquet retains every parsed review, original source-line references and exact-duplicate flags. Summary statistics exclude exact duplicates only; repeated generic text is reported but not automatically deleted.</p>'''
    limitations='''<ul><li><strong>No pre-purchase intent labels:</strong> reviews describe selected post-purchase experiences. Do not turn a complaint or a 5-star rating into a complete customer profile.</li><li><strong>No rejected alternatives:</strong> a reviewed product is observed; preferences among unpurchased candidates are not.</li><li><strong>Sparse histories:</strong> customer-history personalization must report the eligible subset and cannot generalize to all reviewers.</li><li><strong>Variant mismatch:</strong> parent-level listings may combine sizes, colors and formulations. Preserve review asin and manually verify variant-dependent claims.</li><li><strong>No reliable temporal listing snapshots:</strong> review timestamps cannot establish what listing text was visible before purchase.</li><li><strong>Collected reviews versus rating_number:</strong> these populations can differ and should not be forced to match. Aggregate rating fields must be removed or time-aligned when used as predictors of held-out ratings.</li><li><strong>Existing inferred product segments:</strong> keyword-derived catalog categories remain unvalidated and retain known ambiguous-word errors. They are not ground-truth categories.</li></ul>'''
    protocol='''<ol><li>Start with mixed-experience candidate products and inspect actual positive and negative aspects. Differences may reflect shipping, defects, sellers or authenticity concerns rather than customer needs.</li><li>Use annotation_seed_200.csv to mark only explicit review spans: situation, requirement, preference and positive/negative aspects. Leave unstated needs unknown. The seed is balanced by rating and is not representative of the full corpus.</li><li>Keep the target outcome review out of the model input. If needs are extracted from that same review, label the task retrospective reconstruction, not prospective customer-fit prediction.</li><li>For history-based tasks, build inputs only from earlier reviews; exclude target-product reviews and duplicated product families. Separate reviewer groups for cold-user evaluation where appropriate.</li><li>Group related variants, duplicate listings and transformed examples before development/calibration/test splitting. Random review-row splitting is not an adequate default.</li><li>Collect genuine shopper requests and independent preference judgments to establish perceived fit. Actual-use follow-up is needed for experienced fit. Do not use an LLM as the sole generator and evaluator.</li></ol>'''
    counts=pd.DataFrame([{'check':k,'value':s[k]} for k in ['parse_errors','blank_lines','exact_duplicate_excess','invalid_or_missing_review_rating','noninteger_review_rating','missing_user_ids','missing_parent_ids','invalid_or_missing_timestamp','repeated_user_parent_pairs','repeated_normalized_nonempty_text_groups','repeated_normalized_nonempty_text_excess','variant_asin_differs_from_parent_rows']])
    numerical=pd.DataFrame([{'measure':'Earliest review (UTC)','value':s['review_date_min_utc']},{'measure':'Latest review (UTC)','value':s['review_date_max_utc']},{'measure':'Mean collected review rating','value':s['mean_review_rating']},{'measure':'Median review-text characters','value':s['median_review_text_chars']},{'measure':'Reviews containing customer-context screening phrases','value':s['context_phrase_flag_rows']},{'measure':'Reviews containing trade-off screening phrases','value':s['tradeoff_phrase_flag_rows']}])
    examples=candidates[['parent_asin','listing_title','collected_reviews','low_rating_reviews','high_rating_reviews','collected_mean_rating']].head(15)
    sections=[('What was added',overview),('Sources and join contract',sources),('Integrity and duplicate audit',html_table(counts)),('Review field quality',html_table(quality.drop(columns='types').set_index('field'))),('Rating distribution',html_table(ratings)),('Text and dates',html_table(numerical)+'<p>Phrase flags are transparent keyword screening only. They are not validated intent, emotion, demographic or satisfaction labels.</p>'),('Candidate products for customer-fit research',html_table(examples)+'<p>Thresholds are exploratory screening choices. Mixed star ratings alone do not establish different customer preferences.</p>'),('Research limitations',limitations),('Evaluation and annotation protocol',protocol),('Reproduce', '<p>Run <code>.venv/bin/python scripts/add_beauty_reviews.py</code> from the workspace. Full-file counts use all parsed records. The only sampled artifact is the human annotation seed (up to 40 reviews per rating; random seed 42).</p>')]
    body=''.join(f'<section><h2>{html.escape(title)}</h2>{content}</section>' for title,content in sections)
    body+=''.join(f'<figure><h3>{html.escape(title)}</h3><img src="{name}.png" alt="{html.escape(title)}"><figcaption>{html.escape(caption)}</figcaption></figure>' for name,title,caption in charts)
    exports=''.join(f'<li><a href="{p.name}">{p.name}</a></li>' for p in sorted(out.iterdir()) if p.suffix in ['.json','.csv','.parquet'])
    css='body{font:16px/1.6 system-ui,sans-serif;color:#233343;background:#f4f7f9;margin:0}main{max-width:1180px;margin:auto;padding:40px}h1{font-size:38px;line-height:1.15}h2{color:#18576a}section,figure{background:white;border:1px solid #dce5e9;border-radius:12px;padding:24px;margin:22px 0;overflow:auto}table{border-collapse:collapse;font-size:13px;width:100%}th,td{text-align:left;padding:9px;border-bottom:1px solid #e6ecef}th{background:#edf4f6}img{max-width:100%;height:auto}figcaption{font-size:14px;color:#556979}code{overflow-wrap:anywhere}'
    (out/'report.html').write_text(f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>All Beauty — Reviews and Catalog</title><style>{css}</style><main><p><a href="../beauty_eda/report.html">Original catalog EDA</a></p><h1>All Beauty: Reviews + Product Listings</h1>'+body+'<section><h2>Data exports</h2><ul>'+exports+'</ul></section></main></html>')


if __name__ == '__main__':
    main()
