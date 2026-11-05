# Phase 158 — Recovered security panel and estimator sensitivity (2026-11-04)

## Material recovery and integrity

The historical Library search located and materialized **original archived files** `roundlot_phase2.py` (3,377 bytes; SHA-256 `55bcb359a29084c05ba87542796b9572a33a49ac3c4ddeed3474823b4e63ee8b`), `roundlot_phase2_security_panel.csv` (345,329 bytes; SHA-256 `2ccb80427a765ca3858f11f2874d6f87a79a559ec1fdeafc34420e82840e5bbb`) and `roundlot_pilot_daily.csv` (12,054 bytes; SHA-256 `9cd1e7f9fc89a2254211868e1a82cf97fd243bc860ad03eefa99409f94086bba`). Unlike Phase 157, the **actual archived Phase 2 security-level analytical panel and generating script are now accessible**. They are not the original SEC observation ZIP or Nasdaq snapshots; the panel's provenance is therefore still not independently authenticated.

The recovered panel contains 2,262 unique tickers, 68 provisionally treated and 2,194 comparisons, with no missing cells or duplicate ticker keys. All rate columns lie in [0,1]; stored change columns match post minus pre. Observed October days range 12–23 (mean 22.9593); November days range 12–19 (mean 18.9823). This audit does not test the original security/date/exchange keys, unavailable in this aggregated panel.

## Independent HC3 re-estimation from recovered panel

The accompanying Python script was executed against the recovered CSV using statsmodels. The baseline specification includes pre-period hidden-trade and hidden-volume rates. The weighted specification uses each ticker's minimum of pre/post eligible trade counts, so it is **a trade-count-weighted sensitivity estimator**, not a share-volume-weighted one. Trimming is symmetric in the *outcome change* across the full sample and can induce treatment-dependent selection; it is a stress test, not a preferred design.

| Outcome | Specification | N | Treated | Coefficient (percentage points) | HC3 SE (percentage points) |
|---|---|---:|---:|---:|---:|
| Hidden trade-count rate | Unadjusted | 2262 | 68 | -3.462929 | 0.441788 |
| Hidden trade-count rate | Baseline adjusted | 2262 | 68 | -1.081479 | 0.504068 |
| Hidden trade-count rate | Trade-count weighted | 2262 | 68 | -2.289331 | 1.147345 |
| Hidden trade-count rate | Trim 1% each tail | 2216 | 68 | -3.457133 | 0.434416 |
| Hidden trade-count rate | Trim 5% each tail | 2034 | 67 | -3.167058 | 0.394504 |
| Hidden share-volume rate | Unadjusted | 2262 | 68 | -2.572053 | 0.421320 |
| Hidden share-volume rate | Baseline adjusted | 2262 | 68 | +1.478913 | 0.556903 |
| Hidden share-volume rate | Trade-count weighted | 2262 | 68 | -0.972273 | 1.322863 |
| Hidden share-volume rate | Trim 1% each tail | 2216 | 68 | -2.634818 | 0.415962 |
| Hidden share-volume rate | Trim 5% each tail | 2034 | 65 | -2.281242 | 0.368105 |

For the weighted hidden-volume specification, the HC3 p-value is **0.4623541**, compared with approximately **0.00791665** for the baseline-adjusted specification. These HC3 tests remain *inadequate for final policy inference* because they do not address all calendar-date shocks, serial dependence, selection, or treatment misclassification. The large shift under baseline adjustment and weighting is an empirical warning against causal interpretation.

Pre-period means differ sharply: provisionally treated securities have mean hidden-trade rate **0.490516** versus **0.344845** in comparisons, and mean hidden-volume rate **0.492960** versus **0.291590**. Mean eligible trade counts also differ markedly (pre: **837,795.5** versus **214,079.6**). This supports the concern that the groups are structurally incomparable without stronger design work.

## Publication, provenance and limits

Only the executable audit and this report are published; the archived CSV, generating script, and pilot daily CSV remain retained outside GitHub pending redistribution/provenance review. The original `roundlot_phase2.py` requires three source files absent from the recovered set: `nasdaq_october_2025.csv`, `nasdaq_november_2025.csv(1).csv`, and `individual_security_2025_q4.zip`. No source-authentication claim follows from recovering the derived panel. No new October placebo or September pretrend was estimated from the aggregated Phase 2 panel because it lacks daily observations. The previously inventoried ~129 historical ZIPs remain unimported.

## Next task

Recover the original SEC daily archive and both Nasdaq snapshots, authenticate operative November 3 treatment, and reconstruct security-date-exchange observations. Then re-estimate September pretrends, October placebo dates, and event windows with fixed exchange composition, matched-group resampling, common-date shocks and serial dependence. Do not describe any current contrast as causal.
