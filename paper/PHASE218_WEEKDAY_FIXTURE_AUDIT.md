# Phase 218: calendar fixture reproducibility audit

Date: 2026-11-07. Scope: independent round-lot reform study.

## Verified defect in preceding test design

The published Phase 216 fixture advances from 2025-09-02 using `timedelta(days=i)` for 24 observations. It therefore includes weekend dates. Phase 215 admission checks consistency with a *caller-supplied* calendar, not whether the supplied calendar is a valid exchange calendar. Consequently, Phase 216's passing fixture alone cannot establish a valid trading-session lag structure. Phase 217 introduced a separate plausibility screen, but the Phase 216 test fixture was not corrected in place.

## New reproducible correction

`scripts/phase218_weekday_fixture.py` generates an ordered weekday-only *synthetic* sequence with 24 observations and two ten-session windows separated by four observations. It fails if the requested sequence crosses 2025-11-03. `tests/test_phase218_weekday_fixture.py` contains five unittest methods, locally executed successfully on 2026-11-07.

The generator **does not remove exchange holidays or unscheduled closures**. A deliberately adversarial test starts on 2025-09-01 (Labor Day) and verifies that this weekday is included, demonstrating that weekday filtering is **not** calendar authentication. Never treat this fixture as an authenticated NYSE/Nasdaq calendar or as empirical observations.

Run: `python -m unittest discover -s tests -p 'test_phase218_weekday_fixture.py' -v`.

## Outstanding validation and publication inventory

No authenticated SEC observation files, treatment assignment archive, or previously recovered historical ZIPs were imported in this phase. No historical estimates, causal effects, or real-data figures were produced. The September pretrends, October placebo warning, security/exchange controls, weighting sensitivity, common-date matched-group inference, and serial-dependence-aware *historical* inference remain unresolved. Recovered historical ZIPs are **not verified as published** by this checkpoint.

Next: replace the old fixture in a read-before-write change; authenticate exchange calendars and raw SEC source hashes; execute full clean-checkout tests; run fixed-roster placebo diagnostics on verified historical data. The November 14 deadline remains conditional.
