# Phase 402 — Leave-one-date-out pilot influence audit (2026-11-16)

Recovered Library input: `roundlot_pilot_daily.csv`, 12,054 bytes, SHA-256 `9cd1e7f9fc89a2254211868e1a82cf97fd243bc860ad03eefa99409f94086bba`. Not redistributed because source provenance and redistribution permission remain unverified. The data have 126 rows, 42 distinct dates, and complete 10/40/100 lot-tier observations on each date. The original SEC source has not been authenticated.

The estimand is the denominator-pooled difference in hidden rate between combined 10/40-share tiers and the 100-share tier, differenced across periods. Each leave-one-date-out (LOO) calculation deletes all three tiers on one date, preserving common-date grouping. These are sensitivity ranges, **not confidence intervals**. No security, exchange, matched-control or serial-dependence inference is possible from this aggregated pilot.

| Metric | Contrast | Point (pp) | LOO minimum (pp) | LOO maximum (pp) | Largest influence date | Max absolute shift (pp) | Sign flips |
|---|---|---:|---:|---:|---|---:|---:|
| Hidden trade-count | Late vs early October placebo | -0.942183 | -1.125414 | -0.736429 | 2025-10-31 | 0.205754 | 0 |
| Hidden trade-count | November vs late October | -2.147596 | -2.353350 | -1.964365 | 2025-10-31 | 0.205754 | 0 |
| Hidden share-volume | Late vs early October placebo | +1.162480 | +0.730486 | +1.448864 | 2025-10-17 | 0.431994 | 0 |
| Hidden share-volume | November vs late October | -2.727491 | -3.013875 | -2.295497 | 2025-10-17 | 0.431994 | 0 |

Early October contains 11 observed dates; late October 12; November 19. The October placebo contrasts persist under all single-date deletions. This does **not** rule out multi-date confounding, serial dependence, nonrandom group composition or errors in source/treatment assignment.

Reproduce locally: `python scripts/phase402_pilot_loo.py /path/to/roundlot_pilot_daily.csv`. Tests: `PYTHONPATH=scripts python -m unittest discover -s tests -p 'test_phase402_pilot_loo.py'`. Six fixture-based tests passed locally (2026-11-16); exact GitHub checkout/full suite not executed.

**Release status:** Original November 14 target missed; November 30 remains provisional. Not publication-certified. Prior October placebo, September pretrends, matching and treatment-authentication gaps remain. Next: recover authenticated daily security-exchange panel and 204-control matching map, rerun diagnostics with matched groups and dependence-aware inference.
