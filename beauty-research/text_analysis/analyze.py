"""Step 5. Results tables from the scaled predictions, with PPI++ intervals.

Tables (all shares are of reviews, 95% PPI++ intervals unless marked):
  T1 aspect prevalence: share of reviews that mention each aspect, and that criticise it (neg or mixed)
  T2 criticism by star rating
  T3 what low ratings are about: among 1-2 star reviews, share criticising each aspect
  T4 customer context stated in reviews
  T5 concentration: share of each aspect's predicted criticism that comes from the top 1 and top 10 products
  T6 by group (Sephora: category, skin type, recommended; Amazon: verified purchase, year)
  T7 LLM-only estimate vs PPI++ on the same calib sample (interval width)
  plus distinctive terms (weighted log-odds), example verbatim quotes, label quality and agreement.

Usage: python analyze.py <source>   -> outputs/<source>/results.json, results.md
"""
from __future__ import annotations

import json
import os
import sys
from collections import defaultdict

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from aspects import ASPECTS, CONTEXT  # noqa: E402
from scale import PRIMARY, gold_name, load_labels, ppi_mean  # noqa: E402

SECOND = "claude-sonnet-5-5"
MIN_CALIB = 40


def pct(x, d=1):
    return "–" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{100 * x:.{d}f}%"


def fmt(r):
    return f"{pct(r['est'])} [{pct(max(r['lo'], 0))}, {pct(min(r['hi'], 1))}]"


def group_ppi(df, ca, target, group_col, values):
    out = {}
    for v in values:
        g_all = df[group_col] == v
        g_cal = ca[group_col] == v
        if g_cal.sum() < MIN_CALIB:
            out[str(v)] = {"est": float(df.loc[g_all, target].mean()), "lo": float("nan"), "hi": float("nan"),
                           "n": int(g_cal.sum()), "classifier_only": True}
            continue
        out[str(v)] = ppi_mean(ca.loc[g_cal, "y_" + target], ca.loc[g_cal, target], df.loc[g_all, target])
    return out


def agreement(out):
    full = os.path.exists(os.path.join(out, f"labels_calib__{SECOND}.jsonl"))   # whole calib, written by codebook.py
    a = load_labels(out, "calib" if full else "agree", SECOND).set_index("review_id")
    b = load_labels(out, "calib", PRIMARY).set_index("review_id").loc[lambda x: x.index.isin(a.index)]
    a = a.loc[b.index]
    res = {}
    for asp in ASPECTS:
        for k in ("mention", "neg"):
            t = f"{k}_{asp}"
            x, y = b[t].values, a[t].values
            tp = int(((x == 1) & (y == 1)).sum())
            po = (x == y).mean()
            pe = x.mean() * y.mean() + (1 - x.mean()) * (1 - y.mean())
            kappa = (po - pe) / (1 - pe) if pe < 1 else float("nan")
            res[t] = {"n": len(x), "haiku_pos": int(x.sum()), "sonnet_pos": int(y.sum()), "both": tp,
                      "agreement": round(float(po), 3), "kappa": round(float(kappa), 3)}
    return res


def quotes(out, k=2):
    q = defaultdict(list)
    for name in ("calib", "train"):
        with open(os.path.join(out, f"labels_{name}__{PRIMARY}.jsonl")) as f:
            for line in f:
                for l in json.loads(line)["labels"]:
                    key = (l["a"], "neg" if l["p"] in ("neg", "mixed") else "pos")
                    if len(q[key]) < k and 6 <= len(l["q"].split()) <= 25:
                        q[key].append(l["q"])
    return {f"{a}|{p}": v for (a, p), v in q.items()}


