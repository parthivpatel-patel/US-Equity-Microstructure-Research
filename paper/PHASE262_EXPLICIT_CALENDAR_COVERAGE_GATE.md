# Phase 262 — Explicit calendar coverage gate (2026-11-09)

## Verified predecessor
Read `scripts/phase259_pretrend_audit.py` (blob `5f7f0f445e6c0e7a5c3c1328027cca6ef060365d`) and `paper/PHASE261_MISSING_SESSION_ADMISSION_AUDIT.md` (blob `a4fe0b1cc71696336f8c7721594fab9423a7c4b3`) before additive publication.

## Implementation
`scripts/phase262_calendar_gate.py` accepts an explicit, ordered calendar and matched date-pair outcomes. It rejects duplicate pairs, malformed outcomes and invalid calendar ordering; reports omitted sessions, extra sessions and partially covered pair rosters; and refuses sample admission when any defect exists. It never imputes missing values. The provided calendar is NOT authenticated by this function, and successful structural admission NEVER authorizes historical inference.

## Verification and caveats
Ten deterministic cases were run locally against the same algorithm in a standalone implementation: all passed. The published test file contains ten corresponding cases but was not rerun byte-for-byte after upload. All dates and values are illustrative synthetic fixtures, not SEC observations or authenticated exchange sessions. The function does not validate trading holidays, halts, security-specific trading eligibility, exchange identity, provenance or data licensing. An empty or wrongly defined roster can pass a complete-date test if not externally checked against a frozen treatment roster.

## Research implications
Apply this gate before Phase 259 pretrend or Phase 260 sensitivity estimation, only after independently authenticating the exchange calendar, treatment classification and raw SEC inputs. September pretrends and the substantial October 2025 placebo remain unresolved; a structurally admitted sample cannot establish causal identification or dependence-aware inference. Next: obtain source checksums and historical rosters, freeze eligible common dates, and execute placebo and pretrend models with security/exchange controls and serial-dependence-aware uncertainty.

## Publication inventory
This phase adds one script, one synthetic test file and this report. Earlier local-only Phase 252–254 code and recovered historical ZIP archives remain unverified and unpublished. No historical estimates, figures or licensed datasets were imported. November 14 manuscript completion remains conditional.
