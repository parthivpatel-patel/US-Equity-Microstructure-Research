# Phase 328 — Exact-decimal aggregate feasibility reproduction (2026-11-13)

## Source and computation
Read the existing public `results/phase130_summary.csv` through the connected GitHub repository, without editing it. The published count row reports contrast −0.7346606598677254 pp, 78 placebo windows, 2 windows at least as negative, 2 windows at least as extreme in absolute value, minimum −1.4475738789418606 and maximum +1.0538523294152946.

Under the documented common-window definitions, the two observations at or below the negative event contrast are necessarily absolute extremes. The reported positive maximum exceeds the absolute event contrast and must be an additional, distinct absolute extreme. Consequently the minimum feasible extreme count is **3**, versus **2** published. This is an exact-arithmetic contradiction, not an estimate of reform impact.

For volume, the published contrast +0.626597999820323, negative-tail 48/78, absolute-extreme 76/78, minimum −1.8665501312689659 and maximum +1.4840122108986915 do not contradict the analogous necessary-extrema condition. Passing a necessary condition does not validate the volume row.

## Reproduction and validation
The source CSV was retrieved from the existing public GitHub repository. An independent local Python Decimal implementation reproduced the count contradiction and volume necessary-condition pass. Eight deterministic synthetic unit tests passed locally (zero failures). This report is the publication artifact for this session; no authenticated placebo-window observations or SEC security/exchange panel were recovered.

## Interpretation and unresolved blockers
The Phase 130 count row must remain quarantined pending reconstruction from the original dated placebo windows and summary-producing code. The 78 overlapping windows are not 78 independent randomizations. September pretrends, October placebo effects, round-lot treatment authentication, selection/weighting sensitivity, common-date and serial-dependence-aware inference, and historical ZIP provenance remain unresolved. Do not claim causal effects or publication certification. The November 14 target is conditional.
