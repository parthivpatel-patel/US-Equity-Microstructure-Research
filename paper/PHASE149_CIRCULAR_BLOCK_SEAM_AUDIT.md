# Phase 149 — Circular-block seam and dependence diagnostic (2026-11-04)

## Executed synthetic diagnostic

A standalone NumPy script executed locally with assertions passing. It uses a deterministic, detrended 87-date synthetic residual series and a separate eight-group synthetic panel. The detrended residual endpoint-to-start jump is **0.411951025**, exceeding the maximum ordinary adjacent jump **0.222260225**. Thus the circular-block method can create an artificial seam that is larger than any adjacent residual change in this constructed case. The scan returns **48** eligible candidates for 87 dates and a 20-date window. The common-date index check passed for all eight groups.

These numbers are **synthetic diagnostics only**, not estimates from SEC data, and do not establish how frequently or materially seam artifacts occur in the actual research panel. A circular block bootstrap is not universally invalid; the counterexample demonstrates a sensitivity that requires measurement rather than an assumption of harmlessness.

## Implication for Phase 146

The existing Phase 146 bootstrap samples calendar blocks circularly, including wraparound across the sample endpoint. In a nonstationary or imperfectly detrended panel, this may manufacture sharp transitions. In addition, Phase 146 fits separate linear trends by group before bootstrapping, but does not validate residual stationarity or establish the null distribution's empirical calibration. Joint group/date resampling preserves within-date dependence for each draw, but this alone does not guarantee correct inferential coverage. A max-statistic p-value cannot be treated as a causal test without credible treatment authentication and pretrend identification.

## Required empirical checks

Before quoting empirical breakpoint significance: (1) recover and authenticate the Phase 131 panel and SEC/UTP source mapping; (2) quantify residual endpoint jumps versus interior first differences by group and outcome; (3) compare circular blocks against noncircular moving blocks and stationary or wild/block alternatives, with multiple block lengths; (4) run whole-scan null calibration and size/power diagnostics under constructed nulls with common-date shocks and group heterogeneity; (5) inspect September pretrends and the October placebo under security/exchange and weighting sensitivity. Do not interpret the September scan maximum as a November reform effect.

## Reproducibility and publication scope

Run `python tests/test_phase149_bootstrap_diagnostics.py` with NumPy installed. The source was executed locally prior to publication; a fresh checkout run remains to be performed. No historical ZIP, SEC source record, processed panel, proprietary dataset, or empirical figure was imported this phase. The previously reported 129 archives remain unverified and unpublished. This work is strictly independent of GIG and other projects. The November 14 deadline remains provisional; no causal effect is established.
