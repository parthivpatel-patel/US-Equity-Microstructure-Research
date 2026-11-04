# Phase 130 — Historical pseudo-event scan and matched-group sensitivity

Executed November 3, 2026. **Exploratory analysis; no causal claims.**

## Data and design

Inherited processed daily matched-group panel: 14,416 records, 68 matched groups, 106 trading dates, two outcomes. These counts and the output below originate from the prior Phase 130 research package, **not** a fresh GitHub-side rerun or independent SEC source authentication.

For every eligible candidate date, compute each group's mean of five subsequent trading days minus its mean for five preceding trading days; average the 68 group differences. Pre-reform pseudo-events require their entire five-day post-window to end before November 3. Compare November 3 with the previously explored October 6 pseudo-event and the full historical scan. Historical windows overlap; their ranks are *not* calibrated p-values.

| Outcome | Nov. 3 (pp) | Oct. 6 (pp) | Nov. minus Oct. (pp) | Prior pseudo-events equally or more negative |
|---|---:|---:|---:|---:|
| Hidden trade count | -1.335781 | -0.601120 | -0.734661 | 2/78 |
| Hidden share volume | -0.006939 | -0.633537 | +0.626598 | 48/78 |

## Exploratory resampling

10,000 seeded matched-group bootstrap draws per outcome of the paired November-minus-October five-day contrasts:

| Outcome | Difference (pp) | 95% group-bootstrap percentile range (pp) |
|---|---:|---|
| Hidden trade count | -0.734661 | [-2.093991, +0.573944] |
| Hidden share volume | +0.626598 | [-0.936264, +2.229543] |

Both intervals include zero. Group-only resampling does not preserve uncertainty associated with common calendar-date shocks, so it is insufficient for final inference. October 6 was chosen during prior exploratory analysis, not preregistered. Historical assignments remain provisional.

## Next tasks

Historical round-lot treatment authentication, SEC source-file reconciliation, corporate action/ticker crosswalk, pre-event frozen cohort and weighting design, and matched-group plus common-date block inference. No causal reform effect has been established.
