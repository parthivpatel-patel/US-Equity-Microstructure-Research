# Phase 354 — Numeric-stability correction for calendar-indexed covariance (14 November 2026)

## Reproduced defect
Read the existing published Phase 352 implementation through the connected GitHub integration and reproduced a numerical failure in a local copy of the same source. Four finite observations with values (+1e308, -1e308) in each of two matched groups yield a finite descriptive mean (0) but overflowing covariance score products: lag products [inf, -inf], serial component nan, and raw/serial-adjusted variances nan. The previous implementation returned these values with an ordinary descriptive status and negative_serial_variance=False. This is an input-domain/numerical safety issue, **not** an empirical result from SEC observations.

## Correction
Reject nonfinite derived weighted means, group/date scores, intersection sums, lag products, and final covariance components by raising ValueError. Existing finite-input validation remains intact. The correction intentionally does not silently clip values, assert positive variance, or imply calibrated confidence intervals.

## Verification and scope
A local Python unittest run against the corrected Phase 352 implementation passed 4/4 deterministic cases: extreme-but-finite overflow rejection, ordinary hand-check mean and lag products, nonfinite input rejection, and off-calendar date rejection. The repository test file reproduces these cases. The exact published checkout and complete repository test suite have not been executed in this session. No authenticated market data were analyzed.

## Unresolved empirical and publication gates
The September pretrends, substantial October placebo effect, original 78 dated placebo observations, Phase 130 discrepancy, treatment assignment and round-lot provenance, security/exchange aggregation, matched-support selection, serial-dependence-aware confidence intervals, and historical ZIP inventory/import remain unresolved. Publication certification and causal interpretation are not warranted.

## Next step
Run a fresh-checkout regression suite and source-provenance inventory before further estimator development; reproduce original dated placebos on authenticated panel data. Preserve any historical artifacts only after checking licensing, integrity and size.
