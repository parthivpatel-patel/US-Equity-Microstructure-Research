# Phase 222 — Fixed-roster panel completeness admission

Date: 2026-11-07. Scope: independent U.S. equity round-lot reform research.

## New methodological safeguard

The existing session-level HAC prototype accepts one date-level contrast per observation. That is insufficient to establish whether each contrast was constructed from a stable set of securities and exchanges. A changing roster can masquerade as a time-series movement, including a pre-reform placebo signal.

The new `scripts/phase222_panel_gate.py` provides a deliberately strict rectangular-panel admission check before any aggregation: every specified security, exchange, and session combination must appear exactly once; missing cells are rejected rather than silently zero-filled. It rejects duplicate keys, unknown exchanges/securities, overlapping treated/control identifiers, invalid integer counts, hidden counts above total counts, and dates reaching the November 3, 2025 reform. Its returned flags explicitly mark calendar, source, and treatment authentication as false.

## Verification

Nine deterministic tests passed in a local standalone module execution. The published test imports the same function via the repository `scripts` package; exact published checkout execution remains to be verified. All tests use fabricated software fixtures, not SEC observations. No historical effect size, uncertainty interval, or causal estimate is reported.

## Important limitations

This is a strict complete-case admission policy, not proof that a rectangular panel is representative. Genuine exchange/security absence can occur and must be documented separately; requiring a full rectangle can induce selection bias. The metric names `hidden_count` and `total_count` are generic placeholders and **must not** be assumed to match SEC field definitions without a source-level schema map. It does not authenticate trading calendars, Nasdaq treatment assignments, matched controls, data provenance, or exposure definitions. No security/exchange fixed effects or historical HAC estimates were run.

The substantial October 2025 placebo warning and September pretrends remain unresolved. Treatment classification, weighting sensitivity, and serial-dependence-aware historical inference are still blocking causal interpretation.

## Next reproducible step

Authenticate the SEC extract, field definitions and 2025 exchange calendar; produce a missing-cell and roster-stability audit on the historical panel; define explicit exclusion/weighting rules; then form fixed-roster daily matched-group contrasts and apply the already published joint-window HAC estimator. Preserve both the complete-case and available-case sample accounting and test the October placebo before interpreting the November reform.

## Archive inventory status

Previously recovered historical ZIPs, manuscripts, charts and code have not been authenticated or imported in this phase. Redistribution permission and file checksums remain unverified. No licensed source data were published.
