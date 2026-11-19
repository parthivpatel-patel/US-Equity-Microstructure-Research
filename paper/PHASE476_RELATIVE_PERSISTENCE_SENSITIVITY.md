# Phase 476 — Relative persistence of common-date and pair-specific shocks

Date: 2026-11-19. **Exact constructed-model analysis only; not SEC data or causal evidence.**

## Question and extension

Phase 475 assumed serially independent pair-specific residuals while allowing an AR(1) common-date factor. That can exaggerate *relative* common-factor standard-error inflation if the residual component is itself persistent. This phase explicitly allows separate AR(1) persistence parameters for the common factor and pair-specific residuals.

Let D[g,t] = a[g] + delta F[t] + u[g,t], with G independent matched pairs, stationary unit-variance F and independent across-pair stationary residual differences u with variance 2. Let rho_F and rho_u denote their respective AR(1) correlations. For balanced 40-session pre/post weights w (20 pre and 20 post),

Var(theta) = delta² Q(rho_F) + (2/G) Q(rho_u),

where Q(rho) = sum_t sum_s w[t] w[s] rho^abs(t-s). The benchmark comparison holds rho_u fixed and removes the common factor:

SE ratio = sqrt(1 + delta² G Q(rho_F) / (2 Q(rho_u))).

## Exact results

With G=68, delta=0.5, and unit stationary marginal variances, the calculated ratios are:

| Pair-specific rho_u | Common-date rho_F=0 | rho_F=0.5 | rho_F=0.8 |
|---:|---:|---:|---:|
| 0.0 | 3.082207 | 4.893874 | 7.238153 |
| 0.5 | 2.036700 | 3.082207 | 4.475897 |
| 0.8 | 1.551094 | 2.189956 | 3.082207 |

When both components share the same temporal correlation kernel, Q cancels in the *relative* variance ratio, which is exactly sqrt(1+delta² G/2) regardless of rho. This is a relative-ratio identity, **not** a claim that absolute uncertainty is unaffected by serial correlation: both absolute variance terms change with rho.

This refines the interpretation of Phase 475. Its large ratios at positive rho_F partly reflect the assumption rho_u=0, rather than a universal effect of serial correlation.

## Reproduce and validate

The following Python 3 code uses only the standard library and exhaustively sums the 40-by-40 covariance kernel. It asserts the equal-persistence identity and prints the nine ratios:

```python
from math import sqrt

T, G, delta = 40, 68, 0.5
w = [-1 / 20] * 20 + [1 / 20] * 20

def q(rho):
    assert -1 < rho < 1
    return sum(w[t] * w[s] * rho ** abs(t - s)
               for t in range(T) for s in range(T))

def ratio(rho_u, rho_f):
    return sqrt(1 + delta ** 2 * G * q(rho_f) / (2 * q(rho_u)))

for ru in (0, 0.5, 0.8):
    for rf in (0, 0.5, 0.8):
        print(f"rho_u={ru:.1f}, rho_F={rf:.1f}, ratio={ratio(ru, rf):.6f}")
    assert abs(ratio(ru, ru) - sqrt(1 + delta ** 2 * G / 2)) < 1e-12
assert abs(q(0) - 0.1) < 1e-12
```

The exact enumeration and equal-persistence identity were independently checked locally. No stochastic simulation, SEC dataset, or externally sourced research archive was used.

## Interpretation, provenance and publication gates

This model assumes balanced pairs, identical factor-loading differences, cross-pair residual independence, stationary AR(1) covariance, known variance parameters, and no selection effects. Real securities may share sector, exchange, liquidity, and calendar shocks that violate these assumptions. It does not resolve September pretrends, the substantial October placebo warning, treatment authentication, selection/weighting sensitivity, or source-data licensing and verification. The 68 pairs are a *constructed benchmark parameter*, not an authenticated treatment classification.

The November 14, 2026 publication deadline was missed; the manuscript remains **not publication-certified**. Previously recovered Phase 430/436 archives and Phase 472 standalone executable files remain unverified/unpublished in this phase. Next: authenticate original source observations and treatment mapping; estimate residual covariance and exposure heterogeneity; then compare multiway clustered and date-block inference with simultaneous placebo adjustment. Keep this study separate from GIG and all other projects.
