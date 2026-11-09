# Phase 275 — Window endpoint and partition admission (2026-11-09)

## Verified audit of Phase 274
Reviewed `scripts/phase274_pretrend.py` at blob SHA `322e0786a3f6f79870137d9eacafe8c9c51f15ca`. Phase 274 checks that each requested window contains at least two calendar sessions, but does not require window endpoints to be actual exchange sessions, and does not report calendar sessions excluded between windows or outside the selected span. Thus a weekend endpoint, an out-of-calendar endpoint, or a gap between windows can be silently accepted when two observations remain in each window. This is not necessarily an error for explicitly separated pretrend windows; it is an **admission and reporting choice** that must be declared before estimating.

## New validation
Added `scripts/phase275_pretrend_window_audit.py` with explicit ISO-date format checks, strict session order, exchange-session endpoints, counts of omitted sessions, and optional complete contiguous partition enforcement. Added 12 synthetic unit tests. All 12 passed locally using Python unittest on 2026-11-09; this is not a historical SEC replication or proof that the published checkout passes.

## Interpretation
A contiguous partition is optional, not universal: predeclared early and late September windows may intentionally omit intermediate sessions. In that case the omitted count must be recorded, and endpoint validity still checked. The supplied calendar is not independently authenticated by this code. No source files, historical coefficients, historical charts, causal effects, or treatment assignments are authenticated here.

## Outstanding evidence
Original SEC data downloads and provenance; independent exchange-session calendar; pre-reform and post-reform round-lot treatment roster; matched-security and exchange composition; September pretrends and October placebo using authenticated data; full-series HAC plus paired and date-aware bootstrap sensitivity; prior ZIP archives and Phase 252–254 artifacts. No historical archive was imported in this session. Target November 14 remains conditional.
