"""Full-file, deterministic EDA. No LLM calls or external data transfers."""
import argparse, collections, hashlib, html, json, math, re, unicodedata
from pathlib import Path
import numpy as np
import pandas as pd


def norm(v):
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFKC', str(v or '')).casefold()).strip()


def empty(v):
    return v is None or (isinstance(v, str) and not v.strip()) or (isinstance(v, (list, dict)) and not v)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--input',default=str(Path.home()/'Downloads/meta_All_Beauty.jsonl'))
    parser.add_argument('--output',default='output/beauty_eda')
    a=parser.parse_args(); out=Path(a.output); out.mkdir(parents=True,exist_ok=True)
    source=Path(a.input); records=[]; errors=[]; blanks=0; checksum=hashlib.sha256()
    fields=collections.defaultdict(lambda: {'present':0,'null':0,'empty_non_null':0,'types':collections.Counter()})
    attrs=collections.Counter(); attrvals=collections.defaultdict(collections.Counter); mains=collections.Counter()
    exact=collections.Counter(); rawprices=collections.Counter(); image_urls=collections.Counter()
    rows=[]
    patterns={
      'Hair extensions / wigs':r'\b(wig|wigs|weave|weft|extensions|braiding|toupee|hairpiece)\b',
      'Hair care':r'\b(shampoo|conditioner|hair oil|hair mask|scalp|hair growth|hair spray|hairspray)\b',
      'Skin care':r'\b(serum|moisturiz\w*|cleanser|sunscreen|facial|face cream|retinol|toner|acne|lotion)\b',
      'Makeup':r'\b(lipstick|lip gloss|eyeliner|eyeshadow|mascara|foundation|concealer|blush|makeup|cosmetic)\b',
      'Nail products':r'\b(nail|nails|manicure|pedicure|cuticle)\b',
      'Fragrance':r'\b(perfume|cologne|fragrance|eau de|body mist)\b',
      'Grooming / removal':r'\b(razor|shav\w*|trimmer|epilator|depilatory|waxing|beard)\b',
      'Tools / accessories':r'\b(brush|comb|mirror|dryer|straightener|curler|scissors|tweezer|headband|bonnet|clip|clips)\b',
    }
    flags={'natural':r'\bnatural\b','organic':r'\borganic\b','vegan':r'\bvegan\b','cruelty_free':r'\bcruelty[ -]?free\b','sensitive':r'\bsensitive\b','anti_aging':r'\banti[ -]?aging\b','hydration':r'\b(hydrat\w*|moisturiz\w*)\b','professional':r'\b(professional|salon)\b','multipack':r'\b(pack of|\d+[ -]?(pack|pcs|pieces)|set of)\b'}
    with source.open('rb') as f:
      for lineno,line in enumerate(f,1):
        checksum.update(line)
        if not line.strip(): blanks+=1; continue
        try:
          r=json.loads(line)
          if not isinstance(r,dict): raise ValueError('Record is not an object')
        except Exception as e: errors.append({'line':lineno,'error':str(e)}); continue
        for k,v in r.items():
          fields[k]['present']+=1; fields[k]['types'][type(v).__name__]+=1
          if v is None: fields[k]['null']+=1
          elif empty(v): fields[k]['empty_non_null']+=1
        exact[hashlib.sha256(json.dumps(r,sort_keys=True).encode()).hexdigest()]+=1
        d=r.get('details') or {}; attrs.update(d.keys())
        for k,v in d.items():
          if not empty(v): attrvals[k][str(v)]+=1
        title=r.get('title') or ''; desc=' '.join(map(str,r.get('description') or [])); feat=' '.join(map(str,r.get('features') or []))
        ims=r.get('images') or []; vids=r.get('videos') or []
        urls=[x.get('hi_res') or x.get('large') or x.get('thumb') for x in ims if isinstance(x,dict)]
        urls=[x for x in urls if x]; image_urls.update(set(urls))
        store=r.get('store'); brand=d.get('Brand'); price=r.get('price'); rawprices[type(price).__name__]+=1
        row={'source_line':lineno,'parent_asin':r.get('parent_asin'),'title':title,'title_normalized':norm(title),'store':store,'brand':str(brand).strip() if not empty(brand) else None,'manufacturer':d.get('Manufacturer'),'main_category':r.get('main_category'),'average_rating':r.get('average_rating'),'rating_number':r.get('rating_number'),'price':price,'title_chars':len(title),'title_words':len(title.split()),'description_chars':len(desc),'feature_chars':len(feat),'description_count':len(r.get('description') or []),'feature_count':len(r.get('features') or []),'image_count':len(ims),'unique_image_count':len(set(urls)),'hi_res_count':sum(bool(x.get('hi_res')) for x in ims if isinstance(x,dict)),'video_count':len(vids),'details_count':len(d),'has_price':not empty(price),'has_description':bool(desc.strip()),'has_features':bool(feat.strip()),'has_brand':not empty(brand),'has_store':not empty(store),'has_video':bool(vids),'has_hi_res':any(isinstance(x,dict) and x.get('hi_res') for x in ims),'discontinued':norm(d.get('Is Discontinued By Manufacturer')),'upc':str(d.get('UPC') or '').strip()}
        labels=[label for label,p in patterns.items() if re.search(p,title,re.I)]
        row['segment_heuristic']=labels[0] if labels else 'Unclassified'
        row['segment_matches']=' | '.join(labels); row['segment_match_count']=len(labels)
        for label,p in flags.items(): row['title_claim_'+label]=bool(re.search(p,title,re.I))
        rows.append(row); mains.update([str(r.get('main_category'))])
    df=pd.DataFrame(rows); n=len(df)
    for c in ['average_rating','rating_number','price']: df[c]=pd.to_numeric(df[c],errors='coerce')
    df['brand_normalized']=df.brand.map(norm); df['store_normalized']=df.store.map(norm)
    df['metadata_signals']=df[['has_price','has_description','has_features','has_brand','has_store','has_video','has_hi_res']].sum(axis=1)
    df.to_csv(out/'products_profile.csv',index=False)
    pd.DataFrame(errors,columns=['line','error']).to_csv(out/'parse_errors.csv',index=False)
    quality=[]
    for k,v in fields.items():
      missing=n-v['present']; usable=n-missing-v['null']-v['empty_non_null']
      quality.append({'field':k,'present':v['present'],'absent':missing,'null':v['null'],'empty_non_null':v['empty_non_null'],'usable':usable,'usable_pct':100*usable/n,'types':json.dumps(v['types'])})
    quality=pd.DataFrame(quality).sort_values('usable_pct'); quality.to_csv(out/'field_quality.csv',index=False)
    numeric=['average_rating','rating_number','price','title_chars','title_words','description_chars','feature_chars','image_count','unique_image_count','hi_res_count','video_count','details_count','metadata_signals']
    stats=df[numeric].describe(percentiles=[.01,.05,.25,.5,.75,.9,.95,.99]).T
    stats.to_csv(out/'numeric_summary.csv')
    attrtable=pd.DataFrame([{'attribute':k,'key_present':v,'nonempty':sum(attrvals[k].values()),'coverage_pct':100*sum(attrvals[k].values())/n,'unique_values':len(attrvals[k]),'top_value':attrvals[k].most_common(1)[0][0] if attrvals[k] else None} for k,v in attrs.items()]).sort_values('nonempty',ascending=False)
    attrtable.to_csv(out/'attribute_coverage.csv',index=False)
    av=[{'attribute':k,'value':v,'products':count} for k in attrs for v,count in attrvals[k].most_common(20)]
    pd.DataFrame(av).to_csv(out/'top_attribute_values.csv',index=False)
    storetable=df[df.has_store].groupby('store_normalized').agg(products=('parent_asin','size'),display_store=('store','first'),median_rating=('average_rating','median'),median_rating_count=('rating_number','median'),total_rating_count=('rating_number','sum'),priced_pct=('has_price',lambda s:100*s.mean()),median_observed_price=('price','median')).sort_values('products',ascending=False)
    storetable.to_csv(out/'stores.csv')
    brandtable=df[df.has_brand].groupby('brand_normalized').agg(products=('parent_asin','size'),display_brand=('brand','first'),median_rating=('average_rating','median'),median_rating_count=('rating_number','median'),total_rating_count=('rating_number','sum'),priced_pct=('has_price',lambda s:100*s.mean())).sort_values('products',ascending=False)
    brandtable.to_csv(out/'brands.csv')
    segments=df.groupby('segment_heuristic').agg(products=('parent_asin','size'),median_rating=('average_rating','median'),median_rating_count=('rating_number','median'),priced_pct=('has_price',lambda s:100*s.mean()),median_observed_price=('price','median'),has_description_pct=('has_description',lambda s:100*s.mean()),has_video_pct=('has_video',lambda s:100*s.mean()))
    segments['catalog_pct']=segments.products/n*100; segments=segments.sort_values('products',ascending=False); segments.to_csv(out/'segments_heuristic.csv')
    missingcompare=df.groupby('has_price').agg(products=('parent_asin','size'),median_rating=('average_rating','median'),mean_rating=('average_rating','mean'),median_rating_count=('rating_number','median'),mean_rating_count=('rating_number','mean'),median_title_chars=('title_chars','median'),description_pct=('has_description',lambda s:100*s.mean()),features_pct=('has_features',lambda s:100*s.mean()),brand_pct=('has_brand',lambda s:100*s.mean()),median_images=('image_count','median'),video_pct=('has_video',lambda s:100*s.mean()))
    missingcompare.to_csv(out/'priced_vs_unpriced.csv')
    corrcols=numeric+['has_price','has_description','has_features','has_brand','has_video']
    df[corrcols].corr(method='spearman').to_csv(out/'spearman_correlations.csv')
    availability=df[['has_price','has_description','has_features','has_brand','has_store','has_video','has_hi_res']]
    availability.corr().to_csv(out/'availability_correlations.csv')
    stop=set('the a an and or for to of with in on by from at is it this that as all new women woman men man hair inch inches pack pcs oz ounce beauty black brown white'.split())
    tokens=collections.Counter()
    for title in df.title:
      tokens.update(set(t for t in re.findall(r'[a-z][a-z-]{2,}',title.lower()) if t not in stop))
    pd.DataFrame(tokens.most_common(100),columns=['title_token','products_containing']).to_csv(out/'title_tokens.csv',index=False)
    claims=pd.DataFrame([{'title_claim':c.removeprefix('title_claim_'),'products':int(df[c].sum()),'catalog_pct':100*df[c].mean()} for c in df if c.startswith('title_claim_')]).sort_values('products',ascending=False)
    claims.to_csv(out/'title_claims.csv',index=False)
    dupt=df[df.title_normalized.ne('') & df.duplicated('title_normalized',keep=False)].sort_values('title_normalized'); dupt.to_csv(out/'duplicate_titles.csv',index=False)
    dupid=df[df.duplicated('parent_asin',keep=False)]; dupid.to_csv(out/'duplicate_ids.csv',index=False)
    upc=df[df.upc.ne('') & df.duplicated('upc',keep=False)].sort_values('upc'); upc.to_csv(out/'shared_upcs.csv',index=False)
    outcols=['parent_asin','title','brand','store','price','average_rating','rating_number','segment_heuristic']
    df.nlargest(30,'rating_number')[outcols].to_csv(out/'most_rated_products.csv',index=False)
    df.nlargest(30,'price')[outcols].to_csv(out/'highest_observed_prices.csv',index=False)
    drift=df.title.str.contains(r'leather conditioner|cow brush|cattle|livestock|mobility.{0,20}scooter|standing power body lift|sit to stand',case=False,regex=True)
    df.loc[drift,outcols].to_csv(out/'suspected_category_drift.csv',index=False)
    df[df.price.gt(0)].nsmallest(30,'price')[outcols].to_csv(out/'lowest_observed_prices.csv',index=False)
    df[df.average_rating.ge(4.5) & df.rating_number.lt(5)][outcols].head(100).to_csv(out/'high_rating_low_evidence_examples.csv',index=False)
    rc=df.rating_number.fillna(0).clip(lower=0).sort_values(ascending=False); total=rc.sum()
    quant={str(p):float(df.price.quantile(p)) for p in [.01,.05,.25,.5,.75,.9,.95,.99]}
    checks={'rating_outside_1_5':int((~df.average_rating.between(1,5)).sum()),'nonpositive_rating_number':int(df.rating_number.le(0).sum()),'noninteger_rating_number':int(df.rating_number.mod(1).ne(0).sum()),'nonpositive_observed_price':int(df.price.le(0).sum()),'invalid_parent_asin_format':int((~df.parent_asin.fillna('').str.fullmatch(r'[A-Z0-9]{10}')).sum()),'blank_titles':int(df.title.str.strip().eq('').sum()),'duplicate_id_excess':int(df.duplicated('parent_asin').sum()),'exact_duplicate_excess':sum(v-1 for v in exact.values()),'duplicate_normalized_title_excess':int(df[df.title_normalized.ne('')].duplicated('title_normalized').sum()),'products_sharing_normalized_titles':len(dupt),'products_with_duplicate_image_entries':int(df.image_count.gt(df.unique_image_count).sum()),'images_shared_across_products':sum(v>1 for v in image_urls.values()),'products_with_shared_upc':len(upc)}
    both=df.has_brand & df.has_store
    summary={'source':str(source),'source_bytes':source.stat().st_size,'sha256':checksum.hexdigest(),'rows':n,'blank_lines':blanks,'parse_errors':len(errors),'main_categories':dict(mains),'checks':checks,'unique_stores_nonempty':len(storetable),'unique_brands_nonempty':len(brandtable),'brand_store_exact_normalized_match_pct_when_both_present':float(100*(df.loc[both,'brand_normalized']==df.loc[both,'store_normalized']).mean()),'price_quantiles':quant,'rating_count_total_NOT_unique_reviews':int(total),'top_1pct_products_share_rating_counts':float(rc.head(math.ceil(n*.01)).sum()/total),'top_10pct_products_share_rating_counts':float(rc.head(math.ceil(n*.1)).sum()/total),'rating_count_le_1':int(df.rating_number.le(1).sum()),'rating_count_le_5':int(df.rating_number.le(5).sum()),'rating_count_ge_100':int(df.rating_number.ge(100).sum()),'five_star_products':int(df.average_rating.eq(5).sum()),'five_star_products_lt_5_ratings':int((df.average_rating.eq(5)&df.rating_number.lt(5)).sum()),'title_only_no_description_or_features':int((~df.has_description & ~df.has_features).sum()),'ambiguous_heuristic_segment_matches':int(df.segment_match_count.gt(1).sum()),'spearman_price_rating':float(df[['price','average_rating']].dropna().rank().corr().iloc[0,1]),'spearman_price_rating_count':float(df[['price','rating_number']].dropna().rank().corr().iloc[0,1]),'top10_store_share_all_products':float(storetable.products.head(10).sum()/n)}
    (out/'summary.json').write_text(json.dumps(summary,indent=2))
    report(summary,df,quality,stats,attrtable,storetable,brandtable,segments,missingcompare,claims,tokens,out)
    print(json.dumps(summary,indent=2))


