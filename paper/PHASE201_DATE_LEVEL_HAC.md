# Phase 201 — Date-level HAC descriptive uncertainty (2026-11-06)

This dependency-free diagnostic adds a Bartlett-weighted Newey–West standard error for the mean of a prevalidated, strictly increasing series of daily matched-group contrasts. It is intended downstream of Phase 200, **not** as a substitute for the source-authentication and admission gates. Lag counts observed sessions, not calendar days. The input must already have fixed matched-group and security/exchange support; this function does not verify that condition.

## Verified constructed-data example

Four ordered observations on October 1, 2, 3 and 6 with contrasts 1, 2, 3, 4 yield mean 2.5. The lag-zero HAC standard error is sqrt(1.25/4) = 0.5590169944. The lag-one Bartlett standard error is sqrt(1.5625/4) = 0.625. This is **not** an SEC estimate. Eight deterministic tests passed locally after correcting an initially incorrect expected lag-one value. The exact published files still require fresh-checkout testing.

## Limits and next steps

This estimator treats the date as the unit for serial dependence but is not automatically robust to cross-group dependence, time-varying matched rosters, exchange-level shocks, small numbers of dates, placebo-date selection, or treatment misclassification. It supplies no t-test, p-value or confidence interval. Lag selection and sensitivity analysis must be prespecified before historical inference. The substantial October 2025 placebo warning and September pretrends remain unresolved; no causal effect has been established.

Original SEC daily panel, original historical Nasdaq classification provenance, and recovered historical research ZIPs remain unverified/unpublished in this phase. Next: execute published tests from a clean checkout, authenticate the source panel, and run placebo/pretrend estimates with multiple dependence specifications and fixed support.
