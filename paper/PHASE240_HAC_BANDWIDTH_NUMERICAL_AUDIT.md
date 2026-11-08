# Phase 240 — HAC bandwidth edge-case numerical audit (2026-11-08)

## Scope and source review
Reviewed the published `scripts/phase224_common_date_hac.py`, `scripts/phase238_hac_bandwidth_sensitivity.py`, and `tests/test_phase238_hac_bandwidth_sensitivity.py` on the repository default branch. This is an **independent arithmetic replication** of the published HAC formula, not execution of the repository's original test suite, and not SEC market-data analysis.

## Reproducible synthetic experiment
The six synthetic daily contrasts are `[0.1, 0.2, 0.3, 0.4, 0.5, 0.6]`, with the first three assigned to the early window and the final three to the late window. Both outcome keys in the published test fixture use the same values. The early mean is 0.2, the late mean is 0.5, and the late-minus-early contrast is 0.3. Define within-window demeaned residuals `u_t`; define signed scores `s_t=-u_t/3` in the early window and `s_t=u_t/3` in the late window. For Bartlett bandwidth `L`, the published estimator computes

`V_L = sum_t s_t^2 + 2 sum_{l=1}^L (1-l/(L+1)) sum_{t=l+1}^6 s_t s_{t-l}`

and `SE_L=sqrt(max(0,V_L))`. An independent Python 3 calculation using this exact expression returned:

| L | HAC variance | HAC standard error |
|---|---:|---:|
| 0 | 0.004444444444444444 | 0.06666666666666667 |
| 1 | 0.005555555555555555 | 0.07453559924999298 |
| 2 | 0.004444444444444444 | 0.06666666666666667 |
| 3 | 0.0027777777777777775 | 0.05270462766947299 |
| 4 | 0.0017777777777777779 | 0.04216370213557839 |
| 5 | 0.0014814814814814812 | 0.03849001794597505 |

The point estimate does not depend on bandwidth. The estimated uncertainty is not monotonic in bandwidth: the largest standard error in this fixture occurs at L=1, while L=5 gives a much smaller value. Therefore **choosing a bandwidth to minimize the standard error would be indefensible**. Bandwidths should be prespecified or justified by an independent selection rule, and sensitivity reported across a credible range. With only six observations, asymptotic HAC-based significance is particularly unreliable.

## Exact reproduction
```python
from math import sqrt
v = [.1, .2, .3, .4, .5, .6]
r = [x - sum(v[:3])/3 for x in v[:3]] + [x - sum(v[3:])/3 for x in v[3:]]
s = [-x/3 for x in r[:3]] + [x/3 for x in r[3:]]
for L in range(6):
    V = sum(x*x for x in s)
    V += sum(2*(1-l/(L+1))*sum(s[t]*s[t-l] for t in range(l,6))
             for l in range(1,L+1))
    print(L, repr(V), repr(sqrt(max(0,V))))
```

## Identification and provenance limitations
This is a **synthetic numerical audit** only. It does not independently authenticate SEC observations, historical round-lot treatment, exchange-session calendars, matched securities, or data redistribution rights. It does not resolve September 2025 pretrends, the substantial October 2025 placebo warning, selection/weighting sensitivity, security clustering, or common-date dependence in actual historical data. No causal effect has been established. The original repository tests were not executed in this session. Previously recovered historical ZIP archives were not available for verified import; their file-level inventory remains incomplete.

## Next action
Run the exact published test suite with real repository dependencies, authenticate source files and treatment rosters, then compare fixed-roster pretrends and October placebo dates under date HAC and security-cluster-aware inference. Preserve all earlier results and avoid publishing unsupported significance claims.
