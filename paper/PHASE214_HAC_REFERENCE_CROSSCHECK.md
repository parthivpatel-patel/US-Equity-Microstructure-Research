# Phase 214: Independent joint-window HAC sandwich cross-check

Date: 2026-11-07. Scope: synthetic software verification only.

The published Phase 213 joint-window HAC standard errors were compared against an independently implemented, explicit two-column OLS sandwich calculation. The two regressors are indicators for early and late windows, with an observation-level score of zero outside both windows. The covariance matrix is formed by summing all ordered pairs of score vectors within the specified Bartlett bandwidth, then transforming with the inverse group sample sizes and the late-minus-early contrast vector.

The independent implementation agreed with Phase 213 to 11 decimal places at lags 0, 1, 3, and 8 on a constructed 30-observation series containing a gap between windows. A second constructed 20-observation series with constant values within each window yielded a mean difference of 6 and zero estimated standard errors at lags 0, 1, and 3. Both deterministic tests passed locally using Python unittest.

Important limitation: these tests are algebraic/software checks, not evidence that HAC inference has correct coverage in short, serially dependent, nonstationary or cross-sectionally correlated historical panels. Calendar-day test observations are synthetic and are not a verified exchange-session calendar. The Phase 213 estimator does not authenticate raw SEC records, historical Nasdaq treatment assignment, matching, exchange composition, calendar completeness, or weighting. Zero estimated variance in a deterministic constructed series is not evidence of certainty in real data.

The substantial October 2025 placebo result, September pretrends, selection and weighting sensitivity, treatment authentication, and historical common-date inference remain unresolved. No historical coefficient was calculated, and no causal effect is established.

Archive inventory for this session: no previously recovered historical ZIPs or papers were available for verified import; no historical data or figures were published. Next: run these tests from a clean checkout and recover authenticated source observations before empirical estimation.
