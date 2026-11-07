# Phase 227 — Exact-source inspection and narrow session-calendar regression

Date: 2026-11-07. Independent U.S. equity round-lot reform research. No GIG assets or code.

## Exact published source inspected

Read GitHub contents API versions of `scripts/phase224_common_date_hac.py`, `scripts/phase225_matched_date_bootstrap.py`, `scripts/phase226_matched_hac_bridge.py`, and `tests/test_phase226_matched_hac_bridge.py` before writing this note.

The Phase 225 `matched_daily` function checks ISO-format dates and dates before 2025-11-03 but does not reject weekends or exchange holidays. Thus a weekend or Labor Day date can pass its date predicate if a complete synthetic panel is supplied. Phase 226 calls this function directly; it does not invoke the Phase 217 calendar screening. This is a source-level finding, **not** an executed Phase 226 integration-test result.

The Phase 224 HAC function requires dates to be ordered and aligned but does not authenticate a trading calendar. It retains cross-window covariance through full-series scores. Its inference is not security-cluster robust. Phase 226 duplicates the matched contrast into the pooled-count key only as a bridge, then removes that key from its result; it explicitly does **not** implement pooled-count weighting.

## New locally executed test

`tests/test_phase227_calendar_contract.py` is a standalone narrow calendar-contract demonstration. Seven deterministic tests passed locally using Python `unittest` on 2026-11-07. It rejects a Saturday, Labor Day (2025-09-01), Thanksgiving (2025-11-27), duplicates, unsorted dates, and noncanonical strings; admits 2025-09-02 and 2025-09-03. This is **not** a comprehensive NYSE calendar, nor a validation against original SEC observations. Closure examples require independent authoritative source confirmation before being used for empirical admission.

## Execution limitation

A clean checkout of the exact repository could not be obtained in the local runtime: `git clone` failed with `Could not resolve host: github.com`. The exact Phase 226 integration tests were therefore **not executed**. The GitHub connector successfully retrieved the exact published source for inspection. The standalone Phase 227 tests were executed locally, but clean-checkout execution remains outstanding.

## Research and provenance status

No historical SEC data, matched roster, Nasdaq historical round-lot assignments, or archived ZIPs were authenticated or imported. No historical coefficients, confidence intervals, or empirical charts were generated. The October 2025 placebo warning, September pretrends, treatment reconstruction, selection/weighting sensitivity, and joint common-date/security-level uncertainty remain unresolved. No causal reform effect is established.

## Next concrete tasks

Obtain an independently authenticated exchange calendar and source-data checksums; wire its admission gate into Phase 225/226; execute exact-repository integration tests; then conduct fixed-roster matched placebo comparisons under equal-cell and pooled-count weighting with full-series HAC and security-level sensitivity. Inventory recovered archives only after locating authentic copies and checking redistribution rights.
