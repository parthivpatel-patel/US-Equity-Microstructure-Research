# Phase 248: fail-closed historical-input provenance gate

Date: 2026-11-08. Scope: independent November 3, 2025 U.S. round-lot reform study.

The Phase 247 guarded placebo scanner validates structural dates and reports overlap but does not independently authenticate source observations, exchange sessions or treatment assignments. This phase adds an **additive**, standard-library-only input admission diagnostic.

`scripts/phase248_authentication_gate.py` checks that a declared manifest contains source URL, retrieval timestamp, SHA-256, calendar reference, treatment reference and rule version, and license-review note; it recomputes SHA-256 from local bytes. Missing fields, absent files, malformed digests and changed bytes fail closed. A matching digest proves only consistency with the declared hash, **not** source authenticity, accuracy, exchange-session validity, treatment validity or redistribution rights. Successful outputs explicitly mark these matters false/unverified.

Execution: `PYTHONPATH=scripts python -m unittest discover -s tests -p 'test_phase248_authentication_gate.py' -v`. Five isolated synthetic tests passed locally on November 8, 2026; this is not a complete repository integration test. No historical SEC data, historical coefficients or charts were produced.

**Outstanding:** obtain and authenticate original SEC data and authoritative exchange calendars; reconstruct historical round-lot treatment using versioned contemporaneous rules and prices; review redistribution licenses; inventory recovered ZIPs; run fixed-roster September pretrend and substantial October placebo tests with matched-security and exchange controls, common-date effects, dependence-aware uncertainty and selection/weighting sensitivity. This module is not yet wired into the historical estimator. The November 14 publication target is conditional. No causal effect has been established.
