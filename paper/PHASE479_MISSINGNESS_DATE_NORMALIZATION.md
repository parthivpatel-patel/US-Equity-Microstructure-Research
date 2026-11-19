# Phase 479 — Missingness changes signed date-factor cancellation

Date: 2026-11-19. **Exact constructed covariance benchmark; not historical SEC data.**

## Motivation
Phase 478 considered constant pair weights in a balanced panel. Actual security-date-exchange panels may have absent observations, and a date-normalized estimator then changes its effective weights from date to date. This matters even when the nominal security weights are fixed.

## Estimator and exact covariance
Let paired differences be `D[g,t] = alpha[g] + delta[g] F[t] + u[g,t]`, where the common factor `F` has stationary unit variance and AR(1) correlation `rho_F`, and mutually independent pair-specific residuals `u` have variance `sigma_u^2` and AR(1) correlation `rho_u`. This is a deliberately simplified model; `alpha[g]` is not guaranteed to cancel when missingness changes composition.

For observed indicator `A[g,t]`, nonnegative fixed pair weight `w[g]`, and pre/post date contrast `c[t]` (minus 1/20 before, plus 1/20 after), define `h[g,t] = c[t] A[g,t] w[g] / sum_j A[j,t]w[j]`. The estimator is `theta = sum_g,t h[g,t]D[g,t]`. Define signed date exposure `b[t] = sum_g h[g,t]delta[g]`. Then, conditional on the availability mask, its *stochastic* variance is exactly

`Var(theta | A) = sum_t,s b[t]b[s] rho_F^|t-s| + sigma_u^2 sum_g,t,s h[g,t]h[g,s] rho_u^|t-s|`.

This covariance identity does not require Gaussian innovations. It assumes the mask is fixed/exogenous for conditional variance calculation. Informative missingness may bias the estimator and invalidate this conditioning for causal interpretation.

## Reproducible two-pair example
There are 40 dates, two matched pairs with factor loadings `+0.5` and `-0.5`, equal nominal weights, unit-variance factor, residual variance 2 per pair, and both AR(1) correlations 0.5. Both pairs are observed on all dates in the balanced case. In the unbalanced case, the negative-loading pair is missing for all 20 post dates.

| Conditional covariance component | Balanced | Negative-loading pair absent post |
|---|---:|---:|
| Common-factor variance | 0.0000000000 | 0.0350000024 |
| Pair-residual variance | 0.2700000381 | 0.4100000477 |
| Total stochastic variance | 0.2700000381 | 0.4450000501 |
| SE ratio vs omitting factor *within configuration* | 1.000000 | 1.041809 |

The post-period signed exposure becomes `+0.5` per date instead of zero. This breaks factor cancellation. **The larger change in total variance also reflects changed residual concentration; do not attribute the whole difference to common-date factors.** In addition, if pair intercepts differ, changing composition creates a nonzero pre/post contrast even under no treatment. Neither result is an observed reform effect.

## Validation and reproduction
Run `python scripts/phase479_missingness.py` and `python -m unittest discover -s tests -p 'test_phase479_missingness.py' -v` from the repository root. Six tests passed locally, covering balanced cancellation, missingness effect, common loading identity, weight scaling, empty-date rejection, and zero loadings. Full repository regression tests were not executed.

## Empirical implications and unresolved gates
The eventual historical panel audit must enumerate security-date-exchange coverage, date-specific effective weights and signed exposures, absent versus true-zero cells, exchange composition, and sensitivity to balanced-only samples and fixed-composition estimators. Missingness must not be imputed as zero execution without source-level justification. September pretrends and the substantial October 2025 placebo warning remain unresolved; round-lot treatment assignments and SEC observations require authentication. This benchmark does not substitute for matched-security and common-date clustered or serial-dependence-aware empirical inference. The November 14, 2026 deadline was missed; the manuscript remains **not publication-certified**. Phase 430/436 archives and Phase 472 standalone executable artifacts remain unimported or unverified for publication.
