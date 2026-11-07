# Phase 221: Cross-window covariance adversarial check

Date: 2026-11-07. Scope: independent U.S. equity round-lot reform research.

## Reproducible calculation

A constructed ten-observation sequence [1,3,2,4,5,7,6,8,9,11] is split into five early and five late observations. Early mean = 3; late mean = 8.2; contrast = 5.2. The score for each early observation is -(y-3)/5, and for each late observation is (y-8.2)/5. The Bartlett-weighted variance is the sum of score products for all pairs within the selected lag bandwidth.

| Bandwidth | Full-sequence HAC variance | Artificially block-separated variance |
|---|---:|---:|
| 0 | 0.992000 | 0.992000 |
| 1 | 1.334400 | 1.238400 |
| 3 | 1.492000 | 1.096000 |
| 5 | 1.029333 | 0.730667 |

The block-separated comparator deliberately omits cross-window score products. It is **not** a recommended estimator. Here the omission understates variance; in other datasets it may overstate variance. The test establishes a nonzero cross-window term and detects implementations that inadvertently suppress it.

Run: `python -m unittest tests/test_phase221_cross_window_covariance.py` (or `python tests/test_phase221_cross_window_covariance.py`).

## Interpretation and boundaries

This is deterministic mathematical software verification using synthetic inputs, not historical SEC observations. The Phase 213 source was read from the existing public repository before this addition. The test is standalone and does not prove the published Phase 213 or Phase 216 implementations pass clean-checkout tests. Historical calendars, source extracts, treatment classifications, fixed rosters, September pretrends, and the substantial October placebo remain unauthenticated or unresolved. A valid sandwich covariance is not evidence of causal identification.

## Archive and publication status

No previously recovered ZIPs or papers were available for verified inspection or licensed import in this session. Their contents and redistribution rights are not asserted. No historical data, empirical chart, or manuscript-ready causal coefficient was added. Next: clean-checkout test of the exact published modules, authenticated calendar and SEC source inventory, fixed-roster September/October placebo sensitivity.
