"""Learn-then-Test (Angelopoulos et al., 2021) for the unsupported recommendation rate (URR).

Policy: recommend an item iff score >= lambda. Loss on a recommended item = 1 if its support label is not
`entailed`. For each lambda on a grid, from strictest to loosest, test H0: URR(lambda) > alpha with the exact
binomial p-value over the n calibration items it recommends (k of them unsupported):

    p(lambda) = P[Binomial(n, alpha) <= k]

The grid is fixed before labels are seen (21 label-free quantiles of the calibration scores). Family-wise error
is controlled with Bonferroni: lambda is certified when p(lambda) <= delta / |grid|, and we deploy the loosest
certified one. (Fixed-sequence testing from the strictest lambda stalls here: the strictest thresholds select
only a handful of items, whose p-values can never be small.) With probability >= 1 - delta over the calibration
draw, every certified lambda has URR <= alpha (conditional on the selected count, the usual LTT
selective-risk form).
"""
from __future__ import annotations

import numpy as np
from scipy.stats import binom


def binom_pvalue(k: int, n: int, alpha: float) -> float:
    return 1.0 if n == 0 else float(binom.cdf(k, n, alpha))


def ltt_threshold(scores, unsupported, alpha: float, delta: float = 0.1, grid=None):
    """Loosest certified threshold, or None if even the strictest one fails (then abstain on everything)."""
    scores = np.asarray(scores, float)
    unsupported = np.asarray(unsupported, bool)
    if grid is None:
        grid = np.unique(np.quantile(scores, np.linspace(0, 1, 21)))
    grid = np.asarray(grid, float)
    best = None
    for lam in sorted(grid, reverse=True):
        sel = scores >= lam
        n, k = int(sel.sum()), int(unsupported[sel].sum())
        if binom_pvalue(k, n, alpha) <= delta / len(grid):
            best = float(lam)
    return best


def evaluate(scores, unsupported, groups, alpha, delta=0.1, n_splits=20, cal_frac=0.5, seed=0):
    """Repeated group (product) splits: calibrate on cal_frac of products, test on the rest."""
    scores, unsupported, groups = np.asarray(scores, float), np.asarray(unsupported, bool), np.asarray(groups)
    uniq = np.unique(groups)
    rng = np.random.default_rng(seed)
    rows = []
    for s in range(n_splits):
        cal_g = set(rng.choice(uniq, int(len(uniq) * cal_frac), replace=False))
        cal = np.array([g in cal_g for g in groups])
        lam = ltt_threshold(scores[cal], unsupported[cal], alpha, delta)
        te = ~cal
        if lam is None:
            rows.append({"split": s, "lambda": None, "urr": 0.0, "coverage": 0.0, "recall": 0.0, "n_rec": 0})
            continue
        rec = scores[te] >= lam
        n_rec = int(rec.sum())
        urr = float(unsupported[te][rec].mean()) if n_rec else 0.0
        supported = ~unsupported[te]
        rows.append({"split": s, "lambda": lam, "urr": urr, "coverage": float(rec.mean()),
                     "recall": float(rec[supported].mean()) if supported.any() else 0.0, "n_rec": n_rec})
    return rows


def summarize(rows, alpha):
    u = np.array([r["urr"] for r in rows])
    c = np.array([r["coverage"] for r in rows])
    rc = np.array([r["recall"] for r in rows])
    q = lambda x: (float(np.mean(x)), float(np.percentile(x, 2.5)), float(np.percentile(x, 97.5)))
    return {"urr": q(u), "coverage": q(c), "recall": q(rc), "violation_rate": float(np.mean(u > alpha)),
            "no_threshold_rate": float(np.mean([r["lambda"] is None for r in rows]))}


def risk_coverage(scores, unsupported):
    """(coverage, URR) at every threshold, for plotting."""
    scores, unsupported = np.asarray(scores, float), np.asarray(unsupported, bool)
    out = []
    for lam in np.unique(scores)[::-1]:
        sel = scores >= lam
        out.append((float(sel.mean()), float(unsupported[sel].mean())))
    return out
