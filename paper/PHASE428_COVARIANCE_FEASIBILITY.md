# Phase 428 — Covariance-feasibility bounds for archived specification changes (2026-11-17)

## Provenance and scope

Input: `archive/recovered_outputs/roundlot_phase2_inference_2026-10-27.csv`, read directly from the existing public repository (GitHub blob SHA `be655daf88af11e984376f5c75dbf066aaa23418`). The new script operates on that existing file without redistributing original SEC records. Local independent arithmetic was executed for the two paired outcome/specification comparisons. Regression tests are supplied, but the full repository checkout and test suite have not been executed in this session.

## Algebra and numerical findings

For adjusted-minus-unadjusted estimates D = B - A, the unknown covariance is bounded by Cauchy–Schwarz: `-s_A*s_B <= cov(A,B) <= s_A*s_B`. Consequently `|s_A-s_B| <= SE(D) <= s_A+s_B`, assuming the two reported standard errors describe a coherent joint covariance matrix.

| Archived outcome | Adjusted minus unadjusted | Algebraic SE(D) range | Illustrative absolute z range |
|---|---:|---:|---:|
| Trade-count rate (dr) | +0.023814499944 | 0.000622804179 to 0.009458558858 | 2.51777 to 38.23754 |
| Share-volume rate (dv) | +0.040509659238 | 0.001355830596 to 0.009782223737 | 4.14115 to 29.87811 |

This is a **covariance feasibility calculation**, not a valid confidence interval or hypothesis test. The lower |z| bounds are simply effect difference divided by the largest algebraically possible SE from the *reported* HC3 standard errors. The sample counts agree (2,262 securities, 68 treated) within each pair, but matching counts do not prove identical observation-level support. There is no available covariance matrix, and the HC3 errors may substantially understate dependence-aware uncertainty. Thus **do not interpret these z ranges as evidence of statistically significant specification differences**.

The share-volume point estimate reverses sign under baseline adjustment, and both outcomes exhibit material sensitivity. The separate October placebo row (2,258 securities) is not paired in this audit; it cannot be contrasted with a principal estimate using this same covariance logic without harmonizing samples and windows.

## Required empirical follow-up

Recover and authenticate original security–exchange–date observations and treatment/match assignments; confirm identical common-support samples; recompute September pretrends and October placebo dates; estimate specification contrasts jointly with matched-group and common-date clustering plus serial-block resampling; report security/exchange controls and weighting/selection variants. The October placebo remains a substantial identification warning, not a negative-control success. Historical ZIPs were not recovered/imported in this session; no claim of causal effects or independent SEC source authentication is made.

The November 14, 2026 publication target was missed. The paper remains not publication-certified. This work is independent of GIG and all other projects.
