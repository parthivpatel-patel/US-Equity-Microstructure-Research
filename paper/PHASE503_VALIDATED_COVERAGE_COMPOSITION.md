# Phase 503 — Fail-closed date-integrity and coverage aggregation

Date: 2026-11-20. Status: **synthetic-fixture validation only**.

## Motivation
Phase 501's descriptive coverage aggregation accepts arbitrary nonempty date strings and supplied pre/post labels. Phase 502 checks date and period labels separately. This new standalone implementation combines both checks so an invalid row cannot reach the descriptive aggregation. It preserves the Phase 501 output schema, including distinct equal-date and eligible-count weighted gaps on common support.

## Verification
Local command: `python -m pytest -q test_phase503_validated_coverage.py` with both Phase 503 files in one directory. Result: **14 passed in 0.06 s** on constructed fixtures. This is not a test of authenticated SEC records, nor of the exact remote checkout. A cutoff observation dated 2025-11-03 is assigned to post; noncanonical and impossible dates, mismatched labels, duplicate exchange-dates, invalid counts, excluded dates, and empty common support are explicitly exercised. All input rows are validated before output is produced.

## Interpretation and unresolved gates
Coverage gaps are diagnostics for missingness, **not estimates of hidden-order execution or reform effects**. The exclusion list is caller-supplied and is not a verified market calendar. Exchange IDs and treatment labels are not authenticated; neither are SEC source files, security identifiers, or historical round-lot assignments. Do not use this to infer causal effects. The September pretrends, substantial October placebo, treatment authentication, selection sensitivity, common-date and serial-dependence-aware inference remain open.

## Recovered archive inventory
Phase 430/436 historical ZIPs and Phase 472 artifacts: not verified or imported in this phase. No third-party raw data or purported empirical figures are published.

## Next gate
Obtain and authenticate permitted historical SEC panel/eligibility source records and trading dates, then apply this diagnostic to September/October before re-estimating any placebo or reform comparison.
