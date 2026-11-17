# Phase 431 — Fixed-security support gate (2026-11-17)

## Problem and new diagnostic
Phase 430 identifies group–exchange units paired before and after the November 3, 2025 reform. This is insufficient when the treated and control securities making up each unit change across periods. The Phase 431 script separately intersects pre/post security sets within each (match_group, exchange, treatment arm), then requires at least one fixed treated and one fixed control security. It also reports the gap between nominal pre/post paired units and fixed-security paired units, plus assignment instability.

A constructed counterexample with T1/C1 observed before the cutoff and T2/C2 observed afterward passes the pre/post paired-group gate (one unit) but fails fixed-security support (zero units). This is a **logical counterexample**, not an empirical SEC finding.

## Verification and interpretation
Nine deterministic unit tests passed in local prototype execution, covering fixed support, churn, duplicates, reassignment, count bounds, weekends, empty inputs, missing columns and exchange separation. The published script and tests implement the same logic, but the exact published checkout has not been executed. Run with `python -m unittest discover -s tests -p 'test_phase431_fixed_security_support.py' -v`. Run the audit with `python scripts/phase431_fixed_security_support.py panel.csv --output fixed_support.json`.

The `estimation_ready` field means only *minimal structural eligibility*: it does **not** certify data provenance, sufficient observations, daily balanced support, matched sampling, or valid inference. Security identifiers must be persistent across dates; ticker renames and corporate actions require authenticated mapping. The audit does not estimate a treatment effect.

## Remaining identification and publication gates
Original SEC data, source manifests and treatment assignments remain unauthenticated. September pretrends, substantial October placebo, selection/weighting sensitivity, security/exchange controls, matched-group/common-date and serial-dependence-aware inference remain unresolved. No historical ZIP was imported. November 14, 2026 deadline missed; manuscript not publication-certified. Keep this study independent of GIG and all other projects.
