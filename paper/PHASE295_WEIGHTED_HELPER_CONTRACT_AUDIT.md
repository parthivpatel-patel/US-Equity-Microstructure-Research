# Phase 295 — Weighted helper contract audit (2026-11-10)

## Scope and reproducible result

Read the published Phase 294 revision of `scripts/phase289_common_date_block_bootstrap.py` and `tests/test_phase294_numerical_safety.py`. The bootstrap entry point validates strictly positive integer pair counts and constructs equal positive weights for exchange weighting. However, the internal `_safe_weighted_mean(values, weights)` helper has no independent argument validation.

A standalone Python arithmetic reproduction of its current expression (not an execution of the full repository suite) yielded:

| Values | Weights | Observed outcome |
| --- | --- | --- |
| [1.0, 2.0] | [0, 0] | ZeroDivisionError |
| [1.0, 2.0] | [1, -1] | ZeroDivisionError |
| [1.0, 2.0] | [1] | 1.0 (silently truncates unmatched value) |
| [1e308, 1e308] | [3, 1] | 1e308 |

The mismatched-length case follows from Python `zip` truncation. The zero-weight cases follow from division by zero. **These invalid inputs are not reachable through the currently validated public bootstrap entry point**; this is a helper-level robustness finding, not evidence that current bootstrap outputs are wrong. A future caller importing the helper directly could violate the intended contract.

## Recommended code and tests

Validate nonempty, equal-length sequences; finite numeric values; finite strictly positive weights; and a finite, positive normalized denominator before computing a weighted mean. Include tests for zero, negative and nonfinite weights, unequal lengths, empty vectors, and the previously passing large-finite example. Preserve the outer entry point's provenance restrictions. Avoid claiming that any such tests passed until executed against the exact published checkout.

## Historical-evidence admission

This audit uses authored arithmetic inputs only. It does **not** authenticate SEC source observations, treatment labels, trading calendars, September pretrends, October placebo behavior, exchange/security controls, or hierarchical dependence-aware inference. No reform causal effect is established. Historical archives and the earlier source-integrity prototypes still require a complete verified inventory and licensing review. The November 14 manuscript target remains conditional on those unresolved tasks.
