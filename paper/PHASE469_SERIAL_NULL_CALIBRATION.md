# Phase 469 — Exact serial-correlation null calibration

Date: 2026-11-19. **Analytical Gaussian model only; no authenticated SEC observations, empirical treatment effects, or causal claims.**

## Calculation
For 40 equally spaced observations with a 20/20 pre/post split, let the placebo contrast be the post mean minus the pre mean. Assume a stationary, unit-marginal-variance Gaussian AR(1) null with covariance Cov(Y_i,Y_j)=rho^|i-j|. Compute the exact contrast variance as w' Sigma w, compare with the independent-observation variance sum(w_i²)=0.1, and derive the exact two-sided rejection probability for a nominal 5% standard-normal test incorrectly using the iid standard error. This is a known-variance Gaussian benchmark, not a fitted model or a bootstrap calibration.

| rho | Exact variance | Variance / iid variance | Actual rejection probability under iid SE |
|---|---:|---:|---:|
| 0.0 | 0.100000 | 1.000000 | 5.00% |
| 0.3 | 0.176531 | 1.765306 | 14.02% |
| 0.5 | 0.270000 | 2.700000 | 23.29% |
| 0.8 | 0.604598 | 6.045984 | 42.54% |

Values are exact up to numerical rounding, not Monte Carlo estimates. Local execution: four deterministic unittest cases passed. Reproduce from repository root with `PYTHONPATH=scripts python -m unittest discover -s tests -p 'test_phase469_serial_null.py'` and `python scripts/phase469_serial_null.py`.

## Interpretation and restrictions
A naive independent-session placebo test can substantially over-reject when residuals have positive serial correlation. This benchmark isolates one error source only. It does not establish that any historical placebo is significant or invalid, and it does not account for cross-security, exchange, matched-group, common-date dependence, estimated nuisance parameters, overlapping placebo dates, or treatment misclassification. In particular, this Gaussian known-variance benchmark does not validate the existing block bootstrap. Do not infer the historical autocorrelation parameter from these illustrative settings.

## Next gate
Authenticate source-data files and treatment histories; compute residual autocorrelation and support diagnostics using verified historical observations; then evaluate joint group/date dependence-aware, null-centered simultaneous placebo inference and coverage under calibrated data-generating processes. Preserve the October 2025 placebo warning and September pretrend caveat. The November 14 publication deadline was missed and the manuscript remains not publication-certified.
