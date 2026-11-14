# Phase 368 — AR(1) serial dependence and overlapping placebo windows

Date: 2026-11-14. **Mathematical benchmark only; not SEC empirical inference.**

Phase 366 computed overlap correlation for five-session before/after contrasts under independent homoskedastic daily shocks. This phase relaxes independence: daily shocks follow a stationary AR(1) covariance kernel proportional to rho^|i-j|, with |rho| < 1. For window weights w=(-1,...,-1,+1,...,+1), the exact covariance of contrasts separated by k sessions is sum_i sum_j w_i w_j rho^|i-j-k|; dividing by the k=0 covariance yields correlation. The common scale factor cancels. Exact rational arithmetic avoids floating-point artifacts.

For five-session halves, lag-one correlation is 7/10 for rho=0, 3199/3788 (approximately 0.8445) for rho=+1/2, and 545/1612 (approximately 0.3381) for rho=-1/2. At lag ten, the white-noise correlation is zero, but rho=+1/2 gives -923521/9697280 (approximately -0.0952). Thus overlap alone does not bound the correlation range when underlying daily outcomes are serially dependent. These rho values are **constructed scenarios**, not fitted estimates.

Replication: `PYTHONPATH=scripts python -m unittest discover -s tests -p 'test_phase368_serial_overlap.py' -v` and `python scripts/phase368_serial_overlap.py`. Five focused deterministic tests in the published test file were derived from a six-test local prototype; the redundant self-equality test was omitted. The published checkout and full suite have not been executed. No SEC source rows were available.

The original 78 dated pseudo-events cannot be assigned calibrated p-values from ranks alone. Before empirical inference, authenticate the source observations, treatment classifications, original event dates and matching; verify September pretrends and the substantial October placebo, and use matched-group plus common-date and serial-dependence-aware resampling. Security/exchange coverage, weighting sensitivity, Phase 130 contradiction and unpublished historical archives remain unresolved.

**November 14 publication deadline missed. Manuscript uncertified; no causal claim.**
