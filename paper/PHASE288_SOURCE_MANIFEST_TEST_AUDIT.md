# Phase 288 — Reproducible source-manifest verification prototype (2026-11-10)

## Executed validation
A standalone Python verifier was implemented and executed locally with 11 deterministic unittest cases (11 passed, 0 failed; 0.020 seconds). It streamed SHA-256 hashing of file bytes and compared recorded byte counts; rejected duplicate paths, absolute and parent-relative paths, symlinks escaping the permitted root, invalid digests, altered bytes, HTTP URLs, missing redistribution decisions, and invalid UTC timestamp syntax. Tests used an authored miniature CSV, not SEC observations. The local code and tests are **not included in this report commit** and cannot be considered repository-reproducible until published and rerun.

## Source-integrity limitation
A digest is only a consistency check against the manifest supplied by the researcher. It does not authenticate the SEC as publisher, prove the retrieval timestamp was recorded at acquisition, validate a trading calendar, authenticate treatment status, or establish redistribution rights. HTTPS source URL validation is a syntactic guard, not a publisher-identity check. A metadata field set to 'permitted' must not substitute for documentary evidence of permission. Historical inference must remain blocked until publisher provenance, original observations, schema, roster, and calendar have been independently established.

## Immediate audit consequence
Phase 283 HAC and Phase 286 inference admission are statistical/numerical tools only. The September pretrend and substantial October 2025 placebo concerns cannot be dismissed by passing these checks. Selection, weighting, exchange composition and matched-group/common-date serial dependence remain outstanding empirical sensitivity analyses.

## Publication inventory and gaps
Published in this phase: this methodology report only. Unpublished: Phase 288 verifier and 11 tests, Phase 287 standalone verifier and 10 tests, earlier historical ZIPs, original SEC source extracts, and historical tables/figures. Complete recovered-archive inventory and permissions remain unverified. No historical coefficients, figures, or causal findings were produced.

**No causal effect is established.** November 14, 2026 remains a conditional target. Next priority: publish tested scripts and tests; authenticate original SEC inputs and treatment roster; then run September and October diagnostics before interpreting November.
