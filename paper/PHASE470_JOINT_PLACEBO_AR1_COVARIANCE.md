# Phase 470 — Exact covariance of overlapping placebo contrasts

Date: 2026-11-19. **Analytical Gaussian null benchmark only; no historical SEC observations or estimated effects.**

## Design and result

Extend Phase 469's single-cutoff AR(1) known-variance benchmark to **three overlapping cutoffs** at sessions 10, 20, and 30 of a 40-session illustrative series. Each contrast is the mean after the cutoff minus the mean before the cutoff. Under a zero-mean stationary Gaussian AR(1) with unit marginal variance, Sigma[i,j] = rho^abs(i-j), define weights w_k[i] = -1/k before k, +1/(40-k) after k. Exact covariance of any pair is w_k' Sigma w_l. Normalize by the two exact standard deviations to obtain correlation.

| rho | Var(contrast 10) | Var(contrast 20) | Corr(10,20) | Corr(10,30) |
| ---: | ---: | ---: | ---: | ---: |
| 0.0 | 0.13333333 | 0.10000000 | 0.57735027 | 0.33333333 |
| 0.3 | 0.22993207 | 0.17653061 | 0.59427226 | 0.34122288 |
| 0.5 | 0.34227431 | 0.27000004 | 0.61399873 | 0.35064662 |
| 0.8 | 0.67969081 | 0.60459839 | 0.71066960 | 0.41531653 |

**Finding:** Overlapping placebo contrasts are correlated **even when daily observations are independent** (rho=0). Positive serial correlation strengthens their dependence in these configurations. Treating the September and October placebo tests as independent is therefore not justified merely by eliminating serial correlation. This covariance is about estimated contrasts, unlike the bootstrap *eligibility-indicator* covariance in Phase 466.

## Reproduction and verification

Run `PYTHONPATH=scripts python -m unittest discover -s tests -p 'test_phase470_joint_ar1.py'` and `python scripts/phase470_joint_ar1.py`. Seven deterministic tests passed locally. A separate NumPy matrix-multiplication implementation independently reproduced the reported values. The rho=0.5 variance at cutoff 20 agrees with Phase 469's 0.2700000381469636. No historical data are embedded or distributed.

## Limits and next gate

This is an equally spaced, unit-variance, single-series, known-parameter Gaussian model. It neither estimates actual historical serial dependence nor accounts for treatment assignments, security/exchange effects, common-date shocks, matched-group dependence, weighting or selection, missing observations, multiple testing calibration, or a causal effect. The substantial October 2025 placebo warning and September pretrends remain open; no historical source-data or round-lot treatment authentication was completed. The November 14, 2026 publication deadline was missed, and the paper remains **not publication-certified**.

Next: build a null-centered simultaneous test using the *joint* covariance, verify its size under clustered group/date simulations, and apply only after authenticated source and treatment data are available. Recovered Phase 430/436 historical archives remain unimported.
