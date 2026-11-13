# Phase 338 — Covariance-agnostic bounds for nested-period pretrend differences

Date: 2026-11-13. Source: `results/phase136_trend_uncertainty_presentation.csv`, GitHub blob `e89016144b1b60079a4686c02a945009a2734c06` (20 published aggregate rows). This audit does **not** reconstruct SEC observations or estimate a new regression.

The July–September and July–October regressions use overlapping observations (64 and 87 dates respectively; 68 groups reported in each). Subtracting their published slope estimates without accounting for *unknown cross-estimator covariance* does not supply a valid standard error for an October shift. Cauchy–Schwarz implies `|s_A-s_B| <= SE(B-A) <= s_A+s_B` for marginal standard errors `s_A` and `s_B`. These are algebraic bounds conditional on accepting displayed standard errors, **not** calibrated finite-sample inference.

| Outcome | Lag | July–October minus July–September slope (pp/day) | Upper bound on difference SE | Smallest possible absolute slope-change/SE |
|---|---:|---:|---:|---:|
| count | 0 | -0.032690 | 0.015292 | 2.137719 |
| count | 3 | -0.032690 | 0.019866 | 1.645525 |
| count | 5 | -0.032690 | 0.021692 | 1.507007 |
| count | 10 | -0.032690 | 0.024444 | 1.337342 |
| count | 15 | -0.032690 | 0.025820 | 1.266073 |
| volume | 0 | -0.025812 | 0.017200 | 1.500698 |
| volume | 3 | -0.025812 | 0.020564 | 1.255203 |
| volume | 5 | -0.025812 | 0.021436 | 1.204143 |
| volume | 10 | -0.025812 | 0.022003 | 1.173113 |
| volume | 15 | -0.025812 | 0.021509 | 1.200056 |

**Finding:** Only the count lag-0 row is guaranteed to exceed an illustrative 1.96 ratio across *all admissible correlations* between the two period-specific slope estimates. None of the other nine rows meets that covariance-agnostic criterion. This does **not** establish that those nine differences are insignificant: their actual cross-period covariance is unknown, and the conservative upper bound may be loose. Nor does the lag-0 inequality validate its standard errors, critical value, selection process or causal interpretation. The nested periods are not independent; naive quadrature would be unjustified.

The difference of full-period OLS slopes is **not the same estimand** as an October interaction coefficient or an October-only slope. The October break estimates reported elsewhere must not be conflated with this difference. The substantial October placebo warning, September pretrends, contradictory Phase 130 hidden-count placebo tail counts, unauthenticated treatment and SEC inputs, weighting sensitivity, and common-date/serial-dependence-aware inference remain unresolved.

Reproduce: `python scripts/phase338_covariance_bounds.py results/phase136_trend_uncertainty_presentation.csv`; synthetic checks: `python -m unittest discover -s tests -p 'test_phase338_covariance_bounds.py'`. Seven synthetic tests passed locally. Numerical table was independently recomputed from GitHub-fetched CSV rows. Exact published checkout and full repository suite were not run.

**Publication gate:** The November 14 target is not certified. Recover original dated placebo observations, producing code and authenticated security-exchange panel, then estimate *joint* covariance of period slopes and appropriate dependence-aware uncertainty. Historical research ZIPs remain unverified and unimported; no causal reform claim is warranted.
