# Phase 321 — Exhaustive finite-grid audit of extrema-informed placebo bounds (2026-11-12)

## Scope

This is a **synthetic mathematical falsification test**, not a new SEC-data estimate. The script enumerates every ordered sequence of length 1 through 5 over the integer grid {-3,-2,-1,0,1,2,3}, with event contrasts -2 and +2. For each sequence it computes the lower-tail count L, absolute-extreme count A, minimum, maximum, and observed right-tail count R. It groups sequences by the same published-summary information and checks whether the Phase 320 conservative interval contains every realizable R.

## Executed results

The script was executed locally using Python. The number of distinct feasible summary configurations was:

| Event contrast | n=1 | n=2 | n=3 | n=4 | n=5 |
|---|---:|---:|---:|---:|---:|
| -2 | 7 | 28 | 48 | 72 | 100 |
| +2 | 7 | 28 | 50 | 77 | 109 |

**526 distinct summary configurations passed; no counterexamples were found** within the enumerated grid. The enumeration comprises 2 × (7 + 49 + 343 + 2401 + 16807) = 39,214 synthetic sequences. The repository script re-executes this audit without third-party dependencies.

## Interpretation and limits

The test supports the internal consistency of the Phase 320 logical bounds on this finite grid. It is **not a proof of sharpness**, a proof for arbitrary real-valued placebo contrasts, or validation that the original 78 placebo observations, extrema and counts share the same data universe. It does not resolve the October placebo warning, September pretrends, treatment-label authentication, matched-group composition, weighting sensitivity, serial dependence, or source-data licensing. The Phase 320 count bound 76–77 and volume bound 28–75 remain conditional on the reported aggregate summaries being correct and comparable.

## Publication gate

Do not describe the study as causally identified or complete. Next: independently reconstruct all 78 placebo windows from authenticated underlying data; verify exact tie handling and window chronology, including the October 2025 announcement period; then estimate matched security/exchange contrasts with common-date and serial-dependence-aware uncertainty. The November 14 manuscript target remains conditional. Historical archive inventory and permission checks are outstanding.
