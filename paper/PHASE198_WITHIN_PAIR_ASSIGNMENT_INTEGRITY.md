# Phase 198 — Within-pair treatment assignment integrity (2026-11-06)

## Finding
The published Phase 197 audit compares treatment and matched-group labels by (security, exchange) across all rows, but does not separately report disagreements between count and volume records for the *same* entity and trading date. Such disagreement is a data-integrity defect, not an estimated treatment effect. Phase 198 adds a narrowly scoped independent check keyed by (window, date, security, exchange). It rejects duplicate outcome rows even if the group label differs, flags missing count/volume counterparts, and separately reports group or treatment disagreement within a pair.

## Verification
Ten deterministic unit tests were run locally with Python unittest against a standalone implementation of the same algorithm and passed on November 6, 2026. The exact published files require fresh-checkout execution using `python -m unittest discover -s tests -p 'test_phase198_pair_consistency.py'`. These are constructed inputs, not authenticated SEC observations; no historical coefficients were computed.

## Interpretation and publication status
The checker is a structural preflight, not a substitute for source authentication, historical round-lot treatment reconstruction, exchange calendar validation, dated security identifier mappings, weighting analysis, pretrend tests or common-date dependence-aware inference. In particular, September 2025 pretrends and the substantial October 2025 placebo warning remain unresolved. It always returns `treatment_authenticated: false`. Recovered historical ZIPs, original SEC daily records and licensed source data were not imported in this phase. No causal effect is established.

Next: execute the exact committed files in a clean checkout, obtain authenticated original daily observations, reconcile treatment mapping and source provenance, and then estimate fixed-roster September pretrends and October placebo contrasts with exchange/security controls and serial-dependence-aware inference.
