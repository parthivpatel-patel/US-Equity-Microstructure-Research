# Phase 350 — exploratory serial-date two-way decomposition

This combines Phase 348's equal-matched-group weighting with Phase 349's Bartlett trading-date score lags. The score components are group, date, and group-date intersection. The serial extension substitutes the Bartlett date-score component for the date component, preserving the intersection subtraction.

**Not a calibrated variance estimator, confidence interval, p-value, or causal estimate.** It may omit cross-group/cross-date dependence. Negative raw estimates are flagged, never clipped. Requested lag bandwidth defines Bartlett weights even when fewer lags are observable. Adjacent dates mean adjacent *observed sessions*, not necessarily adjacent calendar days. Input rows must be unique matched-group/date contrasts after a prespecified exchange aggregation rule; no SEC source data were processed.

Ten deterministic prototype tests passed locally on 2026-11-13. Exact published checkout and repository-wide tests remain to be run. September pretrends, October placebo, Phase 130 contradictory counts, 78 dated placebo observations, treatment authentication, serial-dependence calibration and recovered historical ZIPs remain unresolved. No manuscript certification.
