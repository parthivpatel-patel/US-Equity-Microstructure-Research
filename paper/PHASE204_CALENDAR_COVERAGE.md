# Phase 204 — Explicit trading-session coverage gate (2026-11-06)

Phase 203 checks that dates are weekdays, but weekdays are not an authenticated US-equity trading calendar: exchange holidays, special closures, and missing observed sessions require a separate source. This module compares ordered daily contrasts to an explicitly supplied, independently verifiable expected-session roster, reports missing and unexpected dates, and fails admission on either discrepancy or an empty panel. It deliberately does not generate an exchange calendar from weekdays, or certify the supplied calendar as authentic.

Ten deterministic local unit tests passed on constructed examples (2025-11-03 through 2025-11-05); no historical SEC sample was used. Exact published-file checkout execution remains pending. A complete constructed sample is admitted structurally, not authenticated empirically.

**Identification remains unresolved:** September 2025 pretrends, substantial October placebo results, historical Nasdaq treatment mapping, weighting/selection sensitivity, security/exchange composition, and common-date and serial dependence. The audit cannot substitute for independently authenticated market-session dates or data provenance. No causal effect established.

**Next:** acquire verifiable official exchange session schedule and original SEC panel, compare their dates using this gate, then run fixed-roster placebo and pretrend estimators. Historical research ZIP inventory/import remains incomplete; no archive imported in this phase.
