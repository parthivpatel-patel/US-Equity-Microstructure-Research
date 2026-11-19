# Phase 468 — Exact placebo-bootstrap contrast distortion audit

Date: 2026-11-18. **Constructed six-session data only; no SEC data or reform effects.**

## Design
Following the published Phase 467 paths, enumerate all 16 equally likely original moving-block paths (two length-three blocks, starts 0–3), and all 25 equally likely endpoint-anchored paths (endpoints 0 and 5 fixed; two interior length-two blocks, starts 0–4). Compute the post-minus-pre mean contrast at abstract cutoffs 1 and 3. For the original design average only over paths with both sides supported; for the anchored design all paths qualify. Compare each resampling mean with the full-panel contrast. This is a **finite-path expectation difference**, not a claim about statistical estimator bias or bootstrap coverage.

| Constructed outcome | Cutoff | Full panel | Original eligible paths | Original conditional mean | Anchored mean |
|---|---:|---:|---:|---:|---:|
| Linear 0,1,2,3,4,5 | 1 | 3.000000 | 7/16 | 2.271429 | 3.229333 |
| Linear 0,1,2,3,4,5 | 3 | 3.000000 | 14/16 | 2.038095 | 3.570667 |
| Step 0,0,0,1,1,1 | 1 | 0.600000 | 7/16 | 0.342857 | 0.641333 |
| Step 0,0,0,1,1,1 | 3 | 1.000000 | 14/16 | 1.000000 | 1.000000 |
| Endpoint 1,0,0,0,0,0 | 1 | -1.000000 | 7/16 | -1.000000 | -1.000000 |
| Endpoint 1,0,0,0,0,0 | 3 | -0.333333 | 14/16 | -0.111905 | -0.537333 |

The linear-trend case demonstrates that support-conditioned and anchored resampling expectations differ from each other **and** from the original contrast, despite every path using the same underlying six values. A step perfectly aligned with cutoff 3 is invariant, so distortion is not universal. Endpoint shocks behave differently by cutoff.

## Exact reproduction (Python standard library)
```python
from itertools import product
from statistics import mean
n = 6
original = [tuple(j for s in starts for j in range(s, s+3))[:n]
            for starts in product(range(4), repeat=2)]
anchored = [(0,) + tuple(j for s in starts for j in range(s, s+2))[:4] + (5,)
            for starts in product(range(5), repeat=2)]
assert len(original) == 16 and len(anchored) == 25
def contrast(path, cutoff, values):
    pre = [values[j] for j in path if j < cutoff]
    post = [values[j] for j in path if j >= cutoff]
    return mean(post)-mean(pre) if pre and post else None
for label, values in [('linear', list(range(6))),
                      ('step', [0,0,0,1,1,1]),
                      ('endpoint', [1,0,0,0,0,0])]:
    for cutoff in (1,3):
        observed = contrast(tuple(range(6)), cutoff, values)
        for design, paths in [('original', original), ('anchored', anchored)]:
            valid = [v for p in paths if (v := contrast(p, cutoff, values)) is not None]
            print(label, cutoff, design, observed, len(valid), len(paths), mean(valid))
```

## Interpretation and remaining gates
This exact example strengthens the warning against treating forced-support bootstrap designs as interchangeable or calibrated. It **does not** measure null rejection size, serial correlation, simultaneous coverage, or empirical effects. Next: Monte Carlo under serially dependent nulls, joint cutoff support, and matched-group/common-date dependence; then authenticated historical SEC panel and round-lot treatment validation. October placebo warning, September pretrends, selection/weighting sensitivity, cross-exchange security dependence, archive inventory and licensing remain unresolved. The November 14 deadline was missed; manuscript **not publication-certified**.
