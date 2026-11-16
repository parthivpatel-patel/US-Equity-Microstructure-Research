# Phase 411 — Weighting-estimand reversal diagnostic (2026-11-16)

A new, locally executed six-test Python diagnostic demonstrated a **possible sign reversal** between equal-cell and pooled-denominator hidden-trade-rate gaps, even when all observations are paired on matched group, date, and exchange. This is a constructed counterexample, **not a result from the historical SEC panel**.

Constructed example: date 2025-10-01, treated 9/10, control 5/10; date 2025-10-02, treated 0/1000, control 1/10. Equal-cell average of treated-minus-control rates = **+15 percentage points**; denominator-pooled treated-minus-control rate = **100*(9/1010 - 6/20) = -29.1089 percentage points**. The estimands have different weights, so the opposite signs are mathematically consistent. This example establishes why estimator choice must be specified in advance and reported alongside denominator distributions.

Six local unit tests passed: sign reversal, unpaired exclusion, duplicate blocking, impossible counts blocking, no-overlap blocking, empty-input blocking. These are implementation/fixture tests, not empirical validation. No original SEC security-exchange-day data or authenticated matched roster was available; no new historical effect estimate was computed.

Required follow-up: recover the original authenticated panel, document denominator distributions, evaluate equal-cell, date-balanced, and denominator-pooled estimands on identical matched support, and conduct September pretrend and October placebo tests with matched-group plus common-date and serial-dependence-aware inference. Treatment authentication and redistribution rights remain open. November 14 deadline missed; November 30 provisional, paper not certified. No historical archives imported this session.
