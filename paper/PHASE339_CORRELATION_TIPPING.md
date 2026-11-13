# Phase 339 — Correlation tipping points for overlapping pretrend estimates

Date: 2026-11-13. Input: existing public `results/phase136_trend_uncertainty_presentation.csv` (20 aggregate rows), not authenticated SEC microdata. Extends Phase 338's covariance bounds.

For the July–October minus July–September slope difference, variance equals `s_early² + s_late² - 2*rho*s_early*s_late`. The illustrative absolute ratio exceeds 1.96 only if `rho > (s_early²+s_late²-(delta/1.96)²)/(2*s_early*s_late)`. The unknown correlation must be estimated jointly from original observations; overlapping periods must **not** be treated as independent.

| Outcome | HAC lag | Correlation tipping point | Interpretation |
|---|---:|---:|---|
| Count | 0 | -1.385067 | Above 1.96 for every admissible correlation |
| Count | 3 | -0.406047 | Depends on correlation |
| Count | 5 | -0.180108 | Depends on correlation |
| Count | 10 | +0.069076 | Depends on correlation |
| Count | 15 | +0.165483 | Depends on correlation |
| Volume | 0 | -0.171315 | Depends on correlation |
| Volume | 3 | +0.179765 | Depends on correlation |
| Volume | 5 | +0.246899 | Depends on correlation |
| Volume | 10 | +0.301495 | Depends on correlation |
| Volume | 15 | +0.285926 | Depends on correlation |

The threshold is illustrative, **not a calibrated significance test**. At equality the ratio equals 1.96, not exceeds it. The count lag-0 result is conditional on the reported marginal SEs being correct; no confidence-level guarantee follows from this diagnostic. The full-period slope difference is not an October break coefficient.

Reproduce: `python scripts/phase339_correlation_tipping.py results/phase136_trend_uncertainty_presentation.csv`. Synthetic tests: `python -m unittest discover -s tests -p 'test_phase339_correlation_tipping.py'`. Six synthetic tests passed locally using equivalent module logic; numeric values were calculated from a local transcription of the 20 fetched GitHub CSV rows, not a fresh repository checkout. Full suite not executed.

**Publication gate:** November 14 target remains uncertified. October placebo and September pretrends, Phase 130 contradictory hidden-count tails, treatment and source authentication, selection/weighting, serial/common-date dependence and security-exchange controls remain unresolved. Original dated placebo observations and historical ZIPs are not yet recovered and verified. No causal claim.
