"""Step 4. Scale the LLM labels to every review, and estimate prevalences with valid intervals.

1. Targets per review from the LLM labels: mention_<aspect>, neg_<aspect> (polarity neg or mixed),
   pos_<aspect>, ctx_<context>.
2. Classifier: L2 logistic regression on TF-IDF word 1-2-grams + character 2-5-grams, one per target,
   C chosen by 5-fold cross-validation on the stratified train sample. Applied to all reviews.
3. Prevalence: prediction-powered inference with power tuning (PPI++; Angelopoulos, Bates, Fannjiang,
   Jordan & Zrnic, 2023, Science; Angelopoulos, Duchi & Zrnic, 2023). For a group g,
       theta_hat = lambda * mean_{all reviews in g} f(x) + mean_{calib reviews in g} (y - lambda * f(x)),
   with lambda chosen to minimise variance. The calib sample is a simple random sample that the
   classifier never saw, so theta_hat is unbiased for the share of reviews the LLM would label, and the
   CI is asymptotically valid even if the classifier is poor. A poor classifier only widens the CI.

Usage: python scale.py <source>
Writes outputs/<source>/predictions.parquet, classifier_eval.json.
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np
import pandas as pd
from scipy import sparse
from scipy.stats import norm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, f1_score, roc_auc_score
from sklearn.model_selection import GridSearchCV, StratifiedKFold

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from aspects import ASPECTS, CONTEXT  # noqa: E402

PRIMARY = "claude-haiku-5-5"
MIN_POSITIVES = 15


def load_labels(out: str, name: str, model: str = PRIMARY) -> pd.DataFrame:
    rows = []
    with open(os.path.join(out, f"labels_{name}__{model}.jsonl")) as f:
        for line in f:
            r = json.loads(line)
            if not r["parsed"]:
                continue
            y = {"review_id": r["review_id"]}
            for a in ASPECTS:
                ps = [l["p"] for l in r["labels"] if l["a"] == a]
                y[f"mention_{a}"] = int(bool(ps))
                y[f"neg_{a}"] = int(any(p in ("neg", "mixed") for p in ps))
                y[f"pos_{a}"] = int(any(p in ("pos", "mixed") for p in ps))
            for c in CONTEXT:
                y[f"ctx_{c}"] = int(c in r["ctx"])
            rows.append(y)
    return pd.DataFrame(rows)


def targets() -> list[str]:
    return ([f"{k}_{a}" for a in ASPECTS for k in ("mention", "neg", "pos")] + [f"ctx_{c}" for c in CONTEXT])


def features(texts_fit, texts_all):
    w = TfidfVectorizer(token_pattern=r"(?u)\b[a-z]+(?:'[a-z]+)?\b", ngram_range=(1, 2), min_df=3, max_features=300000, sublinear_tf=True)
    c = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5), min_df=5, max_features=300000, sublinear_tf=True)
    w.fit(texts_fit); c.fit(texts_fit)
    return lambda t: sparse.hstack([w.transform(t), c.transform(t)]).tocsr()


def ppi_mean(y_lab, f_lab, f_unlab, alpha=0.05):
    """PPI++ mean with power-tuned lambda (clipped to [0, 1]). Returns estimate, se, lo, hi, lambda."""
    y_lab, f_lab, f_unlab = map(np.asarray, (y_lab, f_lab, f_unlab))
    n, N = len(y_lab), len(f_unlab)
    if n < 2:
        return dict(est=float("nan"), se=float("nan"), lo=float("nan"), hi=float("nan"), lam=float("nan"), n=n, N=N)
    vf = np.var(np.concatenate([f_lab, f_unlab]), ddof=1)
    lam = 0.0 if vf == 0 else float(np.clip(np.cov(y_lab, f_lab, ddof=1)[0, 1] / ((1 + n / N) * vf), 0, 1))
    est = lam * f_unlab.mean() + (y_lab - lam * f_lab).mean()
    se = np.sqrt(lam ** 2 * np.var(f_unlab, ddof=1) / N + np.var(y_lab - lam * f_lab, ddof=1) / n)
    z = norm.ppf(1 - alpha / 2)
    return dict(est=float(est), se=float(se), lo=float(est - z * se), hi=float(est + z * se), lam=lam, n=n, N=N)


def main(source: str):
    out = os.path.join(HERE, "outputs", source)
    df = pd.read_parquet(os.path.join(out, "reviews.parquet"))
    text = (df.title.fillna("") + " . " + df.text).tolist()
    idx = {r: i for i, r in enumerate(df.review_id)}
    tr, ca = load_labels(out, "train"), load_labels(out, "calib")
    rng = np.random.default_rng(0)
    fit_ids = rng.choice(len(text), size=min(200000, len(text)), replace=False)
    feat = features([text[i] for i in fit_ids], None)
    X_all = feat(text)
    X_tr = X_all[[idx[r] for r in tr.review_id]]
    X_ca = X_all[[idx[r] for r in ca.review_id]]
    preds = {"review_id": df.review_id.values}
    evals = {}
    for t in targets():
        y = tr[t].values
        if y.sum() < MIN_POSITIVES or (len(y) - y.sum()) < MIN_POSITIVES:
            evals[t] = {"skipped": f"fewer than {MIN_POSITIVES} positives in train", "train_pos": int(y.sum())}
            continue
        gs = GridSearchCV(LogisticRegression(max_iter=2000, solver="liblinear"), {"C": [0.5, 2, 8, 32]},
                          scoring="average_precision", cv=StratifiedKFold(5, shuffle=True, random_state=0), n_jobs=4)
        gs.fit(X_tr, y)
        p_all = gs.best_estimator_.predict_proba(X_all)[:, 1]
        preds[t] = p_all.astype(np.float32)
        yc, pc = ca[t].values, gs.best_estimator_.predict_proba(X_ca)[:, 1]
        e = {"C": gs.best_params_["C"], "train_pos": int(y.sum()), "calib_pos": int(yc.sum()),
             "cv_avg_precision": round(gs.best_score_, 3)}
        if 0 < yc.sum() < len(yc):
            e.update(calib_auroc=round(roc_auc_score(yc, pc), 3), calib_avg_precision=round(average_precision_score(yc, pc), 3),
                     calib_f1_at_0_5=round(f1_score(yc, pc >= 0.5), 3))
        evals[t] = e
    pd.DataFrame(preds).to_parquet(os.path.join(out, "predictions.parquet"), index=False)
    with open(os.path.join(out, "classifier_eval.json"), "w") as f:
        json.dump(evals, f, indent=2)
    return evals


if __name__ == "__main__":
    ev = main(sys.argv[1])
    for k, v in ev.items():
        print(k, v)
