# Phase 233 — Calendar evidence boundary (2026-11-08)

## Source inspection
Read the published source of Phase 229 (session gate), Phase 230 (calendar-gated HAC), Phase 232 (provenance-safe wrapper), and Phase 226 (matched HAC bridge) before this change.

Phase 229 verifies a digest of a caller-supplied calendar, rejects weekend entries, and checks membership. It does **not** authenticate exchange holidays or the source of the calendar. Phase 230 requires a caller-supplied `source_authenticated=True` assertion, not independent proof. Phase 232 corrects its output metadata but does not authenticate inputs.

## New safeguard
`scripts/phase233_calendar_evidence.py` creates a conservative evidence record requiring a source URL, retrieval timestamp, raw-source SHA256, and explicit documentation of any independent review. Even documented review does not automatically set `historical_calendar_authenticated` to true: source identity, historical session validity, and cross-source agreement remain to be checked separately.

Seven deterministic unit tests passed locally on 2026-11-08 with Python unittest. No historical SEC data or external calendar were used. These tests do not prove real exchange-calendar validity.

## Research status
The September pretrend and October placebo warnings, treatment classification, source authenticity, weighting sensitivity, and security-cluster inference remain open. No new empirical estimates or causal claims. Historical archives were not available for import or a complete file-level inventory in this session.

## Next work
Obtain and retain permitted original SEC releases and authoritative historical exchange-calendar records; record raw-byte hashes, timestamps, and independently check session dates before re-estimating fixed-roster matched placebo contrasts.
