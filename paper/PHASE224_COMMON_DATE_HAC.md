# Phase 224: Common-date window contrasts and full-series HAC

**Scope:** independent U.S. equity round-lot reform research. This checkpoint adds a descriptive pre-reform estimator for the two daily weighting estimands emitted by Phase 223. It does not establish a causal reform effect.

## Estimator

For a common ordered set of dates partitioned into an early and late window, calculate the late minus early mean of each daily treated-minus-control contrast. For each date, subtract its own window mean to form residual u_t. Define score s_t = -u_t/n_early for early observations and s_t = u_t/n_late for late observations. The Bartlett HAC variance is sum(s_t^2) + 2 sum_{k=1}^L (1-k/(L+1)) sum_{t=k+1}^n s_t s_{t-k}. The lag sums traverse the full ordered sample, **including cross-window covariance**. This is the uncorrected OLS sandwich covariance for the difference coefficient; no small-sample adjustment is applied.

## Deterministic validation

Synthetic six-date contrast sequence [1,2,3,4,5,6] with three observations per window yields a late-minus-early difference of 3. At lag 0 the HAC variance is 4/9; at lag 1 it is 5/9. The latter includes the boundary cross-window product. The second weighting series is deliberately twice the first, so its mean difference is 6. Eight standalone unittest cases passed locally against the authored module before publication. A clean-checkout test of the published bytes is still required.

## Important limits and safeguards

The supplied date list is checked for strict order, uniqueness, and agreement with records, **not** for completeness against an authenticated exchange calendar. The estimator is intended to consume the Phase 223 output after Phase 222 fixed-roster admission, but end-to-end execution against exact published dependencies is not yet demonstrated. No SEC observations or actual market-effect estimates were processed in this checkpoint. HAC inference is not a substitute for security-level dependence, matched-roster uncertainty, or calendar authentication. Bandwidth choice, pretrend failures, the substantial October 2025 placebo, selection into complete panels, denominator weighting, and historical Nasdaq treatment reconstruction remain unresolved.

## Provenance and archive inventory

Source: new original code and deterministic synthetic test values, no third-party data. No historical research ZIPs, licensed data, original SEC extracts, manuscript figures, or recovered legacy charts were imported this session. Their completeness and redistribution status remain unverified. The November 14, 2026 paper target is conditional on empirical authentication and reproducibility. No causal effect is established.

## Next execution

Run exact GitHub modules together in a clean checkout; independently authenticate SEC source files, official trading dates and Nasdaq treatment; then compare September pretrends and October placebo windows using common dates, both weighting schemes, fixed matched rosters and security/exchange dependence-aware sensitivity.
