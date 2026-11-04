# Phase 136 — Group-cluster and common-date HAC sensitivity

**Executed November 3, 2026. Exploratory descriptive analysis only.**

## Input integrity

The recovered Phase 131 `daily_group_contrasts.csv` was extracted from the previously archived reproducibility ZIP. Its SHA-256 matches `6347d66cd7fa7ffa070b60529935e7ca9c93ef5c7f8dc61050fba33582f9aea1`. The processed panel contains 14,416 group-date-outcome records, 68 groups, 106 dates, and two outcomes. No original SEC source-level authentication was performed.

## Estimator

For each outcome, regress group-demeaned daily treated-minus-control contrast on a common centered trading-day index. Compute CR0 sandwich score variances using (a) matched-group clustering, (b) calendar-date Bartlett/Newey–West HAC scores at lags 0, 3, 5, 10, 15, and (c) subtract cell-level HC0 overlap. The two-way variance is `V_group + V_date_HAC - V_cell`. No small-sample correction; 1.96-SE intervals are **heuristic**, not calibrated confidence statements under all dependencies. This approach is more sensitive to group and date covariance than date-only HAC, but does not model arbitrary nonlinear pretrends or identify a causal effect.

## Results (percentage points per trading day)

| Outcome | Period | Slope | Two-way SE lag 0 | Two-way SE lag 5 | Two-way SE lag 15 | Heuristic 95% range, lag 5 |
|---|---|---:|---:|---:|---:|---|
| Hidden trade count | July–October | -0.004083 | 0.006697 | 0.010278 | 0.012910 | [-0.024227, +0.016062] |
| Hidden trade count | July–September | +0.028607 | 0.008595 | 0.011414 | 0.012910 | [+0.006235, +0.050979] |
| Hidden share volume | July–October | -0.027276 | 0.008278 | 0.011122 | 0.012546 | [-0.049074, -0.005477] |
| Hidden share volume | July–September | -0.001464 | 0.008922 | 0.010314 | 0.008963 | [-0.021680, +0.018752] |

The full July–October hidden-volume slope remains negative under this sensitivity calculation. Its July–September counterpart is close to zero. Conversely, the July–September hidden-count slope is positive. This reinforces the central October information-event and specification-sensitivity warning. The trend estimates match the Phase 135 point estimates.

## Scientific limitations

The October 1 round-lot assignment publication is not a no-information placebo; October must not be treated as an ordinary pre-reform month without qualification. Group contrasts are already aggregated and cannot resolve security-by-exchange composition, venue missingness, or treatment classification errors. Time scores are Bartlett-HAC rather than a validated joint block-bootstrap distribution. Source data, matched cohort provenance, historical Nasdaq round-lot assignments and cross-venue controls remain unverified. No causal effect has been established.

## Reproduction

Run `python src/phase136_two_way_trend.py /path/to/daily_group_contrasts.csv` with pandas and NumPy. The script checks the archived input SHA-256, balanced structure and duplicates, then writes `results/phase136_trend_uncertainty.csv`. The processed input itself is **not included on GitHub** pending source rights and lineage checks.
