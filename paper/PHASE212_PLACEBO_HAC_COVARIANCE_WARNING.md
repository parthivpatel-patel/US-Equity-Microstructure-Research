# Phase 212: Placebo-window HAC covariance warning

2026-11-07. Independent U.S. equity round-lot reform research. This checkpoint contains no historical coefficient estimates.

## Verified local calculation
A standalone Python prototype and 12 unittest cases were executed locally (12 passed, after correcting one test's mistaken lag threshold). The prototype takes sorted, unique pre-November-3-2025 date-level contrasts and two disjoint windows. It computes a late-minus-early mean contrast and Bartlett/Newey-West lag sensitivity separately within each window. A constructed 24-calendar-date linear sequence, with early September 1–10 and late September 13–24, produced a difference of 13 units. This is **synthetic test data**, including weekends; it is not a trading calendar and is not SEC evidence.

## Substantive methodological warning
The standard error obtained by summing separate within-window HAC variances and taking a square root implicitly sets the covariance between the early- and late-window sample means to zero. Disjoint calendar windows do **not** imply stochastic independence, especially for serially persistent daily market contrasts. Consequently this simple calculation is a **sensitivity diagnostic only**, not a defensible confidence interval for the placebo shift. A valid next estimator must account for cross-window covariance using a full-sample HAC regression on the window indicator (with appropriate treatment of gaps and trends), or a dependence-preserving resampling procedure with transparent block design. Any inference must also address cross-sectional clustering, common-date shocks and security/exchange fixed-roster composition.

## Outstanding identification failures
The historical October 2025 placebo warning and September pretrends remain substantive objections to causal interpretation. Nasdaq historical round-lot treatment assignments, source SEC observations, exchange calendar, selection rules and weighting remain unauthenticated in this checkpoint. No causal effect is established. The original recovered ZIPs, historical data and figures were not available for authenticated, rights-checked import. This document does not claim a complete inventory of archives.

## Publication status
The local prototype and tests were executed but are not included in this checkpoint. They must be independently published and tested from a clean checkout before claiming full executable reproducibility. Next prioritize authenticating source data, freezing rosters, running September/October placebo comparisons, and implementing a full-sample serial-dependence-aware estimator rather than assuming zero cross-window covariance.
