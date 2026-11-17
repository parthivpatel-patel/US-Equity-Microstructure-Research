# Phase 422 — Matched-panel membership stability and calendar guard (2026-11-17)

## Motivation
Phase 421 computes paired group/exchange/date rates but does not authenticate fixed security-to-group and treatment membership. A security moving between groups or treatment labels can produce misleading pretrend and placebo series. This new audit detects such shifts across the September–October 2025 input window, duplicate security/exchange/date observations, weekend dates, invalid count ranges, and groups without both arms. It reports structural failures and exits nonzero.

## Execution and evidence
A standalone local prototype was executed with Python unittest: **10/10 deterministic tests passed**. The published implementation and published tests are equivalent in scope but are not the exact same bytes as the tested prototype; the published checkout has **not** been executed. All fixtures are constructed; no historical SEC estimates were calculated.

## Limitations
The audit assumes security membership is time-invariant; documented rematching must be represented in a separately authenticated mapping. A weekday is not necessarily an exchange trading day. Passing this audit does not verify contemporaneous round-lot classifications, original SEC data, source permissions, or inference. Phase 421 itself still lacks serial-dependence-aware standard errors. The substantial October placebo and September pretrend concerns remain open.

## Publication gates and archive inventory
November 14, 2026 target missed. Manuscript not publication-certified. The repository already contains selected recovered code and memos under archive/recovered_code and archive/recovered_memos and at least one recovered output CSV under archive/recovered_outputs. This is not a complete inventory of the earlier ZIPs. Original authenticated panel, 204-control assignments, and other historical ZIP contents were not accessible in this session and were not imported.

## Next
Run the exact published test suite, recover source-authenticated original panel and matching table, verify contemporaneous treatment, then run September and October placebo estimates with common-date and matched-group resampling and serial-dependence sensitivity. No causal interpretation until identification checks pass.
