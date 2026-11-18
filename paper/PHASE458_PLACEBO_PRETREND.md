# Phase 458: pre-reform placebo and trend diagnostic

This is a descriptive **software diagnostic**, not an authenticated empirical result. For each exchange and matched group, it forms treated-minus-control outcome means on common dates before 2025-11-03. It calculates the change between dates before and on/after the 2025-10-01 placebo boundary, and a linear calendar-day slope using only dates before the placebo. The placebo mean weights eligible exchange/matched groups equally.

The fixture's placebo value of 5 and slope of 2 are **constructed**, not SEC measurements. Missing paired dates and groups with fewer than two dates per period are excluded and counted. The routine checks duplicate observations, finite numeric outcomes, and globally consistent treatment flags, but cannot authenticate ticker identity or original treatment assignment. Cross-exchange ticker collisions can trigger conservative rejection.

**No inference:** There are no confidence intervals, serial-dependence corrections, fixed-effects estimates, or historical causal claims. Pretrend slope uses calendar days rather than trading-session counts. An October placebo effect is a warning against naive attribution of November changes. The September trend and October placebo must be re-estimated using independently authenticated SEC data, verified round-lot assignments, and sensitivity to weighting and common-date composition. Existing source, calendar, and assignment preflights are not yet wired into this diagnostic.

**Recovery inventory:** Phase 430 and Phase 436 prototypes and recovered historical ZIPs remain unverified and unpublished. No licensed source data have been redistributed.

**Publication:** The November 14, 2026 target was missed; the paper is not publication-certified.
