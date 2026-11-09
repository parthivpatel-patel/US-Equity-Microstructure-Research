# Phase 252 — Evidence ledger structural verification (2026-11-08)

## Verified work
Inspected the published Phase 251 admission audit and confirmed that the current policy depends on caller attestations rather than independent evidence. Built an offline, fail-closed prototype for structural manifest checks: required metadata, HTTPS source references, UTC timestamps, SHA-256 and byte-size comparison, path containment, distinct analysis and redistribution rights, and mandatory SEC/calendar/treatment categories.

Eight deterministic tests passed locally under Python unittest (8/8; 0.007 s). Cases: matching bytes never confer authenticity; tampered bytes; path traversal; naive timestamp; separate rights; missing roster categories; duplicate categories; boolean file size. The tests used synthetic bytes, not original SEC observations. This is an isolated local test run, not a verified full-repository checkout.

## Important distinction
Hash verification establishes only consistency with the supplied digest, not independent source authentication. A caller-controlled manifest can provide a matching digest for an incorrect file. The prototype therefore **never** sets historical-inference admission to true. Publication URLs, dates, publisher identity, session roster, treatment assignments and rights still require external independent review.

## Empirical status and limitations
No new historical SEC data were authenticated, no historical coefficients or charts were generated, and no historical ZIPs were imported. The September pretrends, substantial October placebo warning, treatment-classification uncertainty, selection/weighting sensitivity, common-date shocks and serial/cross-sectional dependence remain unresolved. No causal effect is established.

## Next actions
Retrieve original SEC source files and independent exchange-session documentation, freeze treatment classification and matched controls, run exact repository tests, then execute pre-specified September/October placebo windows with security/exchange controls, common-date shocks and dependence-aware inference. Maintain a full inventory of recovered archives before import and do not redistribute source data without permission.
