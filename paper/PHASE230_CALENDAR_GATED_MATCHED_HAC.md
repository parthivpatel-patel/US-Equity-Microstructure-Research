# Phase 230: calendar-gated matched HAC integration

This research remains independent of GIG. This phase integrates the Phase 229 pinned-session gate with the Phase 226 matched full-series HAC estimator. The wrapper rejects execution unless the caller explicitly asserts external calendar authentication; it then validates membership and digest before estimation. The assertion is **not** evidence that an exchange calendar was independently authenticated. Output records this limitation.

## Verification

Five isolated deterministic orchestration tests passed locally on November 7, 2026. Tests use stubs for the dependencies and synthetic dates; they do **not** validate the estimator numerics, execute a clean-checkout integration, or analyze SEC historical data. The production wrapper itself delegates to the published Phase 229 and Phase 226 modules.

## Unresolved

Original SEC source data, Nasdaq historical treatment classification, exchange calendar provenance, October 2025 placebo, September pretrends, fixed-roster selection, security-level uncertainty, and weighting sensitivity all require historical re-estimation. No causal conclusion is justified. Previously recovered research ZIP archives were not accessible or imported this session. Do not treat this phase as a publication-ready empirical result.
