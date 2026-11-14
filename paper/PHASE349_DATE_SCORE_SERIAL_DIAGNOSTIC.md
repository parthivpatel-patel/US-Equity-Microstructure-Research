# Phase 349 — Trading-date serial score diagnostic

**Status: mathematical diagnostic only. No authenticated SEC observations, confidence intervals, or causal conclusions.**

Phase 348 includes group and same-calendar-date score terms, but its date term has no cross-date lag products. This module computes the time-ordered date-score lag products for the **same equal-group mean**: each group-date observation has weight 1/(G n_g), with n_g its observed dates. Date scores are sums of weighted demeaned contrasts across matched groups. For lag k, gamma_k = sum over t>=k of score_t score_(t-k). The Bartlett expression gamma_0 + 2 sum_k (1-k/(L+1)) gamma_k is reported as a **date-score component only**, not a complete two-way cluster/HAC covariance or calibrated uncertainty estimate.

Trading dates are indexed by consecutive observed dates, not elapsed calendar days. Missing dates and changes in group support can alter lag products. Group dependence, overlapping groups, selection uncertainty, exchange aggregation, finite-sample correction, lag selection and valid joint group/time inference remain unresolved. Do not add this component mechanically to Phase 348 variance and call it a valid CI.

Six deterministic tests passed in a local execution of an equivalent implementation after correcting an erroneous expected score scale. A constructed three-date fixture has mean 3 pp, date scores (-2/3, 0, +2/3), lag-0 product 8/9 and lag-1 product 0. These are not market estimates. The exact published checkout and repository-wide suite still need execution.

**Publication blockers:** original dated placebo observations (including the Phase 130 contradiction), October 2025 placebo warning, September pretrends, treatment/source authentication, exchange support, weighting sensitivity and historical archive recovery. The November 14 manuscript is not certified.
