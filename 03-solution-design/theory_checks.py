"""Numerical sanity checks for the results in theory.md.

Standard library only, so it runs anywhere: `python3 03-solution-design/theory_checks.py`.
These checks test the statements on synthetic data. They are not a substitute for
the proofs, and they say nothing about the real verifier or the real listings.
"""

import math
import random

# ---------------------------------------------------------------------------
# Binomial helpers
# ---------------------------------------------------------------------------


def binom_cdf(k, n, p):
    """P(Bin(n, p) <= k), summed in log space for stability."""
    if k < 0:
        return 0.0
    if k >= n:
        return 1.0
    if p <= 0.0:
        return 1.0
    if p >= 1.0:
        return 0.0
    lp, lq = math.log(p), math.log1p(-p)
    total = 0.0
    for i in range(k + 1):
        total += math.exp(math.lgamma(n + 1) - math.lgamma(i + 1) - math.lgamma(n - i + 1) + i * lp + (n - i) * lq)
    return min(total, 1.0)


def urr_pvalue(k_unsupported, n_recommended, alpha):
    """Theorem 1 p-value for H: URR(lambda) > alpha. Equal to 1 when nothing is recommended."""
    if n_recommended == 0:
        return 1.0
    return binom_cdf(k_unsupported, n_recommended, alpha)


def cp_upper(k, n, conf_level):
    """One-sided Clopper-Pearson upper bound at level 1 - conf_level (bisection)."""
    if n == 0 or k >= n:
        return 1.0
    lo, hi = k / n, 1.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if binom_cdf(k, n, mid) > conf_level:
            lo = mid
        else:
            hi = mid
    return hi


def cp_lower(k, n, conf_level):
    """One-sided Clopper-Pearson lower bound at level 1 - conf_level."""
    if n == 0 or k == 0:
        return 0.0
    return 1.0 - cp_upper(n - k, n, conf_level)


# ---------------------------------------------------------------------------
# Check 1: Theorem 1 (Learn-then-Test on the selective risk URR) is valid
# ---------------------------------------------------------------------------


def draw_item(rng, base_rate=0.4):
    supported = rng.random() < base_rate
    score = rng.betavariate(5, 2) if supported else rng.betavariate(2, 5)
    return score, supported


GRID = [1.0 - 0.01 * j for j in range(1, 100)]  # strict -> lenient


def true_urr_curve(rng, n_ref=400_000):
    items = [draw_item(rng) for _ in range(n_ref)]
    curve = {}
    for lam in GRID:
        rec = [y for s, y in items if s >= lam]
        curve[lam] = (sum(1 for y in rec if not y) / len(rec)) if rec else 0.0
    return curve


def ltt_select(cal, alpha, delta, n_min=30, tune_frac=0.2):
    """Fixed-sequence testing from strict to lenient; return the most lenient certified lambda.

    The start of the sequence is chosen on a separate tuning split (the strictest lambda that
    recommends at least n_min tuning items). Starting at the very strict end of the grid, where
    almost nothing is recommended, makes the first p-value 1 and stops the sequence at once
    (the "coverage collapse" failure). Choosing the start on held-apart data keeps the
    sequence fixed with respect to the testing split, so validity is untouched.
    """
    n_tune = int(len(cal) * tune_frac)
    tune, test = cal[:n_tune], cal[n_tune:]
    start = next((i for i, lam in enumerate(GRID)
                  if sum(1 for s, _ in tune if s >= lam) * (len(test) / max(n_tune, 1)) >= n_min), None)
    if start is None:
        return None
    chosen = None
    for lam in GRID[start:]:
        rec = [y for s, y in test if s >= lam]
        k = sum(1 for y in rec if not y)
        if urr_pvalue(k, len(rec), alpha) <= delta:
            chosen = lam
        else:
            break
    return chosen


def ltt_select_naive(cal, alpha, delta):
    """Same test, but the sequence starts at the strictest grid point (shows coverage collapse)."""
    chosen = None
    for lam in GRID:
        rec = [y for s, y in cal if s >= lam]
        k = sum(1 for y in rec if not y)
        if urr_pvalue(k, len(rec), alpha) <= delta:
            chosen = lam
        else:
            break
    return chosen


