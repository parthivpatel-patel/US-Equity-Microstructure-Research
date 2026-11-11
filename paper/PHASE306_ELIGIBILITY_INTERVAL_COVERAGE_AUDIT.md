# Phase 306 — Eligibility-interval coverage audit (2026-11-11)

## Scope and distinction
Phase 305's declared-universe Cartesian product assumes each declared security–exchange pair is eligible on every expected date. That is not necessarily true for listings, venue participation, symbol changes, or security exits. A legitimate absence outside an eligibility interval must not be classified as a missing SEC observation. Conversely, absence inside a source-authenticated eligibility interval cannot automatically be imputed as zero trading.

## Local reproducible diagnostic
Implemented a standalone Python prototype `phase306_eligibility_intervals.py` with inclusive (security, exchange, first_date, last_date) eligibility intervals and a caller-supplied ordered exchange-session calendar. Its expected key set is the union of interval-constrained security–exchange–session triples. It detects missing and unexpected cells, duplicate keys, overlapping eligibility intervals and intervals containing no listed sessions. It refuses reversed intervals, noncanonical dates, duplicate/unsorted sessions, and weekends in the supplied calendar. Every result retains explicit `source_authenticated=False`, `eligibility_authenticated=False`, `calendar_authenticated=False`, and `causal_inference_authorized=False`.

Local execution: `python -m unittest -v test_phase306_eligibility_intervals.py`; **11 synthetic deterministic tests passed, 0 failed** on 2026-11-11. Cases included October 30–31 and November 3, 2025; these are constructed fixtures, not downloaded SEC observations. The prototype and tests were generated locally in this session but **not included in this commit**: transfer of those files into the connected GitHub write interface is pending. Do not mistake the test claim for a published-checkout CI result.

## Source and inference gates
Eligibility intervals require an independently documented source and timestamp, including handling of ticker changes, exchange changes, mergers and delistings. Exchange session calendars require an authenticated schedule, not simply weekday filtering. The original SEC security-date-exchange data must be independently fetched, hashed, schema-checked, and reconciled before any empirical estimates. This prototype does not resolve the September pretrends, large October placebo, treatment classification, selection/weighting sensitivity, or the security/matched-group/common-date/serial-dependence inference problem. It must not be used to claim a reform effect.

## Next action
Publish the tested prototype and its eleven tests, rerun from the exact published commit, then authenticate historical source files, eligibility intervals, and calendar before applying the coverage gate. Maintain an inventory of recovered historical archives, with licensing and checksum status. No archives were authenticated or imported this session.
