# Phase 250: Byte-integrity and historical-estimation policy bridge

Date: 2026-11-08. Independent U.S. round-lot research only.

## Verified repository review

Phase 248's `audit_input` returns `admitted=True` after a local SHA-256 match and nonempty provenance text, while explicitly returning false authentication indicators. Phase 249's `historical_estimation_allowed` requires five booleans but does not verify their external evidence. Both source files were read from the public repository before this additive implementation.

## New bridge and execution

`scripts/phase250_provenance_bridge.py` calls the existing Phase 248 byte check and Phase 249 admission policy. It refuses missing or nonboolean attestations, reports failed checks, and labels caller-supplied attestations as unverified. A byte mismatch fails even if every external flag is true. Byte agreement alone never implies source, calendar, treatment or license authentication.

Six isolated Python unittest cases passed locally (0 failures, 0 errors) on synthetic file bytes. The execution used local transcriptions of the two published dependency implementations; it was not a verified full repository checkout or complete test suite. Run the published test with `PYTHONPATH=scripts python -m unittest discover -s tests -p 'test_phase250_provenance_bridge.py' -v`.

## Important limitations

The bridge **does not independently verify caller attestations**. Its all-true case demonstrates conditional policy logic only; a caller can falsely claim authentication. A production admission system must bind each attestation to independently reviewable evidence, hashes, dates and reviewer provenance and must distinguish analytical use from public redistribution rights. The module is additive and has not been wired into the historical estimator.

No authenticated SEC observations were analyzed. No historical estimates, figures, treatment validation, September pretrend resolution or October placebo resolution are claimed. Security/exchange controls, matching, common-date comparisons, weighting sensitivity, multiplicity and serial/cross-security dependence-aware inference remain necessary. Recovered historical ZIPs were not accessible for authenticated inventory or import.

## Next

Verify full-repository execution, obtain source and exchange-session authentication, establish fixed treatment rosters and an evidence-backed attestation ledger, and only then run historical placebo/pretrend specifications. The November 14 manuscript deadline is conditional. No causal effect is established.
