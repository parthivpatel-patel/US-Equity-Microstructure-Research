# Phase 314 — Public-tree publication inventory (2026-11-12)

## Method and reproducible scope

Queried the connected GitHub API for the **recursive `main` Git tree** at commit [`a93a652dc1db19defc36ad5f3f3b1af8d08a2580`](https://github.com/parthivpatel-patel/US-Equity-Microstructure-Research/commit/a93a652dc1db19defc36ad5f3f3b1af8d08a2580):

`GET https://api.github.com/repos/parthivpatel-patel/US-Equity-Microstructure-Research/git/trees/main?recursive=1`

The response reported `truncated=false`. Counted only entries with `type=blob`, grouping by first path component and filename extension; sizes are the API-reported blob byte lengths. This is a **repository presence audit**, not an inspection of unpublished local archives or a validation of the reported SEC panel.

## Verified baseline inventory

- **443 files** (plus six tree/directory entries).
- **182** files in `paper/`; **93** in `scripts/`; **141** in `tests/`; **7** in `src/`; **10** in `results/`; **5** in `provenance/`; **5** top-level files.
- By extension: **188 Markdown**, **241 Python**, **10 CSV**, **2 JSON**, **1 TXT**, **1 `.gitignore`**.
- **Zero ZIP and zero PDF files** in the complete published tree at this baseline commit.
- Total published blob sizes by directory: `paper/` 461,095 bytes; `scripts/` 177,992; `tests/` 279,333; `src/` 18,420; `results/` 7,658; `provenance/` 6,818. These are source-file sizes, not proof of data completeness.

## Reconciliation and interpretation

The existing [archive status](https://github.com/parthivpatel-patel/US-Equity-Microstructure-Research/blob/main/provenance/ARCHIVE_STATUS.md) reports **129 locally recovered historical phase ZIPs**, totaling **1,158,462,147 bytes**; that number is a *previously reported local-workspace inventory*, **not reverified in this session**. The public Git tree contains **none** of those ZIP archives as ZIP files. Whether individual archive members were previously extracted and published is not established by filename counts. No full file-by-file crosswalk or SHA-256 reconciliation of those archives to the published files exists in this audit. No assertion of licensing or redistribution rights follows from file presence.

The `results/` directory contains 10 CSV files, but a CSV extension does not establish authenticated SEC lineage. No source-byte authentication, official historical treatment assignment, independent exchange calendar, or full matched-panel replication is demonstrated here. No new statistical estimates or causal claims were made.

## Remaining gates before November 14 target

1. Recover and inspect local historical ZIP manifests and individual SHA-256 digests; map each eligible member to a published path, with licensing and GitHub size checks. Do not publish licensed raw data without rights.
2. Re-run the published Python test suite from an exact checkout, recording interpreter, dependency versions, and failures; do not equate test counts with empirical validation.
3. Authenticate SEC observations and Nasdaq historical round-lot assignments, then revisit September pretrends, October pseudo-events, venue/security composition, selection and weights, matched common dates, and serial-dependence-aware uncertainty.
4. Publish a falsification-focused manuscript only if its reported results can be independently reproduced and qualified; the November 14 target is not a certification of completion.

This inventory is deliberately limited to the **baseline commit** and must be regenerated after subsequent changes. It is independent of GIG and other projects.
