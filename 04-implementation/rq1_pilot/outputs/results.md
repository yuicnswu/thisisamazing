## All items

Items: 1356 from 399 products. Variants: {'original': 250, 'remove': 250, 'vague': 250, 'remove_prior': 250, 'contradict': 206, 'natural_missing': 150}

**Recommend rate by variant** (product-cluster bootstrap 95% CI). Correct behaviour: original high, every other column 0.

| Matcher | original | remove | vague | remove_prior | contradict | natural_missing | native URR |
|---|---|---|---|---|---|---|---|
| extract__claude-haiku-5-5 | 89% [85%, 93%] | 13% [9%, 17%] | 15% [10%, 20%] | 12% [8%, 16%] | 5% [2%, 8%] | 18% [12%, 25%] | 38% [32%, 44%] |
| keyword__none | 88% [84%, 92%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] |
| naive__claude-haiku-5-5 | 77% [72%, 82%] | 36% [31%, 42%] | 43% [37%, 49%] | 38% [32%, 44%] | 16% [11%, 20%] | 37% [30%, 45%] | 67% [64%, 69%] |
| naive__claude-sonnet-5-5 | 73% [67%, 78%] | 34% [28%, 39%] | 36% [30%, 42%] | 31% [25%, 36%] | 20% [15%, 26%] | 35% [27%, 43%] | 65% [62%, 68%] |
| nesy__claude-haiku-5-5 | 76% [72%, 82%] | 0% [0%, 1%] | 0% [0%, 1%] | 0% [0%, 1%] | 0% [0%, 0%] | 0% [0%, 0%] | 2% [0%, 6%] |
| strict__claude-haiku-5-5 | 81% [76%, 86%] | 10% [7%, 14%] | 12% [8%, 16%] | 9% [6%, 13%] | 7% [4%, 11%] | 10% [5%, 15%] | 35% [28%, 41%] |
| strict__claude-sonnet-5-5 | 73% [67%, 78%] | 10% [6%, 14%] | 12% [9%, 17%] | 10% [6%, 14%] | 8% [5%, 12%] | 9% [5%, 14%] | 38% [32%, 44%] |

**Prior effect** (same product: evidence removed, then famous brand + hype added)

| Matcher | pairs | abstain→recommend | recommend→abstain |
|---|---|---|---|
| extract__claude-haiku-5-5 | 250 | 4 | 6 |
| keyword__none | 250 | 0 | 0 |
| naive__claude-haiku-5-5 | 250 | 22 | 17 |
| naive__claude-sonnet-5-5 | 250 | 19 | 26 |
| nesy__claude-haiku-5-5 | 250 | 0 | 0 |
| strict__claude-haiku-5-5 | 250 | 5 | 8 |
| strict__claude-sonnet-5-5 | 248 | 5 | 5 |

**Learn-then-Test** (50 product splits, 50/50 calibration/test, δ = 0.1). URR and coverage on test, mean [2.5%, 97.5%] across splits; 'viol.' = share of splits with test URR > α.

| Matcher | α | URR | coverage | recall of supported | viol. | no threshold |
|---|---|---|---|---|---|---|
| extract__claude-haiku-5-5 | 0.05 | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% | 100% |
| extract__claude-haiku-5-5 | 0.1 | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% | 100% |
| extract__claude-haiku-5-5 | 0.2 | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% | 100% |
| keyword__none | 0.05 | 0% [0%, 0%] | 16% [15%, 17%] | 88% [85%, 92%] | 0% | 0% |
| keyword__none | 0.1 | 0% [0%, 0%] | 16% [15%, 17%] | 88% [85%, 92%] | 0% | 0% |
| keyword__none | 0.2 | 0% [0%, 0%] | 16% [15%, 17%] | 88% [85%, 92%] | 0% | 0% |
| naive__claude-haiku-5-5 | 0.05 | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% | 100% |
| naive__claude-haiku-5-5 | 0.1 | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% | 100% |
| naive__claude-haiku-5-5 | 0.2 | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% | 100% |
| naive__claude-sonnet-5-5 | 0.05 | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% | 100% |
| naive__claude-sonnet-5-5 | 0.1 | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% | 100% |
| naive__claude-sonnet-5-5 | 0.2 | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% | 100% |
| nesy__claude-haiku-5-5 | 0.05 | 0% [0%, 0%] | 0% [0%, 0%] | 1% [0%, 0%] | 0% | 98% |
| nesy__claude-haiku-5-5 | 0.1 | 2% [0%, 6%] | 7% [0%, 14%] | 35% [0%, 72%] | 0% | 40% |
| nesy__claude-haiku-5-5 | 0.2 | 6% [0%, 14%] | 14% [9%, 18%] | 70% [50%, 84%] | 0% | 0% |
| strict__claude-haiku-5-5 | 0.05 | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% | 100% |
| strict__claude-haiku-5-5 | 0.1 | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% | 100% |
| strict__claude-haiku-5-5 | 0.2 | 1% [0%, 0%] | 0% [0%, 0%] | 1% [0%, 0%] | 2% | 98% |
| strict__claude-sonnet-5-5 | 0.05 | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% | 100% |
| strict__claude-sonnet-5-5 | 0.1 | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% | 100% |
| strict__claude-sonnet-5-5 | 0.2 | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% | 100% |

## Audited items (construction label and quote judge agree; 267 items dropped)

Items: 1089 from 381 products. Variants: {'original': 221, 'remove': 212, 'vague': 201, 'remove_prior': 214, 'contradict': 109, 'natural_missing': 132}

**Recommend rate by variant** (product-cluster bootstrap 95% CI). Correct behaviour: original high, every other column 0.

