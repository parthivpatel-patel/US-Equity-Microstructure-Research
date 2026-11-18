# Phase 457 — Cross-exchange treatment consistency audit

**Date:** 2026-11-18. **Status:** software-only validation; not historical inference.

The Phase 456 local-versus-globally-balanced estimator enforces treatment and matched-group assignment stability within each security/exchange but does not check whether a security is assigned conflicting treatment status across exchanges. Phase 451 does check global treatment consistency. The new Phase 457 audit independently identifies these contradictions, within-exchange matched-group or treatment changes, single-arm matched-group/period cells, and securities absent from either side of the November 3, 2025 boundary. It rejects duplicate security/exchange/date keys and non-Boolean treatment indicators.

Run from the repository root:

```bash
python -m unittest tests.test_phase457_assignment_audit -v
```

The diagnostic flags conflicts rather than silently discarding or reassigning observations. A security absent from one period is an attrition warning, not proof of incorrect treatment. A group-period with one arm cannot identify a contemporaneous treated-minus-control contrast. These checks do not prove that historical round-lot assignments match exchange source records; an independent source-specific treatment authentication manifest remains required.

**Validation:** Eight deterministic tests were run locally against a functionally identical copy of the audit (8 passed). The exact GitHub checkout and repository-wide regression suite were not run in this session. No historical SEC data were analyzed, no empirical effect or confidence interval was calculated, and no causal identification is claimed.

**Outstanding:** Authenticate original SEC observations, historical round-lot changes, exchange trading sessions and recovered research archives; quantify September pretrends and the substantial October placebo, compare weighting/selection specifications, and execute serial-block bootstrap robustness on authenticated data. The November 14, 2026 publication target was missed; manuscript not publication-certified.