def check_ltt_validity(trials=1000, n_cal=1500, alpha=0.10, delta=0.10, seed=0):
    rng = random.Random(seed)
    curve = true_urr_curve(rng)
    violations = certified = naive_certified = 0
    coverages = []
    for _ in range(trials):
        cal = [draw_item(rng) for _ in range(n_cal)]
        naive_certified += ltt_select_naive(cal, alpha, delta) is not None
        lam = ltt_select(cal, alpha, delta)
        if lam is None:
            continue
        certified += 1
        coverages.append(lam)
        if curve[lam] > alpha:
            violations += 1
    lam_oracle = min(l for l in GRID if curve[l] <= alpha)
    print(f"[1] LTT on URR: alpha={alpha}, delta={delta}, n_cal={n_cal}, trials={trials}")
    print(f"    sequence started at the strictest grid point: certified in {naive_certified}/{trials} trials"
          f" (coverage collapse)")
    print(f"    sequence start chosen on a tuning split: certified in {certified}/{trials} trials;"
          f" median lambda {sorted(coverages)[len(coverages)//2] if coverages else None:.2f}"
          f" vs oracle {lam_oracle:.2f}")
    print(f"    true URR > alpha in {violations} trials ({violations / trials:.3f}, must be <= delta={delta})")
    return violations / trials <= delta + 3 * math.sqrt(delta * (1 - delta) / trials)


# ---------------------------------------------------------------------------
# Check 2: Proposition 4 (per-constraint calibration does not control item URR)
# ---------------------------------------------------------------------------


def check_per_constraint_counterexample(alpha=0.05, rho=0.03):
    """Exact construction from the proof, k = 2.

    Constraint 1 is judged entailed on every item and is truly not entailed on a share alpha.
    Constraint 2 is judged entailed only on a share rho <= alpha of items, all of them inside the
    share where constraint 1 is wrong, and constraint 2 is always truly entailed.
    """
    assert rho <= alpha
    p_c1_wrong_given_j1 = alpha            # J1 on all items
    p_c2_wrong_given_j2 = 0.0              # constraint 2 always right
    p_item_unsupported_given_both = 1.0    # J1 and J2 = J2, inside the c1-wrong set
    print(f"[2] Per-constraint counterexample (alpha={alpha}, rho={rho}):")
    print(f"    per-constraint false-entailment rates: {p_c1_wrong_given_j1:.2f}, {p_c2_wrong_given_j2:.2f}"
          f" (both <= alpha); item-level URR = {p_item_unsupported_given_both:.2f}")
    print("    independent-constraint case, URR = 1-(1-alpha)^k:",
          ", ".join(f"k={k}: {1 - (1 - alpha) ** k:.3f}" for k in range(1, 6)))
    return True


# ---------------------------------------------------------------------------
# Check 3: Theorem 2 (label noise) and Theorem 3 (consensus labels)
# ---------------------------------------------------------------------------


def check_label_noise(n=400_000, e_a=0.10, e_b=0.10, seed=1):
    """Recommendation correlated with extractor A's mistakes, to show why only
    the selective error rate matters and why consensus helps under independence."""
    rng = random.Random(seed)
    rows = []
    for _ in range(n):
        y_true = rng.random() < 0.5
        # Extractors only make false-entailed mistakes here (the direction that matters).
        y_a = True if y_true else (rng.random() < e_a)
        y_b = True if y_true else (rng.random() < e_b)
        # The verifier recommends supported items often, and also the unsupported items
        # that look supported to extractor A (shared surface cue), which is the bad case.
        if y_true:
            rec = rng.random() < 0.5
        else:
            rec = rng.random() < (0.6 if y_a else 0.01)
        rows.append((y_true, y_a, y_b, rec))
    rec_rows = [r for r in rows if r[3]]
    p_rec = len(rec_rows) / n
    urr_true = sum(1 for r in rec_rows if not r[0]) / len(rec_rows)
    urr_vs_a = sum(1 for r in rec_rows if not r[1]) / len(rec_rows)
    urr_vs_cons = sum(1 for r in rec_rows if not (r[1] and r[2])) / len(rec_rows)
    eps_marg = sum(1 for r in rows if r[1] and not r[0]) / n
    eps_rec = sum(1 for r in rec_rows if r[1] and not r[0]) / len(rec_rows)
    both_wrong_rec = sum(1 for r in rec_rows if r[1] and r[2] and not r[0]) / len(rec_rows)
    disagree_rec = sum(1 for r in rec_rows if r[1] != r[2]) / len(rec_rows)
    print(f"[3] Label noise: P(rec)={p_rec:.3f}, marginal false-entailed rate eps+={eps_marg:.3f}")
    print(f"    URR vs parser A labels = {urr_vs_a:.3f}; true URR = {urr_true:.3f}")
    print(f"    selective eps+_rec = {eps_rec:.3f}  (naive alpha+eps would add only {eps_marg:.3f};"
          f" bound eps+/P(rec) = {eps_marg / p_rec:.3f})")
    print(f"    URR vs consensus labels = {urr_vs_cons:.3f}; residual both-wrong rate = {both_wrong_rec:.4f}"
          f" (true URR - consensus URR = {urr_true - urr_vs_cons:.4f})")
    print(f"    disagreement rate among recommended = {disagree_rec:.3f} (Lemma 1 upper-bounds eps+_rec"
          f" only when errors are independent given truth AND recommendation; here they are not:"
          f" {disagree_rec:.3f} vs {eps_rec:.3f})")
    ok = abs((urr_true - urr_vs_a) - eps_rec) < 1e-9 and abs((urr_true - urr_vs_cons) - both_wrong_rec) < 1e-9
    return ok


