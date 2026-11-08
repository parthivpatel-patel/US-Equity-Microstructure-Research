# Phase 229 — Pinned calendar membership gate (2026-11-07)

## Exact published-source audit
Read existing Phase 225 matched panel and Phase 226 bridge source before creating new files. Both lack exchange-session membership enforcement. Phase 228 independently demonstrated acceptance of September 1 (Labor Day) and September 6–7 (weekend) as synthetic trading dates.

## New reproducible safeguard
`scripts/phase229_session_gate.py` validates requested dates against a caller-supplied, sorted, unique, weekday-only session roster and requires a SHA256 pin computed from newline-terminated canonical ISO dates. It rejects requested sessions absent from that roster, malformed or duplicate rosters, weekend roster entries, and tampered rosters. An independent authoritative exchange calendar and independently verified digest MUST be supplied before use on historical data. **A checksum is not evidence that a calendar is authentic.** The function therefore returns `calendar_authenticated=False` deliberately.

Eight deterministic tests passed locally using only an explicitly illustrative calendar fixture: `python -m unittest -v test_phase229_session_gate.py`. This module is **not yet integrated** into Phase 226, so the old estimator still accepts invalid sessions. Integration must fail closed without weakening existing tests.

## Empirical and archive limitations
No historical SEC data were loaded or re-estimated. October placebo warning, September pretrends, treatment authentication, source provenance, weighting sensitivity, selection bias, and matched-security dependence remain open. No causal effect established. Approximately 129 previously reported ZIP archives were not accessible for inspection, so no complete file-level inventory or redistribution permission could be verified. No archives were imported.

## Next
Authenticate an authoritative 2025 exchange calendar and historical SEC panel; integrate this gate into the matched estimator with rejection tests; then estimate fixed-roster placebo/pretrend contrasts using full-series HAC plus security-level uncertainty sensitivity.
