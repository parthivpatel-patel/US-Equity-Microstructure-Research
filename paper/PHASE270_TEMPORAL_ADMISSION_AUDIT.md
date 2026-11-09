# Phase 270: Temporal admission audit (2026-11-09)

Phase 269 `full_series_hac` assumes that the supplied series is in chronological order and treats consecutive entries as consecutive observed sessions. It does not itself check uniqueness, ordering, or completeness against an expected exchange-session calendar. The upstream `daily_contrasts` sorts observed dates but does not know whether a valid session is absent. Consequently, a gap can change which observations enter lagged covariance terms without raising an error.

A new, independently tested temporal gate checks strictly increasing unique dates, exact coverage of an externally supplied expected-session list, finite outcomes, and at least two dates on each side of the cutoff. **The supplied calendar is not authenticated by this check.** A structural pass does not authorize historical inference.

Local verification: 10 deterministic synthetic unit tests passed (Python unittest, 2026-11-09). No authenticated SEC observations, historical estimates, or historical figures were produced.

Outstanding: obtain independently authenticated SEC data, official exchange sessions and fixed treatment assignments; apply fixed-roster September pretrend and October placebo analyses, security/exchange controls, and dependence-aware inference. The large October placebo warning and September pretrends preclude a causal claim. Recovered ZIP archive inventory and Phase 252–254 imports remain incomplete. November 14 manuscript readiness remains conditional.
