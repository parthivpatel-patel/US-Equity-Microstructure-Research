# Phase 161 — Stable weighting diagnostics (2026-11-05)

## Audited source
Reviewed the existing Phase 160 validator and report. Its Kish ESS calculation `sum(w)**2 / sum(w*w)` can overflow for very large finite weights even when ESS is defined. This is a demonstrated numerical risk on constructed inputs, not evidence of overflow in the recovered SEC data.

## Executed checks
Seven local Python unittest cases passed: equal weights, concentrated weights, scaling invariance, weights of 1e300, invalid-input rejection, ESS bounds, and ESS/Herfindahl identity. The new standalone implementation normalizes by the maximum weight and uses `math.fsum`. It reports nominal count, Kish ESS, ESS fraction, maximum weight share, and Herfindahl concentration. Constructed [100,1] weights give ESS 10201/10001 and maximum weight share 100/101. No empirical market estimates were computed.

## Required empirical application
On authenticated data, calculate diagnostics separately for provisionally treated and comparison securities under prespecified weighting schemes, and by exchange and matching stratum. Report sample exclusion counts and avoid selecting weights based on statistical significance. Outcome-dependent trimming changes the estimand. Common-date, matched-group, and serial-dependence-aware inference remain required; HC3 cross-sectional errors are insufficient.

## Provenance and limitations
Original SEC daily source files and Nasdaq historical snapshots were not authenticated in this session; historical ZIPs were not imported. The September pretrends, substantial October 2025 placebo, treatment-authentication gaps, and weighting/selection sensitivity remain unresolved. This diagnostic does not support causal attribution. November 14 is a conditional publication target.
