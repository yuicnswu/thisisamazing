# Theory: what the matcher can guarantee, and what it can't

*Stage 3 of WORKFLOW.md (on the workflow branch, PR #1, not yet on `main`). Living document: update it whenever the decision rule, the label design (plan §11) or the calibration code changes. Written 2026-10-17 in reply to the two mock reviews ([round 1](../is-topic/neurips-mock-review.md), round 2 in the shared folder), which both flag the theory as unwritten and the guarantee's novelty as moderate.*

*Numerical sanity checks for every result below: [`theory_checks.py`](theory_checks.py) (standard library only, about a minute). They test the statements on synthetic data; they are not proofs, and they say nothing about the real verifier.*

---

## 0. Verdict first

| Claim in the plan | Status after writing it out | Where |
|---|---|---|
| URR ≤ α with a finite-sample guarantee via conformal risk control or Learn-then-Test | **Holds with Learn-then-Test (LTT). Does not follow from conformal risk control (CRC)**, because URR is a ratio and its linearised loss is not monotone. Guarantee is "with probability ≥ 1 − δ over calibration", not "exactly". | Thm 1, Prop 6 |
| Plan §11.2 (main): true URR ≤ α + ε / P(recommend) | **Holds, but is loose and needs the right ε.** Only false-*entailed* label errors on *recommended* items count: true URR ≤ α + ε⁺_rec. The ε / P(rec) form is the worst case of that. | Thm 2 |
| ε can be made small without humans | **Yes, and better than the plan says:** calibrating on two-extractor *consensus* labels turns the first-order ε into a product of two error rates, under an independence assumption that must be stated. | Thm 3, Lemma 1 |
| "Support, not accuracy" differs from conformal factuality (Mohri & Hashimoto 2024) | **Holds, and can now be shown formally** rather than asserted: different label (evidence-relative vs truth-relative), different risk (selective vs marginal), and a conjunction you can't back off from. | §6, Props 4–5 |
| Two-sided guarantee: abstention doesn't fall disproportionately on new brands | **Holds as a multi-risk LTT result**, if the gap is defined on *supported* items. Needs weaker wording: it bounds a coverage gap on the calibration population, and it can be met by *levelling down* established products, which must be reported. | Thm 4, Prop 7 |
| Disclosure: complete, honest specs become the seller's best move | **Holds for completeness only, and only weakly**, under a perfect verifier and the assumption that false claims are ruled out. Honesty is assumed, not derived. With a verifier that accepts vague text at rate p, it holds only for products whose fit share exceeds p / (1 − q). That threshold is the useful new result. | Props 8–11 |
| The support rule is robust by construction to strategic rewrites (§9A) | **Does not hold for a learned verifier.** True only for an oracle verifier; for the real one, URR under attack is bounded by the clean URR plus a measured invariance-violation rate. No guarantee against an adaptive seller. | Prop 12 |

**Honest overall rating.** The calibration machinery is not new (LTT, binomial p-values, fixed-sequence testing). What is new is narrower: the formal separation from conformal factuality (Props 4–5), the consensus-label correction (Thm 3), the group form with its levelling-down caveat (Thm 4, Prop 7), and the disclosure threshold under a foolable verifier (Prop 11). That supports a "General" NeurIPS paper with theory as a pillar of rigour, not a theory paper. It moves the guarantee's originality from "moderate, possibly overlapping" to "moderate, clearly distinct". It does not make it "high" on its own.

---

## 1. Setup and notation

An **item** is a (listing, need) pair $Z = (x, R)$ with need $R = \{r_1, \dots, r_k\}$, a conjunction of checkable constraints (plan §12.1). The matcher sees only the visible listing text $x$ (title, bullets, description); `details` is hidden (plan §11.1).

**Support labels.** Each constraint has a status $s_i \in \{\mathsf{E}, \mathsf{C}, \mathsf{U}, \mathsf{X}\}$ (entailed, contradicted, unresolved, conflicting) *relative to $x$*. Define

- $Y = \mathbb{1}\{s_i = \mathsf{E}\ \forall i\}$: the item is **supported**.
- $K = \mathbb{1}\{\exists i: s_i = \mathsf{C}\}$: the item is **contradicted**.

$Y^\*$ denotes the true status (what a perfect reader of $x$ would assign); $\tilde Y$ denotes a label we can compute (L1 construction, L2 parser). On L1 items $\tilde Y = Y^\*$ by construction.

**Verifier.** A fixed model (trained on data disjoint from everything below) outputs per-constraint scores $e_i(x, r_i) \in [0,1]$ (entailment) and $c_i(x, r_i) \in [0,1]$ (contradiction). It is calibrated, not retrained, in what follows.

**Decision rule** with parameter $\theta = (\lambda, \tau)$:

$$
d_\theta(Z) = \begin{cases}
\text{reject} & \text{if } \max_i c_i \ge \tau,\\
\text{recommend} & \text{else if } \min_i e_i \ge \lambda,\\
\text{abstain} & \text{otherwise.}
\end{cases}
$$

The $\min$ is the conjunction: an item is recommended only if its weakest constraint clears the threshold. Rejection takes precedence so a contradicted constraint can never be outvoted.

**Risks.**

- Unsupported recommendation rate: $\mathrm{URR}(\theta) = \Pr(Y^\* = 0 \mid d_\theta = \text{recommend})$.
- Unsupported rejection rate: $\mathrm{URJ}(\theta) = \Pr(K^\* = 0 \mid d_\theta = \text{reject})$. A rejection tells the shopper "the listing contradicts your need" and puts the product on a do-not-target list, so it is a claim that also needs control.
- Coverage on supported items in group $g$: $\mathrm{Cov}_g(\theta) = \Pr(d_\theta = \text{recommend} \mid Y^\* = 1, G = g)$, with $G \in \{\text{new}, \text{est}\}$ (unfamiliar vs established, defined as in the proposal and never shown to the verifier).

**Sampling assumption (A1).** Calibration items $Z_1, \dots, Z_n$ and the test item are i.i.d. from one distribution $\mathcal{D}$. In practice this means **one item per product** in the calibration split (L1 builds several variants per listing, and several needs share a product; those are dependent), and product-disjoint calibration and test splits. The guarantee is about $\mathcal{D}$; a different test population (natural listings when calibrating on L1, unseen brands when calibrating on seen ones) is a shift that A1 does not cover.

---

## 2. The URR guarantee

### Theorem 1 (finite-sample control of URR and URJ)

Let $\Theta = (\theta_1, \theta_2, \dots, \theta_M)$ be a finite sequence of parameters fixed before the calibration labels are seen (it may be chosen on a separate tuning split). For each $\theta$, let $N^{\mathrm{rec}}_\theta$ be the number of calibration items recommended and $B^{\mathrm{rec}}_\theta$ the number of those with $\tilde Y = 0$; define $N^{\mathrm{rej}}_\theta, B^{\mathrm{rej}}_\theta$ likewise for rejections and $\tilde K = 0$. Define

$$
p^{\mathrm{rec}}_\theta = F_{\mathrm{Bin}(N^{\mathrm{rec}}_\theta,\ \alpha)}\big(B^{\mathrm{rec}}_\theta\big), \qquad
p^{\mathrm{rej}}_\theta = F_{\mathrm{Bin}(N^{\mathrm{rej}}_\theta,\ \alpha')}\big(B^{\mathrm{rej}}_\theta\big), \qquad
p_\theta = \max\big(p^{\mathrm{rec}}_\theta, p^{\mathrm{rej}}_\theta\big),
$$

with $p = 1$ when the count is zero, and $F_{\mathrm{Bin}(m,a)}$ the binomial CDF. Test $\theta_1, \theta_2, \dots$ in order and stop at the first $p_{\theta_j} > \delta$; let $\hat\Theta$ be the set of parameters tested before stopping. Under A1, with labels $\tilde Y = Y^\*$, $\tilde K = K^\*$ (true on L1):

$$
\Pr\Big(\exists\, \theta \in \hat\Theta:\ \mathrm{URR}(\theta) > \alpha \ \text{ or }\ \mathrm{URJ}(\theta) > \alpha'\Big) \le \delta .
$$

So any $\hat\theta \in \hat\Theta$, in particular the one with the highest calibration coverage, satisfies $\mathrm{URR}(\hat\theta) \le \alpha$ and $\mathrm{URJ}(\hat\theta) \le \alpha'$ with probability at least $1 - \delta$ over the calibration draw.

**Proof.** *Validity of each p-value.* Fix $\theta$. Whether a calibration item is recommended depends only on that item (the verifier is fixed), so under A1, conditional on $N^{\mathrm{rec}}_\theta = m$, the recommended items are $m$ i.i.d. draws from $\mathcal{D}$ conditioned on $d_\theta = \text{recommend}$. Hence $B^{\mathrm{rec}}_\theta \mid N^{\mathrm{rec}}_\theta = m \sim \mathrm{Bin}(m, \mathrm{URR}(\theta))$. Under the null $H^{\mathrm{rec}}_\theta: \mathrm{URR}(\theta) > \alpha$, $\mathrm{Bin}(m, \mathrm{URR}(\theta))$ stochastically dominates $\mathrm{Bin}(m, \alpha)$, so $\Pr(p^{\mathrm{rec}}_\theta \le u \mid N^{\mathrm{rec}}_\theta = m) \le u$ for all $u$, and averaging over $m$ gives $\Pr(p^{\mathrm{rec}}_\theta \le u) \le u$. The same argument applies to $p^{\mathrm{rej}}_\theta$. *Union null.* Let $H_\theta = H^{\mathrm{rec}}_\theta \cup H^{\mathrm{rej}}_\theta$. If $H_\theta$ is true, at least one component null is true, and $p_\theta$ is at least that component's p-value, so $p_\theta$ is valid for $H_\theta$. *Fixed-sequence testing.* Let $j^\*$ be the first index with $H_{\theta_{j^\*}}$ true (a population fact, not random). Some true null is in $\hat\Theta$ only if the procedure passes index $j^\*$, which requires $p_{\theta_{j^\*}} \le \delta$, an event of probability at most $\delta$. $\square$

**Remarks.**

1. *This is an instantiation of LTT* (Angelopoulos, Bates, Candès, Jordan & Lei) with the selective-risk p-value of Geifman & El-Yaniv's SGR. The paper should say so. What it adds is the object (a conjunctive three-way decision), not the calibration algorithm.
2. *No monotonicity is needed.* URR need not decrease as $\lambda$ grows (it often doesn't at the strict end, where a few confident errors dominate). Fixed-sequence testing stays valid; non-monotonicity only costs power.
3. *Coverage collapse is a sequencing problem, and it is avoidable.* If the sequence starts at a threshold that recommends almost nothing, its p-value is near 1 and testing stops at once. In the synthetic check, starting at the strictest grid point certified nothing in 1,000 of 1,000 runs; choosing the start on a 20% tuning split certified a threshold in 875 runs, with true URR above α in 5.9% of runs (δ = 10%). The plan's "minimum selection count $N_{\mathrm{rec}} \ge n_{\min}$" rule is valid only in this form: pick the start (or skip thresholds) using held-apart data or a rule fixed in advance. Skipping thresholds based on the *same* calibration counts and then continuing the sequence is not covered by the proof. Under Bonferroni (test every $\theta$ at $\delta / M$, no sequence) setting $p_\theta = 1$ whenever $N_\theta < n_{\min}$ is always valid.
4. *What "exact" means on L1.* Plan §11.2 says URR ≤ α "holds exactly" on constructed items. The labels are exact; the guarantee is still probabilistic (1 − δ) and population-level. Use "holds with probability at least 1 − δ for items drawn like the calibration items".

### How many calibration items (from `theory_checks.py`, δ = 0.05)

| α | Recommended items needed if none is unsupported | Recommended items for 80% power when true URR = α/2 | Calibration items at 10% coverage |
|---|---|---|---|
| 0.05 | 59 | 390 | ≈ 3,900 |
| 0.10 | 29 | 179 | ≈ 1,790 |
| 0.20 | 14 | 82 | ≈ 820 |

Coverage enters directly: at the 6.65% the simulated run reported, α = 0.05 needs about 5,900 independent calibration products. With one item per product (A1), this is a constraint on the G0 count, not only on compute. Recommendation: report α = 0.10 as the headline operating point and α = 0.05 as a secondary point if the L2 pool allows it.

### Algorithm 1 (what `04-implementation` should build)

1. Split the calibration products into *tune* (20%) and *test* (80%), one item per product.
2. On *tune*, fix the grid $\Theta$ and the order (strict to lenient along a path through $(\lambda, \tau)$), starting at the strictest point that recommends at least $n_{\min}$ (e.g. 30) tune items after rescaling.
3. On *test*, run fixed-sequence testing with $p_\theta$ from Theorem 1.
4. Return the certified $\theta$ with the highest test coverage, or "no certified threshold" (the system then abstains on everything and says so).
5. Report: certified $\hat\theta$, its empirical URR and URJ with Clopper-Pearson intervals on the held-out test set, coverage, and the risk–coverage curve with the certified region marked.

---

## 3. Labels without annotators: the ε correction

On natural listings (L2) the labels come from a parser, so Theorem 1 certifies URR *against the parser*. Write $\widetilde{\mathrm{URR}}(\theta) = \Pr(\tilde Y = 0 \mid d_\theta = \text{rec})$.

### Theorem 2 (single-parser labels)

For every $\theta$,

$$
\mathrm{URR}(\theta) \;\le\; \widetilde{\mathrm{URR}}(\theta) + \varepsilon^+_{\mathrm{rec}}(\theta), \qquad
\varepsilon^+_{\mathrm{rec}}(\theta) := \Pr\big(\tilde Y = 1,\ Y^\* = 0 \mid d_\theta = \text{rec}\big) \;\le\; \frac{\varepsilon^+}{\Pr(d_\theta = \text{rec})},
$$

where $\varepsilon^+ = \Pr(\tilde Y = 1, Y^\* = 0)$ is the marginal **false-entailed** rate. Combined with Theorem 1 (calibrated on $\tilde Y$), with probability ≥ 1 − δ, $\mathrm{URR}(\hat\theta) \le \alpha + \varepsilon^+_{\mathrm{rec}}(\hat\theta)$.

**Proof.** $\Pr(Y^\*=0 \mid \text{rec}) = \Pr(Y^\*=0, \tilde Y=0 \mid \text{rec}) + \Pr(Y^\*=0, \tilde Y=1 \mid \text{rec}) \le \widetilde{\mathrm{URR}} + \varepsilon^+_{\mathrm{rec}}$. For the second inequality, $\Pr(A \mid \text{rec}) = \Pr(A \cap \text{rec}) / \Pr(\text{rec}) \le \Pr(A)/\Pr(\text{rec})$. The bound holds for each fixed $\theta$ as an identity between population quantities, so it holds at the data-chosen $\hat\theta$ on the event of Theorem 1. $\square$

**What this changes relative to the plan.**

- Only one error direction matters: items the parser calls supported that aren't. Parser errors in the other direction make calibration conservative, never invalid. The plan's ε (all errors) overstates the correction in one way and the ε / P(rec) form overstates it in another.
- The errors that matter are the ones *on recommended items*, and they are not a random sample of parser errors: the verifier is likely fooled by the same surface cues as the parser ("gentle" read as fragrance-free). In the synthetic check, a 5% marginal false-entailed rate became a 10.5% selective rate (bound: 17.4%), so a 1.6% URR against parser labels was a 12.1% true URR. The naive α + ε would have reported 6.6%.

### Theorem 3 (consensus labels make the correction second-order)

Let $\tilde Y^A, \tilde Y^B$ be labels from two extractors (the rule-based parser and an LLM extractor from a different model family than the verifier, as plan §11.3 proposes), and calibrate on the **consensus label** $\tilde Y^\wedge = \tilde Y^A \tilde Y^B$ (supported only if both say so). Then for every $\theta$,

$$
\mathrm{URR}(\theta) \;\le\; \widetilde{\mathrm{URR}}{}^\wedge(\theta) + \Pr\big(\tilde Y^A = 1, \tilde Y^B = 1, Y^\* = 0 \mid \text{rec}\big).
$$

If, given $Y^\* = 0$, extractor B's labels are independent of extractor A's labels and of the recommendation event (assumption **A2**), the residual equals $\varepsilon^{+,A}_{\mathrm{rec}}(\theta)\, e_B$, where $e_B = \Pr(\tilde Y^B = 1 \mid Y^\* = 0)$. So with probability ≥ 1 − δ,

$$
\mathrm{URR}(\hat\theta) \;\le\; \alpha + \varepsilon^{+,A}_{\mathrm{rec}}(\hat\theta)\, e_B \;\le\; \alpha + e_B .
$$

Without A2 the residual is still at most $\min\big(\varepsilon^{+,A}_{\mathrm{rec}}, \varepsilon^{+,B}_{\mathrm{rec}}\big)$, so consensus is never worse than either extractor alone.

**Proof.** Same decomposition as Theorem 2 with $\tilde Y^\wedge$ in place of $\tilde Y$; $\tilde Y^\wedge = 1$ iff both labels are 1. Under A2, $\Pr(\tilde Y^A=1, \tilde Y^B=1, Y^\*=0 \mid \text{rec}) = \Pr(\tilde Y^A=1, Y^\*=0 \mid \text{rec})\Pr(\tilde Y^B = 1 \mid Y^\*=0, \tilde Y^A = 1, \text{rec}) = \varepsilon^{+,A}_{\mathrm{rec}}\, e_B$. $\square$

**Notes.** A2 asks only that the *second* extractor's mistakes be unrelated to the verifier's and the parser's, which is why it should be a different model family and should not see the parser's output. A2 is untestable without truth, so the paper must state it and report results across a range of $e_B$. The price of consensus is coverage: truly supported items where either extractor says "not supported" count as unsupported, which makes calibration more conservative but never invalid. In the synthetic check, where the verifier shares extractor A's blind spot, consensus cut the residual from 0.105 to 0.010.

### Lemma 1 (estimating the correction from disagreement)

If, given $Y^\*$ and the recommendation event, the two extractors' errors are independent, and fewer than half of the unsupported recommended items are false-entailed by A ($\Pr(\tilde Y^A = 1 \mid Y^\*=0, \text{rec}) \le 1/2$), then $\varepsilon^{+,A}_{\mathrm{rec}} \le \Pr(\tilde Y^A \ne \tilde Y^B \mid \text{rec})$.

**Proof.** Write $a = \Pr(\tilde Y^A=1 \mid Y^\*=0, \text{rec})$, $b$ likewise for B. Then $\Pr(\tilde Y^A \ne \tilde Y^B \mid \text{rec}) \ge \Pr(Y^\*=0 \mid \text{rec})\,[a(1-b) + b(1-a)]$ and $a(1-b) + b(1-a) - a = b(1-2a) \ge 0$ when $a \le 1/2$. Multiply out: the right side is at least $\Pr(Y^\*=0 \mid \text{rec})\,a = \varepsilon^{+,A}_{\mathrm{rec}}$. $\square$

The condition $a \le 1/2$ fails exactly in the worrying case, where the verifier recommends mostly the items the parser gets wrong. The synthetic check shows this (disagreement 0.097 < $\varepsilon^{+,A}_{\mathrm{rec}}$ = 0.105). So disagreement is a diagnostic, not a bound to lean on; Theorem 3's consensus labels need the weaker assumption and should be the primary design. Estimate disagreement on a held-apart audit split at $\hat\theta$ with a Clopper-Pearson upper bound, and add its failure probability to δ.

### What the natural-listing claim can and can't be

- **L1 calibration does not transfer to natural listings.** Constructed variants and natural listings are different distributions, and A1 fails across them. A threshold calibrated on L1 has no guarantee on L2. The deployed threshold should be calibrated on L2 consensus labels (Theorem 3); L1 stays the exact, controlled setting for training, ablations and the constructed-variant claim. If both are pooled, the guarantee is for the pooled mixture.
- **The L2 pool is filtered** (kept only when visible text and `details` agree). The guarantee covers listings that pass that filter. At deployment the `details` half of the filter can't be applied, so deployed listings include the ambiguous ones the pool dropped. State this as the main remaining gap, and report URR on dropped-but-labelable items separately if L1 construction can label any of them.

---

## 4. Why the conjunction matters (the result R1 asked for)

### Proposition 4 (per-constraint calibration does not control item-level URR)

Suppose each constraint is calibrated separately, so that $\Pr(s_i \ne \mathsf{E} \mid J_i) \le \alpha$ for every $i$, where $J_i$ is the event that constraint $i$ is judged entailed, and the item is recommended on $J = \bigcap_i J_i$.

(a) For any $\alpha > 0$ and $k \ge 2$ there are distributions where every per-constraint rate is at most $\alpha$ and $\mathrm{URR} = \Pr(\exists i: s_i \ne \mathsf{E} \mid J) = 1$.

(b) If the pairs $(J_i, s_i)$ are independent across constraints, $\mathrm{URR} = 1 - \prod_i (1 - a_i)$ with $a_i = \Pr(s_i \ne \mathsf{E} \mid J_i)$. At $a_i = \alpha = 0.05$: 9.8% for $k=2$, 18.5% for $k=4$, 22.6% for $k=5$.

**Proof.** (a) Take $k=2$. Let $J_1$ hold on every item, with $s_1 \ne \mathsf{E}$ on a set $S$ of probability $\alpha$; so $\Pr(s_1 \ne \mathsf{E} \mid J_1) = \alpha$. Let $J_2$ hold on a subset of $S$ of probability $\rho \in (0, \alpha]$ and let $s_2 = \mathsf{E}$ everywhere; so $\Pr(s_2 \ne \mathsf{E} \mid J_2) = 0$. Then $J = J_2 \subseteq S$, so every recommended item has $s_1 \ne \mathsf{E}$. Larger $k$: add constraints that are always judged and truly entailed. (b) Under independence, $\Pr(\forall i: s_i = \mathsf{E} \mid J) = \prod_i \Pr(s_i = \mathsf{E} \mid J_i)$. $\square$

**Why it matters.** It formalises the proposal's "a single confidence score hides the asymmetry": per-attribute checking (what a per-attribute conformal filter or a "check each requirement" prompt does) leaves item-level risk uncontrolled, and the failure grows with need length. Calibrating the item-level $\min$ score (Theorem 1) is what closes it. It also predicts an RQ1 result worth testing: URR of constraint-by-constraint verifiers should rise with $k$.

### Proposition 5 (a marginal guarantee is weaker than a selective one)

Let $M(\theta) = \Pr(d_\theta = \text{rec},\ Y^\* = 0) = \mathrm{URR}(\theta)\Pr(d_\theta = \text{rec})$. Then $\mathrm{URR} \le \alpha \Rightarrow M \le \alpha$, but $M \le \alpha$ allows $\mathrm{URR} = \min\big(1, \alpha / \Pr(\text{rec})\big)$, and this is attained.

**Proof.** The identity gives both directions; for attainment, put the whole unsupported mass $\alpha$ inside the recommended set. $\square$

A marginal guarantee counts every abstention as a success. At 20% coverage, $M \le 0.05$ allows one in four recommendations to be unsupported. The shopper who receives a recommendation cares about the selective rate.

### Proposition 6 (CRC does not apply directly)

$\mathrm{URR}(\theta) \le \alpha$ iff $\mathbb{E}[L_\theta(Z)] \le 0$ with $L_\theta = \mathbb{1}\{d_\theta = \text{rec}\}(\mathbb{1}\{Y^\*=0\} - \alpha)$. But $L_\theta$ is not monotone in $\lambda$: raising $\lambda$ removes a supported item's recommendation and *raises* its loss from $-\alpha$ to $0$. Conformal risk control requires a loss that is monotone in the parameter, so it does not cover URR. LTT does, because it only needs valid p-values. $\square$

---

## 5. The two-sided guarantee: shoppers and new products

### Theorem 4 (group-wise URR and a bounded exposure gap, jointly)

Let $\theta = (\lambda_{\text{new}}, \lambda_{\text{est}}, \tau)$, with group-specific recommendation thresholds (shared thresholds are the special case $\lambda_{\text{new}} = \lambda_{\text{est}}$). Define the **exposure gap on supported items**

$$
\Delta(\theta) = \mathrm{Cov}_{\text{est}}(\theta) - \mathrm{Cov}_{\text{new}}(\theta).
$$

For each $\theta$ compute: the Theorem 1 p-values for $\mathrm{URR}_{\text{new}}$, $\mathrm{URR}_{\text{est}}$ (the URR among recommended items of that group) and URJ; and, with $n_g$ supported calibration items in group $g$ of which $X_g$ are recommended, $p^\Delta_\theta = \inf\{u: \mathrm{UCB}_{\text{est}}(u/2) - \mathrm{LCB}_{\text{new}}(u/2) \le \beta\}$ (1 if no such $u$), where UCB and LCB are one-sided Clopper-Pearson bounds at the stated miscoverage. Let $p_\theta$ be the maximum of the four, and run fixed-sequence (or Bonferroni) testing as in Theorem 1. Under A1, with probability at least $1 - \delta$, every certified $\theta$ satisfies simultaneously

$$
\mathrm{URR}_{\text{new}}(\theta) \le \alpha,\quad \mathrm{URR}_{\text{est}}(\theta) \le \alpha,\quad \mathrm{URR}(\theta) \le \alpha,\quad \mathrm{URJ}(\theta) \le \alpha',\quad \Delta(\theta) \le \beta .
$$

**Proof.** *Gap p-value.* Given $n_{\text{est}}, n_{\text{new}}$, the counts are independent with $X_g \sim \mathrm{Bin}(n_g, \mathrm{Cov}_g)$. If $\Delta > \beta$ and $p^\Delta \le u$, then $\mathrm{UCB}_{\text{est}}(u/2) - \mathrm{LCB}_{\text{new}}(u/2) \le \beta < \mathrm{Cov}_{\text{est}} - \mathrm{Cov}_{\text{new}}$ (using that the bounds tighten monotonically as $u$ grows), so either the upper bound misses $\mathrm{Cov}_{\text{est}}$ or the lower bound misses $\mathrm{Cov}_{\text{new}}$, each with probability at most $u/2$. *Overall URR.* $\mathrm{URR} = \sum_g \Pr(G=g \mid \text{rec})\,\mathrm{URR}_g$ is an average of the group rates, so it is at most α when both are. The rest is Theorem 1 with a four-way union null. $\square$

The synthetic check (true gap 0.12, β = 0.10) falsely certified the gap in 0.2% of 2,000 runs at δ = 0.10: valid and, at these sample sizes, conservative.

**Why the gap is defined on supported items.** A new product whose listing omits its skin type *should* be abstained on; that is the seller-fix channel (H5), not unfairness. Conditioning on $Y^\* = 1$ isolates the matcher's own bias: it measures whether equally well-evidenced listings from unfamiliar brands are recommended less often. The raw abstention gap, which mixes in listing quality, should be reported descriptively next to it.

### Proposition 7 (feasibility and levelling down)

(a) With shared thresholds, the constraints can be infeasible: if the verifier's entailment scores on supported items are stochastically lower for new brands, every shared $\lambda$ with $\mathrm{URR} \le \alpha$ may have $\Delta > \beta$. The procedure then certifies nothing, which is the honest output (R1's question "what happens when the two are infeasible" has this answer).

(b) With group thresholds, $\Delta \le \beta$ can always be met by raising $\lambda_{\text{est}}$, that is, by recommending fewer established products without recommending more new ones. Theorem 4 certifies such a $\theta$ without complaint.

**Proof.** (a) Example: supported-item scores $\sim U[0.5, 1]$ for established and $U[0.3, 0.8]$ for new, with unsupported scores spread over $[0, 0.5]$ in both, so URR ≤ α forces $\lambda$ close to 0.5 or above. For $\lambda \in [0.5, 0.8]$, $\mathrm{Cov}_{\text{est}} = 2(1 - \lambda)$ and $\mathrm{Cov}_{\text{new}} = 2(0.8 - \lambda)$, so $\Delta = 0.4$. For $\lambda > 0.8$, $\mathrm{Cov}_{\text{new}} = 0$ and $\Delta = 2(1-\lambda)$, which is ≤ β only when $\lambda \ge 1 - \beta/2$. So with β < 0.4 every shared threshold that meets the gap constraint recommends no new products at all, and the strictest ones recommend almost nothing, which Theorem 1 cannot certify. (b) $\mathrm{Cov}_{\text{est}}$ is non-increasing in $\lambda_{\text{est}}$ and reaches 0. $\square$

**What to do about (b).** Select among certified parameters lexicographically (highest $\mathrm{Cov}_{\text{new}}$ first, then highest $\mathrm{Cov}_{\text{est}}$), and report $\mathrm{Cov}_{\text{est}}$ at the unconstrained optimum next to the certified one, so any levelling down is visible. Group thresholds also mean the calibration layer uses brand size, which the verifier never sees; that is a policy choice to state in the paper.

**Wording.** Replace "provably does not disadvantage new products" with: *"with probability at least 1 − δ, among listings whose evidence supports the need, unfamiliar products are recommended at most β less often than established ones, while URR ≤ α holds in each group."*

**Label noise in the gap.** On L2, coverage is computed on $\tilde Y^\wedge = 1$ items. False-entailed labels add unsupported items to the denominator; if their rate differs by group, $\Delta$ is biased. Use L1 (exact labels) as the primary population for Theorem 4, and L2 as a check.

---

## 6. Positioning against the closest guarantees

| | Mohri & Hashimoto 2024 (conformal factuality) | Angelopoulos et al. 2024 (CRC) | Angelopoulos et al. (LTT) | Geifman & El-Yaniv 2017 (SGR) | Rubin-Toles et al. 2025 | **This work** |
|---|---|---|---|---|---|---|
| Object | Generated text, split into claims | Any prediction set | Any parameterised predictor | Classifier with reject option | Reasoning chain | **Recommend / reject / abstain decision on a conjunctive need** |
| What a correct label means | Claim is true (entailed by a reference answer) | Task-defined | Task-defined | Prediction is correct | Step is true and deducible from retained steps | **Every constraint entailed by the visible listing**, true or not |
| Risk controlled | Marginal: P(output contains a false claim), counting fully backed-off outputs as safe | Expected monotone loss | Any risk, via p-values | Selective error | Marginal, over the graph | **Selective URR, plus URJ and group-wise URR** |
| Safe fallback | Drop claims until the rest is safe; output stays useful | Larger set | Task-defined | Reject | Drop sub-graphs | **Abstain on the whole item: a constraint can't be dropped, because that changes the shopper's need** |
| Monotone loss needed | Yes (nested back-off) | Yes | No | No (per threshold) | Yes | No (Prop 6) |
| Group / fairness constraint | No | No | Possible, not studied | No | No | **Exposure gap on supported items (Thm 4)** |
| Label noise | Labels assumed correct | Assumed | Assumed | Assumed | Assumed | **Selective ε and consensus labels (Thms 2–3)** |
| Strategic inputs | No | No | No | No | No | **Disclosure incentives (Props 8–11); robustness only as measured (Prop 12)** |

The two lines the paper needs:

1. *Against Mohri & Hashimoto.* Their label is truth-relative and their risk is marginal with a useful back-off; ours is evidence-relative and selective, over a conjunction that admits no partial output. A true but unstated attribute passes their guarantee and fails ours (that is the definition), and Prop 5 shows their marginal form at α permits a selective rate of α / coverage. The approach is borrowed; the guarantee is about a different object.
2. *Against CRC and LTT.* We use LTT, not CRC, because the URR loss is non-monotone (Prop 6). The calibration algorithm is theirs; our contribution is what is calibrated (conjunctive, evidence-relative, three-way, group-wise) and what the labels can and can't certify without annotators.

*To check before submission:* the exact factuality definition and risk statement in Mohri & Hashimoto (§2–3 of the paper), and LTT's venue (arXiv:2110.01052; a journal version may exist). The wiki entries were written from abstracts.

---

## 7. Disclosure: when complete specs become the seller's best move

### Model

A seller knows its product's attribute values $\vartheta = (\vartheta_j)_{j \in \mathcal{J}}$ and chooses which attributes to state, $D \subseteq \mathcal{J}$; everything else is left out or blurred ("gentle", "suitable for most skin"). Demand is a set of needs with weights $w(R) \ge 0$; each need constrains attributes $\mathrm{attr}(R)$, and $\vartheta \models R$ means the product meets it. The seller's payoff is the expected recommendation mass minus disclosure costs $c(D) = \sum_{j \in D} c_j$ (writing, testing, certification).

**Assumption H (hard evidence).** Stated values are true. This is a modelling assumption: false specs contradict `details`, cause returns and draw platform enforcement, but nothing in the matcher enforces truth.

**Oracle verifier.** Recommends need $R$ iff $\mathrm{attr}(R) \subseteq D$ and $\vartheta \models R$; rejects iff some stated attribute violates $R$. So the gross payoff is $V(D) = \sum_R w(R)\,\mathbb{1}\{\mathrm{attr}(R) \subseteq D\}\,\mathbb{1}\{\vartheta \models R\}$.

### Proposition 8 (complete disclosure is weakly dominant under the support rule)

Under H and an oracle verifier with $c = 0$, $V$ is non-decreasing in $D$, so $D = \mathcal{J}$ is a weakly dominant strategy for every product. It is strictly better than $D$ iff some need with positive weight that the product meets touches an attribute outside $D$.

**Proof.** A term of $V$ can only switch from 0 to 1 as $D$ grows. $\square$

This is the classic unravelling result (Grossman 1981; Milgrom 1981) with one difference worth stating: it is *dominance*, not equilibrium. The classic result needs a Bayesian receiver who reasons that silence signals bad news. The support rule installs that scepticism mechanically, so no reasoning about the seller's strategy is needed.

### Proposition 9 (complementarity: one fix pulls in others)

$V$ is supermodular in $D$. Hence the seller's optimal disclosure set $D^\*(c) \in \arg\max_D V(D) - c(D)$ is monotone in costs (Topkis): lowering any $c_j$ weakly enlarges the largest optimal set, possibly adding *other* attributes. The seller's problem is a supermodular maximisation and is solvable in polynomial time.

**Proof.** Each term $\mathbb{1}\{A \subseteq D\}$ has marginal value of adding $j \notin D$ equal to $\mathbb{1}\{j \in A,\ A \setminus \{j\} \subseteq D\}$, which is non-decreasing in $D$. Sums of supermodular functions with non-negative weights are supermodular, and subtracting a modular cost keeps it so. Monotone comparative statics follow from Topkis's theorem; maximising a supermodular function is minimising a submodular one. $\square$

**Why it matters for the seller-feedback loop (H5).** A "state your skin type" fix lowers the effective cost of one attribute. Because needs are conjunctions, it can make disclosing scent and size worthwhile too, which a seller ignored while skin type was missing. This predicts that simulated fixes in H5 should raise coverage by more than the sum of single-attribute effects, a testable claim.

### Proposition 10 (a prior-licensing matcher sustains concealment and favours incumbents)

Suppose instead the matcher recommends on an unstated attribute when a fixed prior $\pi_j(\text{brand}) = \Pr(\vartheta_j \text{ fits} \mid \text{brand, category})$ is at least $\tau$ (a model of an LLM using memorised brand knowledge, not updated on sellers' behaviour). Then (a) an established-brand product whose attribute fails a popular need with $\pi_j \ge \tau$ strictly prefers to stay silent, earning recommendations it does not deserve; (b) a new-brand product with an uninformative prior ($\pi_j < \tau$) earns nothing when silent, so it must disclose to be matched while an incumbent need not.

**Proof.** (a) Silence yields the need's weight; disclosure yields a rejection. (b) Silence yields 0 on needs touching $j$. $\square$

This is the formal version of the liability-of-newness argument: a prior-licensing matcher gives incumbents a disclosure exemption that new brands don't get, and the support rule removes it.

### Proposition 11 (with a foolable verifier, honesty pays only above a fit threshold)

Take one attribute $j$, with all other constraints of the relevant needs stated and entailed. Let $W_{\text{fit}}$ and $W_{\text{non}}$ be the weights of needs on $j$ that the product does and doesn't meet, and $s = W_{\text{fit}} / (W_{\text{fit}} + W_{\text{non}})$ its **fit share**. The verifier reads a stated true value as entailed with probability $1-q$ (else unresolved), misreads a stated non-fitting value as entailed with probability $r$, and accepts vague text as entailing *any* need on $j$ with probability $p$ (pseudo-evidence acceptance). Under H, stating the true value is a best response iff

$$
s \;\ge\; \frac{p - r}{1 - q - r}.
$$

**Proof.** Stating yields $(1-q)W_{\text{fit}} + r W_{\text{non}}$; vagueness yields $p(W_{\text{fit}} + W_{\text{non}})$. Divide by $W_{\text{fit}} + W_{\text{non}}$ and rearrange (assuming $1 - q - r > 0$). $\square$

**Reading.** Niche products (small $s$, e.g. a fragrance-free product when most needs ask for a scent) gain most from blurring, and new indie brands are disproportionately niche. With $q = 0.1$, $r = 0$: a 10% fooling rate means products fitting less than 11% of attribute demand prefer vague listings. Verifier robustness to pseudo-evidence (mock review R4.4) is therefore not only an accuracy issue: it sets which sellers the matcher pushes toward honest disclosure. Theorem 1 gives a partial handle on $p$: by Bayes' rule, the acceptance rate averaged over all unsupported calibration-distribution items is $\Pr(\text{rec} \mid Y^\*=0) \le \alpha \Pr(\text{rec}) / \Pr(Y^\*=0)$ at $\hat\theta$. That is an average over unsupported items, not the rate for the most persuasive vague phrasing, and it holds only for the vagueness found in the calibration data; a seller searching for the most persuasive blur is outside it (Prop 12).

**Wording.** Replace "the matcher makes honest, complete listings the seller's best response" with: *"Under the support rule, stating true specs weakly dominates omitting them, and strictly so for products that meet some demanded need. With a verifier that accepts vague text at rate p, this holds for products whose fit share exceeds p / (1 − q). Truthfulness itself is assumed, not induced."* Plan §10.2 already keeps this in the appendix, which is the right place.

---

## 8. Strategic rewrites: what survives

### Proposition 12

Let $\mathcal{R}_0$ be the rewrites that leave every constraint's true support status unchanged ("no new checkable evidence": marketing language, brand swaps, vague words).

(a) For an oracle verifier ($e_i = \mathbb{1}\{s_i = \mathsf{E}\}$, $c_i = \mathbb{1}\{s_i = \mathsf{C}\}$), decisions and URR are invariant under every $\rho \in \mathcal{R}_0$.

(b) For a learned verifier facing a seller who picks $\rho \in \mathcal{R}_0$ to get recommended, let $\nu(\theta) = \Pr(\exists \rho \in \mathcal{R}_0: d_\theta(\rho(x)) = \text{rec},\ d_\theta(x) \ne \text{rec},\ Y^\* = 0)$ be the **invariance-violation rate**. Then the unsupported-recommendation mass under attack is at most $\mathrm{URR}(\theta)\Pr(d_\theta = \text{rec}) + \nu(\theta)$.

**Proof.** (a) Decisions depend only on support statuses, which $\rho$ preserves. (b) An unsupported item recommended under attack was either recommended before (mass at most $\mathrm{URR} \cdot \Pr(\text{rec})$) or was flipped into a recommendation by some $\rho$ (mass at most $\nu$). $\square$

So "robust by construction" is a property of the *rule*, not of the system. What can be claimed is (a), plus a measured $\nu$ under a stated attack set (pseudo-evidence, GEO-style rewrites, brand swaps). Calibrating on a fixed distribution of rewritten listings gives a Theorem 1 guarantee for *that* distribution only; an adaptive seller who sees the verifier's responses is outside every result here (performative shift, Perdomo et al. 2020). Plan §10.2 already cuts the general robustness bound from the main paper; keep it that way.

---

## 9. What the plan should change

This PR doesn't edit `is-topic/refined-thesis-plan.md`. Suggested edits, by section (section numbers as in the merged plan):

1. **§11.2, bullet 1.** "URR ≤ α holds exactly" → "holds with probability at least 1 − δ for items drawn like the calibration items (one item per product)."
2. **§11.2, bullet 2.** Replace with: "Calibrated on L2 consensus labels from two extractors (§11.3), the true URR is at most α plus the rate at which both extractors call an unsupported recommended item supported; under the independence assumption of Theorem 3 this is at most $\varepsilon^{+,A}_{\mathrm{rec}} \cdot e_B$. With a single parser the correction is first-order, $\varepsilon^+_{\mathrm{rec}} \le \varepsilon^+ / P(\text{rec})$, counting only false-entailed errors." Drop "condition calibration on $N_{\mathrm{rec}} \ge n_{\min}$" or replace with "choose the start of the threshold sequence on a held-apart tuning split" (Theorem 1, remark 3).
3. **§11.1 table.** L1 stays the primary set for training, ablations and the constructed-variant claim; **the deployed threshold for natural listings is calibrated on L2 consensus labels**, because an L1-calibrated threshold has no guarantee on natural listings. Add: one item per product in calibration; product-disjoint splits.
4. **§11.3.** Make consensus labelling the primary use of the second extractor; disagreement becomes a diagnostic (Lemma 1's condition fails in exactly the case that matters).
5. **§9A.** "Robust by construction" → Prop 12 wording. Disclosure → Prop 11 wording; keep it in the appendix.
6. **§9B.** Define the exposure gap on supported items; decide shared vs group-specific thresholds; add the levelling-down report (Prop 7).
7. **§10.2 theory row.** "Thm 4 finite-sample URR + exposure-gap bound" → "Thm 1 (LTT instantiation, stated as such) and Thm 4 (group-wise)". Add **Prop 4 (conjunction)** as the non-obvious result R1 asked for, with its RQ1 prediction (URR rises with need length $k$ for constraint-by-constraint verifiers). Following R1, present the proposal's separation and VOI-blindness results as propositions motivating the design.
8. **§10.3 / G0.** Add the sample-size table (§2): α = 0.05 at 80% power needs ≈ 390 recommended calibration items, so ≈ 3,900 independent products at 10% coverage. Headline α = 0.10 unless G0 shows a large L2 pool.
9. **§10.7, item 2.** "URR ≤ α on the held-out test set across seeds" → "the certified threshold's held-out URR, with Clopper-Pearson intervals, is at most α across calibration resamples in at least a 1 − δ share", which is what Theorem 1 actually predicts.
10. **Citations to add to 02-literature-review:** Learn-then-Test (Angelopoulos, Bates, Candès, Jordan & Lei, arXiv:2110.01052); Clopper & Pearson 1934; Topkis 1978 (*Operations Research*, supermodularity); Grossman 1981; Milgrom 1981; Perdomo et al. 2020; Vovk's Mondrian conformal prediction (group-conditional guarantees). Geifman & El-Yaniv 2017, Mohri & Hashimoto 2024, Angelopoulos et al. 2024 and Rubin-Toles et al. 2025 are already in the wiki.

**Related, outside this file:** the simulated benchmark (`scripts/simulated_mockup_benchmark.py` after the repo cleanup) creates `cal_set` and never uses it (mock review round 2, §1). Algorithm 1 above is the calibration step the real pipeline needs.

## 10. Before this goes in a paper

- **Independent proof check** (plan §10.3 requires one): someone other than the author should re-derive Theorems 1–4 and Props 4, 7 and 9–11.
- **Full-text check** of Mohri & Hashimoto's definitions and of LTT's statement and venue; the comparison table relies on abstract-level reading for those two.
- **Assumptions to state verbatim in the paper:** A1 (i.i.d., one item per product), A2 (second extractor independent given truth), H (hard evidence), the fixed verifier, and the filtered L2 population.
