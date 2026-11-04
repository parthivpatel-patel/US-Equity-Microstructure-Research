# Phase 143 — whole-scan null calibration implementation audit (2026-11-04)

## Executed scope
A standalone NumPy implementation was executed against deterministic synthetic fixtures. It calculates every adjacent 20-trading-day post-minus-pre OLS slope difference, takes the maximum absolute difference across all feasible dates, and generates an exploratory reference distribution by fitting a global linear null and circular-block-resampling centered residuals. Each bootstrap replicate reruns the **entire** scan; this avoids incorrectly treating a selected maximum as a prespecified breakpoint.

The tests passed: 87 dates yield 48 candidates; a constructed slope break yields -5 at the designed breakpoint; linear and constant series yield zero shifts; additive level changes preserve shifts; seeded bootstrap output is reproducible; invalid inputs are rejected. No SEC or Nasdaq data were accessed or used in these tests. **No empirical bootstrap p-value was computed.**

## Important limitation
The prototype operates on a single aggregate series. Its residual circular-block bootstrap does **not** yet preserve matched-group dependence or independently validate the linear-null and stationarity assumptions. It is a tested building block, not a calibrated inference procedure for the research panel. A joint panel bootstrap must preserve common calendar shocks across groups, handle group-level residual dependence, and perform null diagnostics before any inferential interpretation.

## Provenance and archive status
The Phase 131 processed panel, original SEC data, Nasdaq historical lot-size classifications, and recovered historical ZIPs were not accessed or imported in this phase. Their original-source authentication, redistribution rights, and complete publication inventory remain unresolved. Earlier September and October breakpoint estimates remain descriptive and subject to selection and weighting sensitivity.

## Next
Recover and authenticate the Phase 131 panel, extend the whole-scan procedure to joint matched-group/calendar-date resampling, test alternative null trends and block lengths, and reconcile security/exchange observations to original SEC sources. No causal effect of the November 3, 2025 reform has been established.
