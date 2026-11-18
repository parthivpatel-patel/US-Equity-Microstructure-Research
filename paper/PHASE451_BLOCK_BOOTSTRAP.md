# Phase 451 — balanced-calendar circular moving-block sensitivity

Date: 2026-11-18. Scope: independent U.S. equity round-lot reform research only.

## New method
The Phase 450 resampler drew independent dates and did not preserve serial dependence. Phase 451 introduces circular moving-block resampling separately in pre- and post-cutoff periods. The same sampled date blocks are applied to all exchange/matched-group strata, retaining shared calendar shocks. A strict complete-case calendar intersection requires every included stratum to have treated and control observations on every retained date. Each stratum contributes equal weight.

The implementation checks finite outcomes, duplicate security/exchange/date rows, exchange-specific group assignment stability and security-global treatment consistency. It refuses inference unless both periods contain at least twice the chosen block length. It reports excluded unbalanced dates.

## Verification
Ten constructed-data unit tests passed locally with Python unittest after correction of a missing-date accounting defect identified by the initial failing test. No original SEC historical observations were analyzed. The exact GitHub checkout and full repository suite have not yet been executed.

## Interpretation
Percentile intervals are descriptive sensitivity diagnostics, **not** certified confidence intervals or causal evidence. Circular blocks assume sufficient within-period dependence stability; block-length selection is not calibrated. Complete-case date filtering can change the target population and may induce selection bias. The synthetic test's constant effect and zero-width interval do not describe market data. No figures or empirical effects are asserted.

## Publication gates
The November 14, 2026 target was missed. Historical SEC source authentication, historical treatment-size authentication, September pretrends, the substantial October placebo signal, selection/weighting sensitivity, dependence robustness and full reproduction remain open. Phase 430/436 recovered prototypes and historical ZIPs have not been imported or verified for licensing. No archival inventory is claimed complete.

Next: execute the exact published checkout, compare block lengths on authenticated original observations, preserve September/October placebo diagnostics, and integrate source-bound eligibility gates before reporting historical estimates.
