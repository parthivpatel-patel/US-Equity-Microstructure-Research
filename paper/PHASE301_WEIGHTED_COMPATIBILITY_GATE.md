# Phase 301 — Weighted helper integration compatibility gate

Date: 2026-11-10. Scope: synthetic numerical contracts only; no SEC source observations were loaded.

## Source-code evidence
Read the published `scripts/phase289_common_date_block_bootstrap.py`, `scripts/phase296_weighted_contract.py`, `scripts/phase299_numeric_admission.py`, and `tests/test_phase294_numerical_safety.py` before this change.

The Phase 296 helper now rejects extreme integers and invalid weights. However, a direct substitution for the Phase 289 internal helper changes a floating-point result: `safe_weighted_mean([2,-2],[3,1])` returns `1.0000000000000002` while the older internal helper returns exactly `1.0`. This is a rounding difference (~2.22e-16), **not** a demonstrated material estimator bias. An existing Phase 294 regression asserts exact equality for a related panel mean, so blind integration risks test failures. Numerical equivalence should be checked with appropriate tolerances, and any change in published outputs must be disclosed.

## Reproduction
A local isolated reproduction of the Phase 296 implementation and Phase 299 admission logic executed six synthetic unittest cases: **6 passed, 0 failed** after using an approximate-equality assertion for the rounding case. The first exact-equality assertion failed as expected. This isolated execution is not a full repository checkout test. The committed `tests/test_phase301_weighted_compatibility.py` covers six analogous contracts against the repository imports, but was **not executed from the published checkout** in this session.

## Release decision
No change was made to the Phase 289 bootstrap estimator. Integration is deferred until the full regression suite can be executed, numerical tolerances and output-diff expectations are agreed, and the caller's input contract is preserved.

## Empirical identification remains blocked
September pretrends, the large October 2025 placebo signal, treatment roster authentication, selection and weighting sensitivity, exchange/security controls, matched-group and common-date hierarchical dependence-aware inference, and original SEC data provenance remain unresolved. The supplied calendar gate is not independently authenticated. No causal effect is established. No historical figures or coefficients were generated.

## Publication inventory
This phase publishes one regression test and this audit. Previously recovered historical ZIPs, original raw-data receipts, historical figures and complete source archive inventory remain unverified/unimported. Do not infer publication or redistribution permission from filenames. The November 14, 2026 manuscript target remains conditional.

## Next task
Execute the full repository regression suite on an exact checkout, reconcile exact-equality assumptions, and prioritize authenticated original SEC panel inputs and the September/October falsification analyses rather than interpreting November effects.
