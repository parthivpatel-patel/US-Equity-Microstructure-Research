# Phase 357 — Explicit security–session–exchange coverage gate (2026-11-14)

## Source and motivation
Read the existing Phase 352 calendar-serial implementation and Phase 356 missing-session identification audit before adding this independent, opt-in coverage utility. Phase 352 fills absent calendar scores with zero for a descriptive lag diagnostic. Such zero filling is not source authentication.

## Implemented contract
`scripts/phase357_coverage_audit.py` requires a complete, explicitly declared Cartesian grid of security × authenticated session × exchange. Each cell must carry exactly one externally verified status: `observed`, `source_missing`, `not_listed`, `not_trading`, or `exchange_not_applicable`. Only `observed` cells can carry nonnegative finite numeric metrics. An observed zero is separately counted and cannot be substituted for a missing source record. Duplicate, omitted, off-universe, invalid-status, malformed-date, and nonfinite-value cells fail closed. This is a coverage audit, not a mechanism for inferring the true status from absent data.

The calendar, listing status, exchange applicability, and source completeness must be authenticated upstream. The program deliberately does not infer a security's trading status or market closure from an empty record. It also does not certify the underlying source, provenance, or redistributability.

## Executed verification
Ten deterministic tests passed locally using Python unittest. They exercise observed zero versus missing, complete coverage, duplicate and omitted cells, invalid status/value combinations, nonfinite and negative metrics, off-universe records, and date validation. Tests are synthetic software checks, not SEC observations or empirical treatment effects. The exact published checkout and repository-wide suite are not claimed to have run.

## Identification consequences
Before constructing matched security–exchange contrasts or computing common-date inference, document source hashes, session-calendar provenance, security listing/round-lot eligibility, exchange coverage, and explicit missingness. Then report complete-case and observed-support sensitivity separately; never silently replace missing source observations with zero executions. The substantial October 2025 placebo warning, September pretrends, Phase 130 contradiction, treatment-authentication gap, weighting sensitivity, and uncalibrated serial covariance remain unresolved.

## Historical archive inventory
No historical ZIP, licensed market data, original 78 dated placebo observations, or recovered manuscript was accessible and authenticated in this session. None was imported. The existing repository content was preserved; this phase adds only code, tests, and this report.

## Next gate
Apply this schema to an authenticated source manifest and actual security-date-exchange panel, reconcile dated placebo observations, then run integrated pretrend/placebo tests with matched-group and common-date/serial dependence-aware sensitivity. No causal inference is warranted yet.
