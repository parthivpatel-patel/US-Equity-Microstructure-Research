# Phase 500 — Date-stratified treatment/control coverage

Date: 2026-11-20. Status: deterministic diagnostic, **not historical SEC empirical evidence**.

## Why this matters
Phase 499 aggregates eligibility coverage by exchange and treatment group. Aggregate coverage can conceal calendar-specific imbalance. This diagnostic preserves each exchange/date cell, separates pre/post at a canonical cutoff, and reports treatment/control eligible and observed security counts, coverage fractions, and treated-minus-control coverage gaps. A group with zero eligible securities is represented by null coverage, **not** zero coverage. It also distinguishes both groups being eligible from both groups actually being observed.

## Verification
Nine deterministic pytest tests passed locally (0.06 seconds, zero failures) on the matching local implementation. The constructed fixture demonstrates a post-cutoff treated-minus-control coverage gap of 1.0 when one treated security is observed and one eligible control security is missing. This is a *synthetic fixture result*, not a historical estimate. The diagnostic operates on unique keys, not outcome values. No SEC historical records were loaded. The exact remote checkout has not been rerun.

## Limitations and interpretation
No causal or economic effect is estimated. Eligibility keys and treatment labels must be authenticated externally; exchange calendars, symbol histories, source licensing, match construction, and panel missingness must be checked. A coverage gap is not an outcome gap. Security-exchange clustering, common-date matched inference, and date-block resampling remain separate requirements. September pretrends and the substantial October placebo warning remain unresolved. The November 14 manuscript target was missed; the manuscript is not publication-certified.

## Historical artifact inventory / pending work
Recovered Phase 430/436 ZIPs and Phase 472 artifacts remain unpublished pending verified access, checksums, redistribution permissions, and size limits. This phase imports none of them. Next: authenticate SEC source and eligibility records, run Phases 496/498/499/500 on September and October, and compare missingness patterns before any renewed placebo estimation.
