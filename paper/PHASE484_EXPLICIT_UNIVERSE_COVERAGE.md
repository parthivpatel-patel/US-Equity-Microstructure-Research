# Phase 484 — Explicit-universe coverage and authentication gate

**Status:** constructed-fixture tests only. No historical SEC observations or treatment assignments were analyzed.

The preceding Phase 483 script calculates missing cells relative to the *observed* security-exchange union. That denominator can understate missingness when a security-exchange pair is absent throughout the supplied panel. This phase adds an explicit-universe requirement: the analyst must separately supply an eligible security/exchange roster, a trading calendar, and a panel. The Python implementation validates unique roster keys, duplicate observation keys, calendar membership, finite outcomes, and exact CSV schemas; it reports expected cells, missing cells, explicit observed zeros, daily coverage, complete units, and SHA-256 fingerprints.

A local implementation passed **seven** constructed-data unit tests on November 19, 2026: expected counts, fingerprint sensitivity, duplicate panel keys, duplicate universe keys, nonfinite outcomes, ragged rows, and observations outside the supplied universe. These do not establish SEC source authentication, historical coverage, or causal effects.

**Identification caution:** A fixed roster is not necessarily the correct risk set. Exchange eligibility, listing status, and trading activity can vary by day. A subsequent phase must authenticate an eligibility-by-date universe, reconcile source provenance and licensing, and separately test balanced versus changing-composition estimators. Never turn missing rows into zeros. September pretrends and the substantial October placebo warning remain unresolved. The November 14 publication deadline was missed; manuscript not certified. Phase 430/436 archives and Phase 472 executable package remain unimported.
