# Phase 352: Calendar-indexed serial-score correction

## Issue
Phase 350 computes lagged date-score products on the sorted set of *observed* dates. If an authenticated exchange trading session is missing from the observations, its lag-one product may incorrectly join dates two or more sessions apart. Phase 351 detects this gap but does not change the lag calculation.

## Implementation
`scripts/phase352_calendar_serial.py` requires an externally authenticated, strictly increasing session calendar. It places date scores on the full session index, with zero scores for unobserved sessions, and computes Bartlett-weighted lag products at actual session offsets. It preserves the equal-matched-group descriptive mean, the group score component and group-date intersection correction. Missing sessions are explicitly reported. The input is already aggregated to one group-date contrast; exchanges must be aggregated according to a documented policy before use.

## Verification and interpretation
Ten deterministic constructed-data tests passed in a local prototype on November 14, 2026. The repository version should be rerun on a clean checkout. In a fixture with observations on October 1 and October 3 but no October 2 observations, the calendar-indexed lag-one score product is zero; the observed-date-indexed method would treat October 1 and October 3 as adjacent. This is a software-methodology check, not an SEC empirical result. Zero-filling represents the score contribution of a missing session and does **not** impute missing market observations. Selection and missingness remain substantive threats.

## Remaining blockers
No authenticated SEC panel was processed. The original 78 dated placebo observations, Phase 130 contradiction, September pretrends, October placebo break, treatment authentication, matched support, weighting sensitivity, uncertainty calibration, and historical archive inventory remain unresolved. The raw variance components may be negative, are not finite-sample calibrated and do not authorize confidence intervals or causal claims. Calendar provenance and complete clean-checkout tests are required before manuscript certification.
