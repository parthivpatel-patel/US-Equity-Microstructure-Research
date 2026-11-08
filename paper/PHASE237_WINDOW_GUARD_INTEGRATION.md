# Phase 237 — strict window guard integration

Date: 2026-11-08. Scope: independent November 3, 2025 U.S. equity round-lot reform study.

## Source inspection
Inspected existing published `scripts/phase235_structural_preflight.py` (blob 6822cb3880a91e840b11164765f2a22285b8a92f) and `scripts/phase236_window_guard.py` (blob 24159361d48e33b3876b99f87fb3d9e8a8cedebc). Phase 235 did not call Phase 236. The additive Phase 237 entry point now runs Phase 236 validation before Phase 235, and removes any legacy `calendar_authenticated` field in its result.

## Verification
Six deterministic tests passed locally with Python unittest on 2026-11-08. Tests exercise the actual Phase 236 validation logic and stub the Phase 235 downstream estimator; they reject empty early windows, noncanonical ISO dates, unordered sessions, dates missing from the supplied roster and generator input before estimator invocation. A valid fixture confirms forwarding and conservative provenance metadata. This is **not** a full estimator integration test. The local Phase 236 source was transcribed from the GitHub blob identified above.

## Interpretation
This change enforces structural consistency only. No authoritative calendar, raw SEC observations, security-level treatment assignment, historical coefficients, or figures were authenticated or estimated. The substantial October 2025 placebo, September pretrends, selection and weighting sensitivity, matched-security and common-date serial-dependence-aware inference remain open. No causal effect has been established.

## Archive status and next step
Previously recovered historical research ZIPs were not accessible in this session; no archive import or complete file-level inventory is claimed. Next: authenticate raw SEC files and authoritative exchange sessions, test the entire real dependency chain, then rerun fixed-roster placebo and pretrend analyses with sensitivity and dependence-aware uncertainty. November 14 manuscript target remains conditional.
