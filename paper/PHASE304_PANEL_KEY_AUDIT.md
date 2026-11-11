# Phase 304 — Security–date–exchange panel-key audit

## Finding

Phase 303's `audit_calendar` requires one row per date. That is appropriate only for an already aggregated daily series; it is **not** a valid uniqueness condition for the proposed SEC security–date–exchange panel, where multiple securities and exchanges can share a trading date. Applying the Phase 303 helper directly to raw panel rows would reject legitimate observations.

Phase 304 supplies a separate structural checker with the correct composite key `(security, date, exchange)`. It reports duplicate composite keys, and, when an externally supplied expected-date list is provided, missing/unexpected dates separately for each **observed** security–exchange pair. It does not assume that every security trades on every exchange, and cannot detect wholly absent pairs. A supplied calendar may be unauthenticated and security listings may begin/end within the period, so missing pair-dates are diagnostic flags, **not automatically erroneous records**.

## Reproducibility

Run `python -m unittest discover -s tests -p 'test_phase304_panel_key_audit.py' -v` from the repository root. In an isolated local copy, nine synthetic deterministic tests passed (0 failures). The published checkout has not been independently executed. No SEC data were downloaded or analyzed; no numerical market-effect claim follows from these tests.

## Empirical release gate

Authenticate original SEC source files, date/session calendars, security and exchange identifiers, listing/venue eligibility, provisional treatment assignment, and historical lot sizes before interpreting September pretrends, October placebo effects, or November contrasts. Retain sensitivity to weighting and selection, security/exchange controls, matched-group uncertainty, common-date dependence, and serial correlation. The previously observed substantial October placebo warning remains unresolved. **No causal effect is established.**

## Inventory and publication boundary

This session adds a script, tests and this audit report. Previously recovered historical ZIPs, manuscripts, original SEC files, and historical charts have not been authenticated or imported by this session. No redistributability claim is made for those assets. November 14, 2026 remains a conditional publication target.
