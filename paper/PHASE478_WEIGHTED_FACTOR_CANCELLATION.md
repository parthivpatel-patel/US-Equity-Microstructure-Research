# Phase 478 — Weighting breaks signed common-date factor cancellation

Date: 2026-11-19. **Constructed covariance benchmark only, not historical SEC evidence.**

## Extension of Phase 477

Phase 477 established that equal weighting of 34 pairs with loading +0.5 and 34 with loading -0.5 cancels a common-date factor. This phase shows that unequal *positive* pair weights can undo that cancellation even when the matched sample and signed exposures do not change.

Define paired difference D[g,t] = a[g] + delta[g] F[t] + u[g,t]. The pooled pre/post contrast uses normalized pair weights p[g] and date contrast weights c[t] = -1/20 for dates 1–20 and +1/20 for dates 21–40. Assume a stationary unit-variance AR(1) common factor with correlation rho_F, independent pair-specific stationary AR(1) residuals with variance 2 and correlation rho_u, and no cross-pair residual covariance. Define Q(rho) = sum_t sum_s c[t] c[s] rho^abs(t-s). Then:

Var(theta) = (sum_g p[g] delta[g])^2 Q(rho_F) + 2 (sum_g p[g]^2) Q(rho_u).

Effective number of equally weighted pairs is 1 / sum_g p[g]^2. Relative to a model omitting the common factor, the exact standard-error ratio is sqrt(1 + (weighted signed loading)^2 Q(rho_F) / (2 sum_g p[g]^2 Q(rho_u))). This identity holds at the covariance level without requiring Gaussianity.

## Exact constructed results

68 pairs, 40 dates, 34 positive loadings (+0.5), 34 negative loadings (-0.5), rho_F = rho_u = 0.5. Relative weight multipliers apply to the positive group versus the negative group.

| Positive:negative pair weight | Weighted signed loading | Effective pairs | SE inflation |
|---|---:|---:|---:|
| 1:1 | 0.000000 | 68.0 | 1.000000 |
| 2:1 | 0.166667 | 61.2 | 1.360147 |
| 1:2 | -0.166667 | 61.2 | 1.360147 |
| 4:1 | 0.300000 | 50.0 | 1.802776 |

The signed factor loading is zero under equal weights, but no longer zero when weights shift. Reversing which group receives larger weights reverses the sign of the aggregate exposure without changing variance. When factor and residual AR(1) correlations are equal, their Q terms cancel in the relative SE ratio, **not** in the absolute variance.

## Reproduction and validation

Run `python scripts/phase478_weighted_exposure.py`. Run tests from the repository root with `PYTHONPATH=scripts python -m unittest discover -s tests -p 'test_phase478_weighted_exposure.py' -v`. Five deterministic tests were executed locally and passed: cancellation, sign permutation, scale invariance, equal-persistence ratio invariance, and invalid-weight rejection. Full repository tests were not run.

## Research interpretation and open gates

Weighting choice can transform a theoretically cancelling factor into an important variance component. Thus the empirical paper must separately disclose equal-security, trade-count and share-volume weighting; inspect signed exposure and effective sample size under each; and test sensitivity to missing observations, exchange composition, security fixed effects, and common-date dependence. Neither the synthetic 68-pair count nor the loading patterns authenticate treated securities.

The substantial October 2025 placebo warning and September pretrends remain unresolved. Historical SEC data and treatment classification must be authenticated before any causal interpretation. Joint placebo tests require estimated-covariance and serial-dependence-aware inference. The November 14 deadline passed; the manuscript remains **not publication-certified**. Historical Phase 430/436 archives and Phase 472 executable package remain unimported/unpublished as previously reported. No historical data or figures were introduced here.
