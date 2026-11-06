# Phase 182 — Identifying the common historical placebo calendar (2026-11-05)

## New methodological result

Phase 181 established that the published denominators 82, 78, 74, 68 and 58 do not identify their five-way intersection. This session adds a **testable conditional implication**: if all five windows use a common historical candidate-date universe, identical exclusion rules except for symmetric window length, and no window-specific missingness or data-dependent screening, then the eligible-date sets should be nested (15-day subset of 10-day subset of 7-day subset of 5-day subset of 3-day). Under these **unverified assumptions**, the common-date intersection is exactly the smallest set, **58 dates**. This is not an observed intersection or a claim about actual SEC records.

Non-nesting is possible if missing security/exchange observations, endpoint rules, sample-selection filters or differing calendars affect each window. Consequently, even a monotone sequence of counts does not establish nested membership.

## New reproducible gate

`scripts/phase182_membership_audit.py` reads an explicit eligible-date membership CSV with columns `window_days,placebo_date,outcome`, rejects duplicates, invalid dates, unknown windows/outcomes and count/volume membership discrepancies, and requires denominators to match the previously published summary. It reports the exact union and intersection and whether sets are nested. It **does not** fabricate dates or recover contrasts from counts.

Run: `python scripts/phase182_membership_audit.py path/to/authenticated_membership.csv`

## Empirical and provenance status

No authenticated eligible-date membership file or original SEC daily panel was available for execution here. The 58-date nested result is a conditional mathematical deduction, **not an empirical finding**. September pretrends, the substantial October pre-reform placebo shift, treatment authentication, weighting/selection sensitivity, security/exchange controls and matched-group/common-date/serial-dependence-aware inference remain unresolved. No recovered historical ZIP/PDF was imported. The Phase 176 inventory remains the last reported public archive inventory; a new comprehensive archive inventory was not performed.

Next: authenticate SEC source files and Nasdaq treatment assignments, reconstruct eligible-date memberships from the fixed matched roster, execute this gate, then recompute placebo contrasts on observed common dates. The November 14 deadline remains conditional; no causal effect has been established.
