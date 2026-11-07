"""Experiment 2 (RQ3) without leakage: does stated customer context predict a customer's NEXT
recommendation beyond product popularity?

Leakage in the naive design: is_recommended, the star rating and the review text are written in the same
review, so any feature taken from the target review (its text, rating, aspects) leaks the answer.
Here every feature is computed only from reviews submitted on EARLIER days than the target review
(strictly earlier: same-day reviews are excluded because Sephora timestamps are day-resolution), and
the evaluation is a global time split: models are fitted on targets before the cutoff date and tested
on targets after it (the last 20% of days), as in temporal recommender evaluation (Campos et al. 2014;
Ji et al. 2023, "A critical study on data leakage in recommender system offline evaluation").

Models (gradient-boosted trees, same hyper-parameters):
  M0 popularity : product's prior recommend rate (smoothed), prior n, prior mean rating; category prior rate
  M1 + context  : M0 + reviewer's skin type, product's prior recommend rate among same-skin-type reviewers
  M2 + history  : M1 + reviewer's prior n reviews, prior recommend rate, prior mean rating, prior rate in
                  the same category (returning customers only have these)
Reported on all test targets and on returning customers (at least one earlier review): AUROC, log loss,
Brier, with 95% cluster-bootstrap intervals over reviewers for the differences M1-M0 and M2-M0.

Usage: python rq3_temporal.py sephora [--target is_recommended] [--boot 500]
Writes outputs/<source>/rq3_temporal.json and rq3_temporal.md.
"""
from __future__ import annotations

import argparse
import json
import os

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import brier_score_loss, log_loss, roc_auc_score

HERE = os.path.dirname(os.path.abspath(__file__))
M = 10.0   # Bayesian smoothing strength towards the parent rate


def prior_stats(df: pd.DataFrame, keys: list[str], y: str, prefix: str) -> pd.DataFrame:
    """For each row: count and sum of y over rows with the same keys on strictly earlier days."""
    g = df.groupby(keys + ["day"], sort=True)[y].agg(["size", "sum"]).reset_index()
    g = g.sort_values(keys + ["day"])
    g[f"{prefix}_n"] = g.groupby(keys)["size"].cumsum() - g["size"]
    g[f"{prefix}_s"] = g.groupby(keys)["sum"].cumsum() - g["sum"]
    return df[keys + ["day"]].merge(g[keys + ["day", f"{prefix}_n", f"{prefix}_s"]], on=keys + ["day"], how="left")[[f"{prefix}_n", f"{prefix}_s"]]


def build_features(df: pd.DataFrame, target: str) -> pd.DataFrame:
    df = df.sort_values(["date", "review_id"]).reset_index(drop=True).copy()
    df["day"] = df["date"].dt.floor("D")
    df["y"] = df[target].astype(float)
    df["skin_type"] = df["skin_type"].fillna("unknown")
    glob_ = prior_stats(df.assign(_k=0), ["_k"], "y", "g")
    base = (glob_["g_s"] + 1) / (glob_["g_n"] + 2)
    cat = prior_stats(df, ["category"], "y", "c")
    df["cat_rate"] = (cat["c_s"] + M * base) / (cat["c_n"] + M)
    p = prior_stats(df, ["product_id"], "y", "p")
    df["prod_n"] = p["p_n"]
    df["prod_rate"] = (p["p_s"] + M * df["cat_rate"]) / (p["p_n"] + M)
    pr = prior_stats(df, ["product_id"], "rating", "pr")
    df["prod_mean_rating"] = np.where(pr["pr_n"] > 0, pr["pr_s"] / pr["pr_n"].replace(0, np.nan), np.nan)
    ps = prior_stats(df, ["product_id", "skin_type"], "y", "ps")
    df["prod_skin_n"] = ps["ps_n"]
    df["prod_skin_rate"] = (ps["ps_s"] + M * df["prod_rate"]) / (ps["ps_n"] + M)
    df["skin_lift"] = df["prod_skin_rate"] - df["prod_rate"]
    a = prior_stats(df, ["author_id"], "y", "a")
    df["auth_n"] = a["a_n"]
    df["auth_rate"] = np.where(a["a_n"] > 0, (a["a_s"] + 2 * base) / (a["a_n"] + 2), np.nan)
    ar = prior_stats(df, ["author_id"], "rating", "ar")
    df["auth_mean_rating"] = np.where(ar["ar_n"] > 0, ar["ar_s"] / ar["ar_n"].replace(0, np.nan), np.nan)
    ac = prior_stats(df, ["author_id", "category"], "y", "ac")
    df["auth_cat_n"] = ac["ac_n"]
    df["auth_cat_rate"] = np.where(ac["ac_n"] > 0, (ac["ac_s"] + 2 * base) / (ac["ac_n"] + 2), np.nan)
    return df


