# Phase 191 — Source authentication and structural data gate (2026-11-06)

## Verified local work
A standalone prototype was executed locally using Python unittest: seven deterministic tests passed (valid constructed panel, checksum tampering, duplicate composite key, weekend date, missing treatment authentication, nonfinite outcome, invalid outcome). These are **not SEC observations** and no empirical effect was estimated.

## Required data contract
For each security/exchange/trading-date/matched-group/outcome row, require a unique composite key; canonical ISO weekday date; finite contrast; explicit count or volume outcome. An accompanying manifest must contain the SHA-256 of the exact input bytes, HTTPS source URL, UTC retrieval timestamp, explicit license review and treatment-authentication status. Reject mismatches and incomplete provenance before estimation. This gate is necessary but **not sufficient**: a self-declared true flag does not authenticate the historical Nasdaq round-lot mapping, SEC data lineage, matching design, or redistribution rights.

## Important limitation
Weekend rejection is only a minimal calendar check: it does not establish exchange trading sessions, holidays, unscheduled closures, or identifier continuity. A verified market calendar and historical security master remain necessary. An observation-level matched roster, common placebo-date membership, September pretrends, substantial October placebo warning, selection and weighting sensitivity, and serial-dependence-aware inference are still unresolved.

## Publication inventory
At Phase 190's inspected baseline there were ten tracked CSV result/presentation tables and no tracked ZIP, Parquet, PDF or PNG. This does not establish that historical archives do not exist outside the public repository. No archive was recovered or imported this session. Do not redistribute third-party source data without permission.

## Next action
Recover authenticated source observations and archive manifests, independently verify source URLs, licensing and historical treatment assignment, then run this gate before any common-date placebo or security/exchange-controlled analysis. The November 14, 2026 target remains conditional; no causal effect is established.
