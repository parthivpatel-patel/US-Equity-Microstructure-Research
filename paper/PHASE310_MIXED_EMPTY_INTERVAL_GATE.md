# Phase 310 — mixed empty eligibility-interval gate

Date: 2026-11-11. Scope: structural validation only.

## Verified defect and repair
Review of the published Phase 307 and 309 implementations identified a fail-open case. Phase 309 rejects an eligibility universe when **all** intervals contribute zero expected security–exchange–date cells, but accepts a **mixed** universe containing at least one contributing interval and another interval that contributes none. Phase 307 already exposes the latter through its `empty_intervals` result. The new Phase 310 wrapper rejects any such interval instead of silently accepting a partial expected universe.

## Reproduction
The synthetic calendar is 2025-10-30, 2025-10-31, 2025-11-03. One interval (ABC, XNAS, 2025-10-31 through 2025-11-03) contributes two expected cells. Another (DEF, XNYS, 2025-09-01 through 2025-09-02) contributes none. The original Phase 309 gate accepts this mixed input, whereas Phase 310 raises ValueError. This is a conservative **admission policy**, not proof that an interval with no sessions is necessarily erroneous in every study design. If legitimately outside the analysis window, it should be explicitly excluded upstream with provenance.

Six synthetic regression tests passed locally (Python unittest, 0 failures), using locally reconstructed copies of Phase 307/309 fetched and inspected through the connected GitHub tool. A separate test run of the exact final GitHub checkout is not claimed.

## Evidence boundaries
No SEC source observations, security eligibility histories, treatment roster, exchange calendar, historical archives or causal estimates were authenticated in this session. Missing cells are not zeros. September pretrends, the substantial October placebo warning, treatment assignment, selection/weighting sensitivity, security/exchange controls and serial/common-date/matched-group inference remain open. No causal effect is established.

## Next empirical gate
Obtain authenticated source files and hashes, exchange-session calendar, dated treatment classification and eligibility intervals. Run structural validation on real rows, then September pretrends and multiple October placebo dates under matched-security, exchange, common-date and serial-dependence-aware specifications. Maintain a verified inventory of historical archives before any redistribution.