# ---------------------------------------------------------------------------
# Check 4: calibration sample sizes for Theorem 1
# ---------------------------------------------------------------------------


def min_recommended_zero_errors(alpha, delta):
    return math.ceil(math.log(1 / delta) / -math.log1p(-alpha))


def recommended_needed_for_power(alpha, true_urr, delta, power=0.8):
    m = 1
    while True:
        # largest k with p-value <= delta
        k_star = -1
        while binom_cdf(k_star + 1, m, alpha) <= delta:
            k_star += 1
        if k_star >= 0 and binom_cdf(k_star, m, true_urr) >= power:
            return m
        m += 1 if m < 200 else 10


def check_sample_sizes(delta=0.05):
    print(f"[4] Recommended calibration items needed (delta={delta}):")
    print("    alpha | zero errors | power 0.8 at URR=alpha/2 | cal. items at 10% coverage")
    for alpha in (0.05, 0.10, 0.20):
        m0 = min_recommended_zero_errors(alpha, delta)
        m80 = recommended_needed_for_power(alpha, alpha / 2, delta)
        print(f"    {alpha:.2f}  | {m0:>11} | {m80:>24} | {math.ceil(m80 / 0.10):>10}")
    return True


# ---------------------------------------------------------------------------
# Check 5: exposure-gap test (Theorem 4) is valid
# ---------------------------------------------------------------------------


def gap_test_rejects(x_e, n_e, x_u, n_u, beta, delta):
    """Reject H: c_e - c_u > beta when UCB_e(delta/2) - LCB_u(delta/2) <= beta."""
    return cp_upper(x_e, n_e, delta / 2) - cp_lower(x_u, n_u, delta / 2) <= beta


def check_gap_test(trials=2000, beta=0.10, delta=0.10, seed=2):
    rng = random.Random(seed)
    c_e, c_u = 0.60, 0.48  # true gap 0.12 > beta: the null is true, so rejections are errors
    n_e, n_u = 600, 400
    false_rejections = 0
    for _ in range(trials):
        x_e = sum(rng.random() < c_e for _ in range(n_e))
        x_u = sum(rng.random() < c_u for _ in range(n_u))
        false_rejections += gap_test_rejects(x_e, n_e, x_u, n_u, beta, delta)
    print(f"[5] Exposure-gap test under a true gap of {c_e - c_u:.2f} > beta={beta}:"
          f" false certification rate {false_rejections / trials:.3f} (must be <= delta={delta})")
    return false_rejections / trials <= delta


# ---------------------------------------------------------------------------
# Check 6: disclosure threshold (Proposition 11)
# ---------------------------------------------------------------------------


def check_disclosure(q=0.1, r=0.0):
    print(f"[6] Disclosure under a noisy verifier (miss rate q={q}, contradiction-misread r={r}):")
    for p in (0.02, 0.05, 0.10, 0.30):
        s_star = (p - r) / (1 - q - r)
        print(f"    fooling rate p={p:.2f}: honest disclosure is a best response iff fit share s >= {s_star:.3f}")
    return True


if __name__ == "__main__":
    results = [
        check_ltt_validity(),
        check_per_constraint_counterexample(),
        check_label_noise(),
        check_sample_sizes(),
        check_gap_test(),
        check_disclosure(),
    ]
    print("ALL CHECKS PASSED" if all(results) else "SOME CHECK FAILED")
