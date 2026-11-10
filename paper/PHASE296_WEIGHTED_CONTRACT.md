# Phase 296 — Weighted-mean contract hardening (2026-11-10)

The existing Phase 289 bootstrap helper was inspected before this work. Its internal `_safe_weighted_mean` lacks explicit nonempty/equal-length and strictly positive finite weight validation; it can silently truncate mismatched inputs through `zip`. The public estimator currently constructs validated positive weights, so this is a helper-contract weakness, not proof of incorrect historical results.

A separate, fail-closed implementation is provided at `scripts/phase296_weighted_contract.py`, with tests at `tests/test_phase296_weighted_contract.py`. The standalone helper is **not yet integrated** into the Phase 289 estimator. Twelve local deterministic tests passed with zero failures using `python -m unittest -v test_phase296_weighted_contract.py` in a directory with the helper on the Python path. The published checkout has not independently been run. Inputs are authored synthetic cases, not SEC observations.

The new helper rejects empty or unequal-length inputs, boolean/nonfinite values, nonpositive/nonfinite weights, and nonfinite results. Normalized arithmetic mitigates intermediate overflow, without guaranteeing every floating-point edge case is exact.

No authenticated SEC data were loaded or analyzed. The September pretrend, substantial October 2025 placebo, treatment classification, exchange controls, selection/weighting sensitivity, and joint matched-security/common-date dependence-aware inference remain unresolved. The historical ZIP inventory and source-authentication artifacts are still incomplete. No causal reform effect is established. November 14 remains a conditional target.

Next: integrate and rerun the published estimator suite; authenticate original SEC inputs and trading calendars; execute fixed-roster placebo/pretrend analyses before interpreting November estimates.
