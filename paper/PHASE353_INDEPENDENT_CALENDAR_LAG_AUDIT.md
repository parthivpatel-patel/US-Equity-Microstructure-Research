# Phase 353 — Independent calendar-lag audit (14 November 2026)

## Scope and provenance
Read the published Phase 350 and Phase 352 Python implementations and the Phase 352 methodology note through the connected GitHub repository. Independently implemented the same equal-matched-group score decomposition locally in Python and ran ten deterministic unittest checks (10 passed, 0 failed). The local audit used **constructed fixtures only**, not authenticated SEC observations; this report is a mathematical verification, not an empirical result. The independent prototype has not been integrated into the repository.

## Reproducible hand-check fixture
Rows (group, date, contrast in percentage points):
- (A, 2025-10-01, 1), (B, 2025-10-01, 3)
- (A, 2025-10-03, 5), (B, 2025-10-03, 7)

Authenticated-calendar *placeholder for the fixture only*: October 1, 2, 3, 2025. No claim that this is an authenticated exchange calendar. The equal-group mean is 4 pp. Each group has two observations, so each observation has weight 1/4. The date scores are (-1, 0, +1), with October 2 absent from the observed rows. Calendar-indexed lag-zero score product is 2; lag-one product is 0. Omitting October 2 from the supplied session index produces adjacent observed-date scores (-1,+1), with lag-one product -1. Thus an omitted session can alter the serial score calculation without changing the descriptive mean. These numbers are fixture arithmetic only.

## Tests run
Local Python unittest checks: equal-group mean; calendar gap zero lag-one product; observed-index discrepancy; zero-lag equivalence of raw and adjusted variance; row-order invariance; unchanged mean when session support changes; duplicate rejection; off-calendar rejection; boolean contrast rejection; negative lag rejection. All ten passed in 0.001 seconds in the local runtime. This does **not** certify execution of the exact Phase 352 published checkout.

## Further methodological caution
The Phase 352 implementation fills missing session **score contributions** with zero; it does not recover the unobserved market outcomes. A zero score for a missing session is a bookkeeping convention, not evidence of zero market contrast. This distinction is consequential if missingness is nonrandom. A complete sensitivity analysis should compare balanced-session support, calendar-indexed score calculations, and attrition diagnostics. Its Bartlett correction is an exploratory raw score decomposition, not a calibrated standard error or confidence interval.

## Unresolved certification gates
Source-authenticated SEC security-date-exchange observations; contemporaneous treatment assignment and historical round-lot sizes; September pretrends; the large October placebo signal; original 78 dated placebo observations and the Phase 130 contradiction; exchange aggregation; matched-group weighting and support; two-way plus serial-dependence inference; historical ZIP/paper/code/chart provenance and redistribution permissions. None was resolved by this mathematical audit.

## Next executable step
Run published Phases 340–352 from a clean checkout, then run the calendar-indexed diagnostics on a source-authenticated, provenance-manifested panel and a verified exchange session calendar. No causal conclusion or publication certification is warranted yet.
