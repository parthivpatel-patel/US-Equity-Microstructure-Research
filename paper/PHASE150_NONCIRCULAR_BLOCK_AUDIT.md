# Phase 150 — Noncircular common-calendar moving-block diagnostic (2026-11-04)

## Verified synthetic result

A locally executed NumPy test examined 600 seeded noncircular index draws across 40, 87 and 106 dates and block lengths 2, 5, 10 and 20. Every within-block index increment was exactly +1, with no endpoint wrap. A nine-group synthetic common-date-shock preservation assertion passed. Across 100 deterministic seeds for 87 dates and 10-date blocks, circular sampling generated **95 within-block endpoint wraps**, versus **zero** for noncircular moving blocks. These counts concern **synthetic sampling indices**, not market observations or estimated causal effects.

## Interpretation

Noncircular moving blocks remove the *within-block* last-to-first artificial seam documented in Phase 149, but concatenating independently sampled blocks still creates *between-block* discontinuities. Noncircular sampling also changes endpoint inclusion probabilities, so it is not automatically superior or calibrated. Both approaches need null-size diagnostics under common-date shocks, heterogeneous group trends and serial dependence. Do not quote empirical bootstrap significance from this diagnostic.

## Reproduction

Run `python tests/test_phase150_noncircular_blocks.py` with NumPy installed. The published code is equivalent in logic to the locally executed verification, but a fresh checkout test remains pending. No empirical panel, SEC raw data, historical UTP treatment authentication, licensed ZIPs, or new empirical figure was available or imported. The historical archive inventory remains unverified. September pretrends, October 2025 placebo, weighting sensitivity and security/exchange controls remain unresolved. November 14 publication remains conditional; no causal effect established. Independent research only; no GIG assets.
