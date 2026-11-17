# Phase 436 — Provenance linkage audit (2026-11-17)

## Verified local software analysis

Reviewed the published Phase 435 integrated gate source and methodology. Its `daily['observations'] == calendar['observations']` check does **not** prove both reports were computed from the same CSV: two different panels can contain equal numbers of observations. Likewise, a successful structural gate does not authenticate the source of the observations, historical round-lot assignments, matching, or inference.

Developed and executed a local Python SHA-256 provenance verifier using only Python's standard library. The verifier records byte lengths and SHA-256 digests for a panel CSV and two JSON reports, checks exact byte identity against the manifest, rejects absent or unexpected entries, and checks report count agreement. Nine constructed-data unit tests passed locally, including an equal-size changed-panel counterexample, changed reports, invalid JSON, missing input, missing manifest entry and unknown schema. No original SEC observations were involved.

## Critical limitation and workflow

A manifest created **after** both reports are generated does not independently prove the reports were generated from that panel. For robust lineage, each report-producing script must compute the input CSV digest at read time and include that digest in its own report. The joint gate must compare both embedded digests against each other and the current panel. This is the next implementation requirement; a post-hoc manifest alone is insufficient. Independently authenticated source acquisition and signed or archived provenance remain necessary.

## Publication and synchronization inventory

The November 14, 2026 target has passed; the manuscript is not publication-certified. The substantial October 2025 placebo warning, September pretrends, treatment authentication, selection/weighting sensitivity, exchange controls and dependence-aware uncertainty remain unresolved. The Phase 430 prototype/tests and historical recovered ZIPs have not been verified as published. No new historical estimates, causal claims or figures were generated.

Local prototype code and nine tests were executed but not included in this report commit; their publication remains an explicit outstanding item. This report documents the independently reviewed gap and reproducible test scope without claiming historical empirical validation.
