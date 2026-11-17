# Phase 439 — Structural preflight and source-bound report consistency (2026-11-17)

Phase 437 binds the daily and calendar diagnostics to the same input bytes, but does not reject malformed CSV structure before Python DictReader interprets the panel. Phase 438 added an independent fail-closed CSV structural audit. Phase 439 composes the two: the structural audit must succeed before any panel diagnostic runs, and top-level, daily and calendar report SHA-256 digests and byte lengths must agree.

Run `python scripts/phase439_verified_entrypoint.py panel.csv --output report.json` from the repository root. A structurally invalid CSV raises an error before the downstream diagnostics. A downstream support failure yields exit status 2 and a JSON report. This wrapper does not independently verify historical SEC origin, treatment assignments, the original matching procedure, numerical estimands or valid causal identification.

Six deterministic integration contract tests passed locally using mocked upstream modules. They cover successful source binding, structural rejection before downstream execution, top-level fingerprint mismatch, missing daily report, calendar digest mismatch and daily byte-length mismatch. They do **not** constitute an end-to-end execution of the exact published repository checkout or an audit of upstream algorithms. Run `python -m unittest discover -s tests -p 'test_phase439_verified_entrypoint.py' -v` on the published checkout.

No authenticated historical SEC panel, matching assignments, or recovered ZIP archives were imported. September pretrends, substantial October placebo warnings, weighting/selection sensitivity, fixed-security/common-date sample adequacy and serial-dependence-aware inference remain unresolved. The November 14 target was missed and the paper is not publication-certified. Phase 430 and 436 prototype scripts/tests remain unpublished.

Next: execute the published checkout's integration and upstream tests; authenticate the source panel and historical treatment labels; only then estimate the September and October diagnostics with appropriate clustered/date-aware inference.
