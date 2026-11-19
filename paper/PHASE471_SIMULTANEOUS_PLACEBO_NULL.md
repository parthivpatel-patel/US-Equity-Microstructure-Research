# Phase 471 — Simultaneous Gaussian placebo-null benchmark

Date: 2026-11-19. **Constructed mathematical model only; no authenticated SEC observations or historical effects.**

Phase 470 showed that overlapping placebo contrasts are correlated even when observations are independent. This phase evaluates a two-sided familywise test for three cutoffs (sessions 10, 20, 30 of 40) using the exact AR(1) correlation matrix and seeded Gaussian Monte Carlo. The joint critical value is the simulated 95th percentile of the maximum absolute standardized contrast. Naive individual 1.96 thresholds are not familywise-calibrated; Bonferroni 2.39398 is a conservative analytical benchmark.

Seed 471, 200,000 joint Gaussian draws per rho:

| rho | Joint max critical (estimated) | Naive familywise rejection | Bonferroni familywise rejection |
|---:|---:|---:|---:|
| 0.0 | 2.34217 | 12.3935% | 4.4020% |
| 0.3 | 2.34022 | 12.2950% | 4.3670% |
| 0.5 | 2.33693 | 12.1785% | 4.3305% |
| 0.8 | 2.31288 | 11.4150% | 4.0665% |

These are **Monte Carlo approximations**, not exact rejection probabilities; finite Monte Carlo error applies. The joint critical value is calibrated on the same simulation draws and thus should not be described as an independently verified 5% empirical rejection rate. Bonferroni controls familywise error for valid marginal tests regardless of dependence; the covariance-calibrated threshold is conditional on the specified Gaussian AR(1) null and known parameters.

Reproduce: `PYTHONPATH=scripts python -m unittest discover -s tests -p 'test_phase471_joint_max.py'` and `python scripts/phase471_joint_max.py`. Seven local deterministic regression tests passed. Requires NumPy and SciPy.

**Unresolved:** Historical source-data authentication, treatment classification, September pretrends, substantial October placebo, security/exchange effects, matched-group and common-date shocks, weighting and selection, unknown covariance estimation, serial dependence beyond AR(1), and source licensing. No historical ZIPs or Phase 430/436 archives imported. The November 14 publication deadline was missed; paper **not publication-certified**. Next: test covariance-estimation uncertainty and two-way clustered common-date/matched-group nulls before using authenticated data.
