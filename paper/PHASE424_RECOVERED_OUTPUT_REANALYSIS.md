# Phase 424 — Reanalysis of recovered Phase 2 inference table (2026-11-17)

## Evidence actually examined
Read the repository's existing `archive/recovered_outputs/roundlot_phase2_inference_2026-10-27.csv` (five rows) and the recovered Phase 63 memo. This is an **audit of archived derived estimates**, not a rerun on authenticated SEC source records. All computations below were performed directly from the five published CSV rows. The underlying original security-level data and treatment mapping were not available; the recovered output is not independent source authentication.

## Arithmetic cross-check and sensitivity
- Trade-count outcome `dr`: unadjusted estimate **-0.0346292859**; baseline-adjusted **-0.0108147859**. Absolute magnitude shrinks by **68.77%**, computed as `100*(1-abs(adjusted/unadjusted))`.
- Share-volume outcome `dv`: unadjusted **-0.0257205290**; baseline-adjusted **+0.0147891302**. The estimate **changes sign** under baseline adjustment. These are distinct model specifications, not a proven treatment response.
- The **October placebo trade-rate** estimate is **-0.0117032987**, with archived HC3 p-value **0.0081618163** and interval **[-0.0203745387, -0.0030320587]**. Its absolute magnitude is **33.80%** of the unadjusted `dr` estimate, but the samples differ (2,258 versus 2,262 securities), so this is only a descriptive scale comparison.
- Archived `dr` baseline-adjusted nominal HC3 p-value is **0.0319128324**. A *mechanical, illustrative* Bonferroni multiplication over the five displayed rows gives **0.1595641619**. For `dv` baseline-adjusted the corresponding value is **0.0395832716**; for October placebo **0.0408090815**. These numbers are **not** newly validated inferential p-values: the five rows are not a prespecified exhaustive family, and the archived HC3 errors do not establish valid common-date, matched-group or serial-dependence-aware uncertainty.
- All five rows report 68 treated securities. The archive does not provide authenticated historical treatment status, source row keys or a full control matching map.

## Interpretation
The recovered estimates already contain **material specification sensitivity and a substantial pre-reform placebo**. A small nominal HC3 p-value does not rescue causal identification. Phase 63 independently reports October-minus-September pre-reform differences comparable to November-minus-October in many venues; its 50-group/10-venue selected sample is not identical to the five-row Phase 2 table. Do not pool or directly equate the estimands.

## Verification and limitations
Calculations were performed from the published CSV values, without inventing observations. No fresh SEC panel estimates, historical ZIP imports, original source checksum verification, historical lot assignment authentication, two-way clustering, HAC or joint block bootstrap were executed. The original 2026-11-14 deadline was missed; the manuscript remains **not publication-certified**.

## Next
Recover and independently authenticate original SEC Q3/Q4 source ZIPs and September price/November SIP lot records; reconstruct the security-by-exchange-by-day panel and matching assignments. Recompute pretrends, October placebo, selection/weighting sensitivities and date/group-dependent uncertainty on a common sample. Inventory and import historical ZIPs only after permission and integrity review.

## Sources within this repository
- `archive/recovered_outputs/roundlot_phase2_inference_2026-10-27.csv`
- `archive/recovered_memos/RESEARCH_PHASE63_2026-10-31.md`
