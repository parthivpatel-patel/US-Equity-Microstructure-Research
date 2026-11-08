# Phase 232: provenance-safe calendar attestation adapter

Date: 2026-11-07. Independent US equity round-lot reform research.

## Source inspection and defect
The exact published Phase 230 bridge sets `calendar_authenticated=True` after a caller supplies `source_authenticated=True`, despite describing its method as `caller_attestation_not_independently_verified`. Phase 229 only validates a caller-pinned SHA256 and calendar membership; it does not authenticate an exchange calendar. This was verified by fetching both source files through the connected GitHub integration.

## Narrow repair
The additive Phase 232 adapter strips the ambiguous legacy boolean and exposes `calendar_caller_attested`, `calendar_independently_verified=False`, `calendar_verification_basis`, and `calendar_source_authentication_pending=True`. It preserves other estimator outputs. It does not alter the older Phase 230 function or establish historical source authenticity. Users of Phase 230 directly can still encounter the misleading field. A future migration should deprecate that field at the source.

## Tests and scope
Five deterministic unit tests passed locally with Python unittest. They inject a stub Phase 230 dependency and verify that caller attestation never becomes independent verification, the legacy field is removed, provenance remains pending, and an illustrative numerical result is preserved. The 0.25 fixture is synthetic, not an SEC estimate. The complete real dependency chain and historical panel were not executed.

## Empirical blockers
No authenticated original SEC source panel, independently verified exchange-session roster, or validated historical treatment classification was available in this session. The September pretrend, substantial October placebo, selection/weighting sensitivity, matched-security uncertainty, and original-data integrity issues remain unresolved. No causal effect is established. Previously recovered research ZIPs were not available for file-level inventory, rights review or import.

## Next
Authenticate original calendar and SEC input provenance independently, integrate the new adapter into a single canonical estimation entry point, execute real dependencies end to end, then rerun fixed-roster placebo and pretrend inference.
