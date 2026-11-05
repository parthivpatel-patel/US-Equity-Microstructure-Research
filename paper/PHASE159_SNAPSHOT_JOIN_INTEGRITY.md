# Phase 159 — Nasdaq snapshot join integrity audit (2026-11-04)

## Source-level implementation finding

The recovered historical `roundlot_phase2.py` reads `nasdaq_october_2025.csv` and `nasdaq_november_2025.csv(1).csv`, filters allowed round-lot sizes, and calls `drop_duplicates('Symbol')` **without checking agreement among duplicate records**. It merges by symbol, retains identical lot sizes across October/November, sets treatment to a lot below 100, and joins SEC `Ticker` to Nasdaq `Symbol`.

**Verified code-level risk:** When one symbol has conflicting lot sizes, first-row duplicate removal is row-order dependent; it can alter cohort membership or treatment. This does **not** demonstrate that the actual source files contained conflicting duplicates. Requiring October/November agreement also produces a stable-survivor cohort, not the full November 3 eligible universe. The November snapshot may encode post-event information. Ticker-only joins do not establish issuer continuity across symbol changes or reuse.

## Executed software verification

`tests/test_phase159_snapshot_integrity.py` supplies a fail-closed **prototype** that rejects duplicate symbols, malformed symbols, and invalid lots, and never imputes missing/disagreeing snapshots. Eight unit tests passed locally using **constructed fixture rows**. This is not a market-data estimate, and the historical production script has not been modified. The exact published script still requires a fresh-checkout execution.

## Access and archive inventory

Phase 158 recovered the 2,262-security aggregated Phase 2 panel, its generating script, and a pilot daily CSV, but these remain outside the public repository pending provenance/redistribution review. This session's Library search retrieved the historical script and research memos, **not** the two original Nasdaq snapshot CSVs, `individual_security_2025_q4.zip`, authenticated November 3 SIP assignments, or the approximately 129 earlier research ZIPs. No archives were imported. Consequently, actual duplicate frequencies, lot disagreement rates, raw SEC row reconciliation, and fresh September pretrend or October placebo estimates **cannot** be claimed.

## Next empirical steps

1. Recover both historical Nasdaq snapshots; record duplicate counts, lot conflicts, and exclusion flow before filtering.
2. Authenticate operative November 3 assignments using contemporaneous rules and historical primary closing prices, separating stable-survivor and event-date cohorts.
3. Recover original SEC Q3/Q4 archives; validate security/date/exchange keys and venue coverage.
4. Re-estimate September pretrends and October placebo with matched-group, common-calendar-date, serial-dependence-aware inference and fixed exchange/weighting choices.

**Scientific status:** exploratory; no causal effect established. November 14, 2026 remains a conditional target.
