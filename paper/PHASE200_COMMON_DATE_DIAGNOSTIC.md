# Phase 200 — Common-date matched-group descriptive contrasts (2026-11-06)

## Scope
This new dependency-free script calculates treated-minus-control contrasts within each matched group and trading date, then averages matched groups equally. It separates count and volume outcomes and rejects date/outcome slices missing any group/arm cell. Replicate records within a cell are averaged. Dates are **not** pooled into a single naive independent-observation standard error.

## Deterministic verification
Eight unit tests passed locally on 2026-11-06 using an equivalent implementation: empty-panel rejection; balanced contrasts; missing arm; equal group weighting despite replicate imbalance; nonfinite value; boolean treatment; count/volume separation; and roster drift. These tests use constructed observations, not original SEC data. Published-source checkout tests remain to be executed. The new code is deliberately a descriptive diagnostic, not a DiD or causal estimator.

## Important limitations
The function uses a global union of group identifiers and therefore can conservatively reject dates when a matched group appears only in another period. It does not authenticate exchange/security IDs, dates, historical round-lot treatment, original SEC source files, or matched-group definitions. It does not implement security/exchange fixed effects, September pretrend estimation, October placebo inference, serial-dependence-aware standard errors, or treatment-effect estimation. It does not calculate p-values. Apply Phase 191–199 provenance/admission checks before interpreting any actual panel output.

## Outstanding historical evidence
The original authenticated daily SEC panel, Nasdaq historical treatment mapping, and recovered research ZIP archives were not imported. September 2025 pretrends and the substantial October 2025 placebo warning remain unresolved. No causal effect established. November 14 submission remains conditional.
