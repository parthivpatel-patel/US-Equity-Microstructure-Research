# Phase 183: common-date contrasts require row-level inputs

2026-11-05. This note extends Phase 182, which validates eligible-date membership but does not contain placebo contrast values.

## Verified methodological result

The five published placebo denominators (82, 78, 74, 68, 58) do not identify the shared date intersection or the means of the contrasts on that intersection. For a window w, the common-date mean is sum of contrast(w,d) over d in the intersection, divided by the intersection size. Neither the numerator nor the intersection is determined by window totals. Even when eligibility is nested, the 58 shared-date contrasts themselves remain necessary.

## Reproducible local validation

A standard-library prototype was executed locally with seven deterministic unittest cases, all passing. It checked exact ISO date formatting, duplicate date/window/outcome keys, nonfinite contrast rejection, count-versus-volume date alignment, matched-roster count alignment, and rejection of empty common intersections. The fixture used two constructed September 2025 dates per window, with a known five-day mean of 1.0 percentage point. This is a *software fixture*, not an SEC result.

## Important restrictions

The row-level input contract is window_days, placebo_date, outcome, contrast_pp, matched_groups. Matching roster *counts* do not prove identical security membership; authenticated roster IDs are needed for a valid fixed-sample analysis. The prototype's means are descriptive, not a statistical test; clustered or block-resampled inference must operate on original matched-group/date observations, not these aggregates. No new SEC estimates, causal effects, or authentic treatment labels were generated.

## Source inventory and next step

Phase 176 reported no ZIP/PDF archives on the public branch at that time. Historical research ZIPs, original SEC daily observations, treatment snapshot, and exact placebo-date memberships have not been authenticated or imported in this phase. Next: recover source data and publish a hashed manifest before estimating common-date and dependence-aware contrasts. September pretrends, October placebo and weighting/selection sensitivity remain unresolved.
