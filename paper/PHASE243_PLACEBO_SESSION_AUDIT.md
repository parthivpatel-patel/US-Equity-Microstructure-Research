# Phase 243 — placebo session structural audit (2026-11-08)

## Scope and verified finding
Reviewed the published Phase 242 scan implementation and six tests. Its date validation checks sorting and uniqueness, but does not parse calendar dates or reject weekends. Its synthetic test fixture includes 2025-10-04 (Saturday) and 2025-10-05 (Sunday), so the existing tests should not be interpreted as an exchange-session-valid historical placebo scan. This is a test-design and data-contract limitation, not evidence about market outcomes.

Added an additive guard in `scripts/phase243_placebo_calendar_guard.py` and ten deterministic tests in `tests/test_phase243_placebo_calendar_guard.py`. Run from repository root with `PYTHONPATH=scripts python -m unittest discover -s tests -p 'test_phase243_placebo_calendar_guard.py' -v`. Locally, ten tests passed using Python standard library only. This is not a full repository integration test.

## Authentication boundary
The guard validates canonical ISO dates, strict ordering, unique sessions, weekday structure, sorted unique integer cuts, and complete symmetric observation windows. It does NOT establish that weekdays are actual exchange sessions. For example, September 1, 2025 was Labor Day; the synthetic test deliberately demonstrates that a weekday-only guard still accepts this nontrading date. Historical exchange closures require independent authoritative source evidence.

## Interpretation and next work
The guard is not yet wired into Phase 242 and no SEC observations, authenticated treatment roster, or historical coefficients were used. No new empirical chart is warranted. The substantial October 2025 placebo warning, September pretrends, matching and weighting sensitivity, security/exchange controls, serial-dependence-aware inference, and treatment/source authentication remain unresolved. No causal effect is established.

Next: obtain an authoritative exchange-session roster with independently verifiable provenance, integrate this guard into the estimator path, and rerun prespecified September and October placebo cuts on authenticated historical observations. Recovered research ZIPs remain unavailable for verified import and inventory; no archive was uploaded in this session.
