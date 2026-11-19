# Phase 487 — Pre/post eligibility composition audit (2026-11-19)

## Verified local work

A standalone Python prototype and six deterministic unittest cases were executed locally: **6 passed, 0 failed**. The fixture includes eligible security–exchange–date keys, an explicitly observed zero, a missing eligible cell, and a security–exchange unit eligible only after a cutoff. The prototype checks that cutoff dates have eligible dates on both sides and rejects observations outside the eligibility universe.

The analysis differentiates **eligible both/pre-only/post-only** units from **observed both/pre-only/post-only** units. These are not interchangeable: a unit can be eligible but unobserved. An explicitly recorded zero is an observation, not a missing record.

## Interpretation

A fixed security–exchange panel is not a valid default universe without date-specific eligibility authentication. Comparing observed membership alone can mislabel legitimate listing or venue eligibility changes as data loss. Conversely, eligibility data that are reconstructed from observed outcomes can mechanically conceal missingness.

For the October 2025 placebo and September pretrend analyses, report pre/post eligible cells, observed cells, missing cells, explicit zeros, and unit intersections by treatment cohort and exchange. Only after source provenance and treatment assignments are authenticated should these diagnostics inform estimation. Standard-error adjustments do not repair composition bias.

## Scope and publication gap

**No authenticated SEC observations or historical effect estimates were produced.** The local prototype and six tests are not published in this commit; they require an independently verifiable executable publication step. The previous Phase 430/436 historical archives and Phase 472 package also remain outstanding. This report must not be cited as an empirical result or executable replication package.

The November 14, 2026 target was missed. The paper remains **not publication-certified**. Outstanding gates: SEC source authentication, date-specific eligibility and treatment authentication, September pretrends, October placebo diagnosis, estimator/weighting sensitivity, and matched-group plus common-date and serial-dependence-aware inference.
