# Phase 441 — treatment scope versus matching scope

November 17, 2026. Independent round-lot reform research. No original SEC data was used.

## Finding
Phase 432 identifies assignment instability by security alone and conflates match-group variation with treatment variation. Phase 433 checks security/exchange identity, which may miss contradictory treatment assignments for one security across exchanges. The November 3, 2025 round-lot treatment should be established at the security level using authenticated historical reference data; exchange-specific matched-group labels may be valid only with documented matching rules. Neither blanket security-only nor blanket security/exchange-only assignment checking is sufficient.

## Implementation
The Phase 441 audit separately reports security-global treatment conflicts, within-security/exchange treatment conflicts, within-security/exchange matched-group changes, and cross-exchange-only matched-group variation. Structural eligibility fails on global treatment conflicts or within-exchange matched-group changes. Cross-exchange group variation is a warning requiring matching-design review, not an automatic treatment failure.

Run from repository root: `python -m unittest -v tests.test_phase441_assignment_scope` (or `python -m unittest discover -s tests -p 'test_phase441_assignment_scope.py' -v`).

## Evidence and limitations
Ten deterministic constructed-data cases were exercised locally in a separate prototype and passed. The published implementation and tests are equivalent in scope but have not been executed from the exact published GitHub checkout. This audit does not authenticate historical round-lot treatment, source data, match-group design, or estimates. The substantial October placebo warning and September pretrends remain unresolved; selection, weighting, common-date and serial-dependence-aware inference remain required.

## Backlog
Unpublished Phase 430 and Phase 436 prototypes, unrecovered historical ZIPs, and authenticated SEC source panels remain outstanding. Do not import licensed raw data without permission. The November 14 target was missed; the manuscript is not publication-certified.
