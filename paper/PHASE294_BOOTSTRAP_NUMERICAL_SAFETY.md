# Phase 294 — Bootstrap numerical overflow mitigation

## Scope and evidence
The Phase 293 audit identified an overflow hazard in the Phase 289 estimator. This phase changes the estimator to scale finite values before summing weighted exchange contrasts, common-date resample means, and the overall mean. The existing provenance guard, date validation, deterministic resampling, and noncausal return flags remain unchanged.

The new tests cover extreme finite same-sign values, cancellation, very large pair-count weights, ordinary weighted arithmetic, and both helper functions. **These tests are committed but have not yet been executed against the published checkout.** Passing tests must not be asserted until independently run.

## Limitations
Scaling prevents the identified intermediate-overflow case, but does not authenticate source files, exchange calendars, treatment assignment, or identify causal effects. Extreme floating-point cancellation and rounding require additional numerical scrutiny. The circular common-date bootstrap does not yet resample matched-security groups. September pretrends and the substantial October 2025 placebo remain open identification warnings.

## Artifact and publication inventory
Published this phase: updated Phase 289 estimator, Phase 294 regression tests, this report. Not yet verified or imported: recovered historical ZIPs, earlier source-manifest prototypes, authenticated SEC raw observations, treatment source files, original exchange calendar, and complete manuscript/reproducibility archive. Do not represent these as available or published.

## Next verification
Run `python -m unittest tests.test_phase289_common_date_block_bootstrap tests.test_phase294_numerical_safety` in an exact clean checkout. Then authenticate raw SEC files, source timestamps and official calendars; only after authentication execute fixed-roster September and October placebo analyses with common-date and matched-group resampling, exchange controls, and weighting sensitivity. No causal claim is authorized.
