# Phase 297 — Identification and inference gate (2026-11-10)

## Scope and evidence
This audit inspected the repository's `scripts/phase289_common_date_block_bootstrap.py`, `scripts/phase296_weighted_contract.py`, and `tests/test_phase294_numerical_safety.py` on the default branch through the connected GitHub read interface. This is a source-code inspection, **not** an execution of the historical SEC panel or the published test suite. No empirical estimate, p-value, or historical figure is produced here.

## Findings
1. **Unit of resampling:** Phase 289 computes one weighted exchange contrast per date and resamples circular blocks of *dates*. It does not resample matched security groups. Thus it preserves within-date co-movement in already-aggregated exchange contrasts but does **not** propagate matched-pair selection uncertainty, security-level heterogeneity, or exchange-specific cluster dependence into a hierarchical interval.
2. **Weighting:** `pair_counts_by_exchange` is a fixed exchange-level roster, used as weights in `pair` mode. The bootstrap does not recompute the matched cohort or account for uncertainty in treatment assignment. Both `pair` and `exchange` modes should be reported side by side.
3. **Temporal dependence:** Circular blocks wrap the last date onto the first. This imposes a periodic boundary that may be implausible for short event windows; block-length sensitivity and a non-circular moving-block or stationary-bootstrap comparison are needed. No asymptotic coverage claim follows from the current deterministic unit tests.
4. **Intervals:** The code returns percentile endpoints from the sorted draws using integer index truncation, without interpolation. They are descriptive bootstrap intervals and must not be labeled randomization-inference p-values or causal confidence intervals.
5. **Provenance:** The estimator explicitly requires `source_authenticated=False` and returns `causal_inference_authorized=False`. It is not an authentication layer and cannot support a validated SEC result without separate source, trading-calendar, treatment, and roster verification.
6. **Numerical integration:** The stricter Phase 296 `safe_weighted_mean` helper is standalone. Phase 289 still calls its own `_safe_weighted_mean`; the contract is not integrated. Integration should preserve existing behavior on valid panels and add explicit invalid-input regression cases.

## Required empirical admission checks (not completed)
- Authenticate SEC security-date-exchange source files and permitted redistribution; record URLs, retrieval timestamps, byte lengths, hashes, field definitions, and missingness.
- Authenticate the 2025-11-03 treatment classification against actual pre/post round-lot definitions, and document the surviving-universe and matched-roster construction.
- Freeze cohorts and calendar before testing; assess September pretrends and multiple October placebo dates with the *same* model, controls, and weighting choices.
- Run security and exchange fixed-effect variants, pair-count and exchange-equal weighting, balanced and available-case samples, common-date block-length sensitivity, and matched-group-plus-date resampling. Account for multiple placebo comparisons.
- Keep the earlier substantial October placebo warning and September pretrends in the abstract and limitations even if November estimates appear significant.

## Publication decision
**Not validated for causal interpretation or final-paper completion.** The November 14 target remains contingent on authenticated historical inputs and executed diagnostics. Recovered historical ZIPs and prior source-integrity prototypes remain to be inventoried and reconciled before publication. No third-party source data are redistributed in this report.

## Next execution
Run the committed Phase 289/294/296 tests from a clean checkout, integrate the stricter weighted helper with regression tests, and prioritize actual historical SEC source authentication over further synthetic-only method expansion.
