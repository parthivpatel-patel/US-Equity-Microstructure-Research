# Phase 407 — Fail-closed panel identification gate (2026-11-16)

This session adds a reusable structural gate for the **original security–exchange–day panel**, without implying that the original data have been recovered or authenticated. The gate requires dated September 2025 pretrend observations, October placebo observations, dates on/after November 3, matched groups containing treated and control securities, valid numerator/denominator pairs, and unique security–exchange–date keys. Missing fields or missing time windows cause a BLOCKED result. Weekend dates are warnings requiring exchange-calendar review.

Usage: `python scripts/phase407_identification_gate.py /path/to/panel.csv`. Run tests: `python -m unittest discover -s tests -p 'test_phase407_identification_gate.py'`.

A structurally eligible result is **not** source authentication, historical treatment verification, an assessment of common support, evidence of valid parallel trends, or causal identification. The October placebo and September pretrend warnings remain unresolved. This gate deliberately does not compute effect sizes. The recovered 126-row tier-level pilot cannot pass because it has neither security/exchange/match-group fields nor September dates.

Local development tests: five focused cases passed in a standalone equivalent module before publication; full repository integration remains untested. No licensed raw source data or historical ZIPs are included. The November 14 manuscript deadline was missed; November 30 is provisional and publication is blocked by provenance, treatment assignment, pretrends, matching, and dependence-aware inference.
