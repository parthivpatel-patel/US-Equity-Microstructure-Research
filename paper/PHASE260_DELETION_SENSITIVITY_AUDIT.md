# Phase 260 — Fixed-roster deletion sensitivity

This session adds a descriptive leave-one-matched-pair-out and leave-one-observed-date-out sensitivity audit for a complete, equal-weight, fixed-roster matched panel. This is not causal inference and does not estimate standard errors.

## Reproducible synthetic verification

Run `cd scripts && PYTHONPATH=. python -m unittest discover -s ../tests -p 'test_phase260_sensitivity.py'` (or run the test module with the scripts directory on PYTHONPATH). Eight deterministic tests passed in a local Python 3 execution. With two synthetic pairs having post changes of 2 and 4 over four dates, the full estimate is 3, deleting pair A yields 4 and deleting pair B yields 2. Maximum pair-deletion change is 1; maximum date-deletion change is 0 in this deliberately constant-within-period example. These numbers are synthetic only.

## Interpretation and limitations

Pair deletion diagnoses concentration in a small number of matched groups; date deletion diagnoses dependence on an individual observed date, not serial or common-date dependence. Neither is a valid confidence interval, placebo test, or robustness proof. This routine requires at least two pairs and two dates on each side, rejects duplicate cells, nonfinite values, booleans, weekend dates, and incomplete pair/date grids. It does not independently authenticate trading sessions, SEC source observations, exchange-level assignment, treatment classifications, or redistribution rights. It does not implement security/exchange fixed effects, alternative weighting, or clustered inference.

## Historical admission status

Historical estimation remains blocked pending independently authenticated SEC inputs, exchange calendars, frozen treatment rosters, source licensing and historical data reconciliation. September pretrends and the substantial October 2025 placebo remain active falsification warnings. No historical coefficients, p-values, or causal effects were produced. Previously recovered archives and unpublished Phase 252–254 scripts were not available for import in this session. The November 14, 2026 target is conditional.
