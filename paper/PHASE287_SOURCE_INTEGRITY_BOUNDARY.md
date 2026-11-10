# Phase 287 — Source integrity and provenance boundary (2026-11-10)

## Verified work
Reviewed the published Phase 283 HAC estimator, Phase 286 inference gate, and Phase 286 methodology report. The gate validates numerical admissibility, but does not establish that the observations came from SEC source files. A locally executed standalone source-manifest verifier checked SHA-256, exact byte counts, relative-path containment, duplicate paths, HTTPS source URLs, UTC retrieval markers, and explicit redistribution-permission decisions. Ten deterministic tests passed (10/10, zero failures) on 2026-11-10. Tests used an authored miniature CSV, **not SEC data**.

The integrity verifier and tests were executed locally but are **not included in this report commit**; they must be imported and rerun on the exact published checkout before being counted as a reproducible repository deliverable. SHA-256 equality proves local byte consistency with a recorded digest, **not publisher identity**, treatment eligibility, calendar validity, or the truth of the underlying observations. A URL supplied by a researcher is not proof of authoritative origin.

## Audit finding
Phase 283 requires only a dictionary with `source_authenticated=False` and valid shape, while Phase 286 requires explicit negative provenance flags. Neither is an authenticated ingest workflow. Therefore a passing HAC inference gate is not evidence that the September pretrends, substantial October 2025 placebo effect, or November reform comparisons were measured on genuine SEC records.

## Mandatory historical admission
Before computing historical estimates: obtain source files from documented authorized URLs; record retrieval timestamps, byte counts and SHA-256; separately verify publisher/source identity and source schema; reconcile security identifiers, exchange sessions, treatment assignment and matched rosters; record permission for redistribution. Preserve original files privately when redistribution is unverified; publish checksums, transformation code and permitted derived aggregates instead.

## Research status
No authenticated historical SEC observations, historical pretrend coefficients, placebo statistics, causal estimates or historical figures were produced in this session. September pretrends and the substantial October placebo warning remain unresolved. Weighting, security/exchange composition, selection sensitivity and joint matched-group/common-date serial-dependence-aware inference still require execution on authenticated observations. Previously recovered ZIPs and prior papers/charts were not imported; the complete archive inventory is still outstanding.

**No causal effect is established.** The November 14, 2026 manuscript target is conditional. Next: publish and rerun the source-verification implementation and tests, inventory recoverable historical files, authenticate original SEC inputs, then execute September and October diagnostics before any November interpretation.
