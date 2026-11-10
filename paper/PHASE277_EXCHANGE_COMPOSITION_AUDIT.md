# Phase 277 — Exchange composition and fixed-roster admission

## Purpose
The same fixed pair roster can yield materially different descriptive contrasts under pair-weighted and exchange-equal aggregation. The new `scripts/phase277_exchange_balance.py` makes that choice visible rather than treating exchange composition as an implicit constant.

## Deterministic verification
A synthetic two-session panel with three pairs (two on exchange X with contrasts 1 and 3, one on Y with contrast 9) gives an X mean of 2 and Y mean of 9. Pair weighting yields 13/3, whereas exchange-equal weighting yields 11/2. This difference is entirely mechanical and is **not** a historical estimate. Twelve local synthetic checks of an equivalent implementation passed, covering weighting, roster completeness, duplicates, reassignment, invalid calendar and nonfinite values. The published checkout and full repository test suite have not been rerun.

## Admission conditions and limitations
The caller must independently authenticate the calendar, matched security identifiers, treatment assignment, exchange mapping, outcome definitions, source-file hashes and coverage. A complete observed panel is not proof that its externally supplied roster is correct. Exchange-equal weighting does not substitute for security and exchange fixed effects; neither weighting scheme establishes identification. This implementation assumes one exchange per matched pair, a deliberately restrictive audit convention; securities trading on multiple venues require a different key and estimand.

The substantial October 2025 placebo signal, September pretrends, selection/weighting sensitivity and treatment authentication gaps remain unresolved. No historical SEC observations, coefficients or figures were generated. No causal effect has been established.

## Publication inventory and next work
Published in Phase 277: exchange-composition script, synthetic tests and this audit. Earlier recovered ZIP archives, unpublished historical implementations and underlying authenticated SEC source data were **not imported**; their full contents and redistribution permissions remain unverified. Next: authenticate source hashes and roster/calendar, rerun repository tests, and compare September pretrends and October placebo estimates under both aggregation schemes, with security/exchange controls and common-date dependence-aware inference. The November 14, 2026 target remains conditional on validation.
