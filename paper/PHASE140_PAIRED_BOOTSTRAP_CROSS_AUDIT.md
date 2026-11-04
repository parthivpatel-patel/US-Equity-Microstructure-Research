# Phase 140 — Cross-phase paired-bootstrap table audit (2026-11-04)

## Scope and provenance

This is a **new executed numerical audit of two public presentation tables**, not a rerun of the underlying bootstrap or an authentication of original SEC/Nasdaq data. Inputs were fetched through the connected GitHub repository reader from `results/phase139_paired_october_shift_presentation.csv` (Git blob SHA `d15fc17c66d5e9f1a605714fd41b94a7b0041e6b`) and `results/phase137_block_bootstrap.csv` (blob SHA `b327230d5d28aeffd312d724a9fa88b9482aa529`). Calculations were executed in JavaScript on the eight Phase 139 rows, matched by outcome and block length to Phase 137 July–September rows. No raw data, original SEC records, or historical treatment assignments were available for independent validation in this audit.

## Results

* Phase 139 July–September slopes agree with Phase 137 at published rounding precision: count difference +0.000000291097 pp/day; volume difference −0.000000052576 pp/day (Phase 139 minus Phase 137). These are **rounding discrepancies**, not independently corroborated estimates.
* The Phase 139 interval upper bound is below zero for all eight rows (four block lengths per outcome). This is a descriptive check of the published intervals, **not eight independent hypothesis tests**.
* Count interval widths by 3/5/10/15-day block: 0.215569, 0.215045, 0.246308, 0.252172 pp/day. Maximum/minimum width ratio 1.17265 (17.3% larger).
* Volume widths: 0.205383, 0.195718, 0.194962, 0.195387 pp/day. Maximum/minimum width ratio 1.05345 (5.3% larger).
* Interval width is **not strictly increasing** with block length for either outcome; any blanket claim that longer blocks always widen Phase 139 intervals is incorrect.

The derived eight-row table is in `results/phase140_paired_interval_width_audit.csv`. Values are calculated from rounded published Phase 139 values, not unrounded bootstrap draws.

## Identification and reproducibility status

The October slope shift predates November 3, 2025. October 1 information-event contamination, September pretrends, placebo warnings, possible selection/weighting sensitivity, and unauthenticated historical treatment assignments continue to block causal interpretation. The recovered processed panel and complete historical archive are not yet publicly reproducible; their redistribution eligibility remains to be checked. The published bootstrap residual stationarity and group-dependence assumptions have not been validated here.

**Next:** obtain and authenticate source SEC security-exchange-date panels and contemporaneous Nasdaq/NYSE round-lot assignment rules; execute alternative historical breakpoint scans on an authenticated panel, including pre-October dates, with a common-date dependence-aware max-statistic calibration. Do not interpret this table audit as new source-data evidence.
