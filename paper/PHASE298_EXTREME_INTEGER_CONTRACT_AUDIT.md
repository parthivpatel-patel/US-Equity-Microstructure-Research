# Phase 298 — Extreme-integer validation boundary (2026-11-10)

## Reproducible finding
Inspection of the published Phase 296 helper reveals that `math.isfinite` is applied directly to arbitrary-precision Python integers. In CPython, `math.isfinite(10**1000)` attempts float conversion and raises `OverflowError`. Therefore `safe_weighted_mean([1], [10**1000])` does not honor its documented fail-closed `ValueError` contract. This is a helper-level API/exception-consistency defect, not evidence that historical estimates are incorrect. The Phase 289 estimator's pair-count roster similarly accepts unbounded positive Python integers; this edge case warrants explicit admission bounds.

## Verification
A local self-contained reproduction of the exact Phase 296 helper logic ran three unittest cases with zero failures, including confirmation that the extreme-integer input raises `OverflowError`. The committed regression suite marks the desired `ValueError` behavior as `expectedFailure`, so it cannot be mistaken for a repaired implementation. The committed checkout was not executed. No SEC data were used.

## Recommended correction
Validate integer magnitude before calling floating-point predicates, or catch `OverflowError` and convert it into a documented `ValueError`. Explicitly define whether arbitrary-precision weights are supported. Add an integration test for Phase 289's actual roster admission and numerical aggregation. Do not silently clip weights.

## Empirical evidence and release gate
No authenticated SEC source panel, official trading-session calendar, or authenticated treatment roster was available for analysis in this phase. September pretrends and the substantial October 2025 placebo warning remain unresolved. Selection/weighting sensitivity, security/exchange confounding, and matched-group plus common-date serial-dependence inference remain pending. No causal claim is supported. The November 14 target remains conditional.

## Publication inventory
Phase 298 publishes this report and a synthetic regression test only. Previously recovered research ZIPs, historical code, figures and papers remain unverified and not imported; a complete archive inventory is outstanding. No proprietary observations or faux empirical figures are included.
