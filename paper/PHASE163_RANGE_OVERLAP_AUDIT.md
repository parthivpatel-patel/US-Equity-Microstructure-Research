# Phase 163 — Range-overlap insufficiency audit

Date: 2026-11-05. Independent November 2025 round-lot reform research.

## Source reviewed
Read the existing Phase 162 script `tests/phase162_overlap_preflight.py` and the Phase 162 methodology memo before adding these files. No existing files were modified.

## New reproducible verification
Five deterministic Python unittest cases passed locally. The key constructed example uses 100 treated baseline observations (99 at 0.10, one at 0.50) and 100 comparison observations (one at 0.50, 99 at 0.90). Their observed ranges intersect at 0.50, so the Phase 162 range-intersection gate reports overlap; however, only **1/100 observations in each group** lies in the common interval. Thus a Boolean range-overlap result is insufficient to establish meaningful common support. This is a mathematical counterexample, **not** an SEC-data finding.

## Implications for empirical admission
Report the group-specific counts and fractions within the intersection, not merely the Boolean flag. Require joint support assessment for both pre-reform hidden-trade and hidden-volume rates; marginal support in each variable does not imply joint support. Investigate overlap under matched cohorts and weights, and disclose any trimming rule before estimating effects. Never treat overlap as proof of parallel trends. Keep the September pretrends and October placebo as unresolved identification warnings.

## Provenance and publication inventory
This phase publishes only a standard-library synthetic diagnostic test and this report. The archived 2,262-security panel, original generating script, SEC daily source archive, historical Nasdaq snapshots and previously inventoried ZIP collection were **not** imported or authenticated in this session. No empirical market coefficients were computed. Historical redistribution rights and source hashes remain unverified. The November 14, 2026 manuscript target is conditional; no causal effect is established.
