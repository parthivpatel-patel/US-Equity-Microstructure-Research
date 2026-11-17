# Phase 426 — Archived inference internal-consistency audit (2026-11-17)

## Input and scope
Read the **five original numeric rows** from `archive/recovered_outputs/roundlot_phase2_inference_2026-10-27.csv` on the public repository default branch. This is a deterministic arithmetic audit of previously archived *derived* estimates, not a re-estimation using SEC observations. No causal interpretation, source authentication, or new significance claim follows.

## Independent arithmetic checks
For each row compute `z = effect / se_HC3`, `lower_multiplier=(effect-ci_low)/se_HC3`, and `upper_multiplier=(ci_high-effect)/se_HC3`. All five intervals use multipliers approximately **1.95996398454** on both sides (within rounding), consistent with two-sided normal 95% confidence intervals calculated from the reported HC3 standard errors. This checks internal interval arithmetic only; it **does not validate HC3 assumptions**.

| Outcome/specification | Effect / HC3 SE | Controls implied by n minus 68 treated |
|---|---:|---:|
| dr unadjusted | -7.83844 | 2,194 |
| dr baseline adjusted | -2.14550 | 2,194 |
| dv unadjusted | -6.10475 | 2,194 |
| dv baseline adjusted | +2.65560 | 2,194 |
| October placebo trade rate | -2.64530 | 2,190 |

The placebo row has **four fewer total/control securities** than the other rows (2,258 vs 2,262; treated remains 68). Hence even the descriptive comparison of placebo and baseline-adjusted dr does not have verified identical security support.

The change in the reported point estimate between unadjusted and baseline-adjusted specifications is **+0.0238144999442** for dr and **+0.0405096592381** for dv. These are *between-specification differences*, **not** separately estimated treatment effects. The archived table contains no covariance between estimators, so no standard error, confidence interval, or p-value for either difference can be recovered from the five rows alone.

The absolute October placebo point estimate is **1.08216 times** the baseline-adjusted dr point estimate, but those rows use different sample sizes, different windows and different specifications. This ratio is **not** a placebo-adjusted treatment estimate or a valid significance comparison.

## Interpretation and non-certification
These arithmetic checks reveal no internal mismatch between the reported confidence limits and standard errors, but do not establish independence, exchange/date correlation handling, treatment assignment validity, selection robustness, or original-source authenticity. A 95% normal interval calculated correctly from a potentially inappropriate HC3 SE can still have invalid coverage. The October placebo remains a substantial warning, alongside September pretrends and estimator sign reversal. No claims of causation are warranted.

## Required next gate
Recover authenticated SEC security–exchange–day inputs and historical round-lot assignments; reproduce a common-sample September pretrend, October negative control and November contrast; retain original matched groups and exchange controls; compute dependence-aware uncertainty via matched-group and common-date resampling with serial block structure; test weighting and cohort selection sensitivity. Historical ZIP inventory remains incomplete and no archive was imported in this phase.

The original November 14, 2026 publication target was missed. Manuscript **not publication-certified**. Strictly separate from all other projects.
