import os

out_dir = "/Users/cattleya.c/.gemini/antigravity/scratch/all_beauty/eda_outputs"
os.makedirs(out_dir, exist_ok=True)
html_path = os.path.join(out_dir, "eda_report.html")

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>EDA Report: Evidence-Based Launch Matching & GMV (All_Beauty + Meta)</title>
<style>
  :root {
    --bg: #0f172a;
    --card: #1e293b;
    --border: #334155;
    --text: #f8fafc;
    --muted: #94a3b8;
    --accent: #38bdf8;
    --green: #22c55e;
    --amber: #f59e0b;
    --red: #ef4444;
    --purple: #a855f7;
  }
  * { box-sizing: border-box; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: var(--bg);
    color: var(--text);
    margin: 0;
    padding: 32px 24px;
    line-height: 1.55;
  }
  .container { max-width: 1180px; margin: 0 auto; }
  h1 { font-size: 1.9rem; margin: 0 0 8px; color: #fff; }
  h2 { font-size: 1.35rem; margin: 28px 0 12px; color: var(--accent); border-bottom: 1px solid var(--border); padding-bottom: 6px; }
  h3 { font-size: 1.05rem; margin: 16px 0 8px; color: #e2e8f0; }
  p, li { color: #cbd5e1; font-size: 0.95rem; }
  .subtitle { color: var(--muted); font-size: 0.98rem; margin-bottom: 24px; }
  .kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
    gap: 14px;
    margin-bottom: 24px;
  }
  .kpi {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 16px;
  }
  .kpi .label { font-size: 0.8rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.04em; }
  .kpi .val { font-size: 1.6rem; font-weight: 700; margin: 6px 0 2px; color: #fff; }
  .kpi .sub { font-size: 0.82rem; color: var(--muted); }
  .card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 20px;
  }
  .grid-2 {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(480px, 1fr));
    gap: 18px;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.86rem;
    margin-top: 8px;
  }
  th, td {
    padding: 9px 10px;
    border-bottom: 1px solid var(--border);
    text-align: left;
  }
  th { color: var(--muted); font-weight: 600; background: rgba(15, 23, 42, 0.5); }
  td.num, th.num { text-align: right; font-variant-numeric: tabular-nums; }
  .bar-row { margin: 9px 0; }
  .bar-label { display: flex; justify-content: space-between; font-size: 0.84rem; margin-bottom: 4px; }
  .bar-track { background: #0f172a; height: 12px; border-radius: 6px; overflow: hidden; }
  .bar-fill { height: 100%; border-radius: 6px; }
  .badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 600;
  }
  .b-green { background: rgba(34,197,94,0.18); color: #4ade80; }
  .b-red { background: rgba(239,68,68,0.18); color: #f87171; }
  .b-amber { background: rgba(245,158,11,0.18); color: #fbbf24; }
  .b-blue { background: rgba(56,189,248,0.18); color: #38bdf8; }
  code { background: #0f172a; padding: 2px 6px; border-radius: 4px; color: #38bdf8; font-size: 0.85em; }
</style>
</head>
<body>
<div class="container">
  <h1>Exploratory Data Analysis: New Product Launch Matching &amp; GMV</h1>
  <div class="subtitle">
    Dataset: UCSD Amazon Reviews 2023 (<code>All_Beauty.jsonl</code> &times; <code>meta_All_Beauty.jsonl</code>) &bull;
    Target Cohort: <code>hackathon_beauty_gmv_dedup.csv</code> (2005-02-02 to 2023-09-09)
  </div>

  <div class="kpi-grid">
    <div class="kpi">
      <div class="label">Full Joined Priced Reviews</div>
      <div class="val">185,623</div>
      <div class="sub">$3,869,809 Verified GMV across 17,704 priced items</div>
    </div>
    <div class="kpi">
      <div class="label">Deduplicated Repeat-Buyer Cohort</div>
      <div class="val">15,606</div>
      <div class="sub">13,868 users &times; 5,585 products (487 variant dupes removed)</div>
    </div>
    <div class="kpi">
      <div class="label">Cohort Total GMV</div>
      <div class="val">$338,741</div>
      <div class="sub">$270,605 Verified Purchase GMV (83.0% verified)</div>
    </div>
    <div class="kpi">
      <div class="label">Cold-Start Launch Share (&lt;10 revs)</div>
      <div class="val">44.5%</div>
      <div class="sub">6,942 launch-window purchases ($168,856 GMV)</div>
    </div>
    <div class="kpi">
      <div class="label">Verified Regret Rate (&le;2&#9733;)</div>
      <div class="val">16.4%</div>
      <div class="sub">$41,699 Verified Regret GMV at stake</div>
    </div>
  </div>

  <h2>1. Executive Summary &amp; Four Smoking-Gun Findings for RQ1&ndash;RQ3</h2>
  <div class="card">
    <ul>
      <li><strong>Finding 1 &mdash; Why AI Recommenders Default to Priors (RQ1):</strong> In the deduplicated repeat-buyer cohort (<code>N = 15,606</code>), <strong>Priors are 96%&ndash;100% populated</strong> (<code>meta_rating_number</code> 100%, <code>meta_average_rating</code> 100%, <code>store_brand</code> 96.3%), whereas <strong>Verifiable Evidence is missing 42%&ndash;98% of the time</strong> (<code>features_text</code> missing 42.4%, <code>item_form</code> missing 52.2%, <code>hair_type</code> missing 82.6%, <code>skin_type</code> missing 84.2%, <code>material_type_free</code> missing 95.9%). Without explicit abstention, models are forced to rely on priors and title keywords.</li>
      <li><strong>Finding 2 &mdash; The "Hype Trap" in Verified Purchases (RQ1 &amp; RQ2):</strong> Among verified purchases (<code>n = 12,935</code>), listings with <strong>High Persuasive Hype (&ge;2 superlative/hype tokens) + Low/Missing Structured Evidence</strong> suffer the <strong>highest Regret Rate (19.8%) and highest Regret GMV share (19.0%)</strong>. When high persuasive copy is backed by <strong>High Verifiable Evidence (&ge;3 structured specs + bullets)</strong>, satisfaction jumps to <strong>78.1%</strong> and Regret GMV drops to <strong>14.2%</strong> (&minus;4.8 pp).</li>
      <li><strong>Finding 3 &mdash; The "Partial-Evidence Trap" Motivates Strict Conjunctive Abstention (RQ2 &rarr; RQ3):</strong> When a customer has multiple stated needs in prior reviews and the listing supports <em>all</em> of them, verified satisfaction is <strong>77.1%</strong> and Regret GMV is <strong>12.6%</strong>. When the listing supports <em>only part</em> of their needs (e.g., matches hair type but misses chemical-free/scent constraint), verified satisfaction plunges to <strong>70.3%</strong> and <strong>Regret Rate spikes to 22.4% (20.8% Regret GMV)</strong>.</li>
      <li><strong>Finding 4 &mdash; Cold-Start Unverified/Vine Seeding Confounder (Data Quality Flag):</strong> During the Cold-Start window (<code>1&ndash;9 prior product reviews</code>), <strong>25.6%&ndash;29.8%</strong> of reviews are unverified/promotional (<code>verified_purchase = False</code>) with 82.5%&ndash;84.2% positive ratings, vs. only <strong>5.2%</strong> unverified in established products (<code>50+ prior reviews</code>). <strong>Rule for RQ3:</strong> Always evaluate post-launch outcome metrics on <code>verified_purchase == True</code>.</li>
    </ul>
  </div>

  <h2>2. Data Quality &amp; Funnel Audit (Raw &rarr; Analysis Cohort)</h2>
  <div class="card">
    <table>
      <thead>
        <tr>
          <th>Pipeline Stage</th>
          <th class="num">Row Count</th>
          <th class="num">Unique Products</th>
          <th class="num">Unique Users</th>
          <th class="num">Total GMV ($)</th>
          <th>Quality / Filtering Note</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>1. Raw <code>All_Beauty.jsonl</code></td>
          <td class="num">701,528</td>
          <td class="num">112,565</td>
          <td class="num">631,986</td>
          <td class="num">&mdash;</td>
          <td>89.0% of users have only 1 review in category</td>
        </tr>
        <tr>
          <td>2. Raw <code>meta_All_Beauty.jsonl</code></td>
          <td class="num">112,590</td>
          <td class="num">112,590</td>
          <td class="num">&mdash;</td>
          <td class="num">&mdash;</td>
          <td>96.0% have <code>details</code>; 15.7% (17,704) have numeric USD <code>price</code></td>
        </tr>
        <tr>
          <td>3. Joined Priced Reviews</td>
          <td class="num">185,623</td>
          <td class="num">17,704</td>
          <td class="num">171,340</td>
          <td class="num">$3,869,808.95</td>
          <td>Verified GMV: $2.96M Satisfied (76.6%) vs. $640k Regret (16.5%)</td>
        </tr>
        <tr>
          <td>4. Repeat Buyers w/ Prior History (<code>t &lt; t_buy</code>)</td>
          <td class="num">16,093</td>
          <td class="num">5,585</td>
          <td class="num">13,868</td>
          <td class="num">$350,173.26</td>
          <td>Contains 487 multi-variant duplicate <code>(user_id, parent_asin)</code> rows</td>
        </tr>
        <tr>
          <td><strong>5. Clean Deduplicated Hackathon Cohort</strong></td>
          <td class="num"><strong>15,606</strong></td>
          <td class="num"><strong>5,585</strong></td>
          <td class="num"><strong>13,868</strong></td>
          <td class="num"><strong>$338,741.04</strong></td>
          <td><span class="badge b-green">Zero Leakage</span> Strictly 1 row per <code>(user_id, parent_asin)</code></td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="grid-2">
    <div class="card">
      <h3>Priors vs. Evidence Availability (N = 15,606)</h3>
      <p>Priors are nearly universal, while specific evidence fields are sparse:</p>
      <div class="bar-row">
        <div class="bar-label"><span><strong>Prior:</strong> Popularity (<code>meta_rating_number</code>)</span><span>100.0% present</span></div>
        <div class="bar-track"><div class="bar-fill" style="width:100%;background:var(--amber)"></div></div>
      </div>
      <div class="bar-row">
        <div class="bar-label"><span><strong>Prior:</strong> Brand / Store (<code>store_brand</code>)</span><span>96.3% present</span></div>
        <div class="bar-track"><div class="bar-fill" style="width:96.3%;background:var(--amber)"></div></div>
      </div>
      <div class="bar-row">
        <div class="bar-label"><span><strong>Evidence:</strong> Bullet Features (<code>features_text</code>)</span><span>57.6% present</span></div>
        <div class="bar-track"><div class="bar-fill" style="width:57.6%;background:var(--accent)"></div></div>
      </div>
      <div class="bar-row">
        <div class="bar-label"><span><strong>Evidence:</strong> Item Form (<code>item_form</code>)</span><span>47.8% present</span></div>
        <div class="bar-track"><div class="bar-fill" style="width:47.8%;background:var(--accent)"></div></div>
      </div>
      <div class="bar-row">
        <div class="bar-label"><span><strong>Evidence:</strong> Hair Type (<code>hair_type</code>)</span><span>17.4% present</span></div>
        <div class="bar-track"><div class="bar-fill" style="width:17.4%;background:var(--accent)"></div></div>
      </div>
      <div class="bar-row">
        <div class="bar-label"><span><strong>Evidence:</strong> Scent (<code>scent</code>)</span><span>16.5% present</span></div>
        <div class="bar-track"><div class="bar-fill" style="width:16.5%;background:var(--accent)"></div></div>
      </div>
      <div class="bar-row">
        <div class="bar-label"><span><strong>Evidence:</strong> Skin Type (<code>skin_type</code>)</span><span>15.8% present</span></div>
        <div class="bar-track"><div class="bar-fill" style="width:15.8%;background:var(--accent)"></div></div>
      </div>
      <div class="bar-row">
        <div class="bar-label"><span><strong>Evidence:</strong> Product Benefits (<code>product_benefits</code>)</span><span>12.6% present</span></div>
        <div class="bar-track"><div class="bar-fill" style="width:12.6%;background:var(--accent)"></div></div>
      </div>
      <div class="bar-row">
        <div class="bar-label"><span><strong>Evidence:</strong> Material Type Free (<code>material_type_free</code>)</span><span>4.1% present</span></div>
        <div class="bar-track"><div class="bar-fill" style="width:4.1%;background:var(--red)"></div></div>
      </div>
      <div class="bar-row">
        <div class="bar-label"><span><strong>Evidence:</strong> Active Ingredients (<code>active_ingredients</code>)</span><span>2.4% present</span></div>
        <div class="bar-track"><div class="bar-fill" style="width:2.4%;background:var(--red)"></div></div>
      </div>
    </div>

    <div class="card">
      <h3>Numeric Distributions &amp; Quantiles (N = 16,093 / 15,606)</h3>
      <table>
        <thead>
          <tr>
            <th>Metric</th>
            <th class="num">Mean</th>
            <th class="num">p25</th>
            <th class="num">Median</th>
            <th class="num">p75</th>
            <th class="num">p95</th>
            <th class="num">Max</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><code>price_usd</code> (GMV $)</td>
            <td class="num">$21.76</td>
            <td class="num">$9.90</td>
            <td class="num">$14.99</td>
            <td class="num">$24.95</td>
            <td class="num">$55.99</td>
            <td class="num">$1,185.72</td>
          </tr>
          <tr>
            <td><code>rating</code> (Stars)</td>
            <td class="num">4.15</td>
            <td class="num">4.00</td>
            <td class="num">5.00</td>
            <td class="num">5.00</td>
            <td class="num">5.00</td>
            <td class="num">5.00</td>
          </tr>
          <tr>
            <td><code>user_prior_reviews_count</code></td>
            <td class="num">2.50</td>
            <td class="num">1.00</td>
            <td class="num">1.00</td>
            <td class="num">2.00</td>
            <td class="num">7.00</td>
            <td class="num">161</td>
          </tr>
          <tr>
            <td><code>product_prior_reviews</code></td>
            <td class="num">83.36</td>
            <td class="num">3.00</td>
            <td class="num">13.00</td>
            <td class="num">62.00</td>
            <td class="num">420.00</td>
            <td class="num">1,894</td>
          </tr>
          <tr>
            <td><code>meta_rating_number</code></td>
            <td class="num">1,023.1</td>
            <td class="num">43</td>
            <td class="num">215</td>
            <td class="num">1,010</td>
            <td class="num">5,312</td>
            <td class="num">13,676</td>
          </tr>
          <tr>
            <td><code>evidence_struct_cols</code> (0&ndash;7)</td>
            <td class="num">1.16</td>
            <td class="num">0</td>
            <td class="num">1</td>
            <td class="num">2</td>
            <td class="num">3</td>
            <td class="num">5</td>
          </tr>
          <tr>
            <td><code>listing_hype_words</code></td>
            <td class="num">0.84</td>
            <td class="num">0</td>
            <td class="num">0</td>
            <td class="num">1</td>
            <td class="num">3</td>
            <td class="num">20</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <h2>3. Task-Driven Segment Cuts for RQ1, RQ2, and RQ3 (Verified Purchases, n = 12,935)</h2>
  <div class="grid-2">
    <div class="card">
      <h3>RQ1 &amp; RQ2: Persuasive Hype vs. Verifiable Evidence</h3>
      <table>
        <thead>
          <tr>
            <th>Listing Segment (Verified Only)</th>
            <th class="num">n</th>
            <th class="num">GMV ($)</th>
            <th class="num">Sat % (&ge;4&#9733;)</th>
            <th class="num">Regret % (&le;2&#9733;)</th>
            <th class="num">Regret GMV %</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>High Evidence + High Persuasive Copy</strong></td>
            <td class="num">329</td>
            <td class="num">$7,396</td>
            <td class="num"><span class="badge b-green">78.1%</span></td>
            <td class="num">15.8%</td>
            <td class="num"><span class="badge b-green">14.2%</span></td>
          </tr>
          <tr>
            <td><strong>High Evidence + Low/Factual Copy</strong></td>
            <td class="num">511</td>
            <td class="num">$9,078</td>
            <td class="num">76.1%</td>
            <td class="num">16.8%</td>
            <td class="num">18.3%</td>
          </tr>
          <tr>
            <td><strong>Moderate Evidence Mix</strong></td>
            <td class="num">8,486</td>
            <td class="num">$176,366</td>
            <td class="num">75.4%</td>
            <td class="num">15.9%</td>
            <td class="num">14.6%</td>
          </tr>
          <tr>
            <td><strong>Low/Missing Evidence + Low Hype</strong></td>
            <td class="num">3,437</td>
            <td class="num">$75,004</td>
            <td class="num">75.5%</td>
            <td class="num">17.0%</td>
            <td class="num">15.7%</td>
          </tr>
          <tr>
            <td><strong>Low/Missing Evidence + High Persuasive Hype</strong></td>
            <td class="num">172</td>
            <td class="num">$2,760</td>
            <td class="num">75.6%</td>
            <td class="num"><span class="badge b-red">19.8%</span></td>
            <td class="num"><span class="badge b-red">19.0%</span></td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="card">
      <h3>RQ2 &rarr; RQ3: Customer Prior Need Support in Listing</h3>
      <table>
        <thead>
          <tr>
            <th>Prior Need Alignment Status</th>
            <th class="num">n</th>
            <th class="num">GMV ($)</th>
            <th class="num">Sat % (&ge;4&#9733;)</th>
            <th class="num">Regret % (&le;2&#9733;)</th>
            <th class="num">Regret GMV %</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>1. All Stated Needs Supported</strong></td>
            <td class="num">772</td>
            <td class="num">$16,572</td>
            <td class="num"><span class="badge b-green">77.1%</span></td>
            <td class="num"><span class="badge b-green">14.9%</span></td>
            <td class="num"><span class="badge b-green">12.6%</span></td>
          </tr>
          <tr>
            <td><strong>2. Partially Supported (Half-Match Trap)</strong></td>
            <td class="num">219</td>
            <td class="num">$4,458</td>
            <td class="num"><span class="badge b-red">70.3%</span></td>
            <td class="num"><span class="badge b-red">22.4%</span></td>
            <td class="num"><span class="badge b-red">20.8%</span></td>
          </tr>
          <tr>
            <td><strong>3. Missing Evidence for Stated Needs</strong></td>
            <td class="num">2,416</td>
            <td class="num">$51,367</td>
            <td class="num">75.0%</td>
            <td class="num">16.3%</td>
            <td class="num">14.3%</td>
          </tr>
          <tr>
            <td><strong>4. General / Implicit Prior History</strong></td>
            <td class="num">9,528</td>
            <td class="num">$198,208</td>
            <td class="num">75.7%</td>
            <td class="num">16.2%</td>
            <td class="num">15.3%</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <h2>4. Cold-Start Launch Lifecycle &amp; Promotional Seeding Bias (N = 15,606)</h2>
  <div class="card">
    <table>
      <thead>
        <tr>
          <th>Product Launch Stage at Purchase</th>
          <th class="num">Total Purchases</th>
          <th class="num">Unverified / Vine Share</th>
          <th class="num">Unverified Sat %</th>
          <th class="num">Verified Sat %</th>
          <th class="num">Verified Regret %</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>1. Day-1 Launch (0 prior reviews)</td>
          <td class="num">1,879</td>
          <td class="num">17.7%</td>
          <td class="num">79.9%</td>
          <td class="num">77.4%</td>
          <td class="num">14.9%</td>
        </tr>
        <tr>
          <td>2. Early Launch (1&ndash;4 prior reviews)</td>
          <td class="num">3,122</td>
          <td class="num"><span class="badge b-amber">25.6%</span></td>
          <td class="num"><span class="badge b-amber">84.2%</span></td>
          <td class="num">75.7%</td>
          <td class="num">16.0%</td>
        </tr>
        <tr>
          <td>3. Cold-Start Window (5&ndash;9 prior reviews)</td>
          <td class="num">1,941</td>
          <td class="num"><span class="badge b-amber">29.8%</span></td>
          <td class="num"><span class="badge b-amber">82.5%</span></td>
          <td class="num">75.6%</td>
          <td class="num">16.4%</td>
        </tr>
        <tr>
          <td>4. Growth Stage (10&ndash;49 prior reviews)</td>
          <td class="num">4,278</td>
          <td class="num">17.2%</td>
          <td class="num">81.1%</td>
          <td class="num">74.3%</td>
          <td class="num">17.3%</td>
        </tr>
        <tr>
          <td>5. Established (50+ prior reviews)</td>
          <td class="num">4,386</td>
          <td class="num"><span class="badge b-blue">5.2%</span></td>
          <td class="num">72.8%</td>
          <td class="num">75.8%</td>
          <td class="num">16.1%</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
</body>
</html>
"""

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Static HTML report written to {html_path} ({os.path.getsize(html_path)} bytes)")
