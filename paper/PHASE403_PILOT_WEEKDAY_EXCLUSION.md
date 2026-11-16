# Phase 403 — Weekday-exclusion sensitivity of recovered pilot contrasts

Date: 2026-11-16. Source: previously recovered Library file `roundlot_pilot_daily.csv` (126 rows, 42 observed dates; 11 early-October, 12 late-October, 19 November dates). Historical SEC provenance and redistribution permission remain unverified; source CSV is **not** republished.

## Method
For each date, pool the 10- and 40-share tiers by numerator and denominator and subtract the pooled 100-share rate. Compare late October (Oct 16–31) with early October (Oct 1–15), and November with late October. Repeat after excluding *all* observations from one weekday across all three windows, preserving common-date exclusions. The analysis checks unique date/tier rows, complete tiers per observed date, positive denominators and recomputed rates. Run `python scripts/phase403_weekday_exclusion.py /path/to/roundlot_pilot_daily.csv`. No third-party packages required.

## Computed results (percentage points)

| Excluded weekday | October trade placebo | October volume placebo | November trade contrast | November volume contrast |
|---|---:|---:|---:|---:|
| None | -0.9422 | +1.1625 | -2.1476 | -2.7275 |
| Monday | -0.5744 | +1.5775 | -2.2578 | -2.7420 |
| Tuesday | -0.8569 | +1.4766 | -2.0271 | -2.5119 |
| Wednesday | -1.1107 | +0.8966 | -1.8634 | -2.5203 |
| Thursday | -1.3266 | +0.5299 | -2.0761 | -2.6631 |
| Friday | -0.8553 | +1.2519 | -2.5063 | -3.1382 |

All four contrasts retain their signs after each full weekday deletion. This is a **deterministic sensitivity check**, not a bootstrap, standard error, significance test, or protection against shared trends. The October placebo warning persists. The 42-date aggregate pilot cannot identify securities, exchanges, matched controls, September pretrends, or authentic historical treatment assignments. Do not interpret the November contrasts causally.

## Provenance and publication gate
Source is a recovered historical Library artifact, not independently downloaded and reconciled to official SEC source files. Original SEC archives, the 78 dated placebo estimates, matched-control mapping and treatment roster remain unverified. No restricted input uploaded. November 14 deadline missed; November 30 is provisional, not a certification. Next: authenticate source archives and reconstruct security-exchange-day panel before confirmatory inference.
