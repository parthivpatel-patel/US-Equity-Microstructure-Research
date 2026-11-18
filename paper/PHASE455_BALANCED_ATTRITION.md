# Phase 455: balanced-panel support attrition audit

The Phase 451 estimator intersects complete treated/control exchange–matched-group dates across *all* strata. This creates an additional selection channel: a date with valid local comparisons in one stratum is discarded if any other stratum lacks a complete comparison. Phase 455 measures the size of this restriction separately before and after November 3, 2025.

The diagnostic reports observed, locally paired and globally retained stratum-date cells, plus retention fractions. Its denominator includes observed stratum-date cells, even those missing one arm; it is **not** a fraction of all theoretically possible security/date observations. A zero retention fraction is meaningful; a missing denominator returns null. The diagnostic validates unique security–exchange–date keys and stable security–exchange matching/treatment assignments. It does not certify security-level source provenance, exchange calendar authority, or treatment origin.

Run: `python -m unittest tests.test_phase455_support_attrition` from the repository root (assuming namespace-package imports are supported). The eight regression tests use constructed observations, not historical SEC observations. Local verification before publication: 8/8 tests passed using the same audit logic, with the test import adjusted for the standalone local module.

**Interpretation:** If post-period global retention is materially lower than pre-period retention, a balanced estimator may change the target population. Report this alongside locally paired sensitivity estimates and pretrend/placebo checks; do not treat balanced support as identification.

**Open gates:** authenticated SEC source files and historical round-lot treatment; September pretrends; October placebo; weighting and selection sensitivity; serial dependence; full-repository test execution; recovered historical ZIP inventory/import. No empirical effect estimate or causal conclusion is supplied.
