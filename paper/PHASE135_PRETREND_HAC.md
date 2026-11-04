# Phase 135: Pre-reform calendar-date HAC trends and leave-month-out sensitivity

Executed November 3, 2026, using the recovered Phase 131 processed matched-group panel. This is **descriptive analysis**, not a causal test.

## Input and audit

The recovered `roundlot_phase131_reproducibility_2026-11-03.zip` contains `daily_group_contrasts.csv`, with 14,416 group-date-outcome rows, 68 groups, 106 dates, and two outcomes. Input SHA-256: `6347d66cd7fa7ffa070b60529935e7ca9c93ef5c7f8dc61050fba33582f9aea1`. There are 87 complete pre-reform trading dates from July 1 through October 31, 2025. This is a processed contrast panel; the raw SEC and historical Nasdaq treatment lineage remain unauthenticated.

## Method

For each date, average the 68 matched-group percentage-point contrasts. Regress the daily mean on an intercept and trading-day index using OLS, with a Newey-West/Bartlett lag-5 heteroskedasticity-and-autocorrelation-consistent covariance and finite-sample multiplier n/(n-2). Report descriptive normal-approximation 95% intervals. Refit excluding each calendar month while preserving original trading-day indices. Calendar-day aggregation accounts for same-date group comovement in the descriptive time-series standard error, but does not identify a reform effect.

## Results

| Outcome | Pre-event slope (pp/trading day) | HAC(5) SE | Descriptive 95% interval | 20-day equivalent |
|---|---:|---:|---:|---:|
| Hidden trade count | -0.004083 | 0.009250 | [-0.022212, 0.014047] | -0.081650 |
| Hidden share volume | -0.027276 | 0.009124 | [-0.045158, -0.009393] | -0.545511 |

The full-period volume trend is downward under this descriptive specification, but excluding October changes its slope from -0.027276 to **-0.001464 pp/day**. Count also changes sign when October is excluded (from -0.004083 to **+0.028607 pp/day**). The full-period slopes therefore do not represent stable pre-event trends across calendar subperiods.

## Interpretation and limitations

1. These are **pre-reform treated-minus-control contrast slopes**, not a formal test of parallel trends or causal identification. Matching assignments are provisional.
2. October 1 was an information/publication event; removing October is a sensitivity analysis, not proof that October is contaminated or a valid counterfactual.
3. Lag 5 is a specification choice; alternate bandwidths, block resampling and calendar-time dependence require sensitivity checks.
4. No venue-level or security-level original records were newly authenticated here; the processed contrasts may reflect composition and weighting changes.
5. The recovered input was verified by SHA-256 locally, but is **not** independently verified against the original SEC source files. Do not describe these intervals as causal confidence intervals or interpret their exclusion of zero as evidence of a reform effect.

## Reproduction

Place the recovered Phase 131 `phase131/daily_group_contrasts.csv` directory beside `src/phase135_pretrend_hac.py` (or run a copy of the script from a directory containing that folder). Install pandas and numpy; run `python phase135_pretrend_hac.py`. The script writes `phase135_pretrend_hac.csv` and prints full precision. The public CSV is a rounded presentation extract, not a claim of bitwise equivalence to the generated file.

## Next work

Reconcile SEC raw quarterly data and Nasdaq round-lot assignments, then implement group-by-date block inference with alternative HAC bandwidths and explicit security/venue selection audits. The full historical ZIP archive is not yet on GitHub.
