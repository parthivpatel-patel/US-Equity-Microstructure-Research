# Phase 145 — independent whole-scan mechanics and finite-simulation calibration audit

Date: 2026-11-04. Scope: reproducibility/methodology only; **no empirical market panel was available in this session**.

## Executed verification

Read the existing `src/phase141_break_scan.py`, `tests/test_phase143_whole_scan_null.py`, and `provenance/PHASE144_PUBLICATION_INVENTORY.md` before adding new files. Executed the standalone Python test locally with NumPy: **PASS: 200 randomized direct/convolution comparisons, linear invariance, candidate counts, finite-simulation tail conventions**. The test compares a direct centered-OLS slope-difference implementation with the convolution approach used in Phase 143 across five series lengths and four windows (where feasible), ten deterministic random trials each. It also checks that adding a global linear trend leaves a slope-difference scan unchanged, that 87 observations with 20-day windows yield 48 candidate breakpoints, and that upper-tail ties are included.

## Inferential correction and limitations

For an observed whole-scan maximum `T_obs` and `B` simulated null maxima, the finite Monte Carlo upper-tail rank is `(1 + sum(T_b >= T_obs)) / (B + 1)`. This prevents reporting zero merely because no simulation exceeds the observed maximum. **This rank is not automatically a valid p-value**: exchangeability/calibration depends on the actual null-generating scheme, dependence assumptions, detrending and stationarity, and selection rules. The Phase 143 residual circular-block generator has not been established as a calibrated null for the market panel. Its tests and this audit use synthetic fixtures, not SEC observations.

The direct/convolution agreement establishes implementation consistency, **not** the validity of the November reform design, the September/October break interpretation, or the original data. The earlier October information-event placebo warning, September pretrends, treatment classification, sample-selection and weighting sensitivity, and security/exchange composition remain open. Do not report causal reform effects.

## Reproduction

`python tests/test_phase145_scan_calibration.py` (requires NumPy). No original SEC or licensed third-party data included. No historical ZIPs imported; the 129-archive inventory reported in Phase 144 remains unverified in this runtime. A fresh public checkout cannot yet reproduce the empirical breakpoint results without the Phase 131 panel.

## Next research gate

Recover and hash-check the processed panel, reconcile to SEC security/exchange source records, authenticate historical Nasdaq round-lot treatment assignments, and execute a whole-scan matched-group/common-date block bootstrap with alternative trend nulls, block lengths, and simultaneous max-statistic calibration. Document every archive's hash, licensing, and disposition before importing.
