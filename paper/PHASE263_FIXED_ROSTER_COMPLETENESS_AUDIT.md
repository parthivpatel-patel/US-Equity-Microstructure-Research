# Phase 263: External fixed-roster coverage gate

Date: 2026-11-09. Status: structural software audit only.

## Finding
The Phase 262 calendar gate derives its roster from the union of pairs appearing in the observed data. A pair that disappears from **every** observed date is absent from that union and can evade detection. This is a selection failure even when all dates are present.

Phase 263 accepts an externally fixed expected pair roster and expected session sequence, then compares the full Cartesian product of expected dates and pairs with actual observations. Missing or extra cells are enumerated. No missing data are imputed.

## Verification
Twelve deterministic synthetic Python unit tests passed locally using `python -m unittest -v test_phase263_roster_gate.py`. The published script and test are equivalent to the executed files; the complete repository test suite was not run. Example: a two-pair, two-date panel with pair B missing on both dates yields **two missing cells**, rather than a false complete-roster result. This is a synthetic test, not a historical SEC estimate.

## Evidence and inference limitations
Neither the expected roster nor calendar is authenticated by this function. The output explicitly leaves source, calendar, treatment, and inference authorization false. The code does not estimate an effect or handle serial/cross-sectional dependence. The October 2025 placebo warning, September pretrends, weighting sensitivity, exchange/security controls, and treatment authentication remain open. No historical observations or recovered archives were imported.

## Publication backlog
Historical ZIPs and prior unpublished Phase 252–254 implementation files remain unverified/unimported. Do not infer source authenticity from a passing structural gate. Next: acquire independently authenticated source snapshots, calendar and treatment roster; then execute fixed-sample historical pretrend and placebo analyses with common-date and serial-dependence-aware uncertainty.
