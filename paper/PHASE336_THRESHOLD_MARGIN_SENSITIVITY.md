# Phase 336 — Reference-threshold sensitivity of published pre-reform trends

Date: 2026-11-13. Source: existing `results/phase136_trend_uncertainty_presentation.csv` (20 published aggregate rows). This is a descriptive calculation from displayed slopes and two-way standard errors, **not** fresh SEC-panel estimation or a calibrated significance test.

## Reproducible method

Run `python scripts/phase336_threshold_margin.py results/phase136_trend_uncertainty_presentation.csv` from repository root. The script verifies the full outcome-period-lag grid, finite values, positive standard errors and consistent reported cluster counts. For each outcome-period group it computes the minimum over HAC lags 0, 3, 5, 10 and 15 of `abs(displayed slope)/displayed two_way_se`, and asks whether **all five** ratios exceed each illustrative reference cutoff 1.96, 2.0, 2.1 and 2.2. These cutoffs are sensitivity probes, **not** justified critical values for two-way clustering.

| Outcome | Period | Minimum absolute ratio | Weakest lag | All lags exceed 2.0? | All lags exceed 2.2? |
|---|---|---:|---:|---|---|
| count | Jul-Oct | 0.316266 | 15 | No | No |
| count | Jul-Sep | 2.215879 | 15 | Yes | Yes |
| volume | Jul-Oct | 2.174079 | 15 | Yes | No |
| volume | Jul-Sep | 0.141888 | 3 | No | No |

Published rows report 68 groups and either 64 (Jul-Sep) or 87 (Jul-Oct) dates. The Jul-Oct volume classification changes at the illustrative 2.2 cutoff, while the Jul-Sep count classification does not. These are **within-reported-SE** comparisons; they do not establish valid finite-cluster p-values, robustness to different covariance estimators, or independent replications. Displayed-value rounding also limits precision.

## Scientific interpretation and release gate

The September trend in count and October-inclusive trend in volume remain material pre-reform warnings. The substantial October placebo/break, Phase 130 count-tail contradiction, original dated placebo-window provenance, historical round-lot treatment authentication, selection/weighting sensitivity and joint security/date dependence-aware inference remain unresolved. This audit does not rehabilitate causal interpretation. Historical ZIPs have not been authenticated or imported. Publication is not certified for the November 14 target.

## Verification

Seven synthetic regression tests passed locally on 2026-11-13. The script was run against a locally transcribed copy of the 20 GitHub-fetched CSV rows; full repository checkout regression was not executed. The tests are designed for execution with `PYTHONPATH=scripts python -m unittest discover -s tests -p 'test_phase336_threshold_margin.py'`.