M0 = ["prod_rate", "prod_n", "prod_mean_rating", "cat_rate"]
M1 = M0 + ["skin_code", "prod_skin_rate", "prod_skin_n", "skin_lift"]
M2 = M1 + ["auth_n", "auth_rate", "auth_mean_rating", "auth_cat_n", "auth_cat_rate"]


def metrics(y, p):
    return {"auroc": roc_auc_score(y, p), "logloss": log_loss(y, np.clip(p, 1e-6, 1 - 1e-6)), "brier": brier_score_loss(y, p)}


def cluster_boot(y, preds: dict, groups, base="M0", B=500, seed=0):
    rng = np.random.default_rng(seed)
    uniq, inv = np.unique(groups, return_inverse=True)
    rows_of = pd.Series(np.arange(len(y))).groupby(inv).apply(np.array).values
    diffs = {k: [] for k in preds if k != base}
    for _ in range(B):
        pick = rng.integers(0, len(uniq), len(uniq))
        idx = np.concatenate([rows_of[i] for i in pick])
        if y[idx].min() == y[idx].max():
            continue
        b = metrics(y[idx], preds[base][idx])
        for k in diffs:
            m = metrics(y[idx], preds[k][idx])
            diffs[k].append({s: m[s] - b[s] for s in m})
    out = {}
    for k, ds in diffs.items():
        d = pd.DataFrame(ds)
        out[f"{k}-{base}"] = {s: {"lo": float(d[s].quantile(0.025)), "hi": float(d[s].quantile(0.975))} for s in d}
    return out


def main(source, target="is_recommended", B=200, test_share=0.2):
    out = os.path.join(HERE, "outputs", source)
    df = pd.read_parquet(os.path.join(out, "reviews.parquet"),
                         columns=["review_id", "product_id", "author_id", "rating", "date", "skin_type", "category", target])
    df = df[df[target].notna() & df.date.notna()]
    f = build_features(df, target)
    f["skin_code"] = f["skin_type"].astype("category").cat.codes
    days = np.sort(f.day.unique())
    cutoff = days[int(len(days) * (1 - test_share))]
    tr, te = f[f.day < cutoff], f[f.day >= cutoff]
    res = {"source": source, "target": target, "n_train": len(tr), "n_test": len(te), "cutoff": str(cutoff)[:10],
           "test_positive_rate": float(te.y.mean()), "returning_share_test": float((te.auth_n > 0).mean()), "models": {}}
    preds = {}
    for name, cols in (("M0", M0), ("M1", M1), ("M2", M2)):
        clf = HistGradientBoostingClassifier(max_iter=300, learning_rate=0.05, max_leaf_nodes=31, random_state=0,
                                             categorical_features=[c == "skin_code" for c in cols])
        clf.fit(tr[cols], tr.y)
        preds[name] = clf.predict_proba(te[cols])[:, 1]
    y = te.y.values.astype(int)
    for subset, mask in (("all", np.ones(len(te), bool)), ("returning", (te.auth_n > 0).values)):
        r = {"n": int(mask.sum())}
        for k, p in preds.items():
            r[k] = {s: round(float(v), 4) for s, v in metrics(y[mask], p[mask]).items()}
        r["bootstrap_95ci"] = cluster_boot(y[mask], {k: p[mask] for k, p in preds.items()}, te.author_id.values[mask], B=B)
        res["models"][subset] = r
    with open(os.path.join(out, "rq3_temporal.json"), "w") as fh:
        json.dump(res, fh, indent=2)
    L = [f"# RQ3: next-review {target}, time split at {res['cutoff']} ({res['n_train']:,} train, {res['n_test']:,} test)\n",
         "Features use only reviews from earlier days. M0 popularity, M1 + skin-type context, M2 + reviewer history.\n"]
    for subset, r in res["models"].items():
        L.append(f"## {subset} test targets (n = {r['n']:,})\n\n| Model | AUROC | Log loss | Brier |\n|---|---|---|---|")
        for k in ("M0", "M1", "M2"):
            L.append(f"| {k} | {r[k]['auroc']:.4f} | {r[k]['logloss']:.4f} | {r[k]['brier']:.4f} |")
        for k, d in r["bootstrap_95ci"].items():
            L.append(f"\n{k}: ΔAUROC 95% CI [{d['auroc']['lo']:+.4f}, {d['auroc']['hi']:+.4f}], "
                     f"Δlog loss [{d['logloss']['lo']:+.4f}, {d['logloss']['hi']:+.4f}]")
        L.append("")
    with open(os.path.join(out, "rq3_temporal.md"), "w") as fh:
        fh.write("\n".join(L))
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("source"); ap.add_argument("--target", default="is_recommended"); ap.add_argument("--boot", type=int, default=200)
    a = ap.parse_args()
    print(json.dumps(main(a.source, a.target, a.boot)["models"], indent=2)[:4000])
