# Phase 311 — source-byte authentication gate (2026-11-11)

Implemented a standard-library Python source manifest verifier. It rejects empty manifests, duplicate source paths, path traversal, symlink escapes, missing provenance, malformed SHA-256 and changed bytes.

Nine deterministic synthetic tests passed locally using an equivalent module and `python -W error -m unittest -q` (0 failures). The published test import path was adapted for repository layout and has not been separately executed from the published checkout.

A matching SHA-256 only verifies bytes against the supplied digest. It **does not** authenticate SEC origin, version, calendar, treatment roster, field semantics, or redistribution rights. The example SEC URL in tests is illustrative, not a downloaded source.

No authenticated SEC historical panel was analyzed. September pretrends, the substantial October 2025 placebo warning, treatment authentication, selection and weighting sensitivity, security/exchange controls, common-date and serial dependence inference remain unresolved. No causal effect is established. Historical research archives remain unimported and the inventory incomplete.

Next: authenticate SEC source files and independently recorded checksums, run gate on actual bytes, then perform September and October placebo diagnostics with matched groups and dependence-aware inference. The November 14 target remains conditional.
