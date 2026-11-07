# Phase 205 — Calendar provenance admission (2026-11-06)

Phase 204 compared observed sessions with a supplied roster, but did not require provenance fields. Phase 205 adds explicit source URL, retrieval timestamp, market, timezone, deterministic document SHA-256, date-order and duplicate checks, and missing/extra observed-session diagnostics.

The calendar is **not authenticated** by these checks. An HTTPS URL, timestamp, and digest can describe an invented or incorrect calendar; `source_authenticated` is always false. The example.org URL in tests is synthetic and not a market-data source. Independent confirmation against an exchange publication and historical closure notices is mandatory. The digest is for reproducibility, not source truth.

Ten deterministic constructed-data unit tests passed locally with Python unittest. No SEC data, exchange calendar or historical treatment roster was imported, and no historical effect estimate was calculated. A clean-checkout run of the exact published versions remains pending.

September pretrends, substantial October 2025 placebo warnings, classification authentication, selection/weighting sensitivity, matched-group common-date comparisons, security/exchange controls, and serial dependence remain unresolved. No causal effect is established.

Historical ZIPs and earlier papers/code/charts: not imported in this phase; complete archive inventory remains unavailable. Do not redistribute third-party raw data absent license review.

Next: retrieve independently verifiable official session schedule and authenticated SEC panel, record source URL/access timestamp/checksum, run coverage audit, and only then estimate fixed-roster placebo and pretrend contrasts.
