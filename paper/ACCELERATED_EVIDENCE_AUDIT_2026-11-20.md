# Accelerated evidence audit — recovered Phase 2 processed panel
**As of 2026-11-20. Research status: exploratory, not source-authenticated, not causal, not publication-certified.**

## Input and validation scope
Reanalyzed the earlier **roundlot_phase2_security_panel.csv** recovered from the research file library (2,262 securities, 68 provisional treated, 2,194 control). SHA-256 of actual input bytes: **2ccb80427a765ca3858f11f2874d6f87a79a559ec1fdeafc34420e82840e5bbb**. This processed CSV is **not redistributed** here. It is a stock-level pre/post panel, not a daily security-exchange panel. Its SEC ZIP provenance, Nasdaq historical round-lot assignments, ticker/identity crosswalk, and filtering decisions have **not been independently authenticated**.

The program in scripts/phase2_sensitivity_reaudit.py validates column schema, unique symbols, finite rates, rate differences, positive denominators, and treatment labels; it computes aggregate sensitivity scenarios. Ten deterministic tests passed locally (constructed fixtures, standard-library unittest) against the development script and a repository-layout copy. A successful SHA-256 match establishes byte identity **only**, not authenticity of original SEC observations.

## Direct results (percentage points)
| Comparison / selection | Treated | Controls | Hidden trade-rate change gap | Hidden volume-rate change gap |
|---|---:|---:|---:|---:|
| Equal-security means | 68 | 2,194 | -3.4629 | -2.5721 |
| Weighted by **pre-period trade count** | 68 | 2,194 | -2.7064 | -1.0065 |
| Exclude bottom quartile of pre-trades within each arm | 51 | 1,645 | -4.1583 | -3.0891 |
| Max pre/post observed days | 68 | 2,162 | -3.5191 | -2.5982 |
| Control pre-trades within observed treated range | 68 | 990 | -3.4807 | -2.3856 |

Weights are archived **pre-period trade counts** and **not** volume-share weights, trade-level SEC weights, or inverse-propensity weights. The original stock-level rates are period-aggregate ratios. Change gaps compare mean post-minus-pre security rates by provisional treatment status. Positive or negative gaps do not identify a treatment effect.

Baseline treated-minus-control hidden rate: **+14.5672 pp** (trades), **+20.1370 pp** (volume). Such large initial differences constrain comparability. Under pre-trade weighting, Kish effective sample sizes are **10.40** treated and **134.65** control despite 68/2,194 nominal units. Hence weighted precision and influence need careful verification. Selecting only higher-trading names changes the estimand, not just variance.

## Reproduction of inherited Phase 2 coefficient (separate local check)
Statsmodels 0.14.6 HC3 regressions run on the same recovered CSV reproduced the earlier Phase 2 memo to rounding:
- Unadjusted dr coefficient -0.0346293; HC3 SE 0.0044179.
- Adjusted for r_pre and v_pre: dr -0.0108148; HC3 SE 0.0050407.
- Unadjusted dv -0.0257205; HC3 SE 0.0042132.
- Adjusted dv +0.0147891; HC3 SE 0.0055690 (**sign reversal**).
This check confirms numerical consistency of the inherited processed file with that memo; it **does not** authenticate raw SEC inputs or validate causal inference. Cross-sectional HC3 standard errors do not capture common-date serial dependence.

## Independent audit of previously published historical *summaries*
Read the existing public results/phase130_summary.csv, phase136_trend_uncertainty_presentation.csv, phase139_paired_october_shift_presentation.csv and phase140_paired_interval_width_audit.csv via the connected GitHub integration. Recomputed 18 numerical identities (Phase 130 November-minus-October differences, Phase 139 October-minus-July/September slopes, Phase 140 interval widths); **18/18 matched** at their published precisions. This is an internal arithmetic consistency audit **only**, not raw-data replication. Existing reported Phase 136 HAC-lag-5 two-way intervals for Jul–Sep count pretrend are [0.006235, 0.050979] pp/session, and Phase 139 October slope differences are -0.170197 (count) and -0.156416 (volume) pp/session, both exploratory and unverified at source level. The large October pre-reform movement remains an identification threat.

## Accelerated publication decision
1. **Immediately:** secure and checksum the original SEC Q3/Q4 security-and-exchange archives and verify metrics, date/venue coverage, and eligibility. Do not publish raw ZIPs until redistribution rights are cleared.
2. **Next:** authenticate the September 2025 round-lot assignment list (including corporate actions and price-band evaluation); construct a frozen, date-specific treated/control roster. A GitHub snapshot is provisional.
3. **Then:** run paired security/exchange/common-date September and October placebo/pretrend diagnostics, composition and weighting sensitivity, and serial-dependence-aware inference; do not select the best result post hoc.
4. **Publication decision:** if source lineage or treatment cannot be authenticated on the compressed schedule, release an openly labeled **exploratory/falsification-focused working paper** with transparent caveats, not a causal or fully replicated claim. If authenticity or pretrend failures remain severe, delay publication certification instead of inventing certainty.

The original 2026-11-14 target has passed. This audit advances the actual numerical evidence but does **not** complete empirical validation or manuscript certification. Archive recovery is still incomplete (Phases 430/436 and 472 absent). This work is strictly independent of GIG and other projects.
