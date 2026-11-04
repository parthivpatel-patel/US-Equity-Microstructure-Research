# Phase 146 — joint group/calendar-block scan mechanics

Date: 2026-11-04. Scope: **synthetic verification, not empirical inference**.

## Work performed

Inspected the existing Phase 145 methodology report and its published Python test before adding a separate Phase 146 file. Locally executed an equivalent prototype using NumPy; the checks passed for common circular-calendar indices applied to all sampled groups, matched-group resampling, a perfectly linear seven-group 87-date panel, a constructed trend break, seeded determinism, and invalid input rejection. The published implementation is a cleaned version of the executed prototype and **has not yet been independently run from a fresh GitHub checkout**.

The prototype takes a group-by-date contrast panel, removes each group's linear fit, resamples group indices with replacement and *one shared sequence* of circular calendar blocks, restores fitted trends, computes the equal-group-weighted aggregate, and repeats the complete 20-day-window maximum absolute slope-shift scan. It uses the finite-simulation upper-tail convention `(1 + number of simulated maxima >= observed maximum)/(B + 1)`.

## Limitations

This is not a validated inferential method for the November 2025 round-lot reform. Resampling residuals around group-specific linear fits assumes an appropriate null trend and sufficiently stationary residuals; neither has been established. Group bootstrap resampling assumes exchangeability of matched groups and may fail to represent cross-group dependence beyond shared calendar shocks. Fixed calendar blocks do not automatically handle long memory or event-dependent heteroskedasticity. The procedure does not yet retain security/exchange-level identifiers or test alternative weighting and selection rules. The test's constructed break is synthetic and **must never be represented as an SEC-data result**.

The original SEC security/exchange observations, historical Nasdaq round-lot assignments, and Phase 131 processed input were unavailable for independent inspection this session. No empirical bootstrap maxima, p-values, figures, or causal estimates were generated. September pretrends and the substantial October information-event/placebo warning remain unresolved.

## Reproduction and publication inventory

Run `python tests/test_phase146_joint_scan.py` with NumPy. No proprietary market records, secrets, or historical ZIP archives are included. The earlier Phase 144 inventory described 129 recovered ZIPs, but those files are not present in this session's working directory; their actual hashes, permissions, and import eligibility remain unverified. The full empirical panel and source-data chain are not yet publicly reproducible.

## Next gate

Recover and hash-check the processed panel; reconcile original SEC security/exchange rows; authenticate treatment using historical Nasdaq notices and closing prices; then run and validate the joint scan across alternative detrending nulls, calendar-block lengths, group weighting, security/exchange composition, and placebo dates. Report maximum-statistic inference only after calibration diagnostics and sensitivity checks.
