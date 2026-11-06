# Phase 181 — Common-date placebo sample: partial identification (2026-11-05)

## Source and method
Read the existing Phase 180 report and script and the published `results/phase131_window_sensitivity.csv` through the connected GitHub service. The published summary table reports eligible placebo counts of 82, 78, 74, 68 and 58 for windows 3, 5, 7, 10 and 15 trading days, respectively. Both outcomes share the counts within each window. The **date identities are not provided**.

For k eligible-date sets with sizes n_i inside a *specified* universe of N dates, the sharp elementary bounds on the all-window intersection size are **max(0, sum(n_i) - (k-1)N)** and **min(n_i)**. Here sum(n_i)=360 and k=5. Without an authenticated common universe and actual date memberships, intersection size and common-date placebo estimates are not identified.

| Hypothetical common universe N | Lower intersection bound | Upper bound |
|---:|---:|---:|
| 82 | 32 | 58 |
| 90 | 0 | 58 |
| 100 | 0 | 58 |

These are *conditional mathematical bounds*, **not** observed historical placebo sample sizes. In particular, N=82 is not established by the maximum individual denominator; it is only an illustrative assumption. Even if intersection size were known, the aggregate exceedance counts do not identify which dates exceed each threshold, nor their contrasts. Consequently, a common-date placebo fraction, serial-dependence-aware uncertainty estimate or calibrated p-value **cannot** be recovered from these summaries.

## Reproducibility
```bash
python scripts/phase181_intersection_bounds.py results/phase131_window_sensitivity.csv
python -m unittest discover -s tests -p 'test_phase181_intersection_bounds.py'
```
A locally run equivalent prototype passed nine deterministic tests. The exact published code still needs fresh-checkout execution.

## Next empirical gate
Recover authenticated original SEC security-date-exchange observations, exact historical placebo cutoff dates, a fixed matched-group roster, the Nasdaq treatment reconstruction and the exchange/trading calendar. Compute date-membership sets before intersecting them; rerun pretrend and October placebo analyses with security/exchange controls, matched-group plus common-date dependence, serial correlation and prespecified weighting. Do not claim causal identification. No original source ZIP or paper archive was imported in this session. November 14 target remains conditional.
