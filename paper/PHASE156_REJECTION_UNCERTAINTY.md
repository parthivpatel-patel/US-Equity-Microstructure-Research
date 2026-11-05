# Phase 156 — Independent reproduction and uncertainty of Phase 155 null rejection rates

**Scope:** Synthetic Monte Carlo only; no SEC/Nasdaq data, no market effect estimate. Executed locally with NumPy, 2026-11-04. Reimplemented the published Phase 155 seeded experiment and independently computed Wilson 95% binomial intervals. Command: `python tests/test_phase156_rejection_uncertainty.py`. This script asserts the 12 Phase 155 rejection counts exactly.

Each cell has 40 synthetic null panels, nine matched groups, 87 dates, 20-date adjacent-window slope scan, 99 bootstrap draws, common-date shocks and AR(1) dependence. Intervals reflect Monte Carlo replication uncertainty *conditional on each fixed simulation configuration*, not confidence intervals for a reform effect. The same panel seeds are used across methods/configurations; cells are not independent.

| AR phi | Common shock | Block | Method | False rejections /40 | Mean p | Wilson 95% interval for rejection probability |
|---:|---:|---:|---|---:|---:|---|
| 0.0 | 0.7 | 10 | Noncircular | 3 | 0.4457 | [0.0258, 0.1986] |
| 0.0 | 0.7 | 10 | Circular | 0 | 0.4390 | [0.0000, 0.0876] |
| 0.7 | 0.0 | 10 | Noncircular | 0 | 0.5613 | [0.0000, 0.0876] |
| 0.7 | 0.0 | 10 | Circular | 0 | 0.5635 | [0.0000, 0.0876] |
| 0.7 | 0.7 | 5 | Noncircular | 12 | 0.2622 | [0.1807, 0.4543] |
| 0.7 | 0.7 | 5 | Circular | 12 | 0.2588 | [0.1807, 0.4543] |
| 0.7 | 0.7 | 10 | Noncircular | 4 | 0.3298 | [0.0396, 0.2305] |
| 0.7 | 0.7 | 10 | Circular | 8 | 0.3207 | [0.1050, 0.3476] |
| 0.7 | 0.7 | 20 | Noncircular | 1 | 0.3980 | [0.0044, 0.1288] |
| 0.7 | 0.7 | 20 | Circular | 0 | 0.3837 | [0.0000, 0.0876] |
| 0.9 | 0.7 | 10 | Noncircular | 8 | 0.2760 | [0.1050, 0.3476] |
| 0.9 | 0.7 | 10 | Circular | 9 | 0.2718 | [0.1232, 0.3750] |

For a **single prespecified** configuration with independent Monte Carlo panels and true rejection probability 0.05, the exact probability of at least 12 rejections in 40 is **3.652669919e-7**. This is an illustrative calibration benchmark, **not** a valid post-selection p-value for the worst cell across the 12 tested cells; shared seeds, multiple configurations, and finite 99-draw p-value resolution matter. The 5-date block is strongly inconsistent with nominal size in this simulated setting. The intervals are wide enough that the relative performance of 10- and 20-date blocks cannot be ranked confidently.

**Audit boundary:** Exact reproduction confirms published numerical output but does not independently validate the statistical bootstrap construction or the underlying empirical data. No archived ZIP was available or imported. No authentic SEC panel, treatment assignment, source manifest, September pretrend, October placebo, security/exchange weighting, or empirical inference was newly verified in this phase. The October 2025 placebo and September pretrends remain central identification warnings. No causal claim is warranted.

**Next priority:** Authenticate and recover the original panel and Nasdaq classification evidence, audit group/date keys and missingness by exchange, and rerun actual pretrend/placebo/weighting analyses; do not rely on nominal p-values from an uncalibrated bootstrap.
