# Phase 220 — Calendar self-consistency is not authentication

Date: 2026-11-07. Scope: independent US equity round-lot reform study. No historical SEC estimates or causal claims.

## New reproducible adversarial check

Five standard-library Python tests passed locally with `python -m unittest discover -s . -p 'test_phase220_calendar_adversarial.py' -v` in the test directory. This is an independent contract-level demonstration, **not execution of the exact repository's Phase 215/216 modules**.

The Phase 215 gate (read from the published repository) compares observed dates against caller-supplied dates. If the caller supplies an incorrect but internally consistent calendar, the gate cannot authenticate it. The Phase 218 fixture (also read from the published repository) filters weekdays, but September 1, 2025 (US Labor Day) is a weekday and is included by such a filter. An omitted session deleted from *both* observations and reference calendar is similarly invisible to an equality check. Omitting it from observations alone is detectable.

These are admission-model counterexamples, not claims of newly discovered historical data errors. The actual Phase 215 implementation explicitly sets `calendar_authenticated=False`; that qualification is correct and must be preserved.

## Required empirical gate

Before computing September pretrends, October placebo contrasts, or joint-window HAC on SEC data, freeze an independently sourced and dated US equity session list; retain URL, retrieval date, raw checksum, declared closures, and any unscheduled closures. Check each security/exchange panel against that list with explicit missingness and delisting handling. Never infer market holidays from weekday filtering alone.

Treatment assignment, panel provenance, October placebo, September pretrends, weighting, exchange composition, serial dependence, and matched common-date analysis remain unresolved. Do not publish causal conclusions. Previously recovered archives were not available to authenticate or import in this phase.

## Next step

Run the repository's actual Phase 219 tests in a clean checkout; independently authenticate the 2025 exchange calendar and original SEC extracts; only then estimate fixed-roster placebo and reform contrasts with security/exchange and common-date controls.
