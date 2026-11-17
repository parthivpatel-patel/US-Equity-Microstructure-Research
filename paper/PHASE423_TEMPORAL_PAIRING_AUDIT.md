# Phase 423 — Temporal and exchange-specific pairing audit (2026-11-17)

## Verified code finding
Reading the published Phase 422 `scripts/phase422_panel_membership.py` shows that `arms[g][t].add(s)` accumulates group membership over the entire September–October period and across exchanges. Consequently `groups_missing_arm` can be empty even when **no group/exchange/trading-date cell has both arms**. Phase 421's `analyze` explicitly requires both arms within each (date, match_group, exchange) cell, and silently drops unmatched cells. The two diagnostics therefore check different support conditions; Phase 422 structural_pass is not evidence that Phase 421 has usable paired observations.

## Executed reproducible fixture checks
A separate standard-library Python audit prototype was executed locally with ten unittest cases; **10/10 passed**. In particular, a treated security observed on September 2 and a control security observed on September 3, both assigned to the same group, produce zero contemporaneously paired cells; likewise, treated and control securities on the same day but different exchanges produce zero paired cells. Other checks cover duplicate keys, invalid counts, weekend rejection, unstable security membership, dates without pairs, empty input, and three fully paired September dates. These are constructed fixtures, **not empirical SEC results**. The locally tested script and tests have not yet been synchronized; their publication remains outstanding.

## Required estimation gate
For each (trading date, matched group, exchange), separately count treated and control securities and denominators. Report total cells, paired cells, unpaired cells by missing arm, paired fraction, date-specific paired coverage, dates with no paired cells, and stable membership. Do not treat an aggregate group-level arm check as sufficient. Evaluate support sensitivity to complete-case filtering; missingness can select the analysis sample and bias descriptive pretrends. Require at least three September paired dates for the existing Phase 421 slope, but do not mistake that minimal numerical condition for robust inference.

## Research and publication limitations
No original authenticated security–exchange–date panel, original 204-control mapping, or recoverable historical ZIP was available in this run. The October 2025 placebo warning, September pretrends, treatment authentication, selection/weighting sensitivity, common-date and serial-dependence-aware uncertainty remain unresolved. The November 14 target was missed; the paper is not publication-certified. Source integrity and redistribution rights require independent validation. No causal effect is claimed.

## Next
Publish the exact pairing audit prototype and tests; run against authenticated original panel and mapping, then quantify selection from missing paired cells before historical placebo and dependence-aware inference.
