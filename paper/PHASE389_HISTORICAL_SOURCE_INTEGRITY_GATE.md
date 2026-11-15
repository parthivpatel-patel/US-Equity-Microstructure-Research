# Phase 389 — historical source integrity and redistribution gate

Date: 2026-11-15. Scope: independent U.S. round-lot reform research only.

The script checks a user-supplied JSON inventory against locally held files: SHA-256, byte count, path containment, duplicate entries, and nonempty source metadata. It deliberately distinguishes integrity from source authentication and independently confirmed redistribution permission. A manifest's `redistributable` flag is a claim requiring documentary review, not a license determination.

Usage: `python scripts/phase389_source_gate.py /path/to/archive_root /path/to/manifest.json`. Required fields per record: `path`, `sha256`, `bytes`, `origin_url`, `retrieved_utc`, `license_status` (redistributable/restricted/unknown), `role`. The script does not upload source bytes.

Ten deterministic local tests passed on constructed files. No historical archives or authenticated SEC panel were available for processing in this session. The reported historical ZIP inventory remains unverified in this run. Nothing here establishes treatment assignment, source authenticity, empirical estimates, causal identification, or permission to publish data.

Outstanding scientific blockers: October 2025 placebo effects, September pretrends, original dated placebo records, historical treatment roster, selection and weighting sensitivity, and matched-pair/date/serial-dependence-aware inference. The November 14 target was missed; the manuscript is uncertified.

Next: locate original archives, validate SHA-256 against independent provenance records, review licenses, and only then reconstruct source-derived estimates and sample attrition.
