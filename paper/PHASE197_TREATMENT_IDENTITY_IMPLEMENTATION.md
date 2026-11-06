# Phase 197 — Published treatment-identity audit (2026-11-06)

This checkpoint follows Phase 196 and publishes an executable structural audit with ten deterministic tests. The audit compares treatment and matched-group labels by (security, exchange), allows intentionally disjoint historical windows, detects unpaired count/volume rows and duplicate keys, and rejects malformed inputs. Its `treatment_authenticated` field is always false: stable labels cannot authenticate historical round-lot classifications.

## Verification and limitations
A local standalone implementation with the same audit logic passed ten constructed-data unittest cases on 2026-11-06. The repository test imports `scripts.phase197_treatment_identity` and is intended to run from the repository root with `python -m unittest discover -s tests -p 'test_phase197_treatment_identity.py'`. A fresh checkout of the published files has not yet been executed. This is not SEC-data analysis.

The check is deliberately conservative but incomplete: it does not validate trading holidays, source data, identifier histories, treatment effective dates, price-based round-lot reconstruction, or selection and weighting. Security-level switches may be legitimate and must be reconciled against dated source rules, not automatically dropped. Equal-sized or disjoint placebo windows do not guarantee common security support. September pretrends and the substantial October 2025 placebo signal remain unresolved. No causal effect is established.

## Publication inventory
New in Phase 197: `scripts/phase197_treatment_identity.py`, `tests/test_phase197_treatment_identity.py`, and this note. Previously recovered historical ZIPs, authenticated original SEC daily panel, and period-specific treatment provenance have not been imported in this phase. Do not publish unlicensed original datasets. Next: clean-checkout test, authenticate original daily data and treatment map, then fixed-roster pretrend/placebo estimation with common-date and serial-dependence-aware inference.
