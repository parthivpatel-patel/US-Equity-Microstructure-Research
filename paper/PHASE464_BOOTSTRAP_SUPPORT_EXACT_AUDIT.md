# Phase 464 — Exact support-selection audit of the Phase 462 bootstrap (2026-11-18)

## Scope and provenance

This is an analytical audit of the published `scripts/phase462_joint_placebo_bootstrap.py`, fetched from the public repository on 2026-11-18 (blob SHA `71b6d4013e9b79562f4dbe5fa35b47180c0bac0d`). It is **not** an estimate from SEC observations. The original code is preserved unchanged.

## Verifiable exact enumeration

The published algorithm samples contiguous blocks of indices of fixed length `L` from an ordered list of `n` sessions. Each start is uniform on `0,...,n-L`; it concatenates blocks until reaching `n` sampled indices, truncates excess indices, and discards a replicate if *any* placebo cutoff has no sampled observations on either side.

Take six sessions indexed `0,1,2,3,4,5`, block length `L=3`, and a cutoff immediately before index `3`. Exactly two length-three blocks are drawn. There are four possible block starts, each with probability `1/4`:

| Start | Sampled indices | Support |
|---|---|---|
| 0 | 0,1,2 | pre only |
| 1 | 1,2,3 | both |
| 2 | 2,3,4 | both |
| 3 | 3,4,5 | post only |

There are `4^2=16` equally likely ordered pairs of starts. A draw lacks post support only for `(0,0)`; it lacks pre support only for `(3,3)`. Thus **14/16 = 87.5%** of draws are eligible for this cutoff, and **2/16 = 12.5%** are discarded.

Now place the cutoff immediately before index `1`, so only index 0 is pre. Only blocks beginning at 0 contain that pre session. The probability of obtaining *no* pre support in either block is `(3/4)^2=9/16`. Therefore only **7/16 = 43.75%** of draws are eligible. These fractions follow directly from the published sampling algorithm; they are exact combinatorial results, not Monte Carlo results.

For the **joint** cutoffs immediately before indices 1 and 3, eligibility requires at least one start 0 and at least one sampled post-index-3 session. Given a start 0, the other start must be 1, 2, or 3 (a second 0 has no post-index-3 session). The valid ordered pairs are `(0,1),(0,2),(0,3),(1,0),(2,0),(3,0)`, hence **6/16 = 37.5%** complete joint draws. This illustrates that adding a cutoff changes the conditional resampling distribution for *all* reported cutoffs.

## Implications

1. `complete_draws` is an essential diagnostic, but a high count alone does not guarantee valid inference. Conditioning on joint support can materially reweight bootstrap paths.
2. Cutoff proximity to the sample edges and the chosen block length directly determine support attrition. Report eligibility rates per cutoff and jointly, including under alternate block lengths.
3. Jointly eligible draws should be used consistently when estimating covariance, but their distribution is conditional on eligibility. A prespecified bootstrap design that maintains both sides of each cutoff is preferable for inferential work; its validity under serial dependence must be assessed separately.
4. Phase 462's percentile intervals remain exploratory. This exact audit does **not** validate null-centered p-values, confidence interval coverage, causal identification, or historical treatment assignment.
5. Group resampling by exchange–matched-group key does not automatically preserve security-level dependence across exchanges. The historical matching and security identifiers must be authenticated before claiming dependence-aware inference.

## Research status and next gate

November 14, 2026 publication target was missed. The paper is NOT publication-certified. Historical SEC source authentication, round-lot treatment authentication, September pretrends, the substantial October placebo warning, alternative weighting, serial dependence, and historical ZIP/Phase 430/436 recovery remain unresolved.

Next: add a deterministic support-eligibility test and per-cutoff/joint attrition diagnostics to the bootstrap implementation, run repository-wide tests, then evaluate a prespecified support-preserving dependent bootstrap using authenticated historical data. No synthetic numbers in this report should be presented as empirical reform findings.
