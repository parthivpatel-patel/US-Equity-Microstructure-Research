# Phase 386 — Balanced matched-pair/date two-way CR0 variance diagnostic

Date: 2026-11-15. **Methodology-only: no authenticated SEC observations processed.**

## Objective and exact calculation

For a complete rectangular panel of matched-pair by common-trading-date gaps, calculate the grand mean and a Cameron–Gelbach–Miller-style two-way inclusion-exclusion **CR0** variance: pair-cluster score squares plus date-cluster score squares minus individual-cell score squares, all divided by the squared observation count. Scores are residuals around the grand mean. Exact rational arithmetic avoids floating-point cancellation. Every pair-date combination must occur exactly once, with at least two pairs and two dates. Missing or duplicate cells are rejected rather than silently filled.

The routine returns all three variance components, sample dimensions and a negative-variance flag. **Negative two-way CR0 variances are possible**: the test fixture with gaps [0,2;2,0] produces -1/4. Such a result is not a valid standard error and must not be silently clipped to zero. Another fixture with pair-specific gaps [0,0;2,2] yields pair component 1/2, date component 0, intersection 1/4 and total 1/4. These are constructed fixtures, not market results.

## Verification and execution

Nine deterministic tests passed locally on 2026-11-15, covering constant panels, pair/date effects, negative variance, duplicates, unbalanced panels, invalid gap types, single-pair rejection and input-order invariance. From repository root: `PYTHONPATH=scripts python -m unittest discover -s tests -p 'test_phase386_two_way_cluster.py'`. The locally executed source was copied verbatim into the GitHub publication operation; the published checkout and full suite still require independent execution.

## Interpretation limits and outstanding empirical gates

CR0 is a diagnostic, not an automatically valid confidence interval. It has no small-cluster correction, wild bootstrap, degrees-of-freedom rule or serial-dependence adjustment beyond same-date clustering. Serially correlated common shocks across adjacent dates remain a concern; matched pairs may also be dependent through shared controls or economic exposures. Balance-based selection and unequal activity weighting can change the estimand. Do not infer a reform effect or claim a causal interpretation.

The original 78 dated placebo comparisons, September pretrends, substantial October 2025 placebo warning, historical treatment authentication and raw SEC/Nasdaq source hashes remain unresolved. No historical ZIP was imported. The repository's `provenance/ARCHIVE_STATUS.md` records 129 historical ZIPs totaling 1,158,462,147 bytes in an earlier local workspace audit, **not** verified as accessible or redistributable in this session. The November 14, 2026 paper deadline was missed; manuscript remains uncertified.

Next: authenticate source data and roster, measure actual balanced-panel attrition, then compare pair/date CR0 diagnostics with serial-dependence-aware alternatives and pretrend/placebo estimates. Preserve source licensing restrictions.
