# Phase 265: Exact bounded-weight sensitivity

**Status:** Deterministic methodology validation only. No authenticated SEC observations, exchange calendars, or treatment classifications were analyzed.

For fixed matched-pair post-minus-pre contrasts \(d_i\), examine \(\sum_i w_i d_i\) with \(\sum_i w_i=1\) and \(l\leq w_i\leq u\). The feasible region is a capped simplex. Because the objective is linear, the exact extrema are obtained by assigning baseline weight \(l\) to each pair and distributing remaining mass, up to \(u-l\) per pair, in ascending order for the minimum and descending order for the maximum. This is a descriptive **weighting robustness envelope**, not a confidence interval.

Synthetic illustration: pair contrasts [-2, 1, 4], lower weight 0.2, upper weight 0.5. Equal weighting yields 1.0; exact admissible minimum is 0.1 (weights [0.5, 0.3, 0.2]) and maximum is 1.9 (weights [0.2, 0.3, 0.5]). Unrestricted nonnegative weights permit [-2, 4]. These values are **not historical reform estimates**.

Local algorithm-equivalent implementation passed eight deterministic tests. The published source and tests should be rerun from a clean checkout; no complete-repository test claim is made.

**Identification limits:** A sign-stable envelope is not evidence of causal identification. The substantial October 2025 placebo warning, September pretrends, source authentication, roster authentication, security/exchange confounding, common-date shocks, and serial dependence remain unresolved. The bounds do not account for changing pair membership or missing observations. Weights must be prespecified rather than selected to manufacture significance.

**Historical application gate:** Independently verify SEC file provenance and hashes, round-lot treatment classifications, exchange calendar, fixed matched roster, outcome definitions, and permissible redistribution before supplying historical pair contrasts. Report weight caps, full envelope, placebo envelope, and pretrend envelope side by side. Do not report historical p-values from this method.

**Outstanding import inventory:** Previously recovered historical ZIPs and earlier unpublished Phase 252–254 implementations have not been authenticated or imported in this session; their full file-level inventory remains unavailable. No licensed raw data or unverified figures were published.
