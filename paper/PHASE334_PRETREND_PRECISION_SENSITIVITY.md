# Phase 334 — Published pretrend uncertainty sensitivity to HAC lag

Date: 2026-11-13. Independent quantitative research. **Source: published presentation aggregates only; no new SEC panel estimate.**

## Provenance
Input: `results/phase136_trend_uncertainty_presentation.csv`, Git blob `e89016144b1b60079a4686c02a945009a2734c06`. The connector returned all 20 published rows, comprising 2 outcomes × 2 periods × 5 lag settings. Reproduce with `python scripts/phase334_pretrend_precision_gate.py results/phase136_trend_uncertainty_presentation.csv`. Tests: `cd scripts && PYTHONPATH=. python -m unittest discover -s ../tests -p 'test_phase334_pretrend_precision_gate.py'`.

## Newly calculated precision diagnostics
The ratio is published two-way SE at lag 15 divided by the published two-way SE at lag 0; all quantities use percentage points per trading day.

| Outcome | Period | Lag-0 SE | Lag-15 SE | Ratio | Reported 95% interval excludes zero at every lag? |
|---|---|---:|---:|---:|---|
| count | Jul–Oct | 0.006697 | 0.012910 | 1.927729 | No |
| count | Jul–Sep | 0.008595 | 0.012910 | 1.502036 | Yes |
| volume | Jul–Oct | 0.008278 | 0.012546 | 1.515583 | Yes |
| volume | Jul–Sep | 0.008922 | 0.008963 | 1.004595 | No |

All four published lag grids are complete (0, 3, 5, 10, 15), and slopes are identical within each period/outcome across lag choices. For Jul–Oct count, reported uncertainty nearly doubles as the lag rises to 15. The exclusion pattern is stable across the five *reported* lags, but this is **not** independent confirmation: each lag is an alternative uncertainty specification on the same underlying estimated slope.

The underlying 68-security membership, raw daily security/exchange observations, dependence structure, bootstrap validity, and provenance are not independently authenticated. No p-value, causal effect, or new significance claim is inferred from this diagnostic. The October pre-reform break and September trend concerns remain publication gates. The Phase 130 count-placebo contradiction and missing 78 dated placebo rows remain unresolved. Historical ZIPs are still not authenticated or imported.

## Validation and next work
Six synthetic unit tests passed locally on an equivalent implementation, exercising complete grids, duplicates, missing lag, invalid interval, inconsistent slope and zero-crossing classification. The GitHub-published script is not certified by a full fresh-checkout regression run. Ratios above were independently recomputed from connector-fetched Phase 136 CSV values. Next: obtain dated placebo rows and authenticated panel source; run security/exchange-controlled estimates with matched groups and common-date/serial-dependence-aware inference before any publication certification.
