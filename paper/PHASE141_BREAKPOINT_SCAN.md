# Phase 141 — Alternative pre-reform breakpoint scan (2026-11-04)

## Executed scope
Recovered Phase 131 processed panel from the previously archived reproducibility ZIP. SHA-256 of the processed CSV matched `6347d66cd7fa7ffa070b60529935e7ca9c93ef5c7f8dc61050fba33582f9aea1`. Verified 14,416 rows, 68 groups, 106 dates, unique group/date/outcome keys, and no missing contrasts. Pre-reform subset: 11,832 rows, 87 trading dates (July–October 2025). These are **processed-panel integrity checks, not independent SEC source authentication**.

For each outcome, scan all 48 feasible pre-reform breakpoint dates with 20 trading observations before and 20 on/after each breakpoint. Compute OLS slopes of the equal-weighted 68-group daily mean separately in each local window, and report post-minus-pre slope. This is a descriptive overlapping-window scan, **not a calibrated hypothesis test**.

## Findings (percentage points per trading day)
- **Hidden trade count:** October 1 local slope shift **−0.155896**. The largest absolute local shift occurred **September 19: −0.285085**. The top five absolute count breaks were September 17, 18, 19, 22, and 23.
- **Hidden share volume:** October 1 local slope shift **−0.192277**. The largest absolute local shift occurred **September 26: −0.235389**. Top five absolute volume breaks: September 25, 26, 29, 30, and October 1.

This reinforces the September pretrend warning: October 1 is not uniquely dominant in the scan, and candidate breaks are strongly overlapping. Breakpoint selection, serial correlation, multiple comparisons, and the October information event preclude naive significance claims. No November reform effect is identified.

## Reproduction and gaps
The script `src/phase141_break_scan.py` was executed locally using the recovered Phase 131 processed CSV; its full 96-row output was generated locally. The processed CSV is not yet published, so public reproduction remains incomplete. Source-level SEC and historical Nasdaq treatment authentication, venue/security composition, and dependence-aware breakpoint inference remain unresolved. No raw licensed source data are redistributed.

Next: publish a permissible processed-data reproduction pathway, authenticate original security/exchange observations and historical lot-size assignments, and implement a common-date-block null distribution for a prespecified break statistic. Preserve the October placebo and selection-sensitivity caveats.
