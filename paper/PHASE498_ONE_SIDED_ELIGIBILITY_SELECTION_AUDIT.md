# Phase 498: one-sided eligibility selection audit (2026-11-20)

## Source-level finding

Reading the published Phase 496 `support_gate` reveals that its exchange-level admission calculations include only units with eligible dates on **both** sides of the cutoff. This is a defensible conditional estimand, but it does not establish complete coverage of the **entire** eligible exchange universe. The returned `eligible_units` count is the two-sided subset, not all eligible units.

## Constructed counterexample (not SEC data)

Two units, A (treated) and B (control), are eligible and observed on 2025-10-01 and 2025-10-03. Unit C is eligible only on 2025-10-01 and is never observed. The Phase 496 logic admits exchange X, reporting two eligible units, because C is excluded from its two-sided subset. The independent exclusion audit reports three eligible units, two two-sided units, one excluded one-sided unit, one missing observation among excluded units, and total eligible-observation coverage of 4/5.

This does not prove the Phase 496 implementation incorrect for its stated *two-sided conditional* population. It shows that treating that admission as a certificate for all eligible exchange observations would be incorrect and could conceal selection or missingness associated with entry/exit.

## New reproducible files

- `scripts/phase498_exclusion_audit.py`: descriptive counts by exchange, with strict canonical-date and duplicate/out-of-universe checks.
- `tests/test_phase498_exclusion_audit.py`: five deterministic tests (local development implementation: 5 passed in 0.06s). Published checkout still requires independent execution.

## Empirical admission requirements

Before any September pretrend, October placebo, or November treatment comparison, report both (a) two-sided conditional support and (b) all-eligible coverage and one-sided exclusions by exchange and treatment group where authenticated labels permit. Evaluate whether entry/exit, missingness, and weighting change the estimated contrast. Date intersections and complete cases do not establish exogeneity. Historical SEC source provenance and treatment assignment remain unauthenticated; no new empirical effect estimates or causal claims are made.

## Publication and archive inventory

November 14, 2026 target missed; manuscript not publication-certified. Previously recovered Phase 430/436 ZIPs and Phase 472 materials remain unverified and unpublished; this phase does not import them. No licensed raw data or invented figures are included.
