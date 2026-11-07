# Phase 217 — Candidate session-calendar plausibility audit

Date: 2026-11-07. Independent U.S. equity microstructure research; unrelated to GIG.

## Identified reproducibility issue

The Phase 216 synthetic integration fixture advances dates with `timedelta(days=i)`, thereby labeling Saturdays and Sundays as candidate trading sessions. Phase 215 checks consistency against a caller-supplied session list, but cannot establish that the list represents actual U.S. equity trading sessions. Passing that fixture therefore does not validate an exchange trading calendar.

## New screening control

`scripts/phase217_session_audit.py` rejects weekend sessions, duplicate/out-of-order dates, noncanonical dates, reform/post-reform dates, unexplained missing weekdays, and supplied closure/session conflicts. It allows caller-supplied weekday closures only as unverified exceptions. Its result explicitly sets `exchange_calendar_authenticated=False` and `historical_inference_validated=False`.

Nine deterministic tests passed locally on 2026-11-07 using `python -m unittest discover -s tests -v` in an isolated working directory containing this module and its tests. This is **not** a clean-checkout test of the entire repository. The published files require independent re-execution.

## Limitations and outstanding historical evidence

A weekday plausibility screen cannot authenticate NYSE/Nasdaq holidays, extraordinary closures, half-days, security-specific suspensions, SEC source files, Nasdaq round-lot treatment assignments, or exchange/security coverage. It is not yet wired into the Phase 216 estimator. No historical coefficients or research figures were calculated.

The October 2025 placebo warning, September pretrends, matched-roster selection, weighting sensitivity, common-date controls, and dependence-aware historical uncertainty remain unresolved. Previously recovered research ZIPs and original source observations were not available for import during this phase. No new historical archive inventory entries were verified.

## Next work

Replace the weekend-containing Phase 216 fixture with an authenticated calendar-derived fixture; run the full test suite from a clean checkout; verify SEC source hashes and Nasdaq treatment classification; then estimate fixed-roster matched-group pretrends and October placebo windows with joint-window HAC sensitivity. Do not interpret results causally without identification checks.
