# Phase 486 — Date-specific eligibility executable and provenance limits

2026-11-19. This session publishes a self-contained standard-library auditor and deterministic test suite for an independently supplied security-exchange-date eligibility file. It follows the methodological finding in Phase 485; the earlier unpublished prototype was not recovered, so this is a new independently written implementation, not a claim to have recovered identical bytes.

## Constructed-fixture verification
Three eligible keys (A/X on October 1 and 2, B/Y on October 2); two observed keys (A/X October 1 outcome 0, B/Y October 2 outcome 2). Expected counts: eligible 3, observed 2, missing 1, observed zeros 1, complete eligible units 1. No SEC historical observations were analyzed. Eight local deterministic tests were executed against a functionally equivalent precursor implementation; the exact committed code was not executed after publication. The repository test suite should be run against the published checkout before certification.

## Provenance and interpretation
Input SHA-256 fingerprints only establish byte identity, not SEC provenance, eligibility validity, licensing, or correctness. A missing eligible observation is not a zero. Complete-unit counts condition on eligibility dates and cannot by themselves resolve selection bias. The eligibility source, listing status, exchange participation, dates, panel schema and source revisions must be authenticated independently.

## Publication gate
November 14 deadline missed. Manuscript not publication-certified. September pretrends, substantial October placebo, round-lot treatment authentication, weighting/selection sensitivity, exchange/security controls, and matched-group/common-date/serial-dependence-aware empirical inference remain open. Recovered Phase 430/436 archives and Phase 472 package remain unpublished and not independently inspected in this session. Next: execute published checkout, authenticate SEC data and eligibility keys, apply coverage diagnostics to October placebo.
