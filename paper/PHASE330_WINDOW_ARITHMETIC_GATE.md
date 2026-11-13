# Phase 330 — Window arithmetic and negative-tail subset audit (2026-11-13)

## Inputs
Read the existing repository's `results/phase130_summary.csv`, `results/phase131_window_sensitivity.csv`, and Phase 329 script and report. No existing files were modified. Reproduced the ten Phase 131 rows using a locally transcribed copy of the retrieved CSV; the script accepts the repository CSV directly.

## Findings
Across the ten Phase 131 rows, reported November-minus-October differences agree with differences of the displayed six-decimal November and October columns within 0.000001 percentage points. Seven rows have exactly zero discrepancy at displayed precision; three have a discrepancy of ±0.000001. All ten satisfy the basic count bounds and the necessary negative-tail-subset condition where the event contrast is negative. The 0.0000015 tolerance accommodates independent six-decimal rounding of the three displayed fields; it is not an empirical confidence interval.

This check does **not** resolve the Phase 130 five-day hidden-count contradiction. Its negative-tail count (2) equals its absolute-extreme count (2), which passes the simple subset check, but the Phase 130 positive maximum above the absolute event threshold demands an additional absolute-extreme observation. The stronger joint feasibility gate remains failed. Arithmetic consistency is not source-data authentication.

## Validation
Eight synthetic tests passed locally, zero failures. The Phase 131 CSV was fetched from GitHub and its ten rows were transcribed into the local execution environment for a run; all ten arithmetic and subset checks passed. The full published checkout's test suite was not executed. The source data and the original 78 dated placebo observations were not recovered.

## Publication status and next steps
No causal effect, calibrated placebo p-value, or independent empirical SEC estimate is claimed. September pretrends, substantial October placebo effects, treatment authenticity, security/exchange controls, weighting/selection sensitivity, serial/common-date inference, and archive provenance remain unresolved. Publication by November 14 is not scientifically certified. Next recover the original placebo producer and dated observations, run the existing Phase 325–330 checks directly on authenticated data, and reconcile the count contradiction. Historical research ZIPs remain unverified and unimported.
