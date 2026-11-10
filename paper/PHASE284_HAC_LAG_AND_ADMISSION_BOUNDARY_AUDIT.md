# Phase 284 — HAC lag sensitivity and admission-boundary audit

Date: 2026-11-10. Scope: software/methodology verification only; **no historical SEC observations** were available in this session.

## Reviewed published source

Read `scripts/phase282_calendar_admission.py` and `scripts/phase283_common_date_hac.py` from the repository default branch before writing this note. Phase 282 checks completeness of a supplied date/exchange grid but explicitly marks source authentication false. Phase 283 computes a Bartlett-kernel HAC standard error from aggregated daily contrasts. Neither component authenticates the supplied calendar, roster, or source data.

## Independently executed numerical diagnostic

Using an independently written Python implementation of the same displayed HAC formula, with six constructed daily contrasts, sample autocovariances divided by n and Bartlett weights `1-k/(L+1)`:

| Synthetic sequence | HAC lag | Mean | Long-run variance | HAC SE |
|---|---:|---:|---:|---:|
| 1,2,3,4,5,6 | 0 | 3.5 | 2.9166666667 | 0.6972166888 |
| 1,2,3,4,5,6 | 1 | 3.5 | 4.3750000000 | 0.8539125638 |
| 1,2,3,4,5,6 | 2 | 3.5 | 4.9722222222 | 0.9103316449 |
| 1,2,3,4,5,6 | 3 | 3.5 | 4.8750000000 | 0.9013878189 |
| 1,-1,1,-1,1,-1 | 0 | 0 | 1.0000000000 | 0.4082482905 |
| 1,-1,1,-1,1,-1 | 1 | 0 | 0.1666666667 | 0.1666666667 |
| 1,-1,1,-1,1,-1 | 2 | 0 | 0.3333333333 | 0.2357022604 |
| 1,-1,1,-1,1,-1 | 3 | 0 | 0.1666666667 | 0.1666666667 |

For six constant observations equal to 2, the mean is 2 and HAC SE is exactly zero at lags 0 through 3. These are **constructed arithmetic checks, not SEC estimates, significance claims, or repository integration-test results**. Lag choice changes uncertainty without changing the point estimate; therefore a historical report must show lag sensitivity, rather than selecting a lag after observing statistical significance.

## Additional code-review findings

1. Phase 283 checks `source_authenticated is False` but accepts any caller-supplied dictionary with that flag and expected fields. It does not cryptographically or structurally bind the input to a verified Phase 282 admission. An external caller can fabricate an admitted object. This is an **admission/provenance trust boundary**, not evidence that Phase 282 itself miscalculates.
2. Phase 282 validates that a supplied calendar is sorted, unique and ISO formatted, but does not verify it against an authoritative trading-session calendar. A complete panel relative to an incomplete supplied calendar remains admissible.
3. Phase 283 returns a zero standard error for constant synthetic contrasts. Downstream reporting must explicitly handle degenerate uncertainty rather than dividing by zero or declaring infinite statistical significance.
4. Daily aggregation followed by HAC does not provide matched-security resampling, exchange-specific common shocks, or causal identification. Pair-count weights assume fixed counts are representative; equal-exchange weights target a different estimand.
5. A very short time series makes lag sensitivity especially material. A future authenticated historical analysis must prespecify a primary lag rule and report alternatives, sample length, coverage and effective dates.

## Evidence and publication ledger

Published this phase: this audit only. The independent scratch calculation is not a historical-data script and is not claimed as repository-integrated code. No historical datasets, research ZIP archives, recovered manuscripts, authenticated rosters, figures or new empirical estimates were imported. The recovered-archive inventory is still incomplete.

## Next required work

Retrieve and hash original SEC source files; authenticate the exchange-session calendar and treatment assignments; preserve a frozen matched-security roster; rerun the published repository tests from an actual checkout; implement provenance-bound admission and degenerate-SE safeguards; execute September pretrends and October placebo dates under pair- and exchange-weighting with prespecified HAC lags and matched-group/common-date serial-dependence-aware bootstrap sensitivity. The substantial October placebo warning and September pretrends remain unresolved. No causal effect of the November 3, 2025 round-lot reform has been established. The November 14 manuscript target remains conditional.
