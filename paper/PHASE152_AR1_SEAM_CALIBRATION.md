# Phase 152 — Stationary AR(1) block-seam calibration (synthetic only)

Date: 2026-11-04. Independent round-lot research. No GIG assets.

## Design and executed result

A local Python run of the companion algorithm used one fixed seeded 87-date stationary AR(1) path (coefficient 0.7, Gaussian innovations), 1,000 bootstrap index draws per method, and 10-date blocks. The noncircular method yielded mean seam/interior absolute-jump ratio **2.027046978593232**, mean seam-minus-interior difference **0.8307344408059933**, and **0** within-block wraps. Circular blocks yielded **2.009538769218789**, **0.8031965373748325**, and **923** within-block wraps. Deterministic rerun, exact seam fixture, dimensions, and invalid block inputs passed.

## Interpretation

Both methods can produce seam jumps substantially larger than within-block jumps, even for a stationary AR(1) synthetic path. Eliminating circular endpoint wraps is **not** equivalent to eliminating concatenation artifacts. These figures are conditional on one synthetic path and seed, not sampling-distribution uncertainty or an empirical comparison. The circular and noncircular draws use successive segments of one random stream, not paired identical start indices. Neither method is established as correctly calibrated for the whole-scan maximum statistic.

## Publication and reproducibility limits

The companion file is a clean transcription of the locally executed script with equivalent operations and tests; a fresh checkout run is still required. No SEC market estimates, treatment classifications, empirical p-values, historical ZIP imports, or licensed data are included. The Phase 131 processed panel and original SEC records remain unavailable for authenticated empirical inference.

## Open identification warnings

Substantial October 2025 placebo; September pretrends; historical Nasdaq round-lot treatment authentication; exchange/security composition and weighting sensitivity; matched-group, common-date and serial dependence; source-data reconciliation. No causal reform effect established.

## Next

Recover authenticated panel and historical archive inventory, audit source checksums and treatment mapping, then compare seam diagnostics and full-scan null calibration under multiple block lengths and trend specifications. Preserve the October placebo as an identification warning rather than treating it as evidence for the November reform.
