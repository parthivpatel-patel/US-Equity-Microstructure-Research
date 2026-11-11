# Phase 305 — Declared-universe coverage gate

## Finding
The Phase 304 panel-key validator checks only security/exchange pairs present in the input. A pair entirely absent from the input cannot be identified as missing. This is a coverage blind spot, not proof that the SEC omitted records.

## New implementation
`scripts/phase305_universe_coverage.py` compares observations with an **externally declared** security/exchange universe crossed with expected dates. It flags wholly absent pairs, missing cells, unexpected cells and duplicate composite keys. It rejects malformed dates and identifiers. It does not silently equate absence with zero activity.

## Verification and limits
Nine deterministic synthetic regression tests were executed locally with zero failures before publication. The published checkout has not been independently executed. The declaration of the expected universe is **not authenticated** by this tool: delistings, changing exchange eligibility, holidays, publication thresholds and genuinely absent observations must be handled upstream. All provenance and causal authorization flags remain false.

## Empirical interpretation
No historical SEC observations were analyzed in this phase. September pretrends, the substantial October 2025 placebo warning, November treatment authentication, security/exchange confounding, weighting sensitivity and matched-security/common-date serial-dependence inference remain unresolved. No causal effect is established.

## Next
Authenticate the SEC observation source, exchange calendar and security/exchange membership intervals; apply coverage checks only to eligible cells. Then run placebo and pretrend diagnostics with declared cohorts and hierarchical inference. Previously recovered historical archives remain unimported and incompletely inventoried.
