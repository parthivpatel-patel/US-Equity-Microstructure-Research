# Phase 452: Calendar gap screen for moving-block inference

**2026-11-18.** Review of the published Phase 451 implementation established that it orders the intersection of observed dates and resamples adjacent *positions* in that array. This is not necessarily equivalent to adjacent exchange trading sessions. If the panel has a prolonged missing-data gap, a moving block can bridge it, undermining the intended serial-dependence interpretation.

This additive, fail-closed screening utility detects gaps larger than a configurable calendar-day threshold within pre- and post-cutoff windows, separately. The default four days is a **heuristic**, not an authenticated exchange calendar. It does not modify Phase 451 or certify any inference. A passed screen cannot rule out missing sessions or incorrect holiday calendars; a failed screen requires inspection, not silent interpolation.

Six deterministic unit tests passed locally on constructed dates (2026-11-18). The repository-wide suite and exact published checkout have not been executed. No original SEC observations, effect estimates, confidence intervals, or causal results are reported.

**Publication gate:** November 14, 2026 deadline missed. September pretrends, the substantial October placebo, treatment and source authentication, selection/weighting sensitivity, exchange/security controls, and block-length sensitivity remain unresolved. Recovered historical ZIPs and Phase 430/436 prototypes were not available for import in this session.

**Next:** combine this diagnostic with authenticated exchange calendars and the Phase 451 matched-date panel, run full tests, then compare block lengths and placebo windows only on authenticated historical data.
