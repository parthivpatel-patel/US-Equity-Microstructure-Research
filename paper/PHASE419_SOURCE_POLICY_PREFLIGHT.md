# Phase 419 — Reproducible as-of-time and public-host syntax gate (2026-11-16)

## Change
Added `scripts/phase419_source_policy.py` and `tests/test_phase419_source_policy.py`. The new deterministic policy check rejects retrieval timestamps beyond an explicit UTC as-of time plus a configurable 0–3600 second tolerance; rejects localhost, loopback, private/non-global IP literal hosts, and malformed hostname syntax; and rejects URL userinfo. It is a **separate policy preflight** for the Phase 417 local-byte integrity audit, not a replacement. The caller must run both. No DNS lookup or network fetch occurs.

## Validation and limitations
Fifteen deterministic local tests passed on a standalone copy of the implementation. The GitHub-published checkout has not been executed. The tests use constructed metadata only; no historical SEC data was analyzed. A syntactically public hostname (including `example.com`) can still be non-authoritative. A domain may also resolve to private IPs; DNS is not resolved here. An as-of time supplied by the same manifest author is not an independent attestation. `POLICY_PASS_NOT_AUTHENTICATED` explicitly prevents treating policy compliance as source authentication. A separate trusted upstream artifact record, independently verified publisher provenance, original treatment roster, and rights determination remain mandatory.

## Research and release gate
The historical panel, original 204-control mapping, and recovered ZIPs were unavailable in this run; no empirical estimates or causal claims. September pretrends, October placebo failures, treatment authentication, sample selection, estimator weighting, and matched-group/common-date/serial inference remain open. The November 14 deadline was missed and the paper is not publication-certified. Prioritize recovering and verifying historical data before further effect estimation.
