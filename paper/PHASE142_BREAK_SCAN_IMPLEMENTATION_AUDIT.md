# Phase 142 — breakpoint implementation audit (2026-11-04)

## Executed verification
Independently reimplemented the Phase 141 20-observation before/after slope difference using the centered OLS covariance formula, rather than the published script's `numpy.polyfit`. Executed the attached synthetic-data test with Python and NumPy. Four deterministic checks passed: constant series, exact linear trend, exact piecewise-linear slope change, and additive-level invariance. For 87 dates and a 20-date window, the test confirms **48 candidate indices**; the constructed piecewise break at index 44 has exact post-minus-pre slope **−5** units per date.

These are **software validation fixtures only**. They do not establish that the reported Phase 141 empirical estimates reproduce, that any empirical breakpoint is statistically significant, or that the original SEC/Nasdaq data are authentic.

## Inference and identification warnings
The 48 candidate windows overlap heavily. Ranking their absolute shifts is selection on the maximum; treating the selected value as if its date had been prespecified invalidates ordinary pointwise inference. A valid null procedure must rerun the *entire scan* on each resample and compare the observed maximum against the distribution of resampled maxima. Calendar-date dependence must be preserved across all matched groups and outcomes. Circularly shifting the raw nonstationary series is not automatically valid: a defensible resampling procedure requires explicit null detrending, residual diagnostics, sensitivity to block length, and joint group/date dependence handling.

The October 1 information event, September pretrends, historical round-lot assignment uncertainty, source-data authentication gaps, and outcome/weighting sensitivity remain unresolved. No causal reform effect is established.

## Publication inventory
This phase adds a test and methodology note only. It does not import any recovered historical ZIPs, original source datasets, manuscripts, or figures; their availability, provenance, and redistribution eligibility require a separate authenticated inventory. The Phase 131 processed input is still not publicly reproducible end to end.

## Next
Recover and hash-verify the processed panel; run a null-calibrated whole-scan max statistic with matched-group and common-calendar-date blocks; compare results against historical placebo breaks; then reconcile original SEC security/exchange observations and Nasdaq lot-size assignments.