def main(source):
    out = os.path.join(HERE, "outputs", source)
    df = pd.read_parquet(os.path.join(out, "reviews.parquet"))
    pfile = os.environ.get("PREDICTIONS", "predictions.parquet")   # predictions_emb.parquet from scale_embed.py
    pr = pd.read_parquet(os.path.join(out, pfile))
    df = df.merge(pr, on="review_id")
    df["year"] = df["date"].dt.year
    df["low"] = (df.rating <= 2).astype(int)
    gold = gold_name(out)
    ca = load_labels(out, "calib", gold)
    ca = ca.rename(columns={c: "y_" + c for c in ca.columns if c != "review_id"}).merge(df, on="review_id")
    have = [c for c in pr.columns if c != "review_id"]
    R = {"source": source, "reviews": len(df), "calib_n": len(ca), "gold": gold, "predictions": pfile}

    def est(t, mask_all=None, mask_cal=None):
        ma = slice(None) if mask_all is None else mask_all
        mc = slice(None) if mask_cal is None else mask_cal
        return ppi_mean(ca.loc[mc, "y_" + t], ca.loc[mc, t], df.loc[ma, t])

    R["T1"] = {a: {k: est(f"{k}_{a}") for k in ("mention", "neg", "pos") if f"{k}_{a}" in have} for a in ASPECTS}
    stars = sorted(df.rating.dropna().unique())
    R["T2"] = {a: group_ppi(df, ca, f"neg_{a}", "rating", stars) for a in ASPECTS if f"neg_{a}" in have}
    R["T3"] = {a: est(f"neg_{a}", df.low == 1, ca.low == 1) for a in ASPECTS if f"neg_{a}" in have}
    R["T4"] = {c: est(f"ctx_{c}") for c in CONTEXT if f"ctx_{c}" in have}
    conc = {}
    big = df.groupby("product_id").review_id.transform("size") >= 20
    for a in ASPECTS:
        t = f"neg_{a}"
        if t not in have:
            continue
        s = df[big].groupby("product_id")[t].sum().sort_values(ascending=False)
        tot = s.sum()
        conc[a] = {"predicted_criticisms": round(float(tot)), "top1_share": float(s.iloc[0] / tot),
                   "top10_share": float(s.iloc[:10].sum() / tot), "top1_product": s.index[0],
                   "products": int((s > 0.5).sum())}
    R["T5"] = conc
    groups = {}
    if source == "sephora":
        df["incentivized_s"] = df.incentivized.astype(str); ca["incentivized_s"] = ca.incentivized.astype(str)
        for col in ("category", "skin_type", "is_recommended", "incentivized_s"):
            vals = df[col].value_counts().index[:8].tolist()
            groups[col] = {a: group_ppi(df, ca, f"neg_{a}", col, vals) for a in ASPECTS if f"neg_{a}" in have}
    else:
        df["period"] = pd.cut(df.year, [1999, 2015, 2018, 2020, 2023], labels=["≤2015", "2016-18", "2019-20", "2021-23"]).astype(str)
        ca["period"] = df.set_index("review_id").loc[ca.review_id, "period"].values
        df["verified_s"] = df.verified.astype(str); ca["verified_s"] = ca.verified.astype(str)
        groups["period"] = {a: group_ppi(df, ca, f"neg_{a}", "period", ["≤2015", "2016-18", "2019-20", "2021-23"]) for a in ASPECTS if f"neg_{a}" in have}
        groups["verified"] = {a: group_ppi(df, ca, f"neg_{a}", "verified_s", ["True", "False"]) for a in ASPECTS if f"neg_{a}" in have}
    R["T6"] = groups
    R["T7"] = {}
    for a in ASPECTS:
        t = f"neg_{a}"
        if t not in have:
            continue
        y = ca["y_" + t].values
        se = np.sqrt(y.mean() * (1 - y.mean()) / len(y))
        R["T7"][a] = {"llm_only": float(y.mean()), "llm_only_halfwidth": float(1.96 * se),
                      "ppi_halfwidth": float(1.96 * R["T1"][a]["neg"]["se"])}
    R["agreement"] = agreement(out)
    for fn, key in (("codebook/codebook_results.json", "codebook"), ("entail_results.json", "entail")):
        if os.path.exists(os.path.join(out, fn)):
            R[key] = json.load(open(os.path.join(out, fn)))
    R["quotes"] = quotes(out)
    R["classifier_eval"] = json.load(open(os.path.join(out, "classifier_eval.json")))
    R["labels"] = json.load(open(os.path.join(out, "labels_summary.json")))
    R["parse"] = json.load(open(os.path.join(out, "parse_summary.json")))
    R["logodds"] = json.load(open(os.path.join(out, "logodds.json")))
    R["topics"] = json.load(open(os.path.join(out, "topics.json")))
    sfx = "" if pfile == "predictions.parquet" else "_emb"
    with open(os.path.join(out, f"results{sfx}.json"), "w") as f:
        json.dump(R, f, indent=1, default=str)
    write_md(R, out, sfx)
    return R


