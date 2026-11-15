# Phase 392 — read-only historical ZIP triage

Date: 2026-11-15. Independent U.S. equity round-lot reform research only.

This phase adds a zero-cost, read-only ZIP archive inventory for historical recovery. It records archive SHA-256, compressed size, member names, declared uncompressed sizes, CRC metadata, and structural warnings for duplicate names, path traversal, symlinks, encryption, excessive member counts, aggregate uncompressed size, and compression ratios. It does not extract or upload third-party archive contents.

Run: `python scripts/phase392_archive_inventory.py /path/to/archive.zip`. Run tests: `python -m unittest discover -s tests -p 'test_phase392_archive_inventory.py'`.

Eight deterministic tests passed in a local equivalent layout on constructed ZIP fixtures. The published test imports from the repository scripts directory; execution against the exact GitHub checkout and full suite is not yet verified.

## Important limits

ZIP metadata is untrusted. This tool does not read/decompress every member, verify CRC against actual bytes, authenticate SEC provenance, validate licenses, establish historical treatment assignment, or declare archives safe to extract. Its `safe_to_extract` field is intentionally always false. Structural warnings do not substitute for safe extraction policy. No original historical ZIP was available for this run; no archive has been imported or cleared for redistribution.

## Publication gates

The November 14, 2026 target has passed without certification. Original 78 dated placebo estimates, September pretrends, substantial October placebo, treatment roster authentication, selection/weighting sensitivity, matched-pair/common-date and serial-dependence-aware empirical inference remain outstanding. Do not interpret test fixtures as empirical results or claim causal effects.
