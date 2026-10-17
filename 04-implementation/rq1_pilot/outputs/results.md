## All items

Items: 1356 from 399 products. Variants: {'original': 250, 'remove': 250, 'vague': 250, 'remove_prior': 250, 'contradict': 206, 'natural_missing': 150}

**Recommend rate by variant** (product-cluster bootstrap 95% CI). Correct behaviour: original high, every other column 0.

| Matcher | original | remove | vague | remove_prior | contradict | natural_missing | native URR |
|---|---|---|---|---|---|---|---|
| extract__claude-haiku-5-5 | 89% [85%, 93%] | 13% [9%, 17%] | 15% [10%, 20%] | 12% [8%, 16%] | 5% [2%, 8%] | 18% [12%, 25%] | 38% [32%, 44%] |
| keyword__none | 88% [84%, 92%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] |
| naive__claude-haiku-5-5 | 77% [72%, 82%] | 36% [31%, 42%] | 43% [37%, 49%] | 38% [32%, 44%] | 16% [11%, 20%] | 37% [30%, 45%] | 67% [64%, 69%] |
| naive__claude-sonnet-5-5 | 73% [67%, 78%] | 34% [28%, 39%] | 36% [30%, 42%] | 31% [25%, 36%] | 20% [15%, 26%] | 35% [27%, 43%] | 65% [62%, 68%] |
| strict__claude-haiku-5-5 | 81% [76%, 86%] | 10% [7%, 14%] | 12% [8%, 16%] | 9% [6%, 13%] | 7% [4%, 11%] | 10% [5%, 15%] | 35% [28%, 41%] |
| strict__claude-sonnet-5-5 | 73% [67%, 78%] | 10% [6%, 14%] | 12% [9%, 17%] | 10% [6%, 14%] | 8% [5%, 12%] | 9% [5%, 14%] | 38% [32%, 44%] |

**Prior effect** (same product: evidence removed, then famous brand + hype added)

| Matcher | pairs | abstain→recommend | recommend→abstain |
|---|---|---|---|
| extract__claude-haiku-5-5 | 250 | 4 | 6 |
| keyword__none | 250 | 0 | 0 |
| naive__claude-haiku-5-5 | 250 | 22 | 17 |
| naive__claude-sonnet-5-5 | 250 | 19 | 26 |
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
| strict__claude-haiku-5-5 | 0.05 | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% | 100% |
| strict__claude-haiku-5-5 | 0.1 | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% | 100% |
| strict__claude-haiku-5-5 | 0.2 | 1% [0%, 0%] | 0% [0%, 0%] | 1% [0%, 0%] | 2% | 98% |
| strict__claude-sonnet-5-5 | 0.05 | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% | 100% |
| strict__claude-sonnet-5-5 | 0.1 | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% | 100% |
| strict__claude-sonnet-5-5 | 0.2 | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% | 100% |

## Audited items (parser and quote judge agree; 47 products dropped)

Items: 1201 from 352 products. Variants: {'original': 223, 'remove': 223, 'vague': 223, 'remove_prior': 223, 'contradict': 179, 'natural_missing': 130}

**Recommend rate by variant** (product-cluster bootstrap 95% CI). Correct behaviour: original high, every other column 0.

| Matcher | original | remove | vague | remove_prior | contradict | natural_missing | native URR |
|---|---|---|---|---|---|---|---|
| extract__claude-haiku-5-5 | 94% [91%, 97%] | 14% [10%, 19%] | 16% [11%, 21%] | 13% [9%, 17%] | 6% [3%, 9%] | 10% [5%, 16%] | 36% [29%, 42%] |
| keyword__none | 89% [84%, 93%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] |
| naive__claude-haiku-5-5 | 81% [76%, 86%] | 38% [30%, 44%] | 45% [38%, 52%] | 39% [33%, 46%] | 17% [12%, 22%] | 29% [22%, 37%] | 65% [62%, 68%] |
| naive__claude-sonnet-5-5 | 77% [71%, 82%] | 34% [28%, 40%] | 38% [31%, 44%] | 33% [27%, 39%] | 20% [14%, 25%] | 27% [19%, 35%] | 64% [60%, 67%] |
| strict__claude-haiku-5-5 | 87% [83%, 91%] | 12% [8%, 16%] | 13% [9%, 18%] | 10% [7%, 14%] | 8% [4%, 13%] | 5% [2%, 9%] | 34% [27%, 40%] |
| strict__claude-sonnet-5-5 | 80% [74%, 85%] | 11% [7%, 15%] | 14% [9%, 18%] | 11% [7%, 15%] | 10% [5%, 14%] | 3% [1%, 6%] | 36% [28%, 43%] |

**Prior effect** (same product: evidence removed, then famous brand + hype added)

| Matcher | pairs | abstain→recommend | recommend→abstain |
|---|---|---|---|
| extract__claude-haiku-5-5 | 223 | 3 | 6 |
| keyword__none | 223 | 0 | 0 |
| naive__claude-haiku-5-5 | 223 | 19 | 15 |
| naive__claude-sonnet-5-5 | 223 | 18 | 21 |
| strict__claude-haiku-5-5 | 223 | 5 | 8 |
| strict__claude-sonnet-5-5 | 222 | 5 | 5 |

**Learn-then-Test** (50 product splits, 50/50 calibration/test, δ = 0.1). URR and coverage on test, mean [2.5%, 97.5%] across splits; 'viol.' = share of splits with test URR > α.

| Matcher | α | URR | coverage | recall of supported | viol. | no threshold |
|---|---|---|---|---|---|---|
| extract__claude-haiku-5-5 | 0.05 | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% | 100% |
| extract__claude-haiku-5-5 | 0.1 | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% | 100% |
| extract__claude-haiku-5-5 | 0.2 | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% | 100% |
| keyword__none | 0.05 | 0% [0%, 0%] | 17% [16%, 17%] | 89% [85%, 93%] | 0% | 0% |
| keyword__none | 0.1 | 0% [0%, 0%] | 17% [16%, 17%] | 89% [85%, 93%] | 0% | 0% |
| keyword__none | 0.2 | 0% [0%, 0%] | 17% [16%, 17%] | 89% [85%, 93%] | 0% | 0% |
| naive__claude-haiku-5-5 | 0.05 | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% | 100% |
| naive__claude-haiku-5-5 | 0.1 | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% | 100% |
| naive__claude-haiku-5-5 | 0.2 | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% | 100% |
| naive__claude-sonnet-5-5 | 0.05 | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% | 100% |
| naive__claude-sonnet-5-5 | 0.1 | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% | 100% |
| naive__claude-sonnet-5-5 | 0.2 | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% | 100% |
| strict__claude-haiku-5-5 | 0.05 | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% | 100% |
| strict__claude-haiku-5-5 | 0.1 | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% | 100% |
| strict__claude-haiku-5-5 | 0.2 | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% | 100% |
| strict__claude-sonnet-5-5 | 0.05 | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% | 100% |
| strict__claude-sonnet-5-5 | 0.1 | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% | 100% |
| strict__claude-sonnet-5-5 | 0.2 | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% | 100% |
