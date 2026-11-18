# Phase 450: paired-date estimator and common-calendar bootstrap (2026-11-18)

This is a **design-only, constructed-data-validated** estimator, not an analysis of authenticated SEC observations. Each exchange × matched-group × date cell contributes only if both treatment arms appear. Each arm is averaged equally across observed securities. Within each exchange × group stratum, the post-minus-pre change in treated-minus-control gaps is computed; eligible strata receive equal weight. Strata lacking paired common dates in either period are excluded.

A shared calendar-date bootstrap resamples whole dates *separately within pre and post*, preserving cross-stratum same-day co-movement. Replicates missing an arm/period for any eligible stratum are discarded, and a percentile interval is suppressed if fewer than 100 valid draws or less than 90% survive. This is **not** a serial-dependence-robust confidence interval: ordinary independent-date resampling does not preserve temporal autocorrelation. Use moving-block or stationary bootstrap, HAC, and matched-group/security clustering sensitivity before publication. Equal-security weighting is not share-volume or trade-count weighting. The procedure does not authenticate source data, infer treatment from historical round lots, establish parallel trends, or resolve selection bias.

Local prototype: 10 deterministic tests passed on constructed data on November 18, 2026. Published code and tests are independently re-authored equivalents; execution of the exact published checkout remains to be verified. Do not interpret synthetic test estimates as empirical findings.

## Outstanding blockers
- Authenticate original SEC data and its schema, timestamps, exchanges, and checksum/provenance.
- Authenticate November 2025 treatment status using dated source evidence; survivorship and exchange scope remain material.
- Re-estimate September pretrends and substantial October placebo warning before interpreting any reform coefficient.
- Compare trade-count, share-volume, equal-security, matched-group and composition-balanced estimands.
- Implement dependence-aware inference with shared calendar dates, serial blocks and security/group clusters.
- Inventory and license-check recovered historical ZIPs; Phase 430 and Phase 436 prototypes remain unpublished.
- November 14, 2026 publication target was missed; paper is **not publication-certified**.
