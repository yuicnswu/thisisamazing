"""Selective risk control for the three-way matcher: Algorithm 1 of `03-solution-design/theory.md` (PR #7).

Decision rule, theta = (lambda, tau), per item with entailment score e and contradiction score c:

    reject     if c >= tau
    recommend  elif e >= lambda
    abstain    otherwise

(Needs in this pilot have one constraint, so the theory's min_i e_i / max_i c_i reduce to e and c.)

Risks, against the CONSENSUS labels of Theorem 3 (supported only if the rule parser AND the independent quote
judge both say entailed; contradicted only if both say contradicted):

    URR(theta) = P(not supported | recommend)        URJ(theta) = P(not contradicted | reject)

Algorithm 1, per random product split:
  1. Products -> calibration (cal_frac) and test. Calibration draws ONE item per product (assumption A1).
     Calibration products -> tune (20%) and certify (80%).
  2. On tune: fix tau (loosest grid value whose tune rejections have Clopper-Pearson URJ upper bound <= alpha'),
     and the lambda path: the distinct tune scores, strict to lenient, starting at the strictest lambda whose
     tune recommendations, rescaled to the certify size, number at least n_min (default: 3x the fewest
     that could ever be certified, 3 * ceil(log delta / log(1 - alpha)), fixed before seeing data).
  3. On certify: fixed-sequence testing along the path with p = max(p_rec, p_rej), the exact binomial p-values
     of Theorem 1; stop at the first p > delta.
  4. Deploy the certified theta with the highest certify coverage, or certify nothing (abstain on everything).
  5. Test on held-out products, every item weighted 1 / (items of its product) so the test distribution is the
     A1 one (pick a product, then one of its items).
Theorem 1: with prob. >= 1 - delta over the calibration draw, URR <= alpha and URJ <= alpha' w.r.t. the labels.
Theorem 3: against the truth, URR <= alpha + P(parser and judge both falsely say entailed | recommend).
"""
from __future__ import annotations

import numpy as np
from scipy.stats import beta as beta_dist

from ltt import binom_pvalue

REC, ABS, REJ = 1, 0, -1


def clopper_pearson(k: float, n: float, conf: float = 0.95):
    if n == 0:
        return 0.0, 1.0
    a = 1 - conf
    lo = 0.0 if k == 0 else float(beta_dist.ppf(a / 2, k, n - k + 1))
    hi = 1.0 if k == n else float(beta_dist.ppf(1 - a / 2, k + 1, n - k))
    return lo, hi


def decide(e, c, lam, tau):
    e, c = np.asarray(e, float), np.asarray(c, float)
    return np.where(c >= tau, REJ, np.where(e >= lam, REC, ABS))


def choose_tau(c, uncontra, alpha_rej, grid):
    """Loosest tau on the tune set whose rejections pass a one-sided 95% Clopper-Pearson bound <= alpha_rej."""
    best = np.inf
    for tau in sorted(grid, reverse=True):
        rej = c >= tau
        n, k = int(rej.sum()), int(uncontra[rej].sum())
        if n and clopper_pearson(k, n, 0.90)[1] <= alpha_rej:
            best = tau
    return best


def lambda_path(e_tune, scale, n_min, grid):
    """Strict-to-lenient lambdas, starting at the strictest one expected to recommend >= n_min certify items."""
    path = sorted(grid, reverse=True)
    for j, lam in enumerate(path):
        if (e_tune >= lam).sum() * scale >= n_min:
            return path[j:]
    return []


def fixed_sequence(e, c, unsup, uncontra, path, tau, alpha, alpha_rej, delta):
    """Theorem 1: certified lambdas (in path order) until the first p_theta > delta."""
    certified = []
    for lam in path:
        d = decide(e, c, lam, tau)
        rec, rej = d == REC, d == REJ
        p_rec = binom_pvalue(int(unsup[rec].sum()), int(rec.sum()), alpha)
        # tau = inf never rejects, so URJ is vacuous; a finite tau with no rejections keeps p = 1 (Theorem 1)
        p_rej = 0.0 if np.isinf(tau) else binom_pvalue(int(uncontra[rej].sum()), int(rej.sum()), alpha_rej)
        if max(p_rec, p_rej) > delta:
            break
        certified.append((lam, float(rec.mean())))
    return certified


