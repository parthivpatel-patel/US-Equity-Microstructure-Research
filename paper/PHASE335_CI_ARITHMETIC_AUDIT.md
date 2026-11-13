# Phase 335 — Published pretrend confidence-interval arithmetic audit

Date: 2026-11-13. This is an **aggregate-presentation consistency check**, not a new SEC-panel regression or causal analysis.

## Input and reproducibility

Read the existing public repository file `results/phase136_trend_uncertainty_presentation.csv` through the connected GitHub file API, and recomputed diagnostics directly from its 20 CSV rows. Run `python scripts/phase335_ci_arithmetic_gate.py results/phase136_trend_uncertainty_presentation.csv` from repository root. This script uses Python's standard library and exact decimal arithmetic. It rejects duplicate/missing lag cells, invalid intervals, and material disagreement with the 1.96-normal-multiplier construction.

## Verified findings

All 20 published rows have confidence-interval centers within 0.0000005 percentage points/day of the displayed slope. The implied half-width-to-SE multiplier ranges from **1.959930509 to 1.960072100** across the 20 rows. These deviations are consistent with six-decimal presentation rounding. The published 95% confidence limits thus appear mechanically consistent with a 1.96 standard-error multiplier, not an independently validated finite-sample or bootstrap calibration.

This **does not validate** the two-way variance estimator, serial dependence correction, date clustering, treatment classification, raw observation authenticity, selection, or the assumptions behind normal-reference intervals. In particular, a correctly calculated CI may still be misleading when its underlying dependence estimator or research design is invalid. The pre-reform October break, September trends, and Phase 130 placebo-count contradiction remain outstanding. Original 78 dated placebo observations and generating code are not authenticated. Historical research archives remain unimported pending access, licensing and inventory verification.

## Next action

Recover dated Phase 130 placebo rows and producer code; audit sample lineage and window overlap, then re-estimate with authenticated security/exchange observations and joint security/date dependence-aware inference. The November 14 publication target is **not certified**.
