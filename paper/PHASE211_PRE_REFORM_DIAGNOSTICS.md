# Phase 211: Published pre-reform descriptive diagnostics

2026-11-07. Independent U.S. equity round-lot reform research; no GIG dependencies.

## Scope and verification
Phase 210 published a checkpoint but not executable code. Phase 211 publishes a clean, standalone implementation and 12 deterministic regression tests. A corresponding local prototype was executed with Python unittest: **12 passed**. Published source and test files have not yet been executed from a clean checkout. The published test imports `scripts.phase211_preperiod_diagnostics`; run from repository root with `python -m unittest discover -s tests -p 'test_phase211_preperiod_diagnostics.py'`.

Input is a sorted series of date-level contrasts from an upstream fixed-roster estimator, with two disjoint inclusive pre-reform windows. Outputs: each window's mean, OLS slope per observed session, and later-minus-earlier placebo mean shift. Constructed linear 12-date input produces a shift of 6 and slope of 1; these are **not historical SEC estimates**. Window boundaries must exist in the supplied observations, but this does not establish an authenticated or complete exchange calendar.

## Critical identification limits
No new historical coefficients, confidence intervals or figures were computed. September pretrends and substantial October 2025 placebo findings remain unresolved. The diagnostics do not handle date-level serial dependence, cross-security dependence, selection, weighting sensitivity, or causal identification. Historical treatment assignments and SEC source data are not authenticated. The November 3, 2025 reform date is a fixed admission boundary, not evidence of an effect.

## Publication and archive inventory
Published in this phase: script, tests, and this checkpoint. Previously recovered historical research ZIPs, historical SEC panel, Nasdaq historical treatment mapping, charts, and manuscript source materials were **not available for authenticated import** during this phase; redistribution rights and file hashes remain unverified. A complete historical archive inventory remains outstanding.

## Next
Execute exact published files from a clean checkout; authenticate SEC observations and historical treatment mapping; freeze common-date/security/exchange support; report September pretrends and October placebo estimates with weighting sensitivity, HAC and block-bootstrap checks. Do not claim a causal reform effect.
