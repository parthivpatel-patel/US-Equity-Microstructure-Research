# Phase 203 — HAC sample-size and bandwidth admission (2026-11-06)

This adds a **structural gate**, not an estimator, to Phase 202's descriptive Newey–West bandwidth sensitivity. An arbitrary four-session constructed example can verify arithmetic but cannot justify empirical uncertainty. The gate requires at least 20 observed weekday sessions by default, strictly ordered unique canonical ISO dates, finite numeric contrasts, and a predeclared unique nonnegative integer lag grid. Its conservative default lag cap is floor((n−1)/4). Both thresholds are **engineering defaults**, not statistically proven universal thresholds; users must justify their choices before analysis. The gate does not detect exchange holidays, missing market sessions, sample selection, or mismatched security/exchange support.

Ten deterministic unit tests passed locally on the prototype (2026-11-06). The published files require clean-checkout execution. Tests contain only constructed data. No authenticated SEC observations, historical Nasdaq treatment classifications or recovered research ZIPs were imported; no historical coefficients were estimated.

**Identification warning:** substantial October 2025 placebo effects, September pretrends, treatment mapping uncertainty, weighting sensitivity and security/exchange composition remain unresolved. Date-level HAC alone does not resolve common shocks, cross-sectional dependence, or small-sample coverage. No causal effect of the November 3 reform is established.

Next: verify the exact published code in a clean checkout, authenticate original panel and historical treatment assignments, audit missing market sessions and fixed-roster support, then estimate prespecified placebo and pretrend specifications with multiple dependence estimators.
