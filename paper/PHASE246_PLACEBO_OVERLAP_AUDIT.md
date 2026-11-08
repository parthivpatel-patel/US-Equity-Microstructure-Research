# Phase 246 — Placebo-window overlap audit (2026-11-08)

## Verified scope
Reviewed the existing Phase 243 structural calendar guard and Phase 244 guarded placebo wrapper on the public repository. Added an additive, dependency-free diagnostic for overlapping symmetric fixed-width placebo windows. No existing source file was overwritten.

The audit treats each cut at index c with half-width h as the half-open observation interval [c-h, c+h). It counts shared session indices across every pair of cuts and identifies a greedily selected nonoverlapping subset. The latter is a *spacing diagnostic*, not an assertion of statistical independence.

## Executed synthetic verification
Ran `python -m unittest -v test_phase246_overlap_audit.py` from a local directory containing the module and test. Four test methods passed. For cuts [4,5,6], half-width 3 and 12 sessions, all three pairs overlap; shared-session counts are 5, 4, and 5. For cuts [3,9] and half-width 3, the windows do not overlap. These are synthetic index calculations, not SEC observations.

## Statistical interpretation
A scan of nearby placebo cuts repeatedly uses much of the same data. Treating the resulting statistics as independent tests, or interpreting the minimum nominal p-value as a prespecified result, is inappropriate. Even disjoint windows can share market shocks, security composition and serial dependence. A future historical scan must predeclare the cut grid, control multiplicity and account for time-series and security dependence. This audit does not itself compute adjusted p-values or correct uncertainty.

## Authentication and publication gaps
No authenticated SEC data, authoritative exchange calendar, treatment roster, original ZIP archive, or historical market coefficient was analyzed in this phase. Historical archives have not been imported or fully inventoried. The substantial October 2025 placebo warning, September pretrends, treatment authentication, selection and weighting sensitivity, and matched-security inference remain unresolved. No causal effect is established.

## Next execution
Integrate the overlap diagnostic into the Phase 244 guarded scanner; execute exact-repository integration tests; then authenticate original SEC inputs and the session roster before running fixed-roster September and October placebo scans. Preserve the separate equal-cell and pooled-count estimands.
