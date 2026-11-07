# Phase 208 — Fixed-roster matched-group contrasts with date-level HAC

## Purpose
Bridge the previously separate Phase 200 common-date contrast, Phase 201 date-level HAC and Phase 207 fixed-roster admission concepts in a single fail-closed descriptive analysis. The implementation is new; no historical SEC observations are analyzed in this phase.

## Estimand and computation
For each observed trading date and matched group, compute the arithmetic mean outcome of treated security/exchange units minus the arithmetic mean of controls. Average group contrasts with equal group weight. The security/exchange roster and each unit's group/treatment assignment must remain constant across all supplied dates. Compute Bartlett-weighted Newey–West standard errors for the mean of the resulting date series at explicitly supplied lag bandwidths. Both count and volume must be run separately; mixed-outcome input is rejected.

## Admission and caveats
Reject empty panels, duplicate or unordered calendar dates, fewer than 20 dates by default, missing fixed-roster cells, duplicate observations, invalid values, treatment switches, unmatched groups, mixed outcomes and invalid HAC lags. The supplied calendar is NOT independently authenticated. The function intentionally returns source_authenticated=false, treatment_authenticated=false and causal_effect_established=false.

HAC over the aggregated date series addresses serial dependence in that descriptive series but does not establish causal identification, handle all cross-sectional dependence, or guarantee finite-sample validity. Equal group weighting is one choice, not a resolution of weighting sensitivity. Date gaps, exchange-specific closures, stale identifiers, selection and survivorship must be audited upstream.

## Validation and remaining blockers
The implementation and ten regression cases were developed with constructed data; ten local prototype tests passed before publication. Exact GitHub-published files and the full repository suite require clean-checkout execution. No authenticated historical panel, treatment mapping, source hashes or recovered research ZIPs were imported in this phase.

The substantial October 2025 placebo and September pretrends remain identification warnings. No post-reform causal conclusion is justified. Before manuscript acceptance: authenticate SEC source observations, validate round-lot assignments against contemporary Nasdaq notices and price history, audit expected exchange sessions, freeze matched support, estimate pretrends and multiple placebo dates, compare equal-group versus alternative weights, and report date-level and other dependence-aware inference.

## Reproduction
From repository root: `python -m unittest tests.test_phase208_fixed_roster_hac -v`. Import: `from scripts.phase208_fixed_roster_hac import analyze`. The function expects one selected outcome per call, records with date/security/exchange/group/treatment/outcome/value, and an explicit ordered session roster.

## Archive inventory
No historical ZIPs, original papers, charts or historical source files were newly recovered or published in this phase. Their completeness, permissions and provenance remain unverified. Do not mistake the test fixtures for empirical data.
