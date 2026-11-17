# Phase 416 — Provenance validation corrections (2026-11-16)

This session inspected the published Phase 414 source and Phase 415 review. The existing audit keys duplicates by the literal relative path rather than its resolved canonical path. It also accepts nonempty but invalid URL, retrieval-time and grain metadata. The code review is confirmed directly against the published source.

A local prototype and ten deterministic tests were executed successfully (10/10) using temporary constructed files only. Cases: normal integrity with restricted rights, canonical aliases, invalid timestamps, timezone-naive timestamps, non-HTTPS URL, unsupported grain, hash mismatch, path traversal, permission-evidence metadata, and empty manifest.

## Corrective validation specification

- Compare resolved paths for duplicates, not user-supplied path strings; continue to reject absolute and escaping paths.
- Require an HTTPS source URL with hostname, a timezone-aware ISO 8601 retrieval timestamp, and a controlled observational-grain vocabulary.
- Separate **local integrity** from **publication clearance**. Restricted or unknown rights must never imply public redistribution permission.
- Even a claimed permitted status plus an evidence URL is only metadata eligibility: permission and publisher identity must be authenticated independently.
- Continue streaming SHA-256 checks and fail closed for missing files, invalid digests and mismatches.
- The observational grain vocabulary does not establish that the underlying CSV has the corresponding keys; schema validation remains separate.

## Empirical status

No original authenticated SEC security–exchange–day panel or recovered historical ZIP was available in this run. No historical regression, placebo statistic or pretrend estimate was produced. October 2025 placebo concerns, September pretrends, matching and treatment authentication, weighting sensitivity and dependence-aware inference remain unresolved.

The November 14 deadline has passed. Publication certification is blocked. Next step: land and execute a hardened provenance implementation in the repository and apply it to authenticated recovered inputs before any empirical claims. No third-party data or synthetic research figures are included.
