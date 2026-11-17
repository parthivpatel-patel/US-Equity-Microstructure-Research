# Phase 437 — Source-byte-bound support diagnostics (2026-11-17)

## What changed

Phase 436 identified that observation-count equality does not establish common source identity. This phase adds `scripts/phase437_source_bound_gate.py`, which reads a CSV file **once as bytes**, computes SHA-256 and byte length, runs the existing Phase 432 daily fixed-security audit and Phase 433 calendar audit on separately parsed copies of those same bytes, and evaluates the existing Phase 435 integrated support gate. Both diagnostic reports and the combined result carry the source digest. The combined JSON includes both diagnostics and the explicit `historical_effect_estimated: false` marker.

This avoids the post-hoc manifest weakness for these two diagnostics: a changed file of identical length will produce a different digest. It does **not** authenticate SEC origin, correct treatment assignment, licensed data provenance, matching construction, or any causal effect. For reproducibility, retain the original input privately where redistribution is prohibited and record its independently authenticated origin.

## Execution and verification

Seven constructed-data regression cases are published in `tests/test_phase437_source_bound_gate.py`, covering valid paired support, same-length mutation, absent post-period support, unpaired treatment arm, duplicate observation, empty bytes, and invalid UTF-8. Python syntax compilation of the local prototype succeeded. An attempted local unittest run was blocked because the prior-phase repository modules could not be downloaded into the isolated execution container (network name resolution failed). **The seven tests are therefore not claimed as passed**; execute them from a complete repository checkout using:

```sh
python -m unittest discover -s tests -p 'test_phase437_source_bound_gate.py' -v
python scripts/phase437_source_bound_gate.py path/to/authenticated_panel.csv --output phase437_result.json
```

The latter command has not been run on historical observations. No fabricated output or numerical result is presented.

## Outstanding publication blockers

The November 14, 2026 target was missed. The manuscript remains not publication-certified. Historical September pretrends, substantial October placebo, treatment authentication, selection and weighting sensitivity, security/exchange controls, common-date and serial-dependence-aware inference remain unresolved. The original SEC daily panel and historical matching assignments are not recovered here. Historical research ZIPs and the Phase 430 prototype/tests remain unverified or unpublished; this phase imports none. No licensed data or secrets are included.

## Next step

Execute these tests on the exact published checkout, then use independently authenticated historical inputs to run the bound gate. If it passes, reproduce pretrend and placebo diagnostics on a fixed-security/common-date matched sample with date- and matched-group-aware uncertainty; do not promote structural validation to causal identification.
