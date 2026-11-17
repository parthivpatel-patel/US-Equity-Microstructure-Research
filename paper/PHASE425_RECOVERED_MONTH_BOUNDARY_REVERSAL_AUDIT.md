# Phase 425 — Recovered monthly-boundary reversal audit (2026-11-17)

## Scope and evidence
This is an arithmetic reanalysis of **already published, rounded values** in `archive/recovered_memos/RESEARCH_PHASE63_2026-10-31.md`, read from the existing public repository. It is not a fresh SEC-data rerun, a source authentication, or an independent replication. Phase 63's 50 matched groups and ten venues differ from the 68-treated-security Phase 2 output; no cross-sample pooling is justified.

## Four-venue share-volume negative-control check
The Phase 63 memo reports *October-minus-September* and *November-minus-October* comparisons of ten-trading-day boundary changes, in percentage points. The following derived values are computed from the memo's **three-decimal rounded numbers**. The column `swing` equals the latter comparison minus the former; it is **not** a treatment effect or a single-month jump.

| Venue | October–September (pp) | November–October (pp) | |pre|/|post| | Swing (pp) | Pre magnitude >= post? |
|---|---:|---:|---:|---:|---|
| Arca | -2.973 | +2.916 | 1.0195 | +5.889 | Yes |
| Edge-X | -2.756 | +2.750 | 1.0022 | +5.506 | Yes |
| Nasdaq | -2.388 | +0.926 | 2.5788 | +3.314 | Yes |
| Boston | +0.015 | +1.613 | 0.0093 | +1.598 | No |

**Interpretation:** Three of these *four selectively reported venues* have a pre-reform comparison at least as large in absolute magnitude as the November comparison. This is **not** a new 3/4 population statistic; the complete ten-venue comparison in Phase 63 already reports **6/10** for the raw share-volume outcome. In Arca and Edge-X, the two contrasts are almost equal in magnitude and opposite in sign, so a large second difference can arise from reversal of the pre-reform movement. Nasdaq's pre-reform magnitude is approximately 2.58 times its November comparison. Boston does not follow this pattern.

The Arca identity reported in Phase 63 checks out at published precision: November boundary change +1.073 pp minus October boundary change -1.843 pp = November-minus-October +2.916 pp. **The +2.916 pp comparison is not the November boundary's +1.073 pp change.** This distinction is essential to avoid overstating the reform-date discontinuity.

## Identification and uncertainty constraints
- Phase 63 reports **8/10** venues with a pre-reform comparison at least as large as the November comparison for raw hidden trade-count rate, **6/10** for raw hidden share-volume rate, and **2/10** for the raw volume-minus-count wedge. These are descriptive counts, not significance tests.
- The same securities recur across boundaries, and shared dates create cross-venue dependence. Neither a binomial model treating venues as independent nor ordinary row-wise resampling is justified.
- The October 1 boundary is strictly before the reform; the August boundary has lookahead cohort selection. September/October selection and trending must be evaluated before interpreting November.
- This exercise uses four rounded venue examples from a previously authored memo, not the underlying 240 monthly-step records. It cannot authenticate treatment, estimate uncertainty, or certify historical findings.

## Next empirical gate
Retrieve the original Phase 63 `results/monthly_boundary_falsification.csv` and the matched daily panel, reconcile each venue and boundary on the same security/exchange support, and recompute the 10-venue comparisons with leave-one-venue-out, fixed-cohort/coverage sensitivity, joint matched-group-and-date block resampling and serial-dependence-aware uncertainty. Before causal interpretation, independently reconcile SEC Q3/Q4 archives and historical round-lot assignments.

**Publication status:** Original November 14, 2026 deadline missed. Manuscript not publication-certified. No historical ZIP imported or newly authenticated in this session. Strictly independent of GIG and other projects.
