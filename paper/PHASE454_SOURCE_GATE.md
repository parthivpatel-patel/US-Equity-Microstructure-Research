# Phase 454 — Byte identity and calendar membership gate (2026-11-18)

## Scope
A reproducible, fail-closed pre-estimation check for CSV byte identity and structural integrity. It compares supplied raw bytes to independently recorded SHA-256 digests; validates exact CSV schemas, dates, finite outcomes, boolean treatment encoding, unique security/exchange/date keys, unique session dates, and observation membership in the supplied calendar.

## Interpretation
**This is not authentication of historical SEC data or treatment assignments.** Hashes generated from the same unauthenticated files prove only internal consistency. The supplied session calendar is not verified against an authoritative exchange source. The gate does not check missing trading sessions between observed dates, stable treatment/group assignment, matched-arm support, September pretrends, October placebo, weighting sensitivity, or serial correlation. Phase 453's session preflight and Phase 451's bootstrap remain separate and are not yet wired into a certified pipeline.

## Verification
Eight deterministic unit tests were executed locally against a functionally equivalent implementation, with 8 passing and 0 failing. The published implementation was separately transcribed into the GitHub connector; **the exact published checkout and repository-wide suite have not been executed**. Constructed fixtures only; no historical SEC observations, estimated effects, or new empirical results.

## Publication blockers
The November 14, 2026 target was missed. Manuscript not publication-certified. Original source downloads and their independent hashes, historical round-lot treatment assignments, the September pretrend warning, substantial October placebo effects, selection/weighting sensitivity, common-date inference and serial dependence remain unresolved. Recovered historical ZIPs and Phase 430/436 prototypes have not been imported or authenticated.

## Next
Run tests from the published checkout; independently establish original SEC file provenance and authoritative session-calendar sources; integrate the gate with Phase 453 and the paired estimator without weakening their preconditions. Only then perform actual-data diagnostics. No causal inference is warranted.
