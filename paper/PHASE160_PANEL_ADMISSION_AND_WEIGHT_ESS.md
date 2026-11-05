# Phase 160 — Security-panel admission and weighting concentration (2026-11-04)

## Source-level findings

Reviewed published `tests/phase158_security_panel_sensitivity.py` and `tests/test_phase159_snapshot_integrity.py` before this supplement. Phase 158 checks the recovered 2,262-row panel with Python `assert` statements and uses the minimum of pre/post trade counts as its WLS weight. It does not report the group-specific effective sample size (ESS) of these weights. Its outcome-tail trimming is based on the dependent variable, so it changes the analysis population based on realized outcomes. These are code-level findings, not newly computed empirical results.

## Executed verification

The Phase 160 standalone script validates unique ticker keys, strict binary treatment, finite rates in [0,1], positive finite trade counts, and consistency of reported pre/post changes. It calculates Kish group-specific ESS as `sum(w)**2/sum(w**2)` using Phase 158's `min(trades_pre,trades_post)` rule. Eight unittest cases passed locally using constructed fixtures. For two treated securities with weights 100 and 1, ESS is `10201/10001 = 1.019998...`, despite two observed treated securities. Thus group counts alone do not characterize weighting concentration.

## Limitations and next empirical checks

This is a synthetic-fixture code audit, not a fresh SEC estimate. The original archived Phase 2 panel was not available for execution in this session. No empirical ESS, treatment classification, September pretrend, October placebo, or common-date/serial-dependence-adjusted estimate was obtained. The Phase 2 pilot (68 treated / 2,194 comparisons) must not be mixed with the later 68/204 matched cohort. When authenticated daily inputs are recovered, calculate group-specific ESS for each specification, report excluded counts by treatment group, use prespecified weights, and run matched-group plus calendar-date and serial-dependence-aware inference.

## Inventory and provenance

Published original code and this report only; no licensed or unverified third-party data. Existing public source scripts were inspected before publication. The recovered private security panel and generating script, Nasdaq October/November snapshots, SEC daily archives, and previously inventoried historical ZIP collection were not imported. Source-data authentication and the substantial October placebo warning remain unresolved. The manuscript is not yet publication-ready, and no causal effect is established.
