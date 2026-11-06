# Phase 194 — Disjoint-window support and matched-group identity

Date: 2026-11-06. Independent U.S. equity microstructure research.

## New methodological result

The Phase 193 audit intersects exact (date, matched-group) keys across every placebo window. This is appropriate only if the design explicitly requires the same historical dates in all windows. For intentionally disjoint event windows, that intersection is empty **by construction**, even if the same matched groups are retained in each window. It therefore cannot by itself diagnose selection bias or invalidate the placebo design.

A valid support audit must distinguish (1) count/volume pairing on identical (date, group) observations *within* each window; (2) roster stability across dates *within* a window; and (3) matched-group identity *across* different windows without requiring identical dates. If the scientific estimand requires a common calendar-date comparison, the design must explain how such overlap is possible and what comparison is being made.

## Deterministic verification

A local Python prototype was executed with eight unittest cases on 2026-11-06: disjoint dates with identical groups, equal counts with different groups, incomplete outcome pairing, within-window roster drift, duplicates, weekend dates, missing outcomes and empty input. All eight passed. These were constructed records, not SEC observations. The local prototype has not been published in this checkpoint, so its execution is not a verified clean-checkout repository test.

## Implications for the paper

Do not interpret zero all-window common unit-dates as evidence of failure when windows are disjoint by design. Report within-window support and cross-window group identity separately. Do not treat equal sample counts as proof of common support. Security/exchange identities must also be retained: a group label alone may conceal different constituent securities or exchanges. The existing Phase 193 schema lacks those identifiers and is insufficient to authenticate a security/exchange-controlled estimand.

The September pretrends, substantial October placebo warning, historical Nasdaq treatment assignments, weighting/selection sensitivity, serial dependence, SEC source provenance and redistribution rights remain unresolved. No historical effect or causal conclusion was estimated.

## Source and publication inventory

The prior Phase 190 audit found 140 tracked files at its inspected baseline and no tracked ZIP/Parquet/PDF/PNG archives. This checkpoint did not recover or authenticate the original SEC daily panel, recovered historical ZIPs, or historical round-lot assignments. Those materials remain unpublished or unverified; the historical archive inventory is not complete.

## Next empirical action

Recover the original row-level daily panel and authenticated treatment roster, retain security and exchange keys, verify window-specific common dates and group identities, and then run pretrends and placebo contrasts under fixed security/exchange rosters with serial-dependence-aware inference. November 14, 2026 remains a conditional target; no causal effect is established.
