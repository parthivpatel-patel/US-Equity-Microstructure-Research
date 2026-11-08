# Phase 235: structural preflight integration (2026-11-08)

## Scope and execution
Inspected exact published Phase 230, 232, 233 and 234 sources through connected GitHub. Introduced a new opt-in entry point that runs the Phase 234 structural calendar-evidence validator before invoking the Phase 232 provenance-safe matched-HAC wrapper. It rejects missing dates, malformed rosters, duplicate/unsorted requested sessions, unpartitioned windows and missing caller attestation before downstream estimation. It strips any legacy `calendar_authenticated` field and explicitly marks independent verification false.

Nine deterministic unit tests passed locally with the actual published Phase 234 validator copied verbatim and an isolated stub for the downstream estimator. The stub deliberately returned a misleading legacy authentication field, which the new wrapper removed. Tests did not execute the full Phase 226 estimator. The local container could not resolve raw.githubusercontent.com; GitHub connector retrieval was used for source inspection.

## Evidence boundaries
All test dates and hashes are fixtures; example.org is not a real calendar source. A raw SHA256 supplied by a caller is metadata, not proof of source authenticity. The wrapper is additive and does not replace older entry points. It checks requested dates against a supplied roster but cannot independently establish holiday closures, ad-hoc exchange closures, full coverage or actual source retrieval. An incorrectly assembled weekday-only roster could still pass.

No SEC observations, historical coefficients, figures or causal effects were produced. The September pretrend, substantial October placebo warning, treatment assignment, weighting sensitivity, matched security/exchange inference and dependence-aware historical uncertainty remain unresolved. Historical research ZIPs were not accessible for authenticated import; complete unpublished inventory remains outstanding.

## Next action
Authenticate original SEC observations and an authoritative historical exchange-session roster, pin raw bytes and licensing evidence, and run the full real-dependency estimator on fixed security/exchange panels. Do not publish a causal claim or treat a passing fixture test as historical authentication.
