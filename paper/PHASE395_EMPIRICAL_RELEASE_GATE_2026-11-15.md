# Phase 395 — Evidence-based empirical release gate (2026-11-15)

## Status and scope

This is a **research-integrity and publication-decision note**, not a new empirical estimate. The November 14, 2026 target was missed. The proposed November 30 date is a planning target, not a validated completion forecast. The repository contains methodological diagnostics through Phase 394; those fixture tests must not be mistaken for analysis of authenticated market observations.

## Non-negotiable release criteria

1. **Source provenance:** identify each SEC dataset version, acquisition URL/date, raw-file SHA-256, observation schema, and any transformations. Confirm permissions before publishing source extracts. Keep restricted data out of the public repository.
2. **Treatment assignment:** establish the historical round-lot sizes on the November 3, 2025 implementation date with contemporaneous records or a fully documented price-based reconstruction; distinguish verified, inferred and unknown assignments. Report how estimates change when inferred/unknown securities are excluded.
3. **Population and matching:** freeze the eligible universe, affected/control roster, match covariates and preperiod, exchange coverage, exclusions, missingness, survivorship checks, and duplicate security-date-exchange handling. Audit balance and common support.
4. **Placebo validity:** recover original dated placebo estimates and their actual estimation-session rosters. Quantify overlapping windows, October 2025 placebo behavior, and sensitivity to the selection of placebo dates. Do not count overlapping windows as independent tests.
5. **Pretrends:** reproduce September 2025 trends using observed security-date-exchange outcomes and matched groups, with date-aligned uncertainty and diagnostics for changing composition.
6. **Estimands and inference:** explicitly distinguish hidden-execution trade-count and share-volume weighting. Report exchange and security composition sensitivity; matched-group estimates with common-date shocks and serial-dependence-aware uncertainty (e.g., two-way clustering and date-block/bootstrap sensitivity where supported). No one estimator alone certifies identification.
7. **Reproducibility:** execute the complete code/test suite against the published commit, regenerate all numerical tables/figures from authenticated input manifests, check hashes, and publish a rerun recipe without restricted raw data.
8. **Claims discipline:** if material October placebo effects, September pretrends or treatment ambiguity persist, frame the paper as a descriptive/identification-limit study, not a causal reform-effect estimate.

## Decision

**NOT READY FOR PUBLICATION CERTIFICATION.** The prior Phase 394 report explicitly states no original 78 dated placebo records or authenticated SEC observations were available for its analysis, and no historical ZIPs were imported. No verified evidence in this note resolves those deficits. A percentage-complete figure is not an empirical validation metric.

## Next reproducible task

Locate and inventory original historical research archives without extracting untrusted members; hash candidate archives; distinguish recoverable research-owned code, figures and reports from third-party licensed data. Only after provenance is established, rebuild the dated placebo panel and run the existing overlap, pretrend and dependence diagnostics on actual observations.

This file does not modify or certify prior empirical findings.
