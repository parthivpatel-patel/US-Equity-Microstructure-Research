# Phase 435 — Joint fixed-security and common-date support gate

Date: 2026-11-17. This is a **structural software audit**, not a new empirical estimate.

## Defect addressed
Phase 432 reports the number of strict-support units but its CLI exits successfully when *at least one* unit passes, even if other included units fail. Phase 434 tests calendar overlap separately. An analyst could therefore mistakenly combine a partial fixed-security sample with calendar results from a different unit inventory.

## New gate
The new script consumes Phase 432 and Phase 433 JSON reports generated from the **same input CSV** and fails closed if any matched-group/exchange unit lacks strict fixed-security support, any unit is absent or duplicated between reports, any treatment assignment is unstable, pre/post common paired dates are empty, or observation counts differ. Output includes the actual intersection dates and failure reasons. Run:

```sh
python scripts/phase432_daily_fixed_support.py panel.csv --output daily.json
python scripts/phase433_calendar_support.py panel.csv --output calendar.json
python scripts/phase435_integrated_gate.py daily.json calendar.json --output joint.json
python -m unittest tests.test_phase435_integrated_gate
```

Eight deterministic tests passed in local prototype execution. The exact published checkout is not separately certified by that run.

## Limits and next steps
Matching observation counts does **not** cryptographically prove the two reports were produced from identical input files; add a shared input SHA-256 manifest and reject mismatches. Calendar intersection is conservative and can be overly restrictive across exchanges with heterogeneous trading schedules. The gate does not authenticate SEC source data, reform exposure, match assignments, or dependence-aware standard errors. The October placebo, September pretrends, estimator sign reversals and weighting sensitivity remain unresolved. No causal claim is warranted. Historical ZIP inventory/import and the unpublished Phase 430 prototype remain outstanding. November 14 publication deadline missed; paper not certified.
