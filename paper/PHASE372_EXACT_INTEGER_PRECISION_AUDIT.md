# Phase 372 — Exact-integer supplementary panel gate

Date: 2026-11-14. Status: software-method validation only; not empirical SEC analysis.

## Audited existing code

Reviewed `scripts/phase371_panel_gate.py` on the public repository before authoring this supplement. It parses count and volume fields using binary floating-point `float()` and checks `.is_integer()`. This can silently lose precision for integers larger than 2^53. For example, `float('9007199254740993') == float('9007199254740992')` is true in ordinary IEEE-754 binary64 Python, so a hidden count exceeding its denominator by one can escape the inequality check.

## New verification

`phase372_exact_integer_gate.py` parses original decimal strings with `decimal.Decimal`, validates finite nonnegative integer values, and compares exact Python integers. It also rejects extra or missing CSV cells. Run this as a supplementary numeric gate alongside Phase 371 structural validation; it does not replace security/date/exchange/cohort checks.

Six deterministic tests passed locally using constructed fixtures, including the precision-sensitive hidden-count violation, legitimate large integer counts, malformed rows, fractional and nonfinite numbers. No original SEC records were loaded. Published-checkout and full-suite execution remain outstanding.

## Research implications and limits

The 2025-11-03 reform effect remains unidentified: substantial October pseudo-event patterns, September pretrends, historical round-lot assignment authentication, matching/weighting sensitivity, original dated placebo observations, common-date shocks, and serial dependence require authenticated data and inference. This software correction supplies no new empirical estimate and supports no causal claim. The November 14, 2026 publication target was not met; manuscript certification is blocked. Historical ZIP imports and completeness inventory remain pending.
