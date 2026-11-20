# Phase 499 — Treatment-stratified eligibility exclusion audit

Date: 2026-11-20. Status: methodological diagnostic; **not an empirical SEC result**.

## Purpose
Phase 498 reports one-sided exclusions by exchange but does not separate the provisional treated and control cohorts. If coverage or exclusions differ between those groups, restricting the sample to two-sided observed units may change the composition of a matched comparison. Phase 499 adds a descriptive audit by exchange and treatment label (0=control, 1=treated). It reports eligible and observed row counts, two-sided and one-sided eligible units, and missing rows in each category. The unit is a security-exchange pair; an eligible row is a security-exchange-date triple. Dates equal to cutoff belong to the post side.

## Verification and limitations
Six constructed-fixture regression tests passed locally with pytest (6 passed, 0 failed, 0.05 seconds) before publication. They exercise stratification, missing one-sided rows, entirely absent observations, duplicate keys, observations outside the eligibility universe, invalid treatment labels and noncanonical cutoff. No historical SEC records were loaded. The test suite is not proof of treatment authenticity, and the exact remote checkout has not been rerun. The auditor validates keys and treatment labels but does not authenticate SEC source files, exchange mappings, round-lot assignments, matching design, serial dependence, or source licensing.

A constructed fixture has treated eligible coverage 2/3, control eligible coverage 2/2, and one missing treated one-sided row. These are *synthetic counts*, not estimates. An observed zero outcome is conceptually different from an absent observation; this diagnostic accepts observation keys only and does not validate outcome values. Inference must not be performed from these counts.

## Outstanding publication gates
November 14, 2026 target missed. Manuscript is not publication-certified. The substantial October placebo warning and September pretrends remain unresolved; treatment assignments, SEC historical inputs, selection/weighting sensitivity, and matched-group common-date plus serial-dependence-aware inference need independent validation. Historical Phase 430/436 archives and Phase 472 artifacts remain unimported pending access, licensing, and integrity verification.

## Next
Authenticate historical SEC files and eligibility dates; run Phases 496, 498 and 499 on September and October separately; compare excluded and missing counts by treatment, exchange and date; only then rerun placebo estimates with common-date and clustered/block-resampling inference.