def algorithm1(e, c, unsup, uncontra, groups, alpha, alpha_rej=0.10, delta=0.10, n_splits=50, cal_frac=0.5,
               tune_frac=0.2, n_min=None, seed=0, extra=None):
    """Repeated product splits of Algorithm 1. `extra` = dict of boolean arrays to average over test recommendations
    (e.g. label-disagreement diagnostics). Returns one row per split."""
    if n_min is None:  # 3x the fewest recommendations that could ever be certified, (1 - alpha)^n <= delta,
        # so that sampling noise around the start point does not end the sequence at its first test
        n_min = 3 * int(np.ceil(np.log(delta) / np.log(1 - alpha)))
    e, c = np.asarray(e, float), np.asarray(c, float)
    unsup, uncontra, groups = np.asarray(unsup, bool), np.asarray(uncontra, bool), np.asarray(groups)
    uniq = np.unique(groups)
    by_g = {g: np.where(groups == g)[0] for g in uniq}
    w_all = np.array([1.0 / len(by_g[g]) for g in groups])
    rng = np.random.default_rng(seed)
    rows = []
    for s in range(n_splits):
        perm = rng.permutation(uniq)
        n_cal = int(len(uniq) * cal_frac)
        cal_g, test_g = perm[:n_cal], perm[n_cal:]
        n_tune = int(n_cal * tune_frac)
        pick = lambda gs: np.array([rng.choice(by_g[g]) for g in gs], int)   # A1: one item per product
        tune, cert = pick(cal_g[:n_tune]), pick(cal_g[n_tune:])
        grid = np.unique(e[tune])  # every tune score; fixed-sequence testing pays nothing for a longer path
        tau = choose_tau(c[tune], uncontra[tune], alpha_rej, np.unique(np.quantile(c[tune], np.linspace(0, 1, 21))))
        path = lambda_path(e[tune], len(cert) / max(len(tune), 1), n_min, grid)
        certified = fixed_sequence(e[cert], c[cert], unsup[cert], uncontra[cert], path, tau, alpha, alpha_rej, delta)
        te = np.concatenate([by_g[g] for g in test_g])
        w = w_all[te]
        row = {"split": s, "tau": None if np.isinf(tau) else float(tau), "n_cert": len(cert),
               "path_len": len(path), "n_certified": len(certified)}
        d = decide(e[te], c[te], certified[-1][0], tau) if certified else np.where(c[te] >= tau, REJ, ABS)
        rec, rej = d == REC, d == REJ
        sup = ~unsup[te]
        row.update(lam=certified[-1][0] if certified else None,
                   urr=float((w * rec * unsup[te]).sum() / (w * rec).sum()) if rec.any() else 0.0,
                   urj=float((w * rej * uncontra[te]).sum() / (w * rej).sum()) if rej.any() else 0.0,
                   coverage=float((w * rec).sum() / w.sum()),
                   recall=float((w * rec * sup).sum() / (w * sup).sum()) if sup.any() else 0.0,
                   rej_rate=float((w * rej).sum() / w.sum()),
                   n_rec=int(rec.sum()), n_rej=int(rej.sum()),
                   urr_k=float((rec * unsup[te]).sum()), urr_n=int(rec.sum()))
        for name, arr in (extra or {}).items():
            a = np.asarray(arr, bool)[te]
            row[name] = float((w * rec * a).sum() / (w * rec).sum()) if rec.any() else 0.0
        rows.append(row)
    return rows


def summarize1(rows, alpha, alpha_rej):
    q = lambda k: (float(np.mean([r[k] for r in rows])), float(np.percentile([r[k] for r in rows], 2.5)),
                   float(np.percentile([r[k] for r in rows], 97.5)))
    out = {k: q(k) for k in ("urr", "urj", "coverage", "recall", "rej_rate")}
    out["violation_rate"] = float(np.mean([r["urr"] > alpha for r in rows]))
    out["urj_violation_rate"] = float(np.mean([r["urj"] > alpha_rej for r in rows]))
    out["no_threshold_rate"] = float(np.mean([r["lam"] is None for r in rows]))
    out["no_reject_rate"] = float(np.mean([r["tau"] is None for r in rows]))
    k, n = sum(r["urr_k"] for r in rows), sum(r["urr_n"] for r in rows)
    out["pooled_urr_cp95"] = clopper_pearson(k, n)  # pooled over splits (overlapping test sets): descriptive only
    for extra in [x for x in rows[0] if x.startswith("diag_")]:
        out[extra] = q(extra)
    return out
