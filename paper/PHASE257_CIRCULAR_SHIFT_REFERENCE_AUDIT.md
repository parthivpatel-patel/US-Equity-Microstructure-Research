# Phase 257 — Circular-shift placebo reference audit (2026-11-09)

## Purpose and executed check

Phase 256 independently flips date signs and can destroy serial dependence. This phase adds a separate cyclic-rotation diagnostic for an already ordered vector of frozen-roster, matched treated-minus-control daily contrasts. Each rotation preserves the observed series values and most local adjacency, but introduces a circular seam. The statistic is post-window mean minus pre-window mean at a fixed cut; all n cyclic rotations provide a conditional reference distribution.

Eight deterministic Python unittest cases passed locally, zero failures. The synthetic [0,0,3,3] series with two pre and two post dates has rotation statistics [3,0,-3,0], observed contrast 3, and absolute-tail fraction 2/4=0.5. These numbers are **synthetic software checks**, not SEC historical estimates.

## Identification and statistical restrictions

Cyclic rotations are not generally exchangeable. Their tail fraction is not a valid p-value without a defensible null that makes cyclic shifts equally plausible, a prespecified cut, a stable roster and appropriate stationarity/boundary assumptions. The artificial seam can disrupt serial dependence; regime shifts, September pretrends, October placebo abnormalities, heteroskedasticity, market-wide shocks, and treatment-selection effects may all invalidate this reference. The algorithm does not construct controls, adjust for exchange/security effects, account for multiple placebo cuts, or authenticate observations. The reference statistic must not be used as evidence of a reform effect.

## Reproduction

`PYTHONPATH=scripts python -m unittest discover -s tests -p 'test_phase257_circular_placebo.py' -v`. Only isolated tests were executed locally, not the entire repository suite.

## Evidence and archive inventory

No authenticated SEC observations, historical coefficients, historical plots, independently authenticated treatment assignments, or source calendars were analyzed in this phase. Historical ZIPs and unpublished Phase 253–254 code remain unavailable for verified import. The substantial October 2025 placebo warning, September pretrends, selection/weighting sensitivity, and dependence-aware inference remain unresolved. No causal effect is established. The November 14, 2026 manuscript target is conditional.

Next: recover original source archives, verify source hashes and licensing, freeze treatment and matched rosters, run historical pretrend/placebo analyses with security/exchange and common-date controls, and compare dependence-aware uncertainty methods under explicit assumptions.
