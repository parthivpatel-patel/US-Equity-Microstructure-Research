# Phase 391 — Dated placebo source-manifest reconciliation

Date: 2026-11-15. Scope: independent November 3, 2025 U.S. equity round-lot study.

## Purpose

Phase 390 checks individual placebo record syntax. This phase cross-references the source_sha256 fields of dated placebo CSV records against a separately provided manifest and, optionally, the local bytes of source files. It fails on duplicate manifest digests, malformed SHA-256, malformed CSV, unsafe relative paths, symlink escapes, or checksum mismatches. Missing manifest entries and missing local source files are reported explicitly. The manifest has columns source_sha256, relative_path, redistribution_status; the placebo file requires source_sha256, placebo_date, estimand.

Run: `python scripts/phase391_source_manifest_reconciliation.py records.csv manifest.csv --source-root /path/to/source-root`.

## Evidence and limitations

The implementation has deterministic unit fixtures; no historical SEC source bytes or original 78 dated placebo records were available to this phase. Passing a checksum establishes consistency only with a supplied digest. It does not authenticate the originating SEC dataset, establish historical treatment assignment, prove redistribution permission, or validate a placebo estimator. All outputs explicitly mark origin authentication, redistribution authorization and empirical inference readiness false. A manifest label of 'permitted' is not independently verified authorization.

## Unresolved publication gates

The November 14, 2026 deadline has passed. Manuscript certification is blocked by September pretrends, the substantial October 2025 placebo warning, original dated placebo records, treatment roster authentication, selection/weighting sensitivity, and common-date plus matched-pair and serial-dependence-aware inference on actual observations. No causal interpretation is warranted. Historical ZIP inventory and rights require independent verification before any import.
