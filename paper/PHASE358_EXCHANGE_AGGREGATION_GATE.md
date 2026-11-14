# Phase 358 — Fail-closed exchange aggregation gate (2026-11-14)

## Scope and provenance
Read the published Phase 357 coverage validator and Phase 352 calendar-indexed serial diagnostic before implementing this opt-in bridge. This phase does **not** use or authenticate SEC observations.

## New audit
`scripts/phase358_panel_gate.py` aggregates a nonnegative metric to security–date only when **every exchange in an explicitly supplied universe** has an observed cell. It reports missing exchange declarations and nonobserved statuses separately; observed zeros are valid but missing-source and exchange-inapplicable records are **not** silently treated as zeros. Duplicate cells, invalid observed values and nonfinite aggregate sums fail closed.

This strict complete-exchange rule is a **sensitivity definition, not an assertion that the same exchange universe is appropriate for every security**. In particular, `exchange_not_applicable` requires an authenticated applicability policy before such a cell may be excluded from a denominator. A complete-case sum can be highly selective; report its support and compare it with a separately justified eligible-exchange specification. The function does not create hidden-execution shares, treatment assignments, pretrend estimates, or confidence intervals.

## Verification
Ten deterministic tests passed locally on 2026-11-14, covering true zero, source missingness, undeclared exchange, inapplicability, duplicate cells, nonfinite inputs and sums, booleans, invalid exchange universe, and row/exchange order invariance. These are constructed software checks only; exact published-checkout and full-suite execution remain pending.

## Publication and archive status
The November 14 manuscript deadline is not met. The substantial October 2025 placebo, September pretrends, original 78 dated placebo observations, Phase 130 contradiction, treatment authentication, selection and weighting sensitivity, and serial-dependence calibration remain unresolved. No historical ZIP, authenticated SEC source file, or licensed third-party data was imported in this phase. The original archive inventory remains incomplete.

## Next empirical gate
Authenticate a session calendar, exchange applicability and security identifiers; reconcile the complete coverage grid with raw source hashes; compare security-date sums under complete-exchange versus authenticated eligible-exchange support; reconstruct dated placebo observations and run matched-group/common-date/serial-dependence-aware sensitivity. No causal conclusion is justified.
