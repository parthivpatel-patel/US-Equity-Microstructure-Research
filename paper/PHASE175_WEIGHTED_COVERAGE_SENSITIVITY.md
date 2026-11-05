# Phase 175 — Fixed-roster weighting sensitivity for missing-pair coverage

Date: 2026-11-05. Independent US equity microstructure study. **No authenticated SEC daily observations used in this phase.**

## Diagnostic

Phase 174 bounds the proportion of complete matched pairs on a fixed expected-date calendar. Phase 175 checks how that completeness measure changes when the *fixed matched-group weights* differ. This is important because the security/equity-volume-weighted and equal-matched-group-weighted populations need not have the same coverage. The routine never estimates an equity-market treatment effect.

For each expected date d and prespecified matched group g, let c(d,g)=1 if a complete pair is observed, 0 if known incomplete, and unknown if absent. Fix strictly positive weights w(g) **before** inspecting outcomes or missingness. The denominator is sum of w(g) across *every* expected date and group, including missing dates. The lower coverage bound assigns zero to unknown cells; the upper assigns one. A known incomplete pair is zero in both. Period-change bounds are [post_lower - pre_upper, post_upper - pre_lower]. These are arithmetic worst-case coverage bounds, **not confidence intervals** and not treatment-effect bounds.

## Constructed-data result

With two groups, one complete and one known incomplete, equal weights yield 50% coverage. Weighting the incomplete group nine times as heavily yields 10% coverage. This difference arises solely from the estimand's weights, without changing any observed cell. In another fixture, complete pre-period coverage and one missing post-period group produce a post-minus-pre coverage-change interval [-50, 0] percentage points under equal weights.

Ten local Python unittest methods passed on 2026-11-05 against a closely matching local implementation. The published code is not yet confirmed from a fresh checkout. Run: `python tests/test_phase175_weighted_coverage.py -v`.

## Identification and source-data gates

The roster, expected dates, treatment assignment, and any weights proportional to historical share volume must be independently authenticated. Using realized post-event volume to define weights risks post-treatment selection. Exchange-specific missingness, security eligibility, changes in listings, corporate actions, September pretrends, and the substantial October 2025 placebo remain unaddressed empirically. Serial and common-calendar-date dependence, security/exchange effects, matched-group uncertainty, and alternative estimands require analysis on the authenticated panel. Do not infer causality from a coverage bound.

## Archive and publication status

No historical SEC archive, Nasdaq historical treatment snapshot, previously recovered ZIP, original paper, or original market-data figure was imported during this phase. Inventory status for those historical materials remains **not authenticated/not imported**; no redistribution permissions have been established. This phase publishes only newly written code and this report. The November 14, 2026 manuscript target remains conditional, and no reform effect is established.