| Matcher | original | remove | vague | remove_prior | contradict | natural_missing | native URR |
|---|---|---|---|---|---|---|---|
| extract__claude-haiku-5-5 | 95% [91%, 97%] | 3% [1%, 6%] | 4% [1%, 7%] | 3% [1%, 5%] | 1% [0%, 3%] | 11% [6%, 17%] | 15% [10%, 20%] |
| keyword__none | 89% [85%, 93%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] |
| naive__claude-haiku-5-5 | 82% [77%, 87%] | 30% [24%, 36%] | 33% [27%, 40%] | 33% [27%, 39%] | 3% [0%, 6%] | 31% [23%, 39%] | 57% [53%, 61%] |
| naive__claude-sonnet-5-5 | 77% [71%, 82%] | 26% [20%, 33%] | 27% [21%, 34%] | 24% [19%, 30%] | 6% [2%, 9%] | 27% [20%, 35%] | 54% [50%, 59%] |
| nesy__claude-haiku-5-5 | 82% [77%, 87%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] |
| strict__claude-haiku-5-5 | 90% [86%, 94%] | 1% [0%, 3%] | 1% [0%, 3%] | 0% [0%, 1%] | 0% [0%, 0%] | 2% [0%, 5%] | 5% [2%, 8%] |
| strict__claude-sonnet-5-5 | 80% [75%, 85%] | 2% [0%, 5%] | 3% [1%, 5%] | 2% [0%, 4%] | 0% [0%, 0%] | 2% [0%, 5%] | 10% [5%, 15%] |

**Prior effect** (same product: evidence removed, then famous brand + hype added)

| Matcher | pairs | abstain→recommend | recommend→abstain |
|---|---|---|---|
| extract__claude-haiku-5-5 | 210 | 2 | 3 |
| keyword__none | 210 | 0 | 0 |
| naive__claude-haiku-5-5 | 210 | 20 | 16 |
| naive__claude-sonnet-5-5 | 210 | 18 | 23 |
| nesy__claude-haiku-5-5 | 210 | 0 | 0 |
| strict__claude-haiku-5-5 | 210 | 0 | 2 |
| strict__claude-sonnet-5-5 | 208 | 1 | 2 |

**Learn-then-Test** (50 product splits, 50/50 calibration/test, δ = 0.1). URR and coverage on test, mean [2.5%, 97.5%] across splits; 'viol.' = share of splits with test URR > α.

| Matcher | α | URR | coverage | recall of supported | viol. | no threshold |
|---|---|---|---|---|---|---|
| extract__claude-haiku-5-5 | 0.05 | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% | 100% |
| extract__claude-haiku-5-5 | 0.1 | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% | 100% |
| extract__claude-haiku-5-5 | 0.2 | 5% [0%, 19%] | 6% [0%, 24%] | 24% [0%, 96%] | 0% | 74% |
| keyword__none | 0.05 | 0% [0%, 0%] | 18% [17%, 19%] | 89% [86%, 94%] | 0% | 0% |
| keyword__none | 0.1 | 0% [0%, 0%] | 18% [17%, 19%] | 89% [86%, 94%] | 0% | 0% |
| keyword__none | 0.2 | 0% [0%, 0%] | 18% [17%, 19%] | 89% [86%, 94%] | 0% | 0% |
| naive__claude-haiku-5-5 | 0.05 | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% | 100% |
| naive__claude-haiku-5-5 | 0.1 | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% | 100% |
| naive__claude-haiku-5-5 | 0.2 | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% | 100% |
| naive__claude-sonnet-5-5 | 0.05 | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% | 100% |
| naive__claude-sonnet-5-5 | 0.1 | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% | 100% |
| naive__claude-sonnet-5-5 | 0.2 | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% | 100% |
| nesy__claude-haiku-5-5 | 0.05 | 0% [0%, 0%] | 13% [0%, 17%] | 63% [0%, 85%] | 0% | 16% |
| nesy__claude-haiku-5-5 | 0.1 | 1% [0%, 6%] | 17% [14%, 20%] | 83% [68%, 97%] | 0% | 0% |
| nesy__claude-haiku-5-5 | 0.2 | 5% [0%, 9%] | 20% [18%, 22%] | 95% [90%, 99%] | 0% | 0% |
| strict__claude-haiku-5-5 | 0.05 | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% | 100% |
| strict__claude-haiku-5-5 | 0.1 | 1% [0%, 6%] | 2% [0%, 18%] | 11% [0%, 79%] | 0% | 80% |
| strict__claude-haiku-5-5 | 0.2 | 7% [2%, 12%] | 20% [16%, 21%] | 89% [77%, 95%] | 0% | 0% |
| strict__claude-sonnet-5-5 | 0.05 | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% | 100% |
| strict__claude-sonnet-5-5 | 0.1 | 1% [0%, 9%] | 11% [10%, 16%] | 56% [49%, 74%] | 0% | 0% |
| strict__claude-sonnet-5-5 | 0.2 | 6% [2%, 16%] | 16% [14%, 19%] | 74% [70%, 84%] | 2% | 0% |

## Where the rule parser and the quote judge disagree

Recommend rate. On *parser missed* the judge quotes verbatim support, so recommending is right; on *parser false positive* the judge finds none, so abstaining is right.

| Matcher | parser missed (n=162) | parser false positive (n=29) |
|---|---|---|
| extract__claude-haiku-5-5 | 60% | 45% |
| keyword__none | 0% | 79% |
| naive__claude-haiku-5-5 | 80% | 34% |
| naive__claude-sonnet-5-5 | 80% | 45% |
| nesy__claude-haiku-5-5 | 2% | 31% |
| strict__claude-haiku-5-5 | 61% | 17% |
| strict__claude-sonnet-5-5 | 57% | 17% |
