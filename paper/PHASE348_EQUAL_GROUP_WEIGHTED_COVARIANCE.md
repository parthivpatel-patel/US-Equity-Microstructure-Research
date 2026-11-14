# Phase 348 — Aligning two-way covariance with equal-group weighting

**Status:** Software diagnostic only; no authenticated SEC observations processed and no calibrated inference or causal claims.

Phase 347 computes covariance for an equal-cell mean, whereas Phase 342 targets an equal-matched-group descriptive contrast. When matched groups have unequal supported date counts, their estimands differ. This new script uses observation weight `w_gd = 1/(G*n_g)`, where `G` is the number of supported groups and `n_g` is the number of included dates for group `g`. Its mean is the average of the within-group date means.

The uncorrected two-way sandwich diagnostic is the sum of squared group score totals plus the sum of squared date score totals minus the sum of squared group-date intersection scores. Each score is `w_gd*(y_gd - weighted_mean)`. This is a **diagnostic**, not a finite-sample corrected variance or a valid confidence interval. Negative results must not be silently truncated. Group-date exchange contrasts require an explicitly documented exchange aggregation policy before use. This estimator is not yet integrated with Phase 342's group-date-exchange rate construction.

In a deliberately constructed unbalanced fixture, group A has two +80 pp cells and group B one -80 pp cell. Equal-group mean is 0 pp, whereas equal-cell mean is +26.6667 pp. Weighted covariance components are group 3200, date 800, intersection 2400, resulting raw variance 1600 (squared pp). These are mathematical checks, not empirical estimates.

Seven deterministic local prototype tests passed after correcting a mistaken expected date component; the published checkout and full repository suite have not been executed. Serial dependence across neighboring dates, small cluster counts, group-selection uncertainty, exchange aggregation, October 2025 placebo shifts, September pretrends, treatment authentication, source provenance and the Phase 130 placebo contradiction remain unresolved. Historical recovered ZIPs were not imported this session.

**Publication gate:** Do not certify the November 14 manuscript until original dated placebo observations and source-data provenance are authenticated, contradictory placebo counts reconciled, pretrends and weighting sensitivity disclosed, and dependence-aware inference validated.
