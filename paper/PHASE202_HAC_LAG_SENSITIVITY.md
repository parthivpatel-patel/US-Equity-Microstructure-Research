# Phase 202 — Date-level HAC lag sensitivity (2026-11-06)

This extends Phase 201 without modifying its published implementation. The same ordered daily contrasts and identical sample support are used for every requested Bartlett Newey–West bandwidth. Lag counts observed sessions, not calendar days; weekend gaps do not imply missing trading sessions. The code rejects duplicates, unsorted dates, nonfinite contrasts, noncanonical ISO dates, duplicate bandwidths and inadmissible bandwidths. It reports clipping of a negative finite-sample long-run variance estimate rather than silently hiding that condition.

## Constructed-data check

Four illustrative dates (October 1, 2, 3 and 6, 2025), contrasts (1, 2, 3, 4), produce mean 2.5; lag-zero HAC SE sqrt(1.25/4) = 0.5590169944 and lag-one HAC SE 0.625. These numbers are **not SEC observations or treatment effects**. Nine deterministic tests passed locally on the implementation prototype; the exact published files require fresh-checkout execution.

## Research integrity and remaining work

HAC bandwidth sensitivity is not a substitute for treatment authentication, historical SEC source provenance, September pretrend tests, October placebo tests, matched-roster stability, security/exchange controls, cluster-robust or cross-sectional dependence assessment, and selection/weighting sensitivity. The four-date example is too small for credible inference. Do not select a lag after observing favorable significance. The historical treatment map and recovered ZIP archive remain unauthenticated and unpublished. No causal effect has been established.

Next: validate published files in a fresh checkout, authenticate the original panel and treatment mapping, then apply fixed-support placebo and pretrend contrasts with prespecified bandwidth sensitivity.
