# Phase 332 — Descriptive window-sign stability and changing placebo populations (2026-11-13)

## Inputs and reproducibility
Read existing public repository file `results/phase131_window_sensitivity.csv` and prior Phase 329–331 reports. No source CSV was modified. Run from repository root:

```sh
python scripts/phase332_window_stability.py results/phase131_window_sensitivity.csv
python -m unittest discover -s tests -p 'test_phase332_window_stability.py' -v
```

The script uses Python standard-library CSV and Decimal arithmetic. Six synthetic cases passed locally in a standalone module-equivalent execution; the published checkout's entire regression suite has not been run. The aggregate audit was executed locally on an exact transcription of the six relevant columns of all ten published Phase 131 rows, not an authenticated daily SEC panel.

## Descriptive results
For count, 4 of 5 windows have negative November-minus-October contrasts and 1 of 5 is positive; the observed contrast range is **1.071826 percentage points** (minimum -0.734661 at 5 days; maximum +0.337165 at 10 days). For volume, 5 of 5 contrasts are positive, with range **0.954766 percentage points** (minimum +0.201918 at 3 days; maximum +1.156684 at 10 days). These are sensitivity descriptions of published aggregates, not independent estimates or inferential significance.

The historical placebo denominator declines monotonically with window length: **82, 78, 74, 68, 58** for 3, 5, 7, 10 and 15 days, respectively, for both outcomes. Therefore the five specifications compare changing placebo-window populations as well as changing event-window lengths. A sign comparison alone cannot separate window-duration sensitivity from changing placebo composition. The negative-tail and absolute-tail counts should be reported with their own denominators, never as interchangeable p-values. The 5-day count row remains internally contradictory when combined with its published Phase 130 extrema, despite passing this script's elementary count bounds.

## Scientific limitations and publication gate
The October 2025 placebo warning, September pretrends, historical round-lot treatment authentication, security/exchange controls, weighting and selection sensitivity, common-date and serial-dependence-aware inference, source-data provenance, and original 78 dated placebo windows remain unresolved. The 5-day count-row joint-feasibility failure documented in Phase 331 remains binding. Neither five window specifications nor their tail frequencies constitute five independent tests. No causal reform effect, calibrated p-value, or publication certification is claimed.

Historical recovered ZIP archives remain unimported pending content, license, checksum, and repository-size verification. Next: locate the Phase 130 producer and dated observations; reconstruct historical placebo counts and denominators; authenticate source data before new matched-panel estimation.
