# Phase 151 — Block-boundary diagnostics (synthetic only)

Date: 2026-11-04. Independent U.S. equity round-lot reform research; no GIG assets.

## Scope
This phase implements a boundary-versus-interior absolute first-difference diagnostic for circular and noncircular common-calendar moving-block indices. It distinguishes within-block endpoint wrapping from discontinuities at *concatenation seams*, which remain possible under either design.

## Verification
The companion script was independently exercised locally using 400 seeded trials (200 per resampling method) on 87 synthetic dates with 10-date blocks. An exact deterministic example produced mean absolute boundary difference 4 and mean interior difference 1. The script checks eight concatenation boundaries and 78 interior transitions per 87-date realization. A nine-group common-calendar control and invalid block-size rejection were also tested.

## Interpretation and limitations
These are numerical software tests, not SEC-derived results. No market effect, empirical bootstrap p-value, or causal identification claim follows. The diagnostic does not establish a bootstrap null or correct dependence calibration. A further empirical audit must preserve group structure, common-date shocks, temporal dependence, and the complete maximum-breakpoint selection procedure.

## Open identification blockers
September 2025 pretrends; substantial October 2025 placebo/information-event warning; Nasdaq historical round-lot treatment authentication; original SEC source reconciliation; weighting and security/exchange composition sensitivity; unavailable processed panel and historical ZIP archives. No archive was imported in this phase.

## Next
Recover authenticated panel; calculate observed seam/interior residual differences across block lengths and detrending assumptions; evaluate full-scan calibration with common-date and matched-group dependence, including noncircular versus circular comparisons. Do not interpret synthetic demonstrations as empirical findings.
