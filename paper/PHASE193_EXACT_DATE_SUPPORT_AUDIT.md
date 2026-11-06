# Phase 193 — Exact placebo-date and matched-group support

Date: 2026-11-06. Scope: independent U.S. equity round-lot reform study only.

## Question

The previously reported placebo window counts (82, 78, 74, 68, 58) cannot establish which exact matched-group/date observations overlap across windows and outcomes. Even equal sample sizes may have zero common observations. An empirical common-date estimator requires the intersection of *identities*, not the minimum sample count.

## Implementation

`scripts/phase193_date_support.py` accepts CSV columns `window_id,trade_date,matched_group_id,outcome` (count or volume), rejects duplicate memberships, malformed dates and weekend dates, and reports the exact intersection of matched-group/date keys across every window and both outcomes. It does not treat weekday validity as exchange-calendar authentication. Missing outcomes fail closed. The script accepts multiple placebo windows; windows are arbitrary labels, not independently validated event definitions.

## Verification

Eight deterministic unit tests on constructed memberships passed in a local execution on 2026-11-06. The test with one observation per outcome in each of two windows, on different dates, correctly returned zero common unit-dates despite equal counts. No SEC data were used. Published code should additionally be tested from a clean checkout.

## Inferential caution

An empty all-window intersection is not itself a failed study: different placebo dates can be deliberately non-overlapping. The audit answers whether a *shared observation sample* exists; a meaningful historical placebo design must additionally define valid window-specific comparisons, preserve a fixed security/exchange roster, and estimate serial-dependence-aware uncertainty. The Phase 187 two-way clustered intercept mean is descriptive and not a substitute for a security/exchange-controlled treatment estimator. Neither two-way clustering nor this membership audit authenticates historical Nasdaq treatment assignments.

## Unresolved and unpublished

Original authenticated SEC daily panel, exact historical window memberships, historical Nasdaq round-lot assignments, archive ZIPs, data licensing and redistribution review, September pretrends, October placebo warning, selection and weighting sensitivity, and controlled inference remain unresolved. No causal effect is established. Target manuscript date November 14, 2026 remains conditional.
