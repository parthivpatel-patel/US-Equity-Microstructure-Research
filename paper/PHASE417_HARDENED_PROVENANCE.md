# Phase 417 — Hardened local provenance validation (2026-11-16)

This session reviewed the existing published Phase 414 implementation and Phase 416 specification before adding a separate version, leaving the original unchanged.

## Changes
The new gate detects duplicate canonical file paths, validates HTTPS metadata, requires an explicitly UTC retrieval timestamp, checks a controlled grain vocabulary, verifies local files with streaming SHA-256, and blocks missing files, path traversal and invalid rights labels. Its publication_clearance field is ALWAYS NOT_ESTABLISHED: matching a declared digest is not publisher authentication, and a rights label is not a verified license.

## Validation and limits
Thirteen deterministic local fixture tests passed using the same implementation logic (including alias paths, invalid dates, non-UTC timestamps, hash mismatches, missing files, rights labels and unsafe paths). No original SEC historical panel was available. No historical regression or placebo statistic is asserted. Full-repository test suite and post-publication checkout execution are not claimed.

## Pending
Recover authenticated original security–exchange–date records and treatment/matching assignments, then examine September pretrends, October placebo cutoffs, matched same-date same-exchange support, weighting sensitivity, and inference robust to common dates and serial dependence. Recovered archives remain unimported; redistribution permission must be separately verified. The November 14 publication target was missed and the paper remains uncertified.
