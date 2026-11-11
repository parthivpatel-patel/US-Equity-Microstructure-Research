# Phase 307 — Publish eligibility-interval coverage gate (2026-11-11)

This release supplies the previously missing executable eligibility-interval structural validator and twelve synthetic regression cases. It is a newly reconstructed implementation of the Phase 306 design, not a claim that the original unpublished local prototype was recovered byte-for-byte.

The validator builds expected security–exchange–session keys from inclusive eligibility intervals, flags absent and unexpected observations, duplicate keys, overlapping intervals, and intervals with no supplied sessions. Missing cells are **not** imputed as zero. The supplied weekday-only calendar is **not** exchange-authenticated. Eligibility records are **not** source-authenticated. Ticker changes, eligibility metadata, SEC original observations, and actual historical exchange schedules remain to be authenticated.

A locally executed equivalent implementation passed 12 deterministic synthetic unittest cases (0 failures); no historical SEC observations were processed. The exact published checkout has not yet been separately executed.

Run from repository root: `python -m unittest discover -s tests -p 'test_phase307_eligibility.py' -v`.

September pretrends, October 2025 placebo evidence, round-lot treatment verification, selection/weighting sensitivity, exchange/security controls and matched-group/common-date/serial-dependence inference remain unresolved. No causal effect is established. Recovered historical archives remain unimported; their inventory and redistribution rights remain unverified. The November 14 target remains conditional on empirical source authentication and reproducible validation.
