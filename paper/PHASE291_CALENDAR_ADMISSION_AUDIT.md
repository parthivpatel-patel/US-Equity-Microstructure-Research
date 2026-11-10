# Phase 291 — Canonical-date and exchange-calendar admission audit

Date: 2026-11-10. Scope: independent code audit and synthetic regression tests, **not historical SEC inference**.

## Verified code gap
The published Phase 289 `bootstrap_common_dates` checks only that each date is a string and lexicographically greater than the preceding date. Therefore an invalid calendar date such as `2025-02-29` can pass its date check, and an otherwise ordered series that skips an expected trading session can pass. Its common-date bootstrap does not independently authenticate exchange-session membership, exchange calendars, matched-security rosters or source provenance. These are input-admission limitations, not claims that historical results were corrupted.

## Tested candidate admission safeguard
The accompanying `tests/test_phase291_date_admission.py` implements a strict canonical ISO-date parser and exact equality against a **caller-supplied** ordered session list. Nine deterministic tests passed locally (Python unittest, 9/9, 2026-11-10), covering valid dates, impossible dates, noncanonical formats, Unicode digits, missing/extra sessions, duplicate calendar entries and complete matching. The tests use authored dates only; they are not evidence of an authenticated official trading calendar. The exact published GitHub checkout has not been rerun. This candidate is intentionally standalone and is **not wired into Phase 289**.

## Evidence and identification boundaries
An exact match to a caller-supplied calendar does not authenticate the calendar's publisher or verify exchange-specific halts. No authenticated SEC observations were admitted and no historical coefficients, charts or causal conclusions were generated. The substantial October 2025 placebo warning, September pretrends, treatment-assignment gaps, weighting and selection sensitivity, security/exchange confounding, and two-way matched-group/common-date dependence-aware inference remain unresolved. Phase 289 is date-block resampling only.

Previously recovered research ZIPs remain unimported and the historical artifact inventory is incomplete. Do not redistribute raw source data before licensing and hash/provenance review. November 14 is a conditional manuscript target, not a validated publication commitment.

Next: integrate the canonical-date guard into the Phase 289 admission pathway only after official session-calendar authentication; run repository-wide tests; authenticate original SEC files and fixed treatment rosters; then run September pretrends and October placebo analyses before interpreting November effects.
