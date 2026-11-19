# Phase 480 — Changing panel composition can generate a false placebo contrast

Date: 2026-11-19. **Deterministic constructed example only. No SEC observations, estimated reform effects, or causal claims.**

## Identification issue

Phase 479 demonstrated that security-date missingness changes the conditional variance of date-normalized contrasts. This phase isolates a separate problem: a nonzero *expected contrast* can appear with **no time-varying underlying outcomes at all**. Let pair-level outcome be `Y[g,t] = alpha[g]` for every observed date. With positive fixed pair weights `w[g]` and availability `A[g,t]`, define `M[t] = sum_g A[g,t] w[g] alpha[g] / sum_g A[g,t] w[g]`. The placebo contrast is the post-period average of `M[t]` minus the pre-period average. It can differ from zero solely because the normalized composition changes. This is not a serial-dependence issue and robust standard errors cannot remove this deterministic bias.

## Verified constructed example

Forty sessions are split 20/20. Two matched pairs have constant outcomes `alpha = (+1, -1)` and equal weights. In the balanced panel, both are observed throughout and every date mean equals zero. In the unbalanced panel, the negative pair is absent for all 20 post sessions. The pre-period date mean is zero and the post-period date mean is +1, so the observed placebo contrast is **+1.0**, despite both pair outcomes being time-invariant. Restricting to pairs observed on every date retains the positive pair only; its pre/post contrast is **0.0**. This complete-case correction eliminates composition change *in this toy example*, but can create selection bias and reduce external validity in real data.

| Configuration | Observed date-normalized contrast | Complete-case contrast | Complete pairs |
|---|---:|---:|---:|
| Both pairs observed | 0.0 | 0.0 | 2 |
| Negative pair absent after cutoff | +1.0 | 0.0 | 1 |

With unequal weights of 1 for the positive pair and 3 for the negative pair, the pre mean is -0.5, post mean +1, and the constructed observed contrast is **+1.5**. This emphasizes interaction between missingness and weighting, without suggesting these values describe historical markets.

## Reproducibility

Run `python scripts/phase480_composition_bias.py` and `python -m unittest discover -s tests -p 'test_phase480_composition_bias.py' -v`. Eight local standard-library regression tests passed on November 19, 2026. Tests cover balanced cancellation, composition artifact, complete-case contrast, equal intercepts, no complete-case support, empty dates, unequal weights, and invalid cutoffs. The entire repository suite was not run. No source datasets are included or simulated as SEC data.

## Required empirical audit

Before reporting historical November 2025 reform estimates: authenticate SEC security-date-exchange rows and round-lot assignments; distinguish missing from true zero; tabulate per-date and per-exchange coverage and effective weights; compare a fixed security/exchange cohort with date-normalized unbalanced estimates; inspect entry/exit, matched-group membership, and exchange changes; test September pretrends and the substantial October placebo warning using dependence-aware inference. Complete-case restriction is a sensitivity specification, not a universal fix. Both treatment classification and source data remain unverified, so the paper is **not publication-certified**. The November 14, 2026 target was missed. Recovered Phase 430/436 archives and Phase 472 executable artifacts remain outstanding and were not imported in this phase.
