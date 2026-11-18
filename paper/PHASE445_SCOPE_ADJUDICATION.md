# Phase 445 — Scope adjudication without suppressing support failures

November 18, 2026. Independent research; no SEC observations bundled.

## Source inspection

Phase 432 tracks membership by security alone, while Phase 442 permits exchange-specific matching groups subject to globally consistent treatment status. Consequently Phase 432's `unstable_security_membership` can include cross-exchange group variation that is not within-exchange instability. Phase 443 still uses Phase 437/432's original daily report. This diagnostic does **not** modify that pipeline or automatically override a failed Phase 435 gate.

## New diagnostic

`scripts/phase445_scope_adjudication.py` accepts two report dictionaries with matching SHA-256, byte length, and observation count. It partitions Phase 432 flags into those also explicitly marked by Phase 442 as permitted cross-exchange variation and those unexplained. It fails closed on unexplained flags, assignment conflicts, incomplete strict group/exchange support, missing fields or inconsistent fingerprints. A matching fingerprint is only an identity check, not SEC source authentication.

## Validation and limitations

Nine deterministic unit tests passed locally using synthetic report dictionaries (Python unittest). This is not a historical panel run or a complete checkout test. The procedure cannot establish that a flagged variation is truly legitimate without authenticated assignment provenance. No historical effects, placebo statistics, or confidence intervals are produced.

## Outstanding publication gates

The November 14 deadline has passed. September pretrends, October placebo failures, selection/weighting sensitivity, matched-group/common-date and serial-dependence-aware inference, SEC source provenance, and treatment authentication remain unresolved. No recovered historical ZIP or original data were imported in this phase. Earlier Phase 430 and Phase 436 prototype code remain unpublished. Next: integrate this adjudication into a source-bound diagnostic without weakening strict support, run repository-wide tests, and apply it to authenticated historical observations.
