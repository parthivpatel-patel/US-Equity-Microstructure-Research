# Phase 302 — Exact block-boundary sensitivity audit

Date: 2026-11-10 (US Eastern). Status: synthetic methodology audit; **not an empirical SEC result**.

## Reproducible calculation

An exact enumeration uses four synthetic date-level contrasts `[0, 0, 0, 12]` and blocks of length two. The circular procedure admits four starting positions, including a block that wraps from the final date to the first; the non-circular procedure admits three starts. Two independently selected blocks form each length-four draw.

| Resampler | Exact ordered draws | Mean of bootstrap means | 2.5th order statistic | 97.5th order statistic |
|---|---:|---:|---:|---:|
| Non-circular | 9 | 2 | 0 | 3 |
| Circular | 16 | 3 | 0 | 6 |

The percentile positions follow the existing Phase 289 integer-index convention. The tiny sample is intentionally illustrative, so these are not reliable confidence intervals. This example proves the two resampling choices can materially change the distribution even with identical input observations; it does **not** quantify sensitivity for the historical panel. The non-circular resampler itself is not asserted to be unbiased or preferable.

Run `python -m unittest tests.test_phase302_boundary_sensitivity -v` from the repository root. Four tests passed in a local isolated reproduction before publication. The published checkout has not been independently executed.

## Scope and identification limits

Phase 289 currently uses circular blocks on already aggregated date-level exchange contrasts. It does not resample matched securities, authenticate source dates, or adjust for security/exchange composition. Before interpreting historical intervals, compare block lengths and circular/non-circular resampling on a fixed authenticated matched roster, preserve common calendar dates, and report both estimand weighting and matched-group resampling sensitivity. The October 2025 placebo warning and September pretrends remain unresolved. Treatment assignment and source-data provenance remain unauthenticated. No causal effect is established.

Recovered ZIP archives and earlier paper/figure artifacts have not been authenticated or imported in this phase; no completeness claim is made. No licensed data, synthetic figure masquerading as research, or secrets are included.