def report(s,df,quality,stats,attrtable,stores,brands,segments,missingcompare,claims,tokens,out):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'figure.dpi':140,'axes.spines.top':False,'axes.spines.right':False,'font.size':10})
    charts=[]
    def save(name,title,draw,caption):
      fig,ax=plt.subplots(figsize=(10,5)); draw(ax); ax.set_title(title,loc='left',fontweight='bold',pad=14); fig.tight_layout(); path=out/f'{name}.png'; fig.savefig(path); plt.close(fig); charts.append((name,title,caption))
    def bars(ax,series,xlabel):
      series.iloc[::-1].plot.barh(ax=ax,color='#287b8e'); ax.set_xlabel(xlabel); ax.set_ylabel('')
    save('01_coverage','Usable field coverage',lambda ax:bars(ax,quality.set_index('field').usable_pct.sort_values(ascending=False),'Percent of all products'),'Empty lists, dictionaries, blank strings and nulls all count as unavailable. Field presence alone overstates coverage.')
    save('02_ratings','Average ratings are not equally reliable',lambda ax:ax.hist(df.average_rating,bins=np.arange(.95,5.16,.2),color='#287b8e',edgecolor='white'),'Each product has equal weight. A five-star average with one rating is weak evidence.')
    save('03_rating_counts','Long tail of rating counts',lambda ax:ax.hist(np.log10(1+df.rating_number.clip(lower=0)),bins=45,color='#287b8e'),'Horizontal axis: log10(1 + rating count). Rating counts are accumulated attention proxies, not sales.')
    save('04_price','Observed prices only (log scale)',lambda ax:ax.hist(np.log10(df.loc[df.price.gt(0),'price']),bins=45,color='#b56c34'),'Horizontal axis: log10(price). Currency is not explicit in this file; no unit-price or current-price interpretation is assumed.')
    save('05_segments','Title-derived product segments (heuristic)',lambda ax:bars(ax,segments.products,'Products'),'First matching rule assigns a primary segment; overlaps and unclassified items are retained in the CSV. This is not Amazon taxonomy.')
    save('06_stores','Largest store labels by catalog count',lambda ax:bars(ax,stores.head(15).set_index('display_store').products,'Products'),'Store labels are not verified brands, sellers or market shares. Denominator is this file only.')
    save('07_attributes','Most available structured attributes',lambda ax:bars(ax,attrtable.head(18).set_index('attribute').coverage_pct,'Percent of all products'),'Nonempty values only. Attributes are product-specific and require standardization before segmentation.')
    save('08_price_missingness','Observed-price availability by inferred segment',lambda ax:bars(ax,segments.priced_pct,'Percent with observed price'),'Price analyses are conditional on availability and product mix; missing prices must not be filled with zero.')
    def rating_evidence(ax):
      bins=pd.cut(df.rating_number,[0,1,5,20,100,1000,np.inf],labels=['1','2–5','6–20','21–100','101–1,000','>1,000']); g=df.groupby(bins,observed=True).average_rating.agg(['mean','median','count']); ax.plot(range(len(g)),g['mean'],'o-',label='Mean product rating'); ax.plot(range(len(g)),g['median'],'s--',label='Median product rating'); ax.set_xticks(range(len(g)),[f'{x}\n(n={int(c):,})' for x,c in zip(g.index,g['count'])]); ax.set_xlabel('Rating-count band'); ax.set_ylabel('Average rating'); ax.legend()
    save('09_rating_evidence','Ratings conditional on evidence volume',rating_evidence,'Descriptive association only. Different product ages, categories and selection mechanisms can explain differences.')
    def concentration(ax):
      v=np.sort(df.rating_number.fillna(0).clip(lower=0).to_numpy()); y=np.r_[0,np.cumsum(v)/v.sum()]; x=np.linspace(0,1,len(y)); ax.plot(x,y,color='#287b8e'); ax.plot([0,1],[0,1],'--',color='gray'); ax.set_xlabel('Cumulative share of products, least to most rated'); ax.set_ylabel('Cumulative share of rating counts')
    save('10_concentration','Concentration of accumulated rating counts',concentration,'This is a catalog concentration curve, not sales concentration or a deduplicated customer/review count.')
    save('11_claims','Claims and positioning terms in product titles',lambda ax:bars(ax,claims.set_index('title_claim').catalog_pct,'Percent of product titles'),'Keyword flags detect words, not verified product benefits, certifications or advertising eligibility.')
    def scatter(ax):
      x=df[df.price.gt(0)].sample(min(10000,int(df.price.gt(0).sum())),random_state=42); ax.scatter(x.price,x.average_rating,s=5,alpha=.12,color='#287b8e'); ax.set_xscale('log'); ax.set_xlabel('Observed price (log scale)'); ax.set_ylabel('Average rating')
    save('12_price_rating','Price versus rating (deterministic sample)',scatter,'At most 10,000 priced products, seed 42. All reported statistics use the full file; this plot samples only for readability.')
    n=len(df); pct=lambda x:f'{100*x/n:.1f}%'; num=lambda x:f'{x:,}'
    sections=[]
    def section(title,text,table=None):
      sections.append(f'<section><h2>{html.escape(title)}</h2>{text}'+('' if table is None else table.to_html(border=0,float_format=lambda x:f'{x:,.3f}',escape=True))+'</section>')
    section('1. Executive findings',f'<ul><li><strong>{n:,} products</strong>, {s["parse_errors"]} malformed records, {s["checks"]["duplicate_id_excess"]:,} duplicate-ID excess rows.</li><li>Prices available for {df.has_price.sum():,} ({pct(df.has_price.sum())}); category paths and bought-together data are unavailable.</li><li>{pct(s["title_only_no_description_or_features"])} have neither usable descriptions nor feature text.</li><li>Median rating count: {df.rating_number.median():,.0f}; {pct(s["rating_count_le_5"])} have at most five ratings.</li><li>Top 1% of products hold {100*s["top_1pct_products_share_rating_counts"]:.1f}% of summed rating counts; this is not sales share.</li><li>Observed median price is {df.price.median():.2f}, conditional on the priced subset.</li></ul>')
    section('2. Scope, provenance and limitations',f'<p>Full-file analysis of {html.escape(s["source"])} ({s["source_bytes"]:,} bytes). SHA-256: <code>{s["sha256"]}</code>. No API calls, scraped enrichment, user-level data or inferred sales. Main-category labels: {html.escape(str(s["main_categories"]))}. Source metadata has no snapshot date or explicit currency field. Treat prices, ratings, stock and discontinued status as historical observations; the file does not establish current availability.</p><p>The row is a parent-product metadata record, not a purchase, review or person. Do not infer conversion, revenue, ROAS, customer demographics, repeat purchases, causal effectiveness, time trends or market share. Summed rating_number is not guaranteed to be unique reviews.</p>')
    section('3. Schema and missingness','<p>All counts below include nulls and semantically empty containers separately. Nested lists are not missing just because a field exists.</p>',quality.set_index('field').drop(columns='types'))
    section('4. Integrity, duplicates and outliers','<p>Duplicate titles, UPCs and image URLs flag possible variants or shared assets; they are not automatic grounds for deletion. Some highly rated products share exactly matching titles across IDs, so summed rating counts should not be treated as independent reviews.</p><p><strong>Category drift is visible:</strong> price extremes include a standing body lift (2,548.98), a mobility scooter (1,485.00) and a livestock brush (1,378.32). The broad All Beauty label is not a reliable guarantee of beauty relevance. A narrow keyword audit exports suspected_category_drift.csv for manual review; it is not an exhaustive contamination estimate. Price extremes may also reflect bundles or professional equipment; inspect before exclusion.</p>',pd.DataFrame.from_dict(s['checks'],orient='index',columns=['count']))
    section('5. Numerical distributions','<p>Prices exclude nulls. Description and feature lengths include zeros when absent. Distribution summaries use all parsed records.</p>',stats)
    section('6. Rating reliability and attention concentration',f'<p>{s["five_star_products"]:,} products have an exact 5.0 average; {s["five_star_products_lt_5_ratings"]:,} of those have fewer than five ratings. A threshold of rating ≥4.5 alone is unsuitable for advertising selection. Use evidence thresholds or Bayesian shrinkage once rating-level assumptions are established. Top 10% account for {100*s["top_10pct_products_share_rating_counts"]:.1f}% of summed rating counts. Rating volume is confounded by listing age, exposure and category.</p>')
    section('7. Prices and selection bias',f'<p>Spearman price–rating association: {s["spearman_price_rating"]:.3f}; price–rating-count association: {s["spearman_price_rating_count"]:.3f}, priced rows only. Associations are descriptive, unadjusted and noncausal. Compare the priced subset below before generalizing. No unit-price comparison is valid without package-size normalization; do not silently drop expensive multipacks.</p>',missingcompare)
    section('8. Store and brand structure',f'<p>{len(stores):,} normalized nonempty store labels and {len(brands):,} normalized nonempty Brand labels. Normalization only applies Unicode compatibility, case folding and whitespace; it does not merge aliases. When both fields exist, {s["brand_store_exact_normalized_match_pct_when_both_present"]:.1f}% match exactly after normalization. Top ten store labels represent {100*s["top10_store_share_all_products"]:.1f}% of all rows. Store is not a verified brand or seller.</p>',stores.head(20))
    section('9. Structured attribute opportunities','<p>Hair Type, Skin Type, Item Form, Material and Product Benefits can support explicit filters. Preserve missingness and distinguish asserted metadata from validated properties. UPCs and package dimensions are identifiers/logistics fields, not customer intent.</p>',attrtable.head(30).set_index('attribute'))
    section('10. Product mix inferred from titles',f'<p>Rules are transparent, English keyword-based and ordered. {s["ambiguous_heuristic_segment_matches"]:,} products match multiple segments. The first match becomes primary; all matches are exported. This can miss synonyms or misclassify unrelated products. Manually validate a stratified sample before using segments in campaign targeting.</p>',segments)
    section('11. Text and positioning opportunities','<p>Titles provide broad coverage, but cannot establish true user needs, benefit efficacy or certification. Descriptions/features can enrich embeddings where available; sparse metadata makes a title-only baseline essential. Title keyword frequencies below are product incidence, not keyword search volume or demand.</p>',claims)
    section('12. Media readiness',f'<p>All products have at least one image entry in this file. {pct(df.has_hi_res.sum())} have a nonempty high-resolution URL and {pct(df.has_video.sum())} have video entries. URLs were not fetched: no assertion is made about availability, licensing, image quality or video usefulness. Duplicate asset entries can inflate raw image counts; unique URL counts are exported.</p>')
    section('13. Marketing actions supported by these data','<ol><li><strong>Repair catalog metadata first:</strong> establish a validated product taxonomy, standardize Brand/Store aliases, and refresh price, availability and package units before launching feeds.</li><li><strong>Build intent-based discovery:</strong> evaluate title-only versus title + verified attributes embeddings against manually judged query–product pairs; measure multi-positive relevance, constraint adherence and latency.</li><li><strong>Prioritize merchandising review:</strong> inspect products with strong rating evidence but weak descriptions or media; low rating count alone does not establish untapped demand.</li><li><strong>Audit creative readiness:</strong> use missing descriptions, attributes and high-resolution URLs to form enrichment queues, then manually verify claims and assets.</li><li><strong>Test business impact separately:</strong> join consented session/campaign, transaction, stock and margin data; run controlled experiments for conversion or profit lift. This metadata cannot measure those outcomes.</li></ol>')
    section('14. Reproducibility and exports','<p>Run <code>.venv/bin/python scripts/beauty_eda.py</code> from the workspace. Numerical analysis scans the complete file; only the scatterplot is sampled (seed 42). No records are silently deduplicated, imputed or winsorized. Exported product profiles retain original IDs and source-line numbers. Original nested data remain unchanged.</p><p>CSV files include field quality, numeric summaries, product profiles, store/brand aggregates, attribute coverage/values, title-derived segments/claims/tokens, correlations, priced/unpriced comparison, duplicate candidates and price/rating extremes.</p>')
    cards=''.join(f'<figure><h3>{html.escape(title)}</h3><img src="{name}.png" alt="{html.escape(title)}"><figcaption>{html.escape(cap)}</figcaption></figure>' for name,title,cap in charts)
    links=''.join(f'<li><a href="{p.name}">{p.name}</a></li>' for p in sorted(out.glob('*.csv')))
    related = '<section id="linked-reviews"><h2>Customer reviews added</h2><p><a href="../beauty_reviews/report.html">Open the linked reviews and catalog analysis</a>, including join coverage, review quality, customer histories and research annotations.</p></section>' if (out.parent / 'beauty_reviews/report.html').exists() else ''
    css='body{font:16px/1.6 system-ui,sans-serif;color:#233343;background:#f4f7f9;margin:0}main{max-width:1180px;margin:auto;padding:40px}h1{font-size:38px;line-height:1.15}h2{color:#18576a;margin-top:0}section,figure{background:white;border:1px solid #dce5e9;border-radius:12px;padding:24px;margin:22px 0;overflow:auto}table{border-collapse:collapse;font-size:13px;width:100%}th,td{text-align:left;padding:9px;border-bottom:1px solid #e6ecef}th{background:#edf4f6}img{max-width:100%;height:auto}figcaption{font-size:14px;color:#556979}code{overflow-wrap:anywhere}header p{color:#556979}'
    (out/'report.html').write_text(f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>All Beauty — Comprehensive EDA</title><style>{css}</style><main><header><p>CATALOG INTELLIGENCE · FULL-FILE ANALYSIS</p><h1>All Beauty: Comprehensive Exploratory Analysis</h1><p>{n:,} products · reproducible local analysis · marketing applications with explicit evidence limits</p></header>'+related+''.join(sections)+'<section><h2>Charts</h2></section>'+cards+'<section><h2>Download tables</h2><ul>'+links+'</ul></section></main></html>')

if __name__=='__main__': main()
