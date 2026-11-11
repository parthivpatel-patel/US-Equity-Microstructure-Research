# Phase 309 — Fail-closed eligibility input admission (2026-11-11)

## Scope and result
Read the published Phase 307 implementation and Phase 308 reproduction report before introducing a separate wrapper rather than overwriting prior code. Phase 307 permits empty trading calendars and eligibility universes; those are structurally ambiguous and should not be admitted to empirical analysis as valid panels.

New `scripts/phase309_admission.py` requires nonempty supplied sessions and eligibility intervals, checks record shapes and nonempty string fields, and rejects an eligibility universe that covers zero supplied sessions. It delegates duplicate, missing, unexpected, overlapping-interval, and date-order checks to the existing Phase 307 validator. Missing observations remain missing, never automatically zero.

## Reproduction
The Phase 307 source fetched via connected GitHub was reproduced in an isolated local workspace alongside the new module and tests. Command:

```sh
python -m unittest discover -s tests -p 'test_phase309_admission.py' -v
```

Observed: 11 tests passed, 0 failures, 0 errors (synthetic input only). This is not a full repository checkout or full test-suite run.

## Limitations
The wrapper does not authenticate the provenance of SEC observations, the exchange calendar, the eligibility universe, or treatment status. It does not establish whether a missing cell is expected under exchange reporting rules. It does not perform pretrend, placebo, matched-sample, security/exchange fixed-effect, or serial-dependence inference. Source-authentication and causal-inference flags remain false.

The substantial October 2025 placebo warning, September pretrends, treatment-roster uncertainty, selection and weighting sensitivity, and dependence-aware inference remain open. No authenticated SEC historical observations were analyzed. No causal effect is established.

## Archive and publication inventory
The previously recovered historical ZIPs, original papers, figures, and datasets were not available for authenticated file-by-file inspection in this session and have not been imported. Redistribution permissions and repository file-size checks remain outstanding.

## Next priority
Run the full published regression suite and authenticate original SEC files, security/exchange eligibility and trading calendar; then apply the gates to actual observations and estimate September pretrends and October placebo tests before any November interpretation. November 14 remains a conditional publication target.
