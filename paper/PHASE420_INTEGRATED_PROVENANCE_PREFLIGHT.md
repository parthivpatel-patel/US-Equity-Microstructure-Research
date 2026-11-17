# Phase 420 — integrated provenance preflight (2026-11-16)

## Scope and result
Phases 417 and 419 were previously independent: the former checks canonical paths, file existence, SHA-256 and metadata syntax, while the latter checks public-host syntax and retrieval timestamp plausibility. A file could pass the former yet fail the latter. Phase 420 composes **both** checks into one fail-closed command and preserves the distinction between integrity, policy, source authentication and redistribution clearance.

Run: `python scripts/phase420_integrated_provenance.py manifest.json --root /path/to/local/source/files --as-of-utc 2026-11-16T23:00:00Z`.

Tests: `python -m unittest discover -s tests -p 'test_phase420_integrated_provenance.py' -v`. Eight deterministic local fixture tests passed using locally reconstructed copies of the published Phase 417 and 419 functions (their contents were separately fetched through the GitHub connector). A fresh clone and full repository test run were unavailable due to local GitHub DNS failure. Exact published-checkout verification remains pending.

**Interpretation:** A status of `INTEGRITY_AND_POLICY_PASS_NOT_AUTHENTICATED` is not independent source authentication, permission to publish, or a valid research estimate. Unknown redistribution rights never grant clearance. Source origin, licensing and independently corroborated hashes still require human verification. The explicit as-of argument is recommended for reproducibility.

## Empirical readiness
No original authenticated SEC security–exchange–day panel, historical archive, or matched 68/204 security assignments was available in this run. No historical results, figures or causal effects are claimed. The September pretrends, October placebo warning, treatment authentication, weighting sensitivity, common-date and matched-group dependence remain outstanding. The November 14 target was missed; the manuscript is not publication-certified.

## Archive inventory
No historical ZIP, source data, previous paper or figure was recovered/imported this session. The full archive inventory is therefore still incomplete; the absence of local files is not evidence that older archives never existed.

## Next task
Locate authenticated historical panel and matching records, validate provenance and redistribution rights, execute existing pretrend/placebo code on the same matched support, then compare date-balanced and denominator-weighted estimands with dependence-aware inference. Avoid further synthetic empirical claims.
