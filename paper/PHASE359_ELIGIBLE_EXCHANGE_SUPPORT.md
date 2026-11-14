# Phase 359 — Explicit eligible-exchange support sensitivity (2026-11-14)

## Scope
Read Phase 357 coverage and Phase 358 complete-exchange aggregation before this addition. This is an opt-in descriptive sensitivity, not a replacement for authenticated eligibility or source-data checks.

## New validation
The script compares strict complete-universe aggregation with aggregation over a caller-declared security-date-specific eligible exchange set. Every exchange cell must still be present. An exchange excluded by policy must be explicitly marked exchange_not_applicable; an eligible exchange so marked fails closed. Missing source data, not-listed and nontrading statuses for eligible exchanges exclude the security-date from aggregation rather than becoming zeros. Observed zero is valid. fsum reduces floating-point accumulation error, with nonfinite totals rejected.

The returned policy_authenticated=False is deliberate: a caller's policy declaration is **not evidence** of historical exchange applicability. A narrower policy can increase complete-case support and change the estimand; comparing raw aggregates alone does not solve selection bias.

## Verification and limitations
Ten constructed-input deterministic tests passed locally on 2026-11-14, covering eligible observed zero, strict support, missing eligible data, missing grid cells, contradictory exclusions, duplicates, nonfinite values, order invariance and required policy. No SEC panel data or historical source ZIP was available for authentication. Full published-checkout and full-suite tests remain pending. The script is a software validation tool, not empirical evidence or a causal estimator.

## Publication and provenance
The November 14 publication deadline is not met. September pretrends, substantial October placebo, the original 78 dated placebo observations, Phase 130 contradiction, treatment authentication, source provenance, weighting and serial-dependence calibration remain unresolved. No historical archives were imported; archive inventory is incomplete.

## Next
Obtain source-hashed raw SEC observations and historical security/exchange eligibility evidence; compare complete-universe and eligible-exchange support with counts by month, cohort and exchange; reconstruct dated placebo tests and matched-group/common-date/serial inference. No causal conclusion is justified.
