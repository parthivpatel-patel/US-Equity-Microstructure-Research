# Phase 292 — Calendar-gated common-date bootstrap

2026-11-10. Scope: software validation, not historical inference.

## Change
Phase 289's circular block bootstrap checks lexicographic ordering but does not independently verify canonical dates or exact coverage of a supplied session calendar. Phase 292 adds a wrapper that checks YYYY-MM-DD dates, valid Gregorian dates, strict uniqueness and chronological order, and equality of the observed session roster to a supplied expected roster before delegating to the unchanged Phase 289 estimator. Existing exchange completeness and numerical safeguards remain in Phase 289.

## Evidence
Twelve deterministic unittest cases passed locally on Python with the published Phase 289 implementation copied from the connected GitHub repository. Tests use constructed two-session, one-exchange data; the integration case confirms mean=2 and causal_inference_authorized=False. These numbers are synthetic test fixtures, not SEC estimates. Run from repository root: `PYTHONPATH=scripts python -m unittest discover -s tests -p 'test_phase292_calendar_gate.py' -v`.

## Important limitations
The expected calendar is caller-supplied and **not authenticated** by this wrapper. Neither source publisher, official market holidays, historical security roster, treatment classification nor licensed redistribution status is verified. No historical September pretrends, October placebo, November treatment effect, hierarchical matched-security/date bootstrap, or original SEC data were analyzed. The October placebo warning and treatment uncertainty remain decisive. No causal effect established.

## Publication and recovery backlog
Previously recovered research ZIPs, source-integrity prototypes from phases 287–288, and historical artifact inventory remain pending verification/import. No historical artifacts or invented figures were uploaded. Next: authenticate original SEC files and calendars, then run fixed-roster placebo and pretrend diagnostics before any causal claims.
