# Phase 165 — Common-date matched-group inference preflight

Date: 2026-11-05. Independent research into the November 3, 2025 U.S. equity round-lot reform.

## Executed method validation

Nine Python standard-library tests passed in a local prototype. The published test script implements the same nine checks and inference logic, but a fresh-checkout execution of the published version remains outstanding. These are constructed fixtures, **not SEC observations**. The tests cover within-matched-group treated-minus-control contrasts by common date, shared-date shock cancellation, incomplete-cell rejection, nonfinite-value rejection, pre/post arithmetic, reproducible noncircular moving-block resampling, constant-contrast bootstrap, invalid block length, and missing periods. The constant fixture yields a pre/post difference of exactly 2 and a bootstrap percentile interval [2,2].

## Estimator and limits

First calculate treated-minus-control differences within matched group and calendar date; then average the group contrasts equally for each date. Compare mean daily contrasts on either side of a specified cutoff. Bootstrap contiguous calendar-date observation blocks **separately within pre and post periods**. This retains within-block serial dependence and common-date dependence across groups through aggregation, but is not a substitute for security/exchange fixed effects, two-way clustered standard errors, matched-group resampling, or an identification argument. The bootstrap percentile interval is a diagnostic, not a guaranteed calibrated causal test. Changing group composition across dates can change the estimand. Dates must be chronologically sortable in their original representation.

## Required empirical work

Reconstruct and authenticate the daily SEC security/exchange panel and historical Nasdaq round-lot assignments. Evaluate September pretrends and prespecified October placebo cutoffs, including the previously substantial October placebo warning. Report matched-group and common-date dependence, serial-dependence sensitivity to block lengths, security/exchange controls, cohort selection, joint baseline support, weighting concentration, and treatment ambiguity. The 68 treated / 2,194 comparison Phase 2 panel must not be confused with the later 68 / 204 matched sample. No reform effect is established.

## Provenance and archive inventory

Phase 164's published test and memo were fetched and read before adding this phase. No existing files were overwritten. This session adds a new method/test script and this report only. The original SEC daily archive, Nasdaq historical snapshots, recovered private security panel, and historical ZIP collection were not available for authenticated empirical execution or redistribution review. No original market data, figures, or unlicensed source files were imported. The November 14, 2026 publication deadline remains provisional; the manuscript is not fully validated.
