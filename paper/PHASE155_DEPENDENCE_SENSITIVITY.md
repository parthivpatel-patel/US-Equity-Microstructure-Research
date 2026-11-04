# Phase 155 — synthetic dependence and block-length sensitivity

**Scope:** independently executed synthetic null calibration, **not empirical SEC/Nasdaq evidence**. Run: `python tests/test_phase155_sensitivity.py` (NumPy required). Code adapted conceptually from Phase 153 but implements independent parameterized experiment and guarded slope scan.

Each cell: 40 seeded null panels, nine groups, 87 dates, 20-date adjacent-slope whole scan, 99 bootstrap draws, 5% nominal rejection threshold, group resampling and shared date-block indices. Innovations combine one common-date shock (weight c) and independent group shocks (weight sqrt(1-c²)), with AR(1) persistence phi. Both methods use the same 40 panel seeds per configuration, though bootstrap random draws differ. Reported p-values have +1 correction.

| phi | common weight c | block | Noncircular rejections / 40 | Circular rejections / 40 | Mean p noncircular | Mean p circular |
|---:|---:|---:|---:|---:|---:|---:|
| 0.0 | 0.7 | 10 | 3 | 0 | 0.4457 | 0.4390 |
| 0.7 | 0.0 | 10 | 0 | 0 | 0.5613 | 0.5635 |
| 0.7 | 0.7 | 5 | 12 | 12 | 0.2622 | 0.2588 |
| 0.7 | 0.7 | 10 | 4 | 8 | 0.3298 | 0.3207 |
| 0.7 | 0.7 | 20 | 1 | 0 | 0.3980 | 0.3837 |
| 0.9 | 0.7 | 10 | 8 | 9 | 0.2760 | 0.2718 |

**Interpretation:** Under the simulated null, the 5-date block yielded 12/40 rejections (30%) for both methods, versus 1/40 and 0/40 at 20-date blocks. The bootstrap is not reliably size-calibrated across these settings; neither circularity choice alone fixes the issue. This is a small sensitivity screen, not a precision estimate of true rejection probabilities. With 40 replications and 99 draws per cell, do not rank methods or infer market effects. The generator uses AR(1) with stationary initialization and group-common shocks, not a validated market DGP.

**Research consequence:** Do not treat a nominal bootstrap p-value from this implementation as confirmatory evidence without further calibration and authenticated data. The October 2025 placebo, September pretrends, treatment classification, SEC source authentication, security/exchange composition and weighting sensitivities remain open. No historical ZIP was recovered or imported in this phase.

**Next:** locate authenticated original panel and source manifests; run treatment classification checks and pretrend/placebo analyses on actual observations. Prioritize empirical provenance over further isolated simulations.
