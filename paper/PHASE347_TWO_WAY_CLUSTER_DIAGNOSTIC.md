# Phase 347 — Common-date and matched-group covariance diagnostic

**Status:** Software-only validation. No authenticated SEC observations analyzed; no causal or inferential conclusion.

For one pre-aggregated contrast per (matched group, calendar date), the uncorrected intercept-only two-way cluster variance diagnostic is V_group + V_date - V_intersection. Each component is the sum of squared cluster sums of demeaned contrasts divided by N squared. This is an **equal-cell mean**, not the equal-matched-group estimand of Phase 342/344 when group cell counts differ. Exchange-specific cells must first be aggregated using a declared policy. The program rejects duplicate group-date keys rather than silently changing weights.

A deterministic four-cell fixture with contrasts [1,3,5,7] percentage points has mean 4, group component 2, date component 0.5, intersection component 1.25, and uncorrected two-way variance 1.25 squared percentage points. These are constructed arithmetic checks, **not empirical estimates**.

Two-way clustering does not by itself resolve serial dependence across adjacent dates, few-cluster bias, matched-selection uncertainty, or overlapping-placebo covariance. The uncorrected estimate may be negative; do not silently truncate or report a confidence interval from it. Before empirical use, authenticate source files, recover original dated placebo rows, verify treatment assignment and date/exchange support, and implement declared weighting and block-based inference. The substantial October 2025 placebo warning and September pretrends remain open. The Phase 130 placebo-count discrepancy remains unresolved.

Local standalone equivalent: four deterministic tests passed after fixing an initially incorrect hand-computed expected variance. Full published-checkout regression remains outstanding. No historical ZIPs were imported or authenticated in this phase.
