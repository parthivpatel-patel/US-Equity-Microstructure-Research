# Phase 153 — synthetic whole-scan null rejection audit

This is a simulation audit, **not** an estimate from SEC or Nasdaq observations. It extends the block-seam diagnostics by testing the actual frequency of rejecting a known no-break null.

## Executed design

- 100 independent seeded synthetic panels per method, each with nine groups and 87 calendar observations.
- AR(1) innovations with coefficient 0.7, combining a shared common-calendar shock and independent group shocks.
- Whole-scan statistic: maximum absolute difference between adjacent 20-observation OLS slopes.
- Group resampling with replacement, and a common calendar-block index shared across all groups.
- 199 bootstrap draws per panel, 10-observation blocks; finite-simulation upper-tail p-value with +1 correction.
- Both circular and noncircular moving-block variants; fitted group-specific linear trends retained under the bootstrap null.
- Executed with Python and NumPy using `python tests/test_phase153_null_size.py`.

## Actual synthetic results

| Method | Rejections at p <= 0.05 | Mean simulated p-value |
|---|---:|---:|
| Noncircular | 5 of 100 | 0.3093 |
| Circular | 10 of 100 | 0.3074 |

Tests for valid block indices, noncircular interior continuity, seeded reproducibility and output bounds passed. The results are **not** sufficient to rank the two resampling methods: 100 Monte Carlo panels yield wide sampling uncertainty, both variants use only one AR coefficient, and the group resampling and detrending procedure may be misspecified for other nulls. Mean p-values below 0.5 suggest the entire p-value distribution merits investigation, independently of nominal 5% rejection counts. The 5-versus-10 difference is not itself a validated statistically significant difference.

## Identification and provenance limitations

The substantial October 2025 placebo signal, September pretrends, unknown historical treatment membership, security/exchange composition, outcome weighting, and source-file authentication remain unresolved. No causal reform effect is established. No historical ZIPs or third-party data were imported in this phase.

Next: increase Monte Carlo replications, vary persistence, block length, group/date shock strength, and detrending; recover and authenticate the original panel before making empirical claims.
