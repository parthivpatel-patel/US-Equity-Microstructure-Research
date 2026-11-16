# Phase 408 — Longitudinal identity and simultaneous matched-group coverage gate

Date: 2026-11-16. Status: structural validation only; no new effect estimate.

## Motivation
The Phase 407 structural gate establishes that some matched groups have treated and control observations somewhere in the panel. That is insufficient for matched-group common-date inference: treated and control observations may occur on disjoint dates. It also does not verify whether a security changes its treatment label or match group over time.

## New audit
The standalone Python script checks (1) duplicate security–exchange–date keys, (2) a security's treatment label remaining stable across dates and exchanges, (3) a security's matched-group assignment remaining stable, (4) treated and control securities appearing within every observed match-group-date cell, and (5) every group containing both types of security. Any failure blocks longitudinal structural eligibility. The tool reports observed paired and unpaired group-date cells. This is intentionally stricter than a pooled-group membership check; it may reject legitimate unbalanced panels and should be reported as a coverage limitation rather than silently dropping dates.

Run: `python scripts/phase408_longitudinal_consistency.py /path/to/panel.csv`. Expected CSV columns: date, security, exchange, treated, match_group. Exit code 2 means BLOCKED; exit code 0 means only longitudinal structure passes.

## Verified local test result
Six deterministic unit tests passed on 2026-11-16, covering a valid toy panel, treatment flip, match-group flip, missing same-day pair, duplicate key, and empty input. Toy observations are exclusively test fixtures, not research evidence. Full repository checkout and original security–exchange–day data were not executed in this session.

## Interpretation and unresolved issues
A structural pass is **not** source-data authentication, treatment verification, evidence of parallel trends, or a causal result. The substantial October 2025 placebo and September pretrends remain unresolved. Historical November 3 treatment status, matched-control identities, exchange-level denominators, weighting sensitivity, common-date dependence and serial correlation still require authenticated data and independent replication. Do not interpret an absence of errors as a green light for causal claims.

The November 14, 2026 target was missed. November 30 is provisional only; manuscript publication certification is blocked. No historical research ZIP or restricted/unauthenticated raw data was imported in Phase 408.
