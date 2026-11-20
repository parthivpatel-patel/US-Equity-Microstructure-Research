# Phase 492: dependency-injected composition audit

## Scope and finding

Phase 491 temporarily overwrote `phase488_period_composition.read` at module scope. That is unsafe under concurrent or nested calls and makes dependency behavior implicit. Phase 492 implements the same coverage and unit-composition summary with a reader explicitly passed to `audit(..., reader=...)`. The default is Phase 490's strict CSV reader. It does not modify global module state, and existing Phase 488/490/491 scripts are preserved.

The summary reports eligible versus observed security-exchange-date cells, missing eligible cells, explicitly observed zero outcomes, exchange-level missingness, and pre/post eligible versus observed security-exchange membership. A unit present on both sides is not necessarily a balanced panel. SHA-256 verifies bytes, not SEC authenticity.

## Validation

Five deterministic tests passed in a local reconstruction on 2026-11-19: zero/missing separation, pre/post unit composition, invalid cutoff, malformed extra CSV field, explicit reader injection, and out-of-eligibility rejection (the first test covers multiple assertions). The local code used a copy of the published Phase 490 strict reader. The exact final GitHub checkout was not executed, so do not claim checkout-level certification. Fixture values are synthetic and not empirical findings.

## Reproduction

From repository root: `python -m pytest -q tests/test_phase492_injected_composition.py`. Import `audit` from `scripts/phase492_injected_composition.py` after adding scripts to PYTHONPATH. Inputs require eligibility CSV columns security,exchange,date and panel CSV columns security,exchange,date,outcome. Dates are ISO canonical, and the cutoff must have eligible dates on each side.

## Research admission gate

No historical SEC panel, eligibility universe, or round-lot treatment file was authenticated or analyzed in this phase. The substantial October 2025 placebo warning and September pretrends remain unresolved. Treatment classification, matching, selection, weighting, exchange/security controls, common-date shocks, and serial-dependence-aware inference remain unverified. No causal conclusion is warranted.

The November 14, 2026 target was missed; the paper is not publication-certified. Phase 430/436 archives and Phase 472 artifacts remain unimported pending access, provenance, licensing, and size review.

## Next

Execute the exact published checkout, establish authenticated source panel and date-specific eligibility with licensing records, and only then apply this audit to September and October 2025 and the reform cutoff.
