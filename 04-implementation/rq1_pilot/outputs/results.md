Items: 1356 from 399 products. Variants: {'original': 250, 'remove': 250, 'vague': 250, 'remove_prior': 250, 'contradict': 206, 'natural_missing': 150}

**Recommend rate by variant** (product-cluster bootstrap 95% CI). Correct behaviour: original high, every other column 0.

| Matcher | original | remove | vague | remove_prior | contradict | natural_missing | native URR |
|---|---|---|---|---|---|---|---|
| keyword__none | 88% [84%, 92%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] | 0% [0%, 0%] |

**Prior effect** (same product: evidence removed, then famous brand + hype added)

| Matcher | pairs | abstain→recommend | recommend→abstain |
|---|---|---|---|
| keyword__none | 250 | 0 | 0 |

**Learn-then-Test** (50 product splits, 50/50 calibration/test, δ = 0.1). URR and coverage on test, mean [2.5%, 97.5%] across splits; 'viol.' = share of splits with test URR > α.

| Matcher | α | URR | coverage | recall of supported | viol. | no threshold |
|---|---|---|---|---|---|---|
| keyword__none | 0.05 | 0% [0%, 0%] | 16% [15%, 17%] | 88% [85%, 92%] | 0% | 0% |
| keyword__none | 0.1 | 0% [0%, 0%] | 16% [15%, 17%] | 88% [85%, 92%] | 0% | 0% |
| keyword__none | 0.2 | 0% [0%, 0%] | 16% [15%, 17%] | 88% [85%, 92%] | 0% | 0% |
