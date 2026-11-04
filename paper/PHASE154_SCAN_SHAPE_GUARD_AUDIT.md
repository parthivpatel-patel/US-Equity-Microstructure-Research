# Phase 154 — independent breakpoint scan shape and guard audit

## Scope and execution

This is a **synthetic software verification**, not analysis of SEC or Nasdaq observations. After reading the published Phase 153 implementation and report, a separate fail-closed adjacent-window slope scanner was implemented and run locally with NumPy.

Command: `python test_phase154_scan_window_guards.py` (the file may be run under `tests/` from a checkout).

Observed stdout: `PASS 600 independent OLS comparisons; 8 invalid cases rejected`.

The 600 comparisons cover series lengths 4, 5, 12, 40, 87 and 106, every eligible window length from 2 to floor(n/2), and five seeded random series per configuration. Convolution results agree with a separate direct least-squares calculation within absolute tolerance 2e-13. Output length is exactly n - 2w + 1, including the single-breakpoint edge case. Eight invalid inputs were rejected: one-observation window, zero window, window too long, fractional window, Boolean window, nonfinite series, two-dimensional series, and too-short series.

## Why this matters

The earlier Phase 147 audit found an invalid one-observation window could yield nonfinite results. The Phase 153 standalone `scan` helper does not itself enforce these input guards. The Phase 154 implementation provides a tested candidate for future integration without modifying the existing Phase 153 implementation before a full regression check. It is **not** a claim that the Phase 153 production path has been repaired.

## Inference and provenance limitations

This does not calibrate bootstrap p-values or establish empirical validity. The September pretrends, substantial October 2025 placebo warning, treatment membership authentication, exchange/security composition, weighting sensitivity, and original SEC data authentication remain open. The Phase 131 empirical panel and historical ZIP archives were not available for inspection or import. No causal effect has been established.

Next: integrate guarded inputs into the resampling pipeline with regression tests; then recover authenticated panel inputs and run pretrend, placebo, weighting, and joint dependence-aware inference.
