# Phase 137 — Joint matched-group and calendar-date residual block bootstrap

Executed November 4, 2026. **Exploratory and not a causal reform estimate.**

## Recovered input and validation

Used the Phase 131 ZIP already available in the working container, extracting `phase131/daily_group_contrasts.csv`. Its SHA-256 is `6347d66cd7fa7ffa070b60529935e7ca9c93ef5c7f8dc61050fba33582f9aea1`, matching the previously recorded manifest. The processed data have 14,416 records, 68 matched groups, 106 trading dates, two outcomes, unique group-date-outcome cells and no missing contrasts. This authenticates the recovered *processed-file bytes*, **not** the original SEC inputs or historical treatment assignments.

## Estimator and uncertainty

For each pre-reform period, estimate a common linear time slope from the equally weighted daily group contrasts. Remove each group's mean and the fitted common slope. For each of 2,000 seeded bootstrap draws, resample entire matched-group trajectories with replacement and apply a **shared** circular moving-block date index to their detrended residuals. This preserves contemporaneous cross-group residual alignment within each draw and local within-block time dependence. Reconstruct the fitted slope and report percentile ranges. Calendar block lengths are 3, 5, 10 and 15 trading days. The residual bootstrap relies on stationarity of detrended shocks and does **not** preserve arbitrary long-range dependence or guarantee calibrated confidence coverage. Centered-tail fractions in the CSV are exploratory only, not valid causal p-values.

## Results

| Outcome and sample | Slope (pp/day) | Block 5 percentile range | Block 15 percentile range |
|---|---:|---|---|
| Count, July–September (64 dates) | +0.028607 | [+0.007344, +0.049231] | [+0.003950, +0.055477] |
| Count, July–October (87 dates) | −0.004083 | [−0.022363, +0.014183] | [−0.031836, +0.022661] |
| Volume, July–September (64 dates) | −0.001464 | [−0.018764, +0.015891] | [−0.018553, +0.016121] |
| Volume, July–October (87 dates) | −0.027276 | [−0.044388, −0.011366] | [−0.049431, −0.005813] |

**Finding:** October changes the descriptive trend direction or magnitude substantially. The positive July–September count trend and negative July–October volume trend persist under these particular block-length sensitivity ranges. They are *pre-reform trends*, not November causal effects. The October 1 announcement makes the July–October window especially problematic as an untreated baseline.

## Execution checks

Executed the analysis with pandas and NumPy on the recovered input, generating 16 specifications. Separately passed a deterministic-seed repeatability check, injected positive-slope check, and fail-closed SHA-256 mismatch check. The script was subsequently published in a functionally equivalent cleaned form; exact reproduction of the CSV must be checked in a fresh checkout with the input supplied. A full environment lockfile, raw SEC lineage, historical round-lot assignments and source-level security/venue records remain unavailable.

## Replication

Run `python src/phase137_joint_block_bootstrap.py /path/to/daily_group_contrasts.csv /path/to/output --draws 2000`. Compare the generated `phase137_block_bootstrap.csv` with `results/phase137_block_bootstrap.csv`. The input is **not** redistributed in this repository pending provenance and rights review.

## Next steps

Verify output in a fresh checkout; compare alternative stationary/wild/bootstrap methods and non-linear trends; authenticate historical Nasdaq classifications, original SEC archives and venue/security coverage. The November 14 manuscript date is a target, not a completed-paper claim. No causal reform effect has been established.
