# Phase 364 — hard-link identity integrity

## Finding
The Phase 363 resolved-path check does not detect two hard links to the same inode: their resolved paths differ even though they reference the same underlying file. This permits duplicate manifest entries for one physical source.

## Correction
The source-byte verifier now records the pair (device ID, inode ID) from `os.fstat` on the opened file descriptor, rejecting a repeated pair. The check uses the opened handle rather than a separate path-based stat. Different files with identical content remain allowed. This does not provide protection against all concurrent filesystem mutations or independently authenticate the origin, licensing, or historical vintage of source bytes.

## Verification
Four deterministic tests passed locally with Python unittest: hard-link alias rejected, distinct equal-content files accepted, single file accepted, and mismatched digest reported. These are synthetic filesystem fixtures, not SEC-panel data. Full-repository tests and published-checkout tests remain pending.

## Empirical and deadline status
No authenticated market observations or recovered historical ZIPs were processed. September pretrends, October placebo effects, original dated placebo observations, historical treatment assignments, and dependence-aware inference remain unresolved. November 14, 2026 manuscript deadline was not met; do not interpret this as a certified causal study.

## Next work
Execute full integration tests and establish authenticated, permission-compatible source files and a complete inventory of unpublished historical artifacts before reconstructing placebo estimates.
