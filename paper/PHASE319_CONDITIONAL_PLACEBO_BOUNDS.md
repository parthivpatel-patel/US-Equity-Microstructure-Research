# Phase 319 — Conditional tightening of placebo right-tail bounds (2026-11-12)

## Source and distinction

Read the public `results/phase130_summary.csv` and Phase 318 analysis using the connected GitHub integration. Define `L = #{x <= d}`, `A = #{|x| >= |d|}`, and `R = #{x >= d}`. The prior conservative result for the positive volume contrast (`d=+0.626597999820323` percentage points, `n=78, L=48, A=76`) was `28 <= R <= 76`.

If **no placebo value equals the positive threshold d**, then the lower and right tails are disjoint. The negative extreme observations are a subset of L and the positive extreme observations are exactly R, hence `A = N + R`, `N <= L`, and `R <= n-L`. Therefore `max(0,A-L) <= R <= min(A,n-L)`: for volume, **28 to 30**.

This is **conditional on no exact ties**, not an unconditional correction. The underlying 78 placebo-window observations were not available to verify ties. Without that verification, retain the previously published **28 to 76** conservative bound. For the negative count contrast, the prior 76-to-78 conservative bound remains. The accompanying script defaults to the unconditional result and only tightens when `no_ties=True` is explicitly supplied.

Nine deterministic unit tests passed locally for the logic and published aggregate inputs; they do not authenticate the SEC panel or establish the no-ties condition. These overlapping, post-hoc placebo counts are not calibrated p-values. The October announcement warning, September pretrends, treatment assignment, selection and weighting, security/exchange effects, and serial/common-date dependence remain unresolved. Historical ZIP archives remain unreconciled. The November 14 publication target remains conditional.

Reproduce: `python -m unittest discover -s tests -p 'test_phase319_placebo_sharp_bounds.py'`.
