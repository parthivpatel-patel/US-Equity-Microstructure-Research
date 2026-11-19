# Phase 477 — Heterogeneous factor loadings and cancellation in matched-pair placebo inference

Date: 2026-11-19. **Exact constructed-model benchmark only. No historical SEC observations, empirical treatment classifications, or causal effects are claimed.**

## Why this extension matters

Phase 476 assumed every matched treatment-control pair had the same common-date factor-loading difference (delta=0.5). That assumption makes the common factor persist after aggregation. Here we allow the factor-loading difference to vary in sign and magnitude across pairs. This is a substantive sensitivity test: the relevant quantity for the *equally weighted pooled contrast* is the average signed loading, not the average absolute loading.

Let D[g,t] = a[g] + delta[g] F[t] + u[g,t]. There are G=68 constructed independent matched pairs, T=40 dates, 20 pre and 20 post, stationary unit-variance AR(1) common factor F and independent across-pair residuals u of variance 2. The factor and pair residuals have correlations rho_F and rho_u respectively. Let w[t] be -1/20 pre and +1/20 post, and Q(rho) = sum_{t,s} w[t]w[s]rho^|t-s|. For the equally weighted pooled contrast:

Var(theta) = mean(delta)^2 Q(rho_F) + (2/G) Q(rho_u).

Relative to a model with the same residual variance but no common factor:

SE inflation = sqrt(1 + G mean(delta)^2 Q(rho_F)/(2 Q(rho_u))).

This is the exact covariance of the specified linear Gaussian-style second-moment model; normality is not needed for the variance identity. It is **not** a variance formula for arbitrary non-independent pairs or estimated loadings.

## Exact reproducible calculations

Set rho_F=rho_u=0.5, G=68. Each nonzero loading is either +0.5 or -0.5.

| Constructed loading pattern | Mean signed loading | SE inflation vs no factor |
|---|---:|---:|
| All 68 pairs +0.5 | 0.50000000 | 3.08220700 |
| 34 pairs +0.5, 34 pairs -0.5 | 0.00000000 | 1.00000000 |
| 51 pairs +0.5, 17 pairs -0.5 | 0.25000000 | 1.76776695 |
| One pair +0.5, 67 pairs zero | 0.00735294 | 1.00091870 |

The exact arithmetic and invariants are implemented in [scripts/phase477_signed_factor_loadings.py](../scripts/phase477_signed_factor_loadings.py). Run with `python scripts/phase477_signed_factor_loadings.py`. The zero-mean loading case cancels the common factor *algebraically in the pooled estimator*, despite nonzero individual pair exposures. This does **not** establish that date clustering can be omitted: unequal weights, missing observations, correlated residuals, estimated matching, changing loadings, and other date factors can all break cancellation.

## Research implications and publication gates

The earlier uniform-loading benchmark is an intentionally adverse sensitivity case, not a general estimate of common-date uncertainty. Before empirical inference, authenticate source SEC observations and the November 3 treatment mapping, document missingness and weights, inspect signed date-factor exposures, preserve exchange and security clustering, and test September pretrends plus the substantial October placebo signal. Joint placebo inference must account for overlapping cutoffs, serial dependence and estimated covariance. A constructed 68-pair count is not proof of 68 authenticated treated securities.

The November 14, 2026 target has passed and the manuscript is **not publication-certified**. Historical Phase 430/436 archives have not been verified or imported, and the Phase 472 standalone code package remains outstanding. No licensed data, secrets, or fabricated figures were added.
