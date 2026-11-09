# Phase 273 — Fixed-window pretrend validation and evidence status

Date: 2026-11-09. This is a methodological diagnostic, **not a historical SEC estimate**.

## Tested local prototype
A Python standard-library prototype was run locally with nine passing deterministic tests (linear trend, missing and unexpected sessions, duplicate dates, nonfinite values, overlapping windows, unsorted calendar, insufficient window, and irregular calendar spacing). The prototype was not published in this commit; it remains an outstanding item for repository integration and retesting. No historical observations were used.

## Estimand and safeguards
For each of two predeclared, nonoverlapping windows, calculate the mean of the fixed-roster daily matched treated-minus-control contrast and its OLS slope against elapsed *calendar days*, not row index. Report late-minus-early mean. Reject observed dates that do not match the independently supplied exchange-session calendar exactly, as well as duplicates, nonfinite outcomes, invalid window ordering, and windows with fewer than two dates. Do not interpret a diagnostic passing as authentication of calendar, roster, or underlying SEC data.

## Important identification limitations
A September 2025 pretrend and substantial October 2025 placebo signal were previously reported and remain unresolved. The November 3, 2025 round-lot treatment assignments and source data require independent authentication. Selection, alternative weighting, security/exchange effects, cross-sectional common-date shocks, and serial dependence remain outstanding. A two-window descriptive contrast is neither a causal reform estimate nor a substitute for dependence-aware uncertainty. No causal effect has been established.

## Publication inventory
Published in this phase: this audit only. Not published in this phase: locally tested prototype and nine tests, recovered historical ZIPs, unverified SEC data, historical charts, and earlier unpublished Phase 252–254 implementations. The archive inventory is incomplete; do not assume recovered files are redistributable.

## Next execution
Import and rerun the pretrend prototype and tests in the repository; authenticate source hashes against independently archived SEC originals, exchange calendar, and treatment roster; freeze fixed security/exchange pair IDs and windows; run September trends and October placebo cutoffs with full-series HAC and bootstrap sensitivity on actual authorized observations. Target November 14, 2026 remains conditional.
