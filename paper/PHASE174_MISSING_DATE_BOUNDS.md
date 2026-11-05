# Phase 174 — Missing expected-date coverage bounds

Date: 2026-11-05. Independent equity microstructure study. **No authenticated SEC observations used.**

## Finding and scope

Phase 173 correctly distinguishes absent expected trading dates from observed zero complete pairs, but its observed-only pooled coverage can still look perfect when an entire expected date is missing. Phase 174 adds *partial-identification bounds* for the fraction of complete matched pairs across a prespecified trading calendar and fixed roster. On a missing date, the lower bound assumes zero complete pairs and the upper bound assumes all roster pairs are complete. These are bounds on **data completeness**, not bounds on the reform treatment effect.

For constructed expected dates October 1, 2, 3, and 6, 2025, with two roster pairs per date, remove October 3 from otherwise fully complete observations. Post-period observed-only coverage is 100%, but calendar-adjusted post coverage is between 50% and 100%. Pre coverage is 100%, so the post-minus-pre *coverage change* is bounded between -50 and 0 percentage points. If both post dates are missing, observed-only coverage is undefined and the coverage-change interval is [-100, 0] percentage points.

The accompanying Python file contains thirteen deterministic tests for these cases and strict admission checks. A closely corresponding local prototype passed 13/13 tests on November 5; **the exact GitHub-published file still requires fresh-checkout execution**.

## Assumptions and limitations

The calendar and fixed roster must be authenticated independently; the script cannot infer holidays, halts, venue-specific availability, treatment assignments, or whether missing dates are missing completely at random. Counts must partition each fixed roster into complete, partial, and absent pairs. The bounds assume no unobserved pairs outside that roster. An absent date is not silently converted into an observed zero date. Observed zero coverage has a point value; a missing date has an interval.

## Empirical priority and provenance

No SEC archive, historical Nasdaq treatment snapshot, historical ZIP, or original paper was imported in this session. Source authentication, September pretrends, substantial October placebo warnings, exchange/security controls, changing-roster and weighting sensitivity, and common-date/serial-dependence-aware inference remain outstanding. No causal claim is warranted. The November 14 target remains conditional.

Reproduction: `python tests/test_phase174_missing_date_bounds.py -v`. Standard-library only.
