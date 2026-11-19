# Phase 475 — Heterogeneous common-date loadings and serial dependence (constructed benchmark)

Date: 2026-11-19. **Synthetic mathematical benchmark, not historical SEC estimates or evidence of causal effects.**

## Model
For matched pair g and date t, define treated-minus-control outcome D[g,t] = alpha[g] + delta F[t] + u[g,t], where delta is the treated-minus-control factor loading. F has stationary AR(1) covariance sigma_F² rho^|t-s|, |rho|<1; u is independent across g,t with variance 2 sigma_u² (the difference of two independent unit-variance idiosyncratic components when sigma_u²=1). The placebo estimator averages D across G matched pairs and then takes post-minus-pre means at cutoff k, using weights w[k,t]. Group intercepts cancel. Its exact covariance is

Cov(theta_k,theta_l) = delta² sigma_F² sum_(t,s) w[k,t] w[l,s] rho^|t-s| + (2 sigma_u²/G) sum_t w[k,t]w[l,t].

An identically loaded common-date factor cancels in treated-control differences (delta=0), but differential exposure leaves residual date dependence. These results assume balanced pairs, independent idiosyncratic innovations, and a known AR(1) covariance.

## Reproducible exact benchmark
T=40, G=68, cutoff=20, sigma_F²=sigma_u²=1. Standard error inflation compares the full covariance to the no-common-factor covariance, holding all other inputs fixed.

| delta | rho | Exact variance | SE inflation |
|---:|---:|---:|---:|
| 0.0 | 0.0 | 0.002941176 | 1.000000 |
| 0.0 | 0.5 | 0.002941176 | 1.000000 |
| 0.1 | 0.0 | 0.003941176 | 1.157584 |
| 0.1 | 0.5 | 0.005641177 | 1.384919 |
| 0.5 | 0.0 | 0.027941176 | 3.082207 |
| 0.5 | 0.5 | 0.070441186 | 4.893874 |
| 1.0 | 0.0 | 0.102941176 | 5.916080 |
| 1.0 | 0.5 | 0.272941215 | 9.633276 |

Values are deterministic model outputs, rounded for display. The group count is an illustrative parameter, not an authenticated treatment count. This extension corrects the risk of interpreting Phase 474's shared-date benchmark as a universal DiD variance multiplier.

## Reproduction
Run `PYTHONPATH=scripts python -m unittest -v tests/test_phase475_heterogeneous_date.py` and `python scripts/phase475_heterogeneous_date.py`. Seven targeted standard-library tests passed locally on 2026-11-19; full repository suite not run.

## Limitations and next gates
No empirical estimates, authenticated SEC source files, treatment mapping, recovered historical ZIP imports, exchange effects, weighting sensitivity, September pretrend resolution, or October placebo resolution are established here. Differential loading is assumed rather than estimated. The AR(1) date factor and balanced independent-pair assumptions may be inadequate. Historical inference must estimate exposures, handle selection/missingness, account for matched security/exchange and common-date dependence, and calibrate simultaneous placebo tests. The November 14, 2026 publication target was missed; manuscript remains not publication-certified. Phase 472 executable artifacts remain unpublished pending recovery.
