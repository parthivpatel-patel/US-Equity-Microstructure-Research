# Phase 162 — Identification preflight and empirical admission gates

Date: 2026-11-05. Independent U.S. equity round-lot research only.

## Newly executed verification

A locally executed eight-test Python fixture suite passed (8/8), covering group overlap, disjoint baseline support, duplicate tickers, nonfinite outcomes, invalid treatment labels, inconsistent pre/post changes, missing comparison groups, and invalid trade weights. These are constructed fixtures, **not** SEC empirical observations. No new causal estimates were calculated.

## Methodological finding

The published Phase 158 script checks row validity and uses pre-period outcome controls, but does not report **common baseline support** between the 68 provisionally treated and 2,194 comparison securities. A regression coefficient can be driven by extrapolation if the baseline distributions barely overlap. The script also does not report treated and comparison effective sample sizes under trade-count weights. The Phase 161 diagnostic provides stable weight ESS, but it has not been applied to the recovered historical panel.

A preflight must report for each baseline outcome (r_pre, v_pre): the intersection of treated and comparison observed ranges; counts outside that intersection in each group; and separate weighted ESS and maximum weight shares. Empty intersection must be flagged, not silently interpreted as identification. Range overlap is only a minimal diagnostic, **not** evidence of adequate propensity overlap or parallel trends.

## Required empirical sequence

1. Recover and authenticate SEC security/date/exchange observations and historical Nasdaq lot classifications; record source hashes and access terms.
2. Run admission gates and common-support diagnostics on the actual panel. Retain a fixed, declared cohort before inspecting outcomes.
3. Re-estimate September leads and multiple October placebo dates on the same matched groups and common calendar dates.
4. Use security and exchange controls, group-aware resampling and date-block dependence sensitivity; report both count-weighted and security-equal results.
5. Treat the substantial October placebo and September pretrends as identification failures until convincingly resolved. Do not describe the reform coefficient as causal.

## Publication inventory and limitations

This memo is newly published; the locally executed fixture script was not yet transferred to GitHub. Previously recovered original Phase 2 panel and generating script remain outside the public repository pending source authentication and redistribution review. The SEC daily archives, Nasdaq historical snapshots and historical ZIP collection remain unverified/unimported in this run. This memo is a methodological audit, not a validated empirical result.

The November 14 deadline remains conditional on full reproducibility and identification checks.
