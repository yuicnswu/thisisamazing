"""Register Sephora CSV snapshots and audit existing-label evaluation feasibility.
No new labels, model calls, or cross-retailer entity matching.
"""
from pathlib import Path
import hashlib, json, html, os
os.environ.setdefault('MPLBACKEND','Agg')
os.environ.setdefault('MPLCONFIGDIR','/private/tmp/sephora-mpl')
import pandas as pd
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/sephora'; SOURCE=Path(os.environ.get('SEPHORA_SOURCE_DIR', str(Path.home()/'Downloads/archive')))

def dump(path,obj): path.write_text(json.dumps(obj,indent=2,default=str)+'\n')

def main():
 OUT.mkdir(parents=True,exist_ok=True)
 sources=[];frames=[]
 files=['product_info.csv','reviews_0-250.csv','reviews_250-500.csv','reviews_500-750.csv','reviews_750-1250.csv','reviews_1250-end.csv']
 for name in files:
  path=SOURCE/name
  frame=pd.read_csv(path,dtype='string',keep_default_na=True)
  sources.append(dict(path=str(path),bytes=path.stat().st_size,sha256=hashlib.file_digest(path.open('rb'),'sha256').hexdigest(),rows=len(frame),columns=list(frame.columns)))
  if name=='product_info.csv': products=frame
  else:
   frame=frame.drop(columns=[c for c in frame if c.startswith('Unnamed:')])
   frame['source_file']=name;frame['source_record']=range(1,len(frame)+1)
   frames.append(frame)
 r=pd.concat(frames,ignore_index=True);del frames
 assert products.product_id.notna().all() and products.product_id.is_unique,'Invalid product join keys'
 content=[c for c in r if c not in ['source_file','source_record']]
 r['exact_duplicate']=r.duplicated(content,keep='first')
 for col in ['rating','is_recommended','helpfulness','price_usd','total_feedback_count','total_neg_feedback_count','total_pos_feedback_count']:
  r[col]=pd.to_numeric(r[col],errors='coerce')
 r['review_date']=pd.to_datetime(r.submission_time,errors='coerce',utc=True)
 for col in ['rating','reviews','price_usd','loves_count']:
  products[col]=pd.to_numeric(products[col],errors='coerce')
 renamed=products.rename(columns={c:'listing_'+c for c in products if c!='product_id'})
 joined=r.merge(renamed,on='product_id',how='left',validate='many_to_one',indicator=True)
 joined['catalog_match']=joined.pop('_merge').eq('both')
 assert len(joined)==len(r)
 joined.to_parquet(OUT/'reviews_with_products.parquet',index=False)
 products.to_parquet(OUT/'products.parquet',index=False)
 c=joined.loc[~joined.exact_duplicate].copy()
 valid=c.is_recommended.isin([0,1]);dates=c.review_date.notna()
 # Date-only timestamps: same-date events must not become earlier history.
 usable=c.loc[c.author_id.notna() & c.product_id.notna() & dates].copy()
 earliest=usable.groupby('author_id').review_date.transform('min')
 usable['has_strictly_earlier_review']=usable.review_date.gt(earliest)
 # A separate product needs an earlier review of a different product, not repeat feedback.
 first=usable.groupby(['author_id','product_id'],as_index=False).review_date.min()
 first['first_any_product']=first.groupby('author_id').review_date.transform('min')
 first['has_earlier_other_product']=first.review_date.gt(first.first_any_product)
 eligible_pairs=first.loc[first.has_earlier_other_product,['author_id','product_id']]
 usable=usable.merge(eligible_pairs.assign(earlier_other=True),on=['author_id','product_id'],how='left',validate='many_to_one')
 # For subsequent reviews of the earliest product, an intervening different product can be earlier too.
 second_distinct=(first.sort_values('review_date').groupby('author_id').nth(1).set_index('author_id').review_date)
 other_first=usable.author_id.map(second_distinct)
 usable['has_strictly_earlier_other_product']=usable.earlier_other.fillna(False) | usable.review_date.gt(other_first)
 usable[['source_file','source_record','author_id','product_id','review_date','has_strictly_earlier_review','has_strictly_earlier_other_product']].to_parquet(OUT/'temporal_eligibility.parquet',index=False)
 h=c.groupby('author_id').agg(review_records=('product_id','size'),distinct_products=('product_id','nunique'),first_review=('review_date','min'),last_review=('review_date','max'))
 h.to_parquet(OUT/'reviewer_history_profile.parquet')
 q=[]
 for scope,f in [('products',products),('deduplicated_reviews',c)]:
  for col in f:
   if col.startswith('listing_'):continue
   missing=f[col].isna() | f[col].astype('string').str.strip().eq('').fillna(False)
   q.append(dict(scope=scope,field=col,rows=len(f),missing=int(missing.sum()),missing_pct=float(missing.mean()*100)))
 pd.DataFrame(q).to_csv(OUT/'field_quality.csv',index=False)
 rating=c.rating.value_counts(dropna=False).sort_index();rating.to_csv(OUT/'rating_distribution.csv')
 rec=c.is_recommended.value_counts(dropna=False);rec.to_csv(OUT/'recommendation_distribution.csv')
 skin=c.groupby('skin_type',dropna=False).agg(reviews=('product_id','size'),mean_rating=('rating','mean'),recommendation_observed=('is_recommended','count'),recommendation_mean=('is_recommended','mean'))
 skin.to_csv(OUT/'skin_type_profile.csv')
 cross=pd.crosstab(c.rating,c.is_recommended,dropna=False);cross.to_csv(OUT/'rating_recommendation_crosstab.csv')
 p=c.groupby('product_id').agg(collected_reviews=('product_id','size'),unique_reviewers=('author_id','nunique'),mean_review_rating=('rating','mean'),recommendation_labels=('is_recommended','count'),recommendation_mean=('is_recommended','mean'))
 p.to_csv(OUT/'product_review_profile.csv')
 stats=dict(products=len(products),raw_reviews=len(r),exact_duplicate_excess=int(r.exact_duplicate.sum()),deduplicated_reviews=len(c),
  raw_matched_reviews=int(joined.catalog_match.sum()),raw_unmatched_reviews=int((~joined.catalog_match).sum()),
  reviewed_products=int(c.product_id.nunique()),unique_reviewers=len(h),reviewers_one_product=int(h.distinct_products.eq(1).sum()),reviewers_at_least_2_products=int(h.distinct_products.ge(2).sum()),reviewers_at_least_5_products=int(h.distinct_products.ge(5).sum()),
  recommendation_labels=int(valid.sum()),recommendation_missing=int(c.is_recommended.isna().sum()),recommendation_invalid_nonmissing=int((c.is_recommended.notna() & ~valid).sum()),
  recommendation_positive=int(c.is_recommended.eq(1).sum()),recommendation_negative=int(c.is_recommended.eq(0).sum()),
  skin_type_observed=int(c.skin_type.notna().sum()),valid_recommendation_with_skin_type=int((valid & c.skin_type.notna()).sum()),
  invalid_or_missing_dates=int((~dates).sum()),invalid_or_missing_ratings=int((~c.rating.isin([1,2,3,4,5])).sum()),
  missing_author_ids=int(c.author_id.isna().sum()),missing_product_ids=int(c.product_id.isna().sum()),
  date_min=c.review_date.min(),date_max=c.review_date.max(),
  labeled_reviews_with_strictly_earlier_history=int((usable.has_strictly_earlier_review & usable.is_recommended.isin([0,1])).sum()),
  labeled_reviews_with_strictly_earlier_other_product=int((usable.has_strictly_earlier_other_product & usable.is_recommended.isin([0,1])).sum()))
 dump(OUT/'summary.json',stats)
 manifest=dict(name='Sephora products and skincare reviews — supplied local snapshots',sources=sources,join=dict(key='product_id',cardinality='many reviews to one product',raw_matches=stats['raw_matched_reviews']),duplicate_policy='Preserve and flag exact content duplicates excluding source index; analyses remove flagged excess rows.',outputs=dict(report=str(OUT/'report.html'),joined_reviews=str(OUT/'reviews_with_products.parquet')),limitations=['Customer attributes are self-reported snapshots, not independently verified or necessarily historical.','Recommendation labels are retrospective opinions, not purchase/return records or prospective suitability.','Product snapshot effective dates are unknown; aggregate ratings can leak future outcomes.','Sephora IDs are not Amazon IDs; sources remain separate.','Temporal eligibility is a data audit, not a frozen benchmark split.','No new human annotations or model evaluations were performed.'],reproduce='.venv/bin/python scripts/add_sephora.py')
 dump(ROOT/'data/sephora_sources.json',manifest)
 fig,axes=plt.subplots(1,2,figsize=(12,4))
 rating.plot.bar(ax=axes[0],color='#326b9b',title='Deduplicated review ratings');axes[0].set_ylabel('Reviews')
 c.skin_type.fillna('Missing').value_counts().plot.bar(ax=axes[1],color='#538d7c',title='Self-reported skin type');axes[1].set_ylabel('Reviews')
 fig.tight_layout();fig.savefig(OUT/'overview.png',dpi=150);plt.close(fig)
 protocol='''# Sephora: evaluation without new human annotation

Question: Does customer context improve prediction of an existing reviewer recommendation beyond popularity, history and non-LLM text baselines?

1. Use only observed binary `is_recommended` labels; never impute missing labels from ratings. Report selection and class balance.
2. Freeze a chronological development/test cutoff after inspecting coverage, with all same-day reviews on the same side. For history, use strictly earlier dates and exclude target-product histories in the stricter condition. Temporal eligibility counts are not final test sizes.
3. Hide the target review text, title, rating, recommendation and feedback fields. Inputs may include product descriptions and earlier review evidence. Audit prior text duplicates across splits. Current customer profiles may not have been recorded before the target: disclose that limitation or omit them from prospective claims.
4. Exclude listing aggregate rating/review/loves counts from historical prediction. Price, ingredients and product highlights are undated snapshot attributes: test their removal and avoid asserting fully time-valid evaluation.
5. Compare training-period majority/popularity, structured customer/product and text-embedding baselines against the same LLM with no profile, observed profile and shuffled profile. Keep labels and target reviews out of prompts.
6. Report AUROC, PR-AUC with positive-class convention, balanced accuracy, macro-F1, log loss/calibration, customer-cluster bootstrap intervals, cost and latency. Lock thresholds/prompts on development data. Test held-out products separately from chronological known-product evaluation.
7. Claim prediction of reported recommendations only. Missing exposure sets mean unreviewed products are not negatives. No causal customer-fit, safety, revenue or conversion claim follows from this audit.

No model experiment has been run. Existing reviews and labels supply evaluation outcomes; no human annotation is requested.
'''
 (OUT/'evaluation_protocol.md').write_text(protocol)
 rows=pd.DataFrame([{'Metric':k.replace('_',' '),'Value':str(v)} for k,v in stats.items()])
 page='''<!doctype html><html><head><meta charset="utf-8"><title>Sephora integration</title><style>body{font:16px/1.6 system-ui;max-width:1100px;margin:40px auto;padding:0 22px;color:#203044}table{border-collapse:collapse;width:100%;font-size:14px}td,th{padding:8px;text-align:left;border-bottom:1px solid #ddd}img{width:100%}section{margin:30px 0}pre{white-space:pre-wrap;background:#f3f6fa;padding:20px}</style></head><body><h1>Sephora: products, reviews and existing preference labels</h1><p>All six supplied files integrated. Original files remain unchanged. No new annotation or LLM calls.</p><p><a href="../beauty_research_workflow/report.html">Combined research workflow</a> · <a href="summary.json">Summary JSON</a> · <a href="../../data/sephora_sources.json">Source hashes and schema</a></p><section><h2>Full-file integration audit</h2>'''+rows.to_html(index=False)+'''</section><img src="overview.png" alt="Rating and self-reported skin type distributions"><section><h2>Skin-type coverage and reported recommendations</h2><p>Unadjusted descriptive groups. Differences do not establish that skin type causes satisfaction or that a product suits a new customer.</p>'''+skin.reset_index().to_html(index=False)+'''</section><section><h2>Rating versus recommendation</h2><p>Existing outcomes can disagree; missing recommendation labels remain missing.</p>'''+cross.to_html()+'''</section><section><h2>No-annotation evaluation protocol</h2><pre>'''+html.escape(protocol)+'''</pre></section><section><h2>Scope and limits</h2><ul>'''+''.join('<li>'+html.escape(v)+'</li>' for v in manifest['limitations'])+'''</ul><p><a href="field_quality.csv">Field quality</a> · <a href="evaluation_protocol.md">Evaluation protocol</a> · <a href="product_review_profile.csv">Product review profile</a></p></section></body></html>'''
 (OUT/'report.html').write_text(page)
 # Discoverability in both regenerated and currently rendered combined report.
 workflow=ROOT/'scripts/beauty_research_workflow.py'
 text=workflow.read_text();marker='<p>EDA tools → evidence ledger → 5 Whys → provisional Good Question Cards → pilot decision.</p>'
 link='<p><a href="../sephora/report.html">Sephora integration and evaluation without new annotation</a></p>'
 if link not in text: workflow.write_text(text.replace(marker,marker+'\n'+link))
 report=ROOT/'output/beauty_research_workflow/report.html'
 if report.exists() and link not in report.read_text():report.write_text(report.read_text().replace(marker,marker+'\n'+link))
 print(json.dumps(stats,indent=2,default=str))

if __name__=='__main__':main()
