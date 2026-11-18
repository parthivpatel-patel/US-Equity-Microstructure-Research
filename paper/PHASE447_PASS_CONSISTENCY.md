# Phase 447 — Report pass-flag coherence

Date: 2026-11-18. Status: constructed-data software validation, not SEC source authentication or publication certification.

## Verified code-level finding

Inspection of the published Phase 446 report contract shows that it validates the assignment-scope pass flag and its relationship to the top-level pass flag, but does not validate the daily or calendar pass flags. Consequently a report with top-level pass=true and daily pass=false can satisfy that earlier contract if all other fields are internally consistent. This is a report-logic vulnerability, not evidence that an actual SEC observation or prior empirical result was affected.

Phase 447 composes the existing Phase 446 contract with strict Boolean checks on daily, calendar and assignment_scope pass flags, then requires top-level pass to equal their conjunction. A legitimately failed component remains a valid report, but panel_pass is false. No earlier source file is overwritten or validation gate weakened.

## Reproduction

Run from the repository root:

```sh
PYTHONPATH=scripts python -m unittest discover -s tests -p 'test_phase447_pass_consistency.py' -v
```

Ten constructed-report tests passed locally (10/10), using a local copy of the inspected Phase 446 implementation. This does not establish that the exact published checkout or full repository test suite passes. No historical SEC panel was used.

## Open blockers and recovery inventory

The November 14, 2026 target has passed; the manuscript is not publication-certified. Source-data provenance, historical round-lot treatment authentication, September pretrends, substantial October placebo effects, selection/weighting sensitivity, matched-group/common-date serial-dependence-aware inference and exchange controls still require empirical resolution. No recovered ZIPs were accessible or imported in this session; Phase 430 and Phase 436 prototypes remain outstanding. No new historical statistics, figures, or causal claims are made.

Next: execute the published test in a full checkout, integrate this validator into the source-bound pipeline, then prioritize authenticated SEC input and prereform falsification.
