# Phase 509 — Panel-to-coverage reconciliation (2026-11-20)

## Purpose
Cross-check security-date-exchange observed panel records against independently supplied exchange-date treated/control coverage totals before any September/October placebo analysis. This is an internal-consistency gate, **not source authentication**.

## Validation
Local deterministic unittest suite: 11/11 passed (constructed fixtures only). Tests include exact matches, count mismatches, unexpected panel cells, duplicate keys, roster conflicts, invalid dates, incorrect period labels, boolean counts, empty panel, and one-sided coverage.

## Interpretation
An exact reconciliation is necessary but insufficient for historical empirical inference. Coverage eligibility counts are not inferred from observed rows. Independently authenticated SEC source extracts, roster effective dates, trading calendars, and treatment definitions remain required. The substantial October placebo and September pretrends remain unresolved; no reform effect or causal claim follows.

## Historical artifact inventory
Phase 430/436 recovered ZIPs: not imported or authenticated. Phase 472 materials: not imported. Phase 507 implementation/tests: previously published. Phase 509 diagnostic: implementation/test publication may lag this report; verify repository before relying on it.

## Next
Apply reconciliation to authenticated historical September/October data; preserve unmatched records and investigate source lineage before calculating any matched-group, common-date, or dependence-aware estimates.
