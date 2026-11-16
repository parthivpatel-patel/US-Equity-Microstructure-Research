# Phase 404 — October pre-reform daily trend audit (2026-11-16)

## Empirical input and scope
Recovered Library file `roundlot_pilot_daily.csv`, SHA-256 `9cd1e7f9fc89a2254211868e1a82cf97fd243bc860ad03eefa99409f94086bba`. October 2025 contains 23 observed trading dates, each with the three aggregate lot categories (10, 40, 100). These are **tier-level**, not security/exchange observations. Source SEC provenance and redistribution rights remain unverified, so the raw file is not published.

## Newly computed results
For each October trading date, aggregate 10- and 40-share tiers using the sum of numerators divided by sum of denominators; subtract the corresponding 100-share-tier rate. Fit OLS of that daily percentage-point gap on observed-session index, with Newey-West/HAC standard errors (5 lags). HAC p-values are exploratory, not confirmatory causal inference.

| Outcome | First date gap (pp) | Last date gap (pp) | Slope (pp/session) | HAC SE | HAC p |
| --- | ---: | ---: | ---: | ---: | ---: |
| Hidden trade-count rate | 12.6977 | 10.9537 | -0.0780 | 0.0456 | 0.0868 |
| Hidden share-volume rate | 11.1540 | 11.1610 | +0.0334 | 0.0583 | 0.5667 |

Across October sessions the daily trade gap ranges from 10.9537 to 15.5310 pp and the volume gap from 11.1540 to 19.5504 pp. No significant linear October trend at conventional 5% thresholds in these exploratory HAC regressions; this **does not negate** the previously observed October placebo *level shifts* or other September pretrends. Testing the slope is not a substitute for a placebo reform-date test. Tier composition and changing denominators can confound trends.

## Reproduction and tests
`python scripts/phase404_october_trend.py /path/to/roundlot_pilot_daily.csv` (requires numpy and statsmodels).
`PYTHONPATH=scripts python -m unittest discover -s tests -p 'test_phase404_october_trend.py'`.
Three local deterministic tests passed: constant-gap slope, invalid numerator, and duplicate date-tier rejection. The entire published checkout was not executed.

## Outstanding identification and provenance gaps
Original SEC security-exchange-day panel, September data, authenticated historical treatment sizes, 204-control matched mapping, 78 dated placebo records, exchange controls and security/date dependence-aware inference remain unavailable for this specific audit. Do not interpret these tier contrasts as a causal effect. November 14 target missed; November 30 provisional; manuscript not publication-certified.
