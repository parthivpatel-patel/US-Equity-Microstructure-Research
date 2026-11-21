# Phase-2 historical source-code chain and recovery targets (2026-11-21)

**Evidence class:** inspection of recovered historical analysis source code in the research Library, not execution on authenticated SEC records. No raw data, ZIP bytes or new empirical estimates were recovered in this audit.

## Newly located historical source code

Library artifacts `roundlot_phase2.py`, `roundlot_phase2(1).py`, and `roundlot_pilot.py` document how the older October–November stock-level panel was constructed. This is a stronger lineage clue than the processed panel alone, but it is not SEC source authentication.

The Phase-2 scripts explicitly read `/mnt/data/individual_security_2025_q4.zip` and the internal member `q4_2025_all.csv`; the earlier pilot script instead references `/mnt/data/individual_security_exchange_2025_q4.zip` and the monthly members `oct25.csv`, `nov25.csv`. These are **different local filenames/member layouts**, which must not be assumed equivalent to the SEC's currently advertised `individual_security_exchange_2025_q4.zip` archive without inspecting original ZIP member lists and hashes. A filename or historical script reference does not prove the ZIP was authentic.

The Phase-2 source joins third-party October/November Nasdaq listing snapshots on exact `Symbol`, retains unchanged `Round Lot Size` values, defines treatment as lot size below 100, then joins SEC-like rows using `Ticker == Symbol`. It filters `Security == Stock`, `20251001 <= Date <= 20251128`, `TradesForHidden > 0`, and `TradeVolForHidden('000) > 0`. It computes security-period hidden-trade and hidden-volume rates from **sums of numerators divided by sums of denominators**, pivots to paired periods, and requires at least ten distinct observed days in each period. These details identify precise points for replication and selection audits.

**Important interpretation correction:** `r_pre/r_post` in the Phase-2 panel are *hidden-trade execution rates*, and `v_pre/v_post` are *hidden-share-volume execution rates*; they are **not returns and volatility**, despite generic spreadsheet metadata that may suggest otherwise. The source code defines `r = hidden/trades` and `v = hv/tv` explicitly.

## Required checks on recovered original bytes

1. Recover the original Q4 SEC ZIP through an authorized route, record UTC retrieval time, URL, HTTP response, original ZIP SHA-256, member names, uncompressed sizes and member SHA-256 values; check whether either historical member layout exists and whether the two local archive names refer to identical bytes.
2. Validate exact column names, numeric types, zero denominators, negative counts, hidden numerator not exceeding eligible denominator, date encoding, duplicated `Ticker-Date-Exchange` keys, and the mapping of the reported `Security` category.
3. Reconstruct the stable exact-symbol cohort from the dated third-party listing snapshots, preserving duplicates, missing tickers, corporate actions, and ambiguous aliases as exclusions or unresolved assignments. Do not treat unchanged November/December fields as official September classification.
4. Recreate the October–November panel with the original period filters and ten-day rule. Compare the resulting row count (historically reported 2,262, including 68 provisional treated), per-security period aggregates and final processed CSV SHA-256. If the digest differs, produce a row-level discrepancy report instead of silently overriding the old panel.
5. Only after Q3 is authenticated, construct September pretrends and October within-month placebo from security-date-exchange observations, using common calendar dates and dependence-aware uncertainty. A stock-level October/November aggregate cannot supply those tests.

## Recovery status

A Library filename-focused search in this session did **not** locate `individual_security_2025_q4.zip`, `individual_security_exchange_2025_q4.zip`, or `q4_2025_all.csv` as standalone named Library items. This negative search is not proof that no inaccessible or differently named copy exists. Historical Phase 430/436/472 packages remain unverified.

**Bottom line:** Historical scripts establish the *claimed transformation recipe* and concrete local source filenames. They do not establish SEC provenance, source integrity, a valid treatment roster, or causal identification. No raw source data is redistributed here.
