# Phase 299 — finite-float admission gate (10 November 2026)

## Verified scope
The existing Phase 296 weighted helper invokes `math.isfinite` on unbounded Python integers. `math.isfinite(10**1000)` raises `OverflowError`, contrary to the documented fail-closed `ValueError` contract. Phase 298 records this as an expected failure.

This phase adds a **standalone**, explicit finite-float admission function which converts allowed exact `int` and `float` types inside an overflow guard and rejects Boolean, complex, string, nonfinite, and unrepresentably large integer inputs. Six deterministic synthetic unittest methods passed locally on 10 November 2026 (0 failures). The repository checkout was not separately executed. This helper has **not** been integrated into Phase 296 or Phase 289; therefore the existing production-path defect remains unresolved.

## Scientific status
No historical SEC observations, treatment assignments, or calendars were authenticated in this phase. September pretrends, October placebo effects, security/exchange controls, matched-group and common-date hierarchical inference, and weighting sensitivity remain unverified. No causal effect is established. The November 14 manuscript target is conditional. Previously recovered ZIP archives have not been inventoried or imported in this phase.

## Next
Integrate admission into Phase 296 after reading current source; rerun existing and new tests, including extreme integer and underflow cases. Then prioritize original SEC source provenance and historical placebo analysis. No third-party data or invented charts are included.
