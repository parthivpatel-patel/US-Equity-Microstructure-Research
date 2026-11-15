# Phase 379 — Exchange-stratified complete-case attrition gate

Date: 2026-11-15. Scope: methodological software, not empirical SEC findings.

Phase 378 requires a complete Cartesian product of pairs, exchanges, dates, and treatment/control arms. This gate enumerates missing keys and measures the retained matched pairs for each exchange before any balanced-panel estimator is applied. The candidate pair universe is the union of observed pair identifiers, and the exchange universe is the union of observed exchange identifiers. Consequently the resulting attrition measure is conditional on the observed universe: wholly absent pairs or exchanges cannot be discovered without an external authenticated roster. It also does not measure selection into the original 68 treated / 204 control security universe.

For each exchange, retention equals the number of pairs with both arms on every required date divided by the number of candidate pairs. The gate uses exact integer checks and Fraction retention values; it does not impute observations or estimate a treatment effect. A fixture with two pairs and two exchanges has 16 expected records. Deleting one control record in exchange Y reduces Y retention to 1/2 while X remains 1. These are constructed fixtures, not SEC estimates.

Seven deterministic local tests passed on 2026-11-15. The full published repository suite and real-data execution have not been performed. The October 2025 placebo warning, September pretrends, treatment assignment authentication, source bytes, historical ZIP inventory, original dated placebo estimates, exchange-level selection, weighting sensitivity, and common-date/serial-dependence-aware inference remain unresolved. No causal inference is warranted.

Next: compare observed pair/exchange/date coverage to authenticated external rosters and raw-source manifests, quantify excluded pairs, then rerun pretrends and placebo estimates on both the original and complete-case universes.
