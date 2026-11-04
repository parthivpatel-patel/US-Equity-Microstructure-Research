# Phase 138 — Published-bootstrap sensitivity and inference audit

Date: 2026-11-04. **Numerical audit of existing Phase 137 published output, not a new source-data estimate or a causal test.**

## Materials and verification scope

Read the public `src/phase137_joint_block_bootstrap.py`, `results/phase137_block_bootstrap.csv`, and `paper/PHASE137_BLOCK_BOOTSTRAP.md` directly from the repository. Independently parsed the 16-row CSV and recomputed each interval's width and zero-exclusion status. The original processed panel was not available for a fresh bootstrap execution in this session; therefore this audit cannot authenticate the original SEC records, the historical treatment assignments, or the published script's full numerical reproduction.

## Recomputed interval sensitivity

Widths are 97.5th minus 2.5th percentile endpoints, in percentage points per trading day. 'Excludes zero' is a descriptive property of the published bootstrap interval, **not** a valid test of the reform's causal effect.

| Outcome | Pre-reform sample | Slope (pp/day) | Width, block 3 | Width, block 15 | Excludes zero for all four blocks? |
|---|---|---:|---:|---:|---|
| Hidden trade count | July–September | +0.028607 | 0.036693 | 0.051527 | Yes |
| Hidden trade count | July–October | −0.004083 | 0.031488 | 0.054497 | No |
| Hidden share volume | July–September | −0.001464 | 0.033753 | 0.034674 | No |
| Hidden share volume | July–October | −0.027276 | 0.029222 | 0.043618 | Yes |

The count July–September interval widens by approximately 40.4% from block 3 to block 15. The count July–October interval widens by approximately 73.1%. The volume July–October interval widens by approximately 49.3%. The volume July–September width is not monotonic in block size. The directional zero-exclusion pattern happens to persist across the four reported block choices, but the estimated uncertainty is materially bandwidth-sensitive.

## Methodological limitations identified by reading the source

1. The script uses circular **fixed-length** moving blocks, not a stationary bootstrap with random block lengths. Wraparound residual segments can join the end of October to the beginning of July; this assumes an approximately stationary detrended residual process.
2. Each group's intercept is removed before resampling and a common slope is imposed. The procedure is conditional on a linear common-trend specification and does not validate nonlinear, security-specific or exchange-specific pretrends.
3. The `centered_null_tail_fraction_exploratory` statistic is calculated as `mean(abs(slopes-beta) >= abs(beta))`. This is a centered-bootstrap tail diagnostic, not a null-imposed hypothesis test; it should **not** be reported as a conventional p-value.
4. Comparing the July–September and July–October percentile intervals does **not** test their difference. The samples overlap, and their bootstraps were not paired to estimate a covariance-aware distribution of the slope change. A separate, prespecified joint resampling design is needed.
5. The October 1 information event and earlier October placebo warnings mean the July–October sample cannot safely be described as an untreated control period.
6. The processed panel's checksum validates byte identity only. It does not authenticate raw SEC data, matched-group construction, exchange composition, or historical Nasdaq treatment assignments.

## Reproduction and next steps

`python tests/audit_phase138_bootstrap_table.py results/phase137_block_bootstrap.csv` checks schema, all 16 expected cells, finite numbers, bounds and the interval-width/zero-exclusion summary using only the Python standard library. The script is newly published and **was not run with a Python interpreter in this session**; the underlying calculations were independently evaluated using JavaScript against the fetched CSV.

Next: recover the processed panel and original source records; rerun Phase 137 from a clean environment; implement a paired, common-date-aware comparison of July–September versus July–October slopes; add venue/security-level composition checks and provenance authentication. Until those checks are complete, do not interpret any pretrend or bootstrap statistic as a causal November reform effect.
