# Phase 249: provenance-to-estimation admission distinction

Date: 2026-11-08. Independent round-lot reform research only.

## Verified source review
The published Phase 248 gate returns `admitted: True` when declared metadata is nonempty and the local file matches its declared SHA-256. That same response explicitly sets independent source authentication, calendar authentication, treatment authentication, and redistribution authorization to false. Thus the word *admitted* means **byte consistency only**, not admission to historical estimation. A downstream caller that treats `admitted` as a sufficient authorization condition would silently bypass the unresolved historical-source and treatment-authentication requirements.

## Added control
`scripts/phase249_admission_policy.py` separates a conservative historical-estimation policy from the Phase 248 byte-integrity check. It requires five explicit booleans: verified bytes, independently authenticated source, authenticated calendar, authenticated treatment, and confirmed license authorization. Any false check rejects. Strings such as `"yes"` are rejected, rather than coerced to true. **This module does not produce or validate the attestations** and is not wired into the historical estimator. A true result is only a policy decision conditional on the truth of caller-supplied attestations, never independent evidence.

## Reproducibility and limitations
A four-case equivalent policy fixture was executed locally using Python unittest (4 passed, 0 failed); the published test file is a repository-importable formulation of those cases, not a claim that the full repository suite was run. The isolated fixture additionally verified SHA-256 consistency of synthetic bytes and showed why this cannot authenticate market provenance. Run published tests with `PYTHONPATH=scripts python -m unittest discover -s tests -p 'test_phase249_admission_policy.py' -v`.

No historical observations, placebo coefficients, causal estimates, or figures were produced. September pretrends, substantial October 2025 placebo findings, fixed treatment rosters, matching/weighting sensitivity, common-date and security/exchange dependence-aware inference remain open. No recovered archives were available for authenticated import or complete inventory verification. The November 14 manuscript target remains conditional; no causal effect has been established.

## Next
Integrate this policy as a mandatory pre-estimation guard, document independently checkable provenance attestations and licensing, then run exact-repository tests and authenticated historical placebo/pretrend analyses.
