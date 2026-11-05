# Phase 172 — Pooled coverage can conceal entire missing dates

Date: 2026-11-05. Independent U.S. equity microstructure project. No empirical SEC observations used.

## Verified methodological result

Phase 171 pools complete matched-group cells within periods. A high pooled coverage rate can nevertheless conceal a completely missing date. In a constructed eleven-date roster with ten expected matched pairs per date, the post-cutoff period (2025-10-08 onward) contains six dates, five with ten complete pairs and one (2025-10-14) with zero. Pooled post coverage is 50/60 = 83.333%, so an illustrative 80% pooled gate passes; a 50% minimum daily coverage gate fails.

A new diagnostic combines period-specific pooled coverage and minimum daily coverage, lists dates below the floor, and reports the longest run of zero-coverage dates in the **supplied expected-date sequence**. Its run statistic is not elapsed calendar days. A missing expected date must already be represented as a zero-coverage row by the fixed-calendar construction; this diagnostic does not authenticate or generate the trading calendar.

## Verification

The local Python implementation at session time passed 10/10 unittest cases after correcting two initially erroneous test expectations. Tests cover high pooled coverage with an absent date, consecutive outages, input ordering, duplicate dates, invalid counts, malformed dates, empty periods, thresholds and inconsistent fractions. These are deterministic constructed-data checks only, not estimates of reform effects. The local implementation is retained for subsequent synchronization if its exact source is not published.

## Empirical and publication gates

Original SEC source archive authentication, historical Nasdaq treatment classification, September pretrend analysis, substantial October placebo, matching/weight sensitivity, security-exchange controls, common-date and serial-dependence-aware inference remain unresolved. Do not infer causality. Thresholds are sensitivity parameters rather than defensible empirical acceptance rules. The historical ZIP/paper/code/chart inventory remains incomplete and no recovered archive was imported in this phase. November 14 remains conditional.
