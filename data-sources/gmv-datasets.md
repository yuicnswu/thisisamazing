# Beauty datasets with real sales / GMV (for RQ2)

Searched 2026-11-07. Goal: an outcome variable that is real sales (revenue, units, order value) rather than listing price, ideally beauty, ideally joinable to reviews or brand/product IDs.

## Ranking

| # | Dataset | Sales field | Beauty coverage | Review text? | Join to our data | Status |
|---|---------|-------------|-----------------|--------------|------------------|--------|
| 1 | **Olist Brazilian E-commerce** (Kaggle `olistbr/brazilian-ecommerce`, CC BY-NC-SA 4.0) | Order-item price + freight, payments per order (real transactions) | `beleza_saude` 9,670 items / 2,444 products / R$1.26M GMV; `perfumaria` 3,419 items / R$0.40M | Yes, Portuguese, tied to the same order (4,680 beauty reviews with text) | No brand names; works as a stand-alone replication | **Downloaded** |
| 2 | **Amazon Products Dataset 2023** (Kaggle `asaniczka/amazon-products-dataset-2023-1-4m-products`) | `boughtInLastMonth` (Amazon's "X bought in past month" badge), `isBestSeller`, price | Beauty & Personal Care categories | No (but ratings and review counts) | **ASIN = our All_Beauty `parent_asin`** (partial overlap expected) | Needs Kaggle login (free); blocked from this machine |
| 3 | **eCommerce Events History in Cosmetics Shop** (Kaggle `mkechinov/...`, REES46) | Purchase events with price, so GMV per product/brand/day | 100% cosmetics, ~2 GB, Oct 2019–Feb 2020 | No | **Brand name** to Sephora/Amazon brands | Needs Kaggle login (free); no working mirror found |
| 4 | **Taobao/Tmall Double-11 makeup** (circulates on Heywhale/GitCode; mirror: github.com/LW-No-Parsley/Taobao-Cosmetics-Sales-Analysis) | Cumulative `sale_count`, `comment_count`, price; 10 daily snapshots (Nov 5–14) | 22 brands (Lancôme, Estée Lauder, Clinique, SK-II, Shiseido, Shu Uemura, Laneige, Maybelline…), 3,497 products, 27,598 rows | No | **Brand name** to Sephora (many overlap) | **Downloaded**. Provenance and licence unclear; the mirror labels dates 2022 |
| 5 | **Amazon Review Data 2018** metadata (McAuley lab, UCSD) | `salesRank` (sales-rank proxy) | All Beauty 33k products / 371k reviews; Luxury Beauty 12k / 575k | Yes | ASIN to the 2018 reviews; partial overlap with 2023 | Free, no form; host blocked from this machine |
| 6 | **Dunnhumby The Complete Journey** (via `completejourney_py`) | `sales_value`, `quantity` per basket line, 2017 | Makeup, hair, skin, oral, fragrance: 24,568 lines, $100k, 5,526 products | No | None (brands anonymised to National/Private) | **Downloaded** (beauty subset only). Weak fit |
| 7 | NielsenIQ Kilts scanner/panel (Chicago Booth), Circana/IRI academic | Weekly UPC sales | Health & beauty aids | No | UPC/brand | Institutional licence, paid. Gold standard if your university has access |

Skipped: Instacart (no prices), H&M Kaggle (fashion, almost no beauty, no reviews), the many "beauty sales" Kaggle/GitHub sets that are synthetic (e.g. GlowNest, "Cosmetics sales" Power BI sets). Bright Data, Apify and similar scraped Sephora/Ulta/Nykaa/Shopee feeds are paid.

## Recommendation

1. **Olist** as the main real-GMV test of RQ2: the only free set where review text and actual paid order value sit on the same order. Caveat: per-product volume is thin (median 1 unit, mean 4), so test at subcategory/seller level or pool by gap topic.
2. **Amazon 2023 `boughtInLastMonth`** as the sales outcome on the All_Beauty corpus we already use: it joins on ASIN, so RQ1 (gaps) and RQ2 (sales) run on the same products.
3. **REES46 cosmetics** or **Taobao Double-11** as a brand-level robustness check (do brands whose products fill gaps sell more?).

## Files here

- `olist/`: all Olist tables except geolocation, plus `olist_beauty_items_with_reviews.csv` (beauty + perfume order items joined to product, order and review; 13,163 rows).
- `taobao-double11-makeup/`: `double11beautysales.csv` (raw), `clean_beautymakeup.xlsx` (cleaned, with category and 销售额 = price × sale_count), `tmall_order_report.csv` (28k Tmall orders, not product-level).
- `dunnhumby-complete-journey-beauty/`: beauty product list and transactions only.
