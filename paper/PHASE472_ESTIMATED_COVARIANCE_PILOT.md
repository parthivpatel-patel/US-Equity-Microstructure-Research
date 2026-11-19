# Phase 472 — Estimated-covariance sensitivity pilot (synthetic only)

Date: 2026-11-19. This is **not** an analysis of SEC observations. It tests the uncertainty introduced when a simultaneous placebo test estimates AR(1) serial correlation from the same 40-session sample used for inference.

## Reproducible local experiment

A deterministic Python-standard-library implementation generated stationary unit-variance Gaussian AR(1) paths with 40 observations and cutoffs 10, 20, 30. It used a demeaned Yule–Walker lag-one estimator (clipped to [-0.95,0.95]), computed the exact finite-sample covariance of pre/post mean contrasts for each estimated rho, and calibrated a two-sided max-|Z| threshold by 1,500 seeded Gaussian draws. The benchmark instead used the *true* rho for its covariance and threshold. For each rho, 200 independent null series were tested. Seed 472; seven deterministic unit tests passed. The experiment was run locally, not on authenticated market data.

| True rho | Mean estimated rho | Rejections, known covariance | Rejections, estimated covariance |
|---:|---:|---:|---:|
| 0.0 | -0.020925 | 11/200 | 12/200 |
| 0.5 | 0.421080 | 14/200 | 10/200 |
| 0.8 | 0.680058 | 4/200 | 3/200 |

These proportions are **noisy pilot outputs**, not reliable size estimates. At 200 replications, a nominal 5% rejection probability has Monte Carlo standard error about 1.54 percentage points, before additional threshold-calibration noise. The estimated AR coefficient exhibits downward finite-sample bias in the tested positively correlated cases. The pilot **does not** demonstrate calibrated 5% coverage or superiority of either procedure.

## Interpretation and gates

The plug-in covariance changes both the estimated standard errors and the joint critical value. A covariance-known benchmark is not a feasible empirical test. Larger outer replication counts, independently calibrated critical values, and procedures that respect matched-security and common-date dependence are required. Yule–Walker on raw outcomes can be contaminated by deterministic trends, treatment shifts and exchange effects; use appropriate residuals only after verifying specification. September pretrends and the substantial October 2025 placebo warning remain identification blockers. Treatment classification, exchange/security composition, source-data provenance, weighting sensitivity and historic ZIP recovery remain unresolved.

## Reproducibility and publication inventory

Local source: `phase472_covariance_uncertainty.py`; tests: `test_phase472.py`; machine-readable output: `results.json`. **These local files were not included in this GitHub commit**; executable publication is pending. This report records the experiment specification and observed pilot results without claiming that the repository alone reproduces them. No licensed data, historical estimates, or synthetic charts masquerading as SEC results are included.

The November 14, 2026 target was missed. The paper remains **not publication-certified**.
