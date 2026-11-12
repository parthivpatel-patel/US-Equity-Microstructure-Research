# Phase 320 — Extrema sharpen the published placebo right-tail bounds (2026-11-12)

## Inputs and provenance
Read `results/phase130_summary.csv` and the Phase 318–319 reports and script from the existing public repository through the connected GitHub integration. These are frozen **aggregate summaries**, not authenticated SEC observations. The reported minima and maxima must refer to the same 78 placebo contrasts as the reported tail counts; this assumption has not been independently verified from raw placebo windows.

Define `L = # {x <= d}`, `A = # {|x| >= |d|}`, `R = # {x >= d}`. The previously published unconditional bounds used only L and A. The observed extrema supply additional logical constraints even **without** a no-ties assumption.

| Outcome | d (percentage points) | L | A | Observed minimum | Observed maximum | Previous unconditional R | Extrema-informed R |
|---|---:|---:|---:|---:|---:|---:|---:|
| Count | -0.7346606598677254 | 2 | 2 | -1.4475738789418606 | +1.0538523294152946 | 76–78 | **76–77** |
| Volume | +0.626597999820323 | 48 | 76 | -1.8665501312689659 | +1.4840122108986915 | 28–76 | **28–75** |

For **count**, d < 0, so `R = n - L + # {x == d}`. Because the observed minimum is strictly below d, at least one of the two lower-tail observations is not tied at d. Therefore `# {x == d} <= L - 1`, and `R <= 77`. The lower bound remains 76.

For **volume**, d > 0. Partition the absolute-extreme observations into `N = # {x <= -d}` and `R = # {x >= d}`, so `A = N + R`. The reported minimum is below `-d`, guaranteeing `N >= 1` and therefore `R <= 75`. Because `N <= L`, `R >= A - L = 28`.

These are conservative **logical** bounds. They are not sampling confidence intervals, calibrated p-values, causal effects, or proof that the underlying reported extrema and counts were computed correctly. The Phase 319 conditional no-ties bound for volume (28–30) remains explicitly conditional and should not replace the unconditional 28–75.

## Validation and next gate
The accompanying script was run locally against the two frozen rows and produced count 76–77 and volume 28–75. Tests provide synthetic checks; they do not verify source-data authentication. Reproduce with `python -m unittest tests.test_phase320_extrema_bounds`.

Before publication: recover the 78 underlying placebo-window values; independently recompute L, A, extrema, ties and directional tails; verify window dates and October 2025 announcement contamination; authenticate treatment labels and source records; assess September pretrends, matched security/exchange controls, selection and weighting sensitivity, common-date dependence and serial correlation. Historical ZIP inventory and redistribution permissions remain unresolved. The November 14 manuscript target remains conditional.
