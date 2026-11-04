# Phase 148 — fail-closed joint-scan validation (2026-11-04)

## Scope
The Phase 147 audit identified a Phase 146 defect: a regression window of one observation yields nonfinite scan statistics. This phase adds a separate checked wrapper rather than overwriting Phase 146 or modifying historical outputs.

## Validation
The wrapper rejects regression windows smaller than two, noninteger and Boolean windows, insufficient date counts, invalid group dimensions, nonfinite panels, invalid calendar block lengths, nonpositive or noninteger draw counts, and invalid random seeds. It checks that returned statistics are finite and have expected dimensions.

An independent local audit implementation (using the exact Phase 146 function bodies fetched through the connected GitHub reader and transcribed into a local temporary test module) passed 18 invalid-input cases, five numerical scan equivalence cases, and a seeded bootstrap equivalence case. The committed wrapper has equivalent validation logic but **has not yet been executed from a fresh checkout**; do not conflate these verification levels. Execute `python tests/test_phase148_joint_scan_validation.py` from the repository root with NumPy installed.

## Inferential limitations
These are synthetic software tests, not SEC data or a new market estimate. The wrapper does not validate detrended-residual stationarity, dependence assumptions, treatment assignments, placebo calibration, or source authentication. In particular, resampling groups and dates does not by itself establish valid bootstrap inference. September pretrends and the substantial October 2025 placebo remain unresolved. No causal reform effect is established.

## Publication inventory
The historical ZIP archives, processed Phase 131 panel, original SEC security/exchange observations and authenticated Nasdaq historical treatment mapping were not accessible in this session. No archive import or empirical result is claimed. Next: execute the committed wrapper from a fresh checkout, inspect residual dependence, and recover source records and historical archive inventory before any empirical significance claim.
