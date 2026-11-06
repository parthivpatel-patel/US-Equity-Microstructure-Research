# Phase 196 — Treatment and matched-group identity risk (2026-11-06)

## Audit finding
Phase 195 checks exact (security, exchange, matched-group) roster stability, but it does not authenticate historical treatment assignment. A security can change its assigned matched group or treated/control status across windows, and a roster check alone does not establish whether such changes reflect historical classification, reconstruction error, or intentional rematching. The treatment indicator must be checked explicitly and independently against period-specific historical round-lot rules.

A constructed counterexample uses the same security AAA and exchange X on 2025-09-02 and 2025-10-01, with group G on both dates but treated=True in September and treated=False in October. Security/exchange/group identity is unchanged; treatment assignment is not. Conversely, two intentionally disjoint date windows can have identical security/exchange rosters without sharing a single calendar date. Neither observation by itself identifies a causal effect.

## Executed verification
Eight deterministic Python unittest checks were executed locally on 2026-11-06 against a standalone prototype identity audit: stable disjoint dates; group switch; treatment switch; equal-sized but different security rosters; conflicting same-day group mapping; nonboolean treatment; weekend date; and empty input. All eight passed. This is **constructed-data software verification only**. The prototype has not been published in this checkpoint and the published research repository has not been clean-checkout tested.

## Required empirical protocol
Freeze a canonical (security, exchange) identifier and dated treatment mapping from authenticated pre-reform reference prices and UTP/Nasdaq notices; record classification source, effective date, reconstruction code and ambiguity. Preserve the original matched-pair mapping. Separate intentionally time-varying classifications from accidental reassignment. Audit stable common-unit samples before computing placebo and post-event contrasts. For September pretrends and the substantial October 2025 placebo movement, report separate fixed-roster and reweighted results, date-clustered and serial-dependence-aware uncertainty, and security/exchange controls. Never treat a structural pass as proof of source authenticity.

## Publication and archive status
No authenticated SEC daily panel, historical Nasdaq treatment roster or recovered ZIP archives were available for empirical execution in this checkpoint. No empirical coefficients, new figures, or causal effects were estimated. Previously recovered archives remain unimported; their completeness and redistribution permissions are not verified. The November 14, 2026 manuscript target remains conditional. The next task is to publish and rerun the identity-audit prototype and tests, then authenticate historical inputs before empirical estimation.
