# Treated-name influence and robust-location audit — 2026-11-22

**Scope:** Direct calculation from the recovered Phase-2 processed CSV, not authenticated SEC source observations. The input `roundlot_phase2_security_panel.csv` was recovered from the research Library; SHA-256 of the actual bytes rechecked in this session: `2ccb80427a765ca3858f11f2874d6f87a79a559ec1fdeafc34420e82840e5bbb`. There are 68 provisionally treated and 2,194 controls. Do not treat provisional classification as certified November 3 assignments.

## New processed-panel diagnostics

All values below are treated-minus-control *post-minus-pre* hidden-execution-rate differences in **percentage points**. These are cross-sectional descriptive comparisons, not causal effects or daily time-series estimates.

| Metric | Hidden trade count rate (`dr`) | Hidden share-volume rate (`dv`) |
|---|---:|---:|
| Untrimmed mean gap | -3.462929 | -2.572053 |
| Median gap (difference of group medians) | -3.442034 | -2.749670 |
| 10% trimmed-mean gap (trim each group independently) | -3.559769 | -2.642802 |
| Range of treated-name leave-one-out mean gaps | [-3.624902, -3.287581] | [-2.708470, -2.434679] |
| Treated-name leave-one-out gaps greater than zero | 0 of 68 | 0 of 68 |

Largest absolute change in the original mean gap when removing a *single treated name*: count rate NFLX (0.175348 percentage points), DJCO (0.161973), ITIC (0.150477), CACC (0.1371), HIFS (0.1289). Volume rate NFLX (0.1374), HIFS (0.1364), DASH (0.1164), ALNY (0.1005), CACC (0.0986). Values rounded; exact rank ordering derives from the full-precision input.

**Interpretation:** Neither one treated stock nor the difference between untrimmed mean, median, and 10% trimmed mean explains the *unadjusted* negative descriptive gaps. This does **not** resolve severe baseline imbalance, October pre-reform movement, treatment misclassification, exchange/day composition, correlated observations, or selection into the panel. It must not be presented as an independent validation of the SEC data or as a causal robustness result.

## Reproduction

With Python, pandas and SciPy installed, read the original CSV and evaluate, for each `x` in `dr,dv`: `t = df.loc[df.treated == 1, x]`, `c = df.loc[df.treated == 0, x]`; `gap = t.mean() - c.mean()`; `median_gap = t.median() - c.median()`; `trim_gap = scipy.stats.trim_mean(t, 0.1) - scipy.stats.trim_mean(c, 0.1)`; `loo = (t.sum() - t) / (len(t) - 1) - c.mean()`. Report `loo.min()`, `loo.max()` and `(loo > 0).sum()`. Recheck the file SHA-256 before execution. The numerical results were executed against the actual recovered CSV; they are not synthetic fixtures.

**Evidence gates still open:** original SEC Q3/Q4 ZIP bytes and member checksums; September 2025 historical round-lot assignments; raw daily September pretrends and October placebo with common security/exchange/calendar coverage; serial-dependence-aware inference; historical Phase 430/436/472 package recovery. The appropriate release remains explicitly exploratory/falsification-focused.
