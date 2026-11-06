# Phase 180 — placebo denominator comparability audit (2026-11-05)

## Evidence and scope
Read the existing Phase 179 script/report and Phase 177 report, then the published `results/phase131_window_sensitivity.csv` via connected GitHub. This is an arithmetic audit of existing summary estimates, **not** a rerun of original SEC security-date-exchange observations. The source panel and treatment assignments remain unauthenticated.

## New cross-window check
| Trading-day window | Eligible placebo comparisons | Count absolute-rank exceedances | Volume absolute-rank exceedances |
|---:|---:|---:|---:|
| 3 | 82 | 7/82 | 71/82 |
| 5 | 78 | 2/78 | 76/78 |
| 7 | 74 | 12/74 | 64/74 |
| 10 | 68 | 21/68 | 47/68 |
| 15 | 58 | 3/58 | 9/58 |

The eligible placebo denominator falls from **82 to 58** as the window expands. Hence cross-window changes in exceedance fractions mix changes in the event-window contrast with changes in the set of eligible historical placebo dates. They must **not** be interpreted as evidence that the same placebo sample supports one window more strongly than another. Overlapping windows also make the placebo contrasts dependent. Neither these ratios nor their cross-window differences are calibrated p-values.

The published ten-row CSV passes the displayed six-decimal November-minus-October subtraction checks, within a two-millionths percentage-point rounding tolerance. Both outcomes have matching placebo denominators *within* each window, but the denominator is not constant *across* windows.

## Reproducibility
```bash
python scripts/phase180_placebo_denominator_audit.py results/phase131_window_sensitivity.csv
```
A closely corresponding local prototype passed seven deterministic validation tests, covering valid pairs, duplicates, missing pairs, arithmetic errors, denominator mismatches, invalid ranks and nonfinite estimates. **The exact published script has not been executed from a fresh checkout.**

## Empirical implications and remaining gates
To make an apples-to-apples comparison, rebuild placebo contrasts on the intersection of eligible historical cutoff dates across all windows, then report both common-date and window-specific placebo samples. Authenticate source SEC files (URL, retrieval timestamp, SHA-256, schema, row counts and license), historical Nasdaq round-lot treatment classification, trading calendar and fixed matched-group roster. Re-estimate September pretrends and the substantial October pre-reform shift with security/exchange controls, matched-group and common-date dependence, serial-correlation-aware inference and prespecified weighting. No historical ZIP/PDF archives were imported this session; the Phase 176 public inventory remains the last checked inventory. **No causal reform effect established. November 14 publication target conditional.**
