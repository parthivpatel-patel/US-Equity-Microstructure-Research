# Phase 456: local versus global common-date support sensitivity

This standalone estimator compares two explicit support rules. Under **local pairing**, a matched exchange/group/date contributes whenever both treated and control observations exist. Under **global balancing**, that date must be paired in every observed exchange/group stratum. Within each stratum, the estimator averages daily treated-minus-control differences in each period and subtracts the pre mean from the post mean; eligible stratum effects receive equal weight.

A deterministic constructed example produces local 6.5, globally balanced 2.0, and global-minus-local -4.5. **These are unit-test arithmetic, not SEC estimates.** This discrepancy demonstrates that a global calendar intersection can change the estimand through selective date retention. The implementation reports eligible strata and contributing paired cells; missing pre/post support returns null, never zero.

The module does not perform inference, authenticate source files, authenticate treatment assignments, or identify causal effects. In particular, it cannot resolve the September pretrend or October placebo warnings. Application to historical observations must be gated on independently verified source provenance, a validated exchange session calendar, and historical round-lot assignments. Serial moving-block bootstrap, security/exchange controls, alternative weighting and placebo sensitivity remain necessary.

Historical recovered ZIPs, Phase 430 and Phase 436 prototypes were not imported in this phase. The November 14, 2026 target was missed and the manuscript is not publication-certified.
