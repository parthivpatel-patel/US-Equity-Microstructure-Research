# Phase 399 — Recovered daily pilot: arithmetic and October placebo audit

Date: 2026-11-15. This is **descriptive analysis of a recovered, provenance-unverified pilot aggregate**, not a security-level causal estimate.

Input: Library file `roundlot_pilot_daily.csv` (not redistributed), SHA-256 `9cd1e7f9fc89a2254211868e1a82cf97fd243bc860ad03eefa99409f94086bba`. The 126 rows contain 42 observed dates and exactly one record per 10-, 40-, and 100-share lot category per date. Verified all reported trade and volume rates equal their numerator/denominator within 1e-10 and that numerators lie between zero and denominators. Dates are observed, not inferred weekdays.

For each lot group, sum reported numerator and denominator separately over the period, then divide. This denominator-pooled rate is **not** an equal-security or matched-group mean.

| Lot | Metric | October 16–31 minus October 1–15 | November 3–28 minus October 16–31 |
|---|---|---:|---:|
| 10 | hidden trade-count rate | -0.031008395 | -0.121164030 |
| 10 | hidden share-volume rate | -0.026505791 | -0.108525323 |
| 40 | hidden trade-count rate | +0.003324276 | -0.011279073 |
| 40 | hidden share-volume rate | +0.012947453 | -0.006349966 |
| 100 | hidden trade-count rate | +0.012442714 | +0.002717327 |
| 100 | hidden share-volume rate | +0.001059138 | +0.015537620 |

Period observation counts: October 1–15 = 11 dates, October 16–31 = 12 dates, November 3–28 = 19 dates. All figures are *rate differences* (multiply by 100 for percentage points). These contrasts have **no confidence intervals or causal interpretation**. October placebo movements are nonzero, and lot-group composition may change over time. The input lacks security IDs, exchange IDs, matched-group assignments, historical treatment authentication, and source-archive provenance. No September data are present; neither September pretrends nor security/date clustering can be assessed. Do not equate lot category with verified reform treatment. This pilot is not a substitute for the original SEC daily panel.

Reproduce with `python scripts/phase399_pilot_diagnostic.py /path/to/roundlot_pilot_daily.csv` and compare the SHA-256 and results. The original pilot CSV is intentionally not published until provenance and redistribution rights are established.

The November 14 deadline was missed; November 30 remains a provisional target, not publication certification. Next: recover original daily security-exchange records and matched mappings, authenticate treatment, then perform pretrend, placebo and dependence-aware inference.
