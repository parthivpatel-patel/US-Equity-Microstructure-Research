# Phase 473 — Exact serial-dependence variance sensitivity (synthetic only)

Date: 2026-11-19. This is an analytic AR(1) model audit, **not** historical SEC analysis or causal inference.

For n=40 stationary unit-variance Gaussian AR(1) observations, the pre/post contrast weights are -1/k for sessions before cutoff k and 1/(n-k) afterward. Its exact variance is the double sum of w_i w_j rho^|i-j|. The independence benchmark is 1/k + 1/(n-k). The standard-error inflation factor is the square root of their ratio.

| AR(1) rho | Cutoff 10 | Cutoff 20 | Cutoff 30 |
|---:|---:|---:|---:|
| 0.0 | 1.0000 | 1.0000 | 1.0000 |
| 0.3 | 1.3132 | 1.3286 | 1.3132 |
| 0.5 | 1.6022 | 1.6432 | 1.6022 |
| 0.8 | 2.2578 | 2.4589 | 2.2578 |

Entries are exact-model standard-error inflation factors rounded to four decimals, not estimated from market observations. The larger inflation for the central split at rho=0.8 illustrates sensitivity to cutoff geometry. No covariance estimation, treatment/control panel, matched-group resampling, or empirical residual dependence is evaluated here.

Reproduction: `python -m unittest tests/test_phase473_covariance_bounds.py` from the repository root, and `python -c "from scripts.phase473_covariance_bounds import sensitivity; print(sensitivity())"`. Four deterministic tests were executed successfully in a local copy with equivalent imports; the full repository suite was not executed.

Source authentication, treatment assignment, September pretrends, the substantial October 2025 placebo warning, security/exchange effects, selection/weighting sensitivity, and matched-group/common-date inference remain unresolved. The historical Phase 430/436 ZIP archives were not imported. The November 14 publication target was missed and the paper is not publication-certified.
