# Phase 467 — Support-preserving resampling: exact eligibility versus distortion

Date: 2026-11-18. Scope: methodological audit only. **No SEC observations or causal estimates were analyzed.**

## Question

Phase 462's moving-block bootstrap rejects draws without pre/post observations for every placebo cutoff. Can forced endpoint support eliminate these rejections without changing the estimand or the resampling distribution?

## Reproducible exact experiment

Use six ordered abstract sessions indexed 0,...,5, block length 3, and cutoffs at indices 1 and 3 (a sampled index is post-cutoff when >= cutoff). The original Phase 462 design samples two independent contiguous length-three blocks, each with uniformly selected starts in {0,1,2,3}, and concatenates the blocks. There are 4^2=16 equiprobable ordered paths.

A competing *anchored* design fixes index 0 as the first sampled session and index 5 as the last sampled session, and fills the four interior positions using two independent contiguous length-two blocks, each starting uniformly in {0,1,2,3,4}. There are 5^2=25 equiprobable ordered paths. This is **not** the same moving-block bootstrap and is not endorsed as a calibrated inferential procedure.

| Diagnostic | Original length-3 moving blocks | Endpoint-anchored interior length-2 blocks |
|---|---:|---:|
| Possible ordered paths | 16 | 25 |
| Eligible at cutoff 1 | 7/16 = 43.75% | 25/25 = 100% |
| Eligible at cutoff 3 | 14/16 = 87.5% | 25/25 = 100% |
| Eligible jointly | 6/16 = 37.5% | 25/25 = 100% |
| Endpoint index 0 included in every draw | No | Yes |
| Endpoint index 5 included in every draw | No | Yes |

The original joint count is also documented by Phase 465; the anchored counts follow by construction because every anchored draw contains indices 0 and 5.

Exact reproduction with Python standard library:

```python
from itertools import product

n = 6
original = [tuple(j for s in starts for j in range(s, s + 3))[:n]
            for starts in product(range(4), repeat=2)]
anchored = [(0,) + tuple(j for s in starts for j in range(s, s + 2))[:4] + (5,)
            for starts in product(range(5), repeat=2)]

def eligible(path, cutoff):
    return any(j < cutoff for j in path) and any(j >= cutoff for j in path)

for label, paths in [('original', original), ('anchored', anchored)]:
    assert len(paths) == (16 if label == 'original' else 25)
    print(label, len(paths),
          sum(eligible(p, 1) for p in paths),
          sum(eligible(p, 3) for p in paths),
          sum(all(eligible(p, c) for c in (1, 3)) for p in paths))
# original 16 7 14 6
# anchored 25 25 25 25
```

## Interpretation

**Eliminating support rejection is not equivalent to improving statistical validity.** The anchored construction assigns probability one to inclusion of both endpoints, changes block length, destroys the original draw law, and may underrepresent serial dependence or overemphasize endpoint shocks. Conditioning the original bootstrap on eligibility also changes its sampling law. Neither method by itself yields calibrated placebo p-values, simultaneous confidence sets, or causal interpretation.

A better next-stage comparison should (i) define an explicit target estimand and null, (ii) preserve the same matched-group and common-date resampling indices across all cutoffs, (iii) retain cross-exchange dependence where securities recur across exchanges, (iv) report per-cutoff and joint support attrition, (v) simulate size and coverage under serially correlated null data and under pretrends, and (vi) only then apply to authenticated SEC observations.

## Outstanding empirical gates

The historical October placebo warning and September pretrends remain unresolved. SEC source hashes and licensing, November 2025 round-lot treatment authentication, matched-group composition, weighting sensitivity, security/exchange dependence, and recovery of historical Phase 430/436 archives remain open. The November 14, 2026 target was missed; the paper is not publication-certified.

No third-party data, charts, or archive material are included in this report.
