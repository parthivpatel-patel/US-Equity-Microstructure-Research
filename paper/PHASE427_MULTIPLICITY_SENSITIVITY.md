# Phase 427 — Archived inference multiplicity sensitivity (2026-11-17)

## Input and execution

Read the five numeric rows from `archive/recovered_outputs/roundlot_phase2_inference_2026-10-27.csv` through the connected GitHub repository. Independently executed the accompanying Python algorithm locally on an exact transcription of these five rows. The script is provided to rerun directly on the archived CSV. This is an arithmetic sensitivity exercise on previously derived estimates, **not** fresh SEC observation-level inference.

## Calculated sensitivity

| Archived row | Original nominal p | Illustrative Holm (five tests) | Illustrative Bonferroni (five tests) |
|---|---:|---:|---:|
| dr, unadjusted | 4.56162143e-15 | 2.28081071e-14 | 2.28081071e-14 |
| dr, baseline adjusted | 0.03191283 | 0.03191283 | 0.15956416 |
| dv, unadjusted | 1.02959075e-09 | 4.11836300e-09 | 5.14795375e-09 |
| dv, baseline adjusted | 0.00791665 | 0.02374996 | 0.03958327 |
| October placebo trade rate | 0.00816182 | 0.02374996 | 0.04080908 |

Holm step-down ordering is computed by sorting p-values ascending and taking the running maximum of `(m-rank+1)*p`, capped at one. Thus the baseline-adjusted trade-count row is **0.03191 under Holm** but **0.15956 under Bonferroni**. These procedures are not interchangeable. Importantly, the October placebo itself also remains nominally small after these illustrative adjustments: it is not a reassuring negative control.

## Identification and inference limitations

The five rows do not form an established preregistered family of hypotheses, and HC3-based nominal p-values cannot be certified for exchange-date correlation, matched-security dependence, or serial correlation. Multiple-testing correction cannot repair an invalid base variance estimator, treatment misclassification, or failure of pretrends. The October placebo has a different security count and observation window. No adjusted p-value here is a defensible causal significance claim. The underlying SEC source data, matched assignments and historical treatment labels are still unauthenticated.

## Publication and archive status

The November 14, 2026 target was missed. The manuscript remains not publication-certified. No historical ZIP or original SEC panel was recovered in this phase. The next empirical gate is authenticated daily matched-panel recovery, September pretrend and October placebo re-estimation on common support, exchange controls and matched-group/common-date serial-block resampling. Keep the project separate from GIG and all other projects.
