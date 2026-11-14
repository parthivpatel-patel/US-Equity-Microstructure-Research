# Phase 351 — authenticated trading-session support gate

Phase 350 treats consecutive *observed* dates as consecutive trading sessions when calculating lagged date-score products. If a session is missing from the observed panel, an observed-neighbor lag may span multiple real trading sessions. The estimator therefore requires an explicit trading-session calendar and a missing-session policy before any inferential interpretation.

Phase 351 adds a separate, fail-closed calendar-support audit. It requires an externally authenticated, ordered session list; it does not guess holidays or infer trading calendars from weekdays. It rejects duplicate group-date rows, off-calendar dates, noncanonical dates and nonfinite contrasts. It reports missing sessions, observed-neighbor pairs, genuinely adjacent session pairs, and pairs spanning gaps. The audit does **not** silently fill missing values, change Phase 350's estimator, or produce a p-value.

Local deterministic tests: 10/10 passed on November 13, 2026, against a locally executed prototype with equivalent logic. Exact published checkout and full repository regression suite are not yet certified. No SEC panel was processed, no source calendar was authenticated, and no causal result is asserted.

Publication blockers remain: authenticate raw panel and treatment cohort, recover the original 78 dated placebo observations, resolve Phase 130 count contradictions, investigate September pretrends and the substantial October placebo effect, establish exchange aggregation and selection/weighting robustness, and calibrate dependence-aware uncertainty. Historical ZIP inventory/import remains incomplete. The November 14 manuscript target is not certified.
