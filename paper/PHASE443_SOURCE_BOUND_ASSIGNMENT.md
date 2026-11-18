# Phase 443 — source-bound assignment gate

This additive entrypoint composes the existing Phase 439 structural/source-bound diagnostics and Phase 442 assignment-scope audit over the **same input bytes**. The structural check runs first. A failed assignment audit forces the composite `pass` field to false. The assignment report records the same source SHA-256 and byte length as the upstream panel report; these fingerprints describe input identity, **not** independent SEC provenance or historical treatment authentication.

Run from repository root: `python scripts/phase443_assignment_source_gate.py input.csv --output report.json`. A nonpassing result exits with status 2. This does not modify or overwrite previous phases.

Six synthetic, mocked-upstream integration contract tests passed locally on November 17, 2026. An initial test run failed four tests due to incorrect patch targets in the tests; after correcting the patch targets, all six passed. These tests do **not** establish that the exact published repository checkout works end-to-end or that SEC data are authenticated. The full repository suite has not been executed.

The preexisting Phase 432 global-security matching scope and Phase 442 exchange-local matching scope may still disagree in the integrated Phase 439 path. Thus, this integration can reject valid cross-exchange group variation until Phase 432 is reconciled. This is an intentionally conservative failure, not evidence of treatment error.

No historical effect estimates, September pretrends, October placebo re-estimates, matched-group/common-date bootstrap or serial-dependence-aware inference were generated. The substantial October placebo and September pretrend warnings remain. The November 14 deadline was missed; the manuscript is not publication-certified.

Recovery inventory: historical ZIPs are not present in this execution environment and none were imported; Phase 430 and Phase 436 prototype code remain outstanding. Next: reconcile Phase 432 scope, run the exact published checkout's tests, authenticate source observations and historical treatment, and only then reproduce empirical sensitivity analyses.
