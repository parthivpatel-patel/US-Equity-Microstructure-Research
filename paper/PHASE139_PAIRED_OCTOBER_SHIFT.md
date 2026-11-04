# Phase 139 — Paired October slope-shift sensitivity (exploratory)

Date: 2026-11-04. **Executed on the recovered Phase 131 processed panel; original SEC source and treatment assignment remain unauthenticated. No causal claim.**

## Input and estimand

The archived processed panel `daily_group_contrasts.csv` passed SHA-256 `6347d66cd7fa7ffa070b60529935e7ca9c93ef5c7f8dc61050fba33582f9aea1`. There are 68 matched groups and 87 pre-November trading dates: 64 July–September and 23 October. Each outcome has a complete 87-by-68 panel. The estimand is **October within-month linear slope minus July–September linear slope** of equal-weighted matched-group contrasts, in percentage points per trading day. This differs from the earlier July–October pooled slope.

## Executed results (2,000 bootstrap draws per specification)

| Outcome | July–September slope | October slope | October minus July–September | 95% paired residual bootstrap, block 5 |
|---|---:|---:|---:|---|
| Hidden trade count | +0.028607 | −0.141590 | −0.170197 | [−0.276373, −0.061328] |
| Hidden share volume | −0.001464 | −0.157880 | −0.156416 | [−0.250259, −0.054541] |

All eight exploratory 95% intervals, for block lengths 3, 5, 10 and 15, exclude zero on the negative side. The full eight-specification output is in `results/phase139_paired_october_shift.csv`.

## Resampling design and limits

Within each of the two time segments, separately fit group-specific intercepts and linear slopes. The synthetic series adds jointly resampled, circular fixed-length calendar blocks of the full-panel residual matrix to those fitted values. A single resampled matched-group index vector and a single common-calendar block-index sequence are used across both periods and outcomes are analyzed separately. This pairs the two slope estimates in each replicate and preserves cross-group calendar shocks within sampled blocks.

**Caution:** The bootstrap is conditional on the two-segment linear trend model, approximate residual stationarity across October 1, circular boundary wraparound, and independent resampling of groups and dates. The October 1 information event could violate these assumptions. The group resampling may not preserve dependence between matched groups. Percentile intervals are exploratory, not validated hypothesis tests, and their zero exclusion is not evidence of a November reform effect. The October shift occurs **before November 3**, and therefore is a warning about identification, not a reform treatment estimate.

## Provenance and next work

Local script execution: Python, pandas and NumPy; fixed RNG seeds 139003/139005/139010/139015 for count and 139103/139105/139110/139115 for volume. Input hash checked before calculations. The public processed input remains absent, so the repository is not end-to-end reproducible yet. Next: publish permitted source-independent processed inputs or documented reconstruction, authenticate original SEC venue/security data and historical Nasdaq round-lot classifications, and test calendar-break sensitivity including October 1.