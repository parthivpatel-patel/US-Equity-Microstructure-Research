# Phase 247 — Guarded placebo scan with observation-window overlap audit (2026-11-08)

## Scope and provenance

Read the published Phase 224, 242, 243, 244 and 246 implementations using the connected GitHub repository service. Added a new wrapper rather than modifying existing modules. It invokes the Phase 244 structural calendar/roster guard and Phase 242 common-date Bartlett HAC contrasts, then appends the Phase 246 shared-session diagnostic. The wrapper does not authenticate the original SEC records, the trading-session calendar, or the treatment roster.

## Executed verification

The local runtime could not resolve raw.githubusercontent.com, so the five dependencies were manually transcribed from connected-GitHub file responses into an isolated test directory. The new wrapper and tests were executed there with:

`python -m unittest -v test_phase247_overlap_guarded_scan.py`

Result: **6 tests passed, 0 failures, 0 errors**. This is an integration test against transcribed dependency sources, **not** a byte-for-byte authenticated checkout or full repository test-suite run. Synthetic weekday fixture: 14 observations; cuts [4,5,6], half-width 3, bandwidth 0. Three overlapping cut pairs share 5, 4 and 5 observation indices. The equal-cell and pooled-count descriptive contrasts were 3 and 6, respectively, across the three cuts. These numbers are artificial test-fixture values, **not** SEC market observations.

The tests also check disjoint windows, weekend rejection, mismatched supplied session rosters, invalid bandwidth and incomplete estimation windows. A weekday-only fixture is not an authoritative trading-session calendar.

## Statistical interpretation and limits

Overlapping placebo cuts reuse the same observations. This diagnostic makes that dependence visible but does not compute adjusted p-values, familywise error control, a joint max-statistic, or security-cluster robust inference. Disjoint observation windows can still be statistically dependent due to serial correlation and shared market shocks. HAC bandwidth 0 in the synthetic fixture is a software test setting, not a defensible historical bandwidth choice. Equal-cell and pooled-count estimands are kept separate.

## Unresolved historical research

The September 2025 pretrends, substantial October placebo warning, treatment assignment authentication, selection and weighting sensitivity, security/exchange controls, common-date and serial-dependence-aware inference, and original SEC source authentication are **not resolved**. No historical coefficients or figures were generated. Previously recovered research ZIPs and papers are not available in the execution environment; a complete archive inventory and permission review remain outstanding. **No causal effect has been established.**

## Next steps

Run exact committed files from a verified checkout, obtain authenticated SEC observation manifests and authoritative session rosters, predeclare placebo dates and multiplicity correction, then execute fixed-roster historical estimates with matched-group, security and exchange controls. Retain all previous warnings in the manuscript. Publication by November 14, 2026 remains conditional on validation.