def write_md(R, out, sfx=""):
    L = []
    w = L.append
    p = R["parse"]
    w(f"# Review text analysis: {R['source']}\n")
    w(f"{R['reviews']:,} reviews after cleaning ({p['raw_rows']:,} raw, {p['exact_duplicates_dropped']:,} exact duplicates and "
      f"{p['empty_text_dropped']:,} empty reviews dropped), {p['products']:,} products, {p['date_min'][:10]} to {p['date_max'][:10]}. "
      f"Shares are of all reviews, with 95% PPI++ intervals from a {R['calib_n']:,}-review random calibration sample. "
      "They estimate what the three-model jury (after the semantic support check) would say about every review; they are not human-validated.\n")
    lab = R["labels"]
    w("## Label quality\n")
    cb = R.get("codebook")
    if cb:
        h = cb["history"]
        ho = cb["held_out"]
        w(f"- Self-refining guide (no human coders): {len(h) - 1} refinement round(s), {len(cb['rules'])} learned rules. "
          f"Dev macro kappa {cb['models']['A']} vs {cb['models']['B']}: " + " → ".join(f"{x['macro_kappa']:.3f}" for x in h) +
          f". Held-out test ({ho['selected']['n']} reviews): {ho['guide_0']['macro_kappa']:.3f} with the original guide, "
          f"{ho['selected']['macro_kappa']:.3f} with the selected guide.")
        pr_ = cb["production"]
        w(f"- Gold labels ({R['gold']}): calib reviews where the two coders disagreed ({pct(pr_['calib_adjudicated_share'])}) were "
          f"adjudicated by {cb['models']['judge']}. Primary coder vs jury on calib: macro kappa {pr_['calib_haiku_vs_jury']['macro_kappa']:.3f}.")
    en = R.get("entail")
    if en:
        cv = en["contrast_validation"]
        w(f"- Semantic support check ({en['judge']}): {pct(en['verbatim_but_unsupported_rate'])} of verbatim gold labels were judged "
          f"not supported by their quote and dropped. On a known-answer contrast set the judge accepted {pct(cv['orig']['supported_rate'])} "
          f"of original labels and rejected {pct(cv['specificity_all_perturbations'])} of perturbed ones "
          f"(flipped polarity {pct(1 - cv['flip']['supported_rate'])}, swapped aspect {pct(1 - cv['swap']['supported_rate'])}, "
          f"wrong quote {pct(1 - cv['wrong']['supported_rate'])}).")
    w(f"- Verbatim quotes: {pct(lab['train']['verbatim_rate'])} of train labels and {pct(lab['calib']['verbatim_rate'])} of calib labels "
      "had a quote found word for word in the review. Labels without one were dropped.")
    ag = R["agreement"]
    ks = [v["kappa"] for k, v in ag.items() if k.startswith("mention_") and not np.isnan(v["kappa"]) and v["haiku_pos"] + v["sonnet_pos"] >= 10]
    w(f"- Second annotator ({SECOND}) on {next(iter(ag.values()))['n']} calib reviews: median Cohen's kappa for aspect mention "
      f"{np.median(ks):.2f} (range {min(ks):.2f}–{max(ks):.2f}, aspects with at least 10 positives).\n")
    w("## T1. What reviews talk about\n")
    w("| Aspect | Mentions | Criticises (neg or mixed) | Praises | Low-star reviews that criticise it (T3) |")
    w("|---|---|---|---|---|")
    order = sorted(R["T1"], key=lambda a: -R["T1"][a].get("mention", {"est": 0})["est"])
    for a in order:
        r = R["T1"][a]
        if "mention" not in r:
            continue
        w(f"| {a} | {fmt(r['mention'])} | {fmt(r['neg']) if 'neg' in r else '–'} | {fmt(r['pos']) if 'pos' in r else '–'} | "
          f"{fmt(R['T3'][a]) if a in R['T3'] else '–'} |")
    w("\n## T2. Criticism by star rating (share of reviews at that rating)\n")
    stars = list(next(iter(R["T2"].values())).keys())
    w("| Aspect | " + " | ".join(f"{float(s):.0f}★" for s in stars) + " |")
    w("|---|" + "---|" * len(stars))
    for a in order:
        if a in R["T2"]:
            w(f"| {a} | " + " | ".join(pct(R["T2"][a][s]["est"]) for s in stars) + " |")
    w("\n## T4. Customer context stated in reviews\n")
    w("| Context | Share of reviews |")
    w("|---|---|")
    for c, r in sorted(R["T4"].items(), key=lambda x: -x[1]["est"]):
        w(f"| {c} | {fmt(r)} |")
    w("\n## T5. Is criticism concentrated in a few products? (products with ≥ 20 reviews, classifier estimates)\n")
    w("| Aspect | Predicted criticisms | Top product's share | Top 10 products' share |")
    w("|---|---|---|---|")
    for a, r in sorted(R["T5"].items(), key=lambda x: -x[1]["predicted_criticisms"]):
        w(f"| {a} | {r['predicted_criticisms']:,} | {pct(r['top1_share'])} | {pct(r['top10_share'])} |")
    w("\n## T6. Criticism by group\n")
    for col, tab in R["T6"].items():
        vals = list(next(iter(tab.values())).keys())
        w(f"**{col}**\n")
        w("| Aspect | " + " | ".join(vals) + " |")
        w("|---|" + "---|" * len(vals))
        for a in order:
            if a in tab:
                w(f"| {a} | " + " | ".join(pct(tab[a][v]["est"]) + ("*" if tab[a][v].get("classifier_only") else "") for v in vals) + " |")
        w("")
    w("\\* fewer than 40 calibration reviews in the group: classifier estimate only, no interval.\n")
    w("## T7. Precision gained by scaling (criticism shares)\n")
    w("| Aspect | LLM labels alone (calib) ± | PPI++ ± |")
    w("|---|---|---|")
    for a, r in R["T7"].items():
        w(f"| {a} | {pct(r['llm_only'])} ± {pct(r['llm_only_halfwidth'])} | {pct(R['T1'][a]['neg']['est'])} ± {pct(r['ppi_halfwidth'])} |")
    w("\n## Distinctive terms, 1–2★ vs 4–5★ (weighted log-odds, z-scores)\n")
    lo = R["logodds"]
    w("- **Low-star:** " + ", ".join(f"{x['term']} ({x['z']})" for x in lo["a_over_b"][:25]))
    w("- **High-star:** " + ", ".join(f"{x['term']} ({x['z']})" for x in lo["b_over_a"][:25]) + "\n")
    w("## Example verbatim quotes\n")
    for a in order:
        for pol in ("neg", "pos"):
            for q in R["quotes"].get(f"{a}|{pol}", [])[:1]:
                w(f"- **{a}, {pol}:** “{q}”")
    w("\n## Classifier quality on the held-out calib sample (vs gold labels)\n")
    w("| Target | AUROC | Avg precision | Calib positives |")
    w("|---|---|---|---|")
    for t, e in R["classifier_eval"].items():
        if "calib_auroc" in e and (t.startswith("mention_") or t.startswith("neg_")):
            w(f"| {t} | {e['calib_auroc']} | {e['calib_avg_precision']} | {e['calib_pos']} |")
    skipped = [t for t, e in R["classifier_eval"].items() if "skipped" in e]
    if skipped:
        w(f"\nNot modelled (too few training positives): {', '.join(skipped)}.")
    with open(os.path.join(out, f"results{sfx}.md"), "w") as f:
        f.write("\n".join(L) + "\n")


if __name__ == "__main__":
    main(sys.argv[1])
    print(open(os.path.join(HERE, "outputs", sys.argv[1], "results.md")).read()[:3000])
