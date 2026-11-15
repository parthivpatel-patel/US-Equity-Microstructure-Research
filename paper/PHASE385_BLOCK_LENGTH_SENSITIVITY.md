# Phase 385 — Exact circular-block length sensitivity and degeneracy audit

Date: 2026-11-15. **Methodology-only; no authenticated SEC observations.**

## Motivation and finding

Phase 384 enumerates circular-block means for one common-date aggregate series. Phase 385 checks the sensitivity of its **resampling distribution** to block length, using exact rational arithmetic. For each length it records enumeration size, distinct means, minimum, maximum, exact variance of the resampled means and whether the distribution is degenerate. This is not a confidence interval or a null test.

A structural mathematical warning follows: when block length equals the number of dates, every circular rotation contains the same observations once. **All resampled means equal the observed mean and their variance is zero**, even if the underlying date series varies. This degeneracy is an artifact of the resampling design and must never be interpreted as perfect certainty. Conversely, length one resamples dates independently and does not preserve serial dependence.

## Verification

Nine deterministic tests passed locally on constructed examples. For date series [0,2], length one yields mean variance 1/2 and three distinct resampled means; length two yields zero variance and one distinct mean. For [0,1,2] and length three, three rotations all yield mean one. These are **constructed mathematical fixtures, not market observations**.

From repository root: `python -m unittest discover -s tests -p 'test_phase385_block_length_sensitivity.py'`. The test imports the **published Phase 384 implementation** rather than substituting an alternative bootstrap. The Phase 385 function accepts the Phase 384 enumerator explicitly for reproducibility.

## Inference and provenance limits

- No source-authenticated SEC security-date-exchange panel was processed, and no historical research ZIP was imported. No new empirical statistic or causal estimate is reported.
- These exact finite-sample distributions do not by themselves validate percentile intervals, hypothesis tests, null centering, or stationary-block assumptions.
- Common-date aggregation does not establish matched-pair cluster inference, exchange-control identification or joint pair/date dependence.
- September pretrends and the substantial October 2025 placebo warning remain unresolved. The original 78 dated placebo estimates, treatment assignment, panel roster and data licensing/provenance require verification.
- The November 14, 2026 publication target was missed. The manuscript remains uncertified.

## Next verification gate

Locate and authenticate historical panel, dated placebo records and historical ZIP inventory. Then calculate actual sample attrition, pretrend/placebo estimates and block-length sensitivity alongside matched-pair/date dependence checks. Do not present causal effects without identification and falsification evidence.
