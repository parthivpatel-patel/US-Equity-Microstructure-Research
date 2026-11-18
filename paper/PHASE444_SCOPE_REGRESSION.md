# Phase 444: matching-scope regression

2026-11-17. Independent, zero-cost round-lot reform research.

Source inspection of Phase 442 and Phase 443 confirms a substantive distinction: treatment status is global to the security, while matched-group assignments may be exchange-local. A security-only matching consistency check can falsely reject an otherwise exchange-consistent panel. Phase 444 adds a standalone constructed-data diagnostic explicitly reporting those false-positive flags and retaining global treatment conflict detection.

Six deterministic tests passed in a local Python unittest run. These are **not** empirical results from the SEC panel. The published tests add an explicit scripts import path to work from a repository checkout; the published exact checkout has not yet been executed.

Do not use this diagnostic to certify source provenance, treatment authentication, parallel trends, or causality. It does not replace the integrated Phase 443 gate. Future work must reconcile Phase 432's identity scope with the integrated source-bound workflow, execute the full published suite, authenticate historical panel and treatment source files, and reproduce September pretrends and October placebo diagnostics under common-date, matched-group, and serial-dependence-aware inference.

Historical recovered ZIPs, the Phase 430 prototype, and Phase 436 prototype tests were not imported in this session. The November 14 manuscript deadline has passed; publication certification remains blocked.
