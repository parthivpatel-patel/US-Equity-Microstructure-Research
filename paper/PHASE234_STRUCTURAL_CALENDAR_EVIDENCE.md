# Phase 234: Structural calendar-evidence validation (2026-11-08)

## Scope and finding
Inspected the exact published Phase 233 implementation. It accepts an arbitrary nonempty retrieval timestamp, HTTP URLs, and a roster without date parsing, ordering, uniqueness or weekend checks. These are structural provenance gaps, **not evidence of an invalid historical SEC result**.

The new additive validator rejects noncanonical dates, weekend sessions, duplicates, unsorted dates, HTTP sources, embedded URL credentials, naive or malformed timestamps, and malformed raw-source SHA256. It normalizes an offset-aware retrieval timestamp to UTC and calculates a reproducible roster digest. It **always** returns historical_calendar_authenticated=false.

## Verification
Ten deterministic unittest cases passed locally using Python. The tests use constructed fixtures and do not authenticate actual source documents or the NYSE holiday schedule. In particular, Labor Day 2025 (September 1) is a weekday: structural validation deliberately does not identify it as a closure. A source-authenticated exchange calendar and exact coverage check are still mandatory. The Phase 233 entry point remains unchanged; downstream migration is pending.

## Empirical and publication limitations
No SEC historical observations were loaded; no pretrend, placebo, causal coefficient or figure was computed. The October 2025 placebo warning, September pretrends, treatment classification, weighting and selection sensitivity, serial dependence, and source authentication remain open. No historical archives were available for import or inventory verification in this session. No causal effect is established. November 14 publication readiness remains conditional.
