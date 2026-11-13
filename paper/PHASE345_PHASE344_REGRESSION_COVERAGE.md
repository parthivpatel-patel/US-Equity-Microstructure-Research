# Phase 345: Phase 344 regression coverage and remaining identification gates

Date: 2026-11-13. Scope: independent round-lot reform study only.

## Contribution
Adds seven deterministic regression tests for the published Phase 344 matched-support attrition diagnostic. Cases cover equal-group versus unequal cell counts, exchange-disjoint support, undefined leave-one-out estimates, duplicate security-date-exchange observations, assignment drift, nonfinite quantities and noncanonical dates.

The unequal-cell example deliberately has two positive 80-percentage-point cells in group A and one negative 80-percentage-point cell in group B. The equal-group estimate is exactly zero, whereas equal-cell weighting would yield +26.6667 percentage points. This is a constructed identity, not an empirical result.

## Limitations
The tests use invented fixtures solely for software checks. They do not authenticate SEC source records, historical round-lot treatment, matching provenance or the 78 original dated placebo observations. In particular, the October 2025 placebo warning and September pretrends prohibit an unqualified causal interpretation. The Phase 130 count inconsistency remains unresolved. Source-data licensing and archive inventory remain unverified. No empirical standard errors or new causal estimates are reported.

## Reproduction
`python -m unittest discover -s tests -p 'test_phase345_phase344_regression.py' -v`

Publication of tests alone does not establish successful execution of the exact GitHub checkout. Execution evidence should be separately recorded before declaring this gate passed.

## Next action
Run the published test suite on a fresh checkout; then execute Phases 340–344 on authenticated observations and document common-date/exchange attrition, weighting sensitivity, and joint matched-group/date serial-dependence inference.
