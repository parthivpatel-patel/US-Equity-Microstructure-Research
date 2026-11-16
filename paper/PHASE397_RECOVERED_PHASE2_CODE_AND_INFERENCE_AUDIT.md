# Phase 397 — Recovered Phase 2 executable and numerical-output consistency audit

Date: 2026-11-15. **Status: historical recovery and arithmetic audit, not a replication of raw SEC observations.**

## Recovery

The user's existing research Library yielded the original `roundlot_phase2.py` (3,377-byte file as indexed) and `roundlot_phase2_inference.csv` (five estimate rows). These are published unchanged in substance at:

- `archive/recovered_code/roundlot_phase2_2026-10-27.py`
- `archive/recovered_outputs/roundlot_phase2_inference_2026-10-27.csv`

The recovered script reads `nasdaq_october_2025.csv`, `nasdaq_november_2025.csv(1).csv`, and ZIP `individual_security_2025_q4.zip` member `q4_2025_all.csv`. Those raw inputs have **not** been recovered, authenticated, or redistributed here. The derived security panel `roundlot_phase2_security_panel.csv` was located in the user's Library but **not yet imported or independently analyzed**. Historical source licensing and redistribution must be checked before importing raw data.

## Actual numerical audit of the recovered inference CSV

Five output rows were parsed and their 95% confidence interval arithmetic independently checked against the recorded coefficient and HC3 standard error. Across all five rows, interval midpoint minus estimate had absolute error at most **5.1e-17**; half-width divided by SE was **1.95996398454** (up to displayed precision), matching the standard normal 97.5% quantile. This is a numerical *internal-consistency* check, not a check of the source observations, model fitting, or validity of HC3 for market-wide common shocks.

| Outcome | Specification | Securities | Treated | Estimate | HC3 SE | Recorded p |
|---|---|---:|---:|---:|---:|---:|
| Hidden trade rate | Unadjusted | 2262 | 68 | -0.0346292858694782 | 0.0044178773396563 | 4.561621427605987e-15 |
| Hidden trade rate | Baseline-adjusted | 2262 | 68 | -0.010814785925263 | 0.005040681518764 | 0.031912832373548 |
| Hidden share-volume rate | Unadjusted | 2262 | 68 | -0.0257205290109133 | 0.0042131965708826 | 1.029590749941424e-9 |
| Hidden share-volume rate | Baseline-adjusted | 2262 | 68 | +0.0147891302272283 | 0.0055690271663983 | 0.0079166543258392 |
| October-only placebo hidden trade rate | Unadjusted | 2258 | 68 | -0.011703298707258 | 0.0044241833298372 | 0.0081618163026794 |

The volume-rate coefficient reverses sign between unadjusted and baseline-adjusted specifications, a **0.0405096592381416** coefficient difference (about **4.05 percentage points**). The October-only placebo estimate has absolute magnitude about **33.8%** of the unadjusted main-period trade-rate estimate, despite being wholly pre-reform; this is a descriptive magnitude comparison, **not** a placebo-adjusted reform estimate or a valid ratio test.

## Design and code inspection

- Script computes security-level ratios of summed eligible counts/volumes for October 1–31 versus November 3–28, then equal-security-weight OLS with HC3 errors; it is not a date-by-security panel with common-date dependence adjustment.
- The script requires matching round-lot labels in October and November Nasdaq snapshots. This is a survivorship and treatment-authentication restriction, not proof of November 3 operative assignments.
- October placebo uses October 1–15 versus 16–31 and requires at least seven observed dates per subperiod, differing from the main period's minimum ten days. Therefore the 2,258-placebo and 2,262-main samples are not identical.
- The script drops duplicate Nasdaq symbols before joining, without documenting which duplicate is retained; ticker identity changes and exchange mix remain unaudited.
- The original code has a fixed `/mnt/data` input directory and requires unavailable raw data; no full reproduction was attempted or claimed.

## Remaining gate

Recover and authenticate the underlying ZIP and Nasdaq snapshots, then rerun the historical script in an isolated environment, inspect the existing derived security panel, and add matched-security/date and serial-dependence-aware tests. Preserve October placebo and September pretrend failures as identification warnings. No causal claim is justified. November 14 deadline missed; November 30 is provisional only.
