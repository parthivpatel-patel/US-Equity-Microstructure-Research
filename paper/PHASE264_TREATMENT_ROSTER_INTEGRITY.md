# Phase 264: treatment-roster structural integrity gate

Date: 2026-11-09. Scope: independently developed structural diagnostic, not an empirical SEC result.

## Finding
A complete date-by-pair grid is insufficient if the externally supplied roster has only one arm of a matched pair, duplicates a security/exchange identity across pairs, or changes treatment labels across observations. This gate requires one treated and one control entry per pair, consistent security/exchange/arm identities, and all expected date-by-roster cells. It rejects duplicates, unexpected cells, and nonfinite outcomes. It never authenticates the supplied roster or calendar.

## Verification
Ten deterministic synthetic tests passed in a local Python unittest execution against an equivalent implementation. The repository version was not independently rerun after upload. No historical SEC coefficients, figures, or p-values were generated.

## Remaining threats
September 2025 pretrends and the substantial October 2025 placebo remain major identification warnings. Treatment status requires independent round-lot reconstruction from authoritative notices and security prices; historical SEC source files and exchange calendars require authentication. Matched-group selection, weighting, common-date effects, security/exchange controls, and serial/cross-sectional dependence remain to be analyzed on authenticated data. No causal effect is established.

## Publication inventory
This phase adds a script, tests and audit note. Historical recovered ZIPs, licensed raw data, and earlier unpublished Phase 252–254 implementations have not been authenticated or imported. Next step: authenticate and hash input files and fixed roster, then run pretrend and placebo diagnostics on a frozen panel.
