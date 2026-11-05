# Phase 167 — Matched-date roster integrity (2026-11-05)

## Source-code audit
Read `tests/test_phase166_composition.py` from the public repository before preparing this note. Its `available_case_contrasts` uses `cells[(d,g)][a] = y` without duplicate rejection, unlike `balanced_contrasts`. Therefore a repeated (date, group, arm) silently overwrites a preceding observation. It also lacks finite-value and arm validation. This is a code-level finding, **not evidence of duplicates in SEC data**.

## Deterministic verification
A local Python test suite with eight tests passed. Tests covered the Phase 166 composition counterexample, duplicate rejection, boolean treatment-arm rejection, nonfinite outcomes, incomplete-arm counting, no balanced groups, dates lacking pairs, and absent pre/post periods. The test fixture had available-case date contrasts [0,0,5,5] versus fixed-roster [0,0,0,0], with pair counts [1,1,2,2]. These are constructed data, not market observations.

## Required empirical protocol
1. Enforce unique (date, matched-group, treatment-arm, exchange) keys before any aggregation; do not silently collapse or overwrite. If multiple securities per arm are intended, aggregate only after authenticating constituent security IDs and declared weights.
2. Report by-date counts of treated and control securities, paired matched groups, excluded groups, and missing arms; stratify by exchange.
3. Freeze the matched roster using predeclared windows, and report both available-case and balanced-panel estimates. Explain selection effects of balance restrictions.
4. For September pretrends and October placebo, retain common calendar dates, use date-cluster or block-based uncertainty with matched-group resampling where feasible, and explicitly test serial-dependence sensitivity.
5. Authenticate historical SEC observations and Nasdaq round-lot treatment assignments before empirical interpretation.

## Provenance and limitations
Reviewed repository file: `tests/test_phase166_composition.py` (blob ed2a054e176a0a820a3f4d0374356d997fa30521). No SEC source archive, original Nasdaq snapshot, or historical research ZIP was authenticated or imported in this session. No empirical coefficients or causal effects are claimed. The November 14 publication target remains conditional.
