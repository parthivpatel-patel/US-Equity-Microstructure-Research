# Phase 363 — Resolved-path duplicate integrity correction (2026-11-14)

## Finding
The Phase 362 manifest checker rejected duplicate literal path strings, but accepted two entries referring to the same actual file via `sample.csv` and `./sample.csv`. The defect was reproduced locally with constructed bytes before the fix. A symlink alias pointing to an in-root file could cause the same double counting.

## Correction and verification
The verifier now tracks resolved file paths as well as literal manifest paths, and rejects a second reference to the same resolved path. Four new deterministic tests passed locally: dot alias rejected, internal symlink alias rejected, ordinary single-file verification, and separate files containing identical bytes accepted. The published checkout and entire repository suite have not been executed. These tests are not empirical SEC market observations.

## Limitations and research status
This check does not detect hard-link aliases sharing an inode, and cannot authenticate historical source origin or licensing. The November 14 publication deadline is not met. The original 78 dated placebo observations, October placebo warning, September pretrends, Phase 130 contradiction, historical treatment and exchange-eligibility authentication, calibrated inference, and recovered historical ZIP inventory remain unresolved. Next: execute integrated tests and obtain authenticated permitted historical SEC data before any empirical claims.
