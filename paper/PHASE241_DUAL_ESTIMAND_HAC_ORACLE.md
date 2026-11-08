# Phase 241 — Dual-estimand Bartlett HAC numerical regression oracle

Date: 2026-11-08. Independent round-lot reform research; synthetic test only.

## Verified source inspection

Read the current public repository implementations `scripts/phase224_common_date_hac.py`, `scripts/phase238_hac_bandwidth_sensitivity.py`, and `tests/test_phase238_hac_bandwidth_sensitivity.py` through the connected GitHub service before adding this file. The Phase 238 tests previously checked point-estimate invariance and loose standard-error bounds for equal-cell contrasts, but lacked a full numerical oracle for both equal-cell and pooled-count contrasts.

## New regression coverage

The accompanying additive test computes Bartlett weighted lag covariances independently of the Phase 224 function and compares variance, standard error and point difference for both contrast series across bandwidths 0 through 5. A second test rejects incomplete date panels. Six observations are deliberately synthetic, not SEC data. These tests verify arithmetic on a small fixture; they do not establish correct asymptotic inference, independence, historical data validity, or causality.

## Execution provenance

The container could not clone GitHub because DNS resolution for github.com failed. Instead, the source of Phase 224 and Phase 238 was retrieved through the connected GitHub service, transcribed into local temporary Python modules, and the two new test methods were run against those local transcriptions with `python -m unittest discover -s tests -v`. Result: 2 tests passed. The actual checked-out repository and its full test suite were **not** executed. This limitation is material and should not be obscured.

## Remaining work

Authenticate SEC source files, calendar and treatment classification; retrieve and inventory historical archives where licensing permits; execute exact repository tests in CI or a verified checkout; evaluate September pretrends, substantial October placebo effects, matched roster and selection sensitivity, exchange/security controls, and common-date plus security-cluster inference. Do not interpret the synthetic oracle as a market finding. No causal effect has been established.
