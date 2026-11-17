# Phase 434 — Fail-closed common-date support gate (2026-11-17)

## Verified defect and correction

Reading the published Phase 433 implementation established that its cross-unit common-date intersection filters out group/exchange units with zero paired dates (`if x['paired_dates']`). Consequently, a positive reported intersection may reflect only a subset of units. This is documented in Phase 433 but remains unsafe as a universal eligibility gate. Phase 434 introduces a separate **fail-closed** eligibility gate over *all* reported units per period. It requires at least one unit, no zero-pair unit, and a nonempty intersection of all unit-level paired dates, separately for pre and post. Exit code 2 signals failure.

This is a deliberately conservative gate, not an estimator or a requirement that all studies use identical dates. Analyses intentionally selecting a smaller common-support population must declare that selection and quantify exclusions. Phase 433's original report remains unchanged.

## Reproduction

Run `PYTHONPATH=scripts python -m unittest -v tests/test_phase434_common_date_gate.py`. Then `python scripts/phase434_common_date_gate.py phase433_output.json --output phase434_gate.json`. Four deterministic tests passed locally (zero failures): excluded zero-pair unit, disjoint calendars, overlapping calendars, and empty units. All test observations are constructed, not SEC data.

## Outstanding empirical requirements

No authenticated SEC daily panel, original matched assignments, historical round-lot classifications, or recovered historical ZIP was imported. The September pretrend and October placebo warnings remain; source-data authentication, treatment identification, weighting sensitivity, fixed-security continuity, security/exchange controls, matched-group/date/serial-dependence-aware inference, and full repository test execution remain outstanding. Phase 430 prototype/tests are still not published. The November 14 publication deadline was missed; manuscript not publication-certified. This work is strictly independent of GIG.
