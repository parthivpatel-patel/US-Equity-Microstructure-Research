# Phase 216 — Session-admitted joint-window HAC integration

**Scope:** software validation only. No historical SEC panel was accessed and no historical treatment effect or placebo coefficient was estimated.

This checkpoint connects the Phase 215 supplied-session-calendar gate to the Phase 213 joint-window HAC estimator. The gate executes before estimation. The combined function rejects missing or duplicated sessions, malformed windows, post-reform dates and invalid lag settings; it also checks that admission and estimation agree on window counts. Tests use constructed dates and contrasts, not market observations.

## Verification status

The new Python files passed syntax compilation locally. Full integration tests could not be run in this session because the container could not resolve the GitHub raw-content host to retrieve the existing dependency modules. The eight published test cases are **not claimed to have passed**. Execute from a clean repository checkout before interpreting their results.

## Interpretation and limitations

A complete panel relative to a **caller-supplied** calendar is not proof that the calendar is authoritative. This wrapper does not authenticate SEC source files, Nasdaq round-lot treatment classifications, security/exchange rosters, matching, weighting or trading-session metadata. Joint-window HAC retains covariance between windows but is not by itself a substitute for security/exchange dependence controls, common-date matched contrasts, pretrend checks or placebo falsification. The September pretrend and substantial October 2025 placebo warning remain unresolved. No causal effect has been established.

## Reproduction

From the repository root: `python -m unittest discover -s tests -p 'test_phase216_admitted_hac.py' -v`. No external dependencies required.

## Unpublished source archive inventory

Historical research ZIPs, original SEC observation files, provenance manifests and historical Nasdaq treatment mappings were not available for authenticated import in this checkpoint. Their contents and redistribution rights remain unverified. Do not interpret this note as a complete inventory of files held outside the repository.

## Next work

Run all published tests from a fresh checkout; obtain source-authenticated SEC panels and an independently verified exchange calendar; verify pre/post treatment mapping; apply fixed-roster common-date matched contrasts and September/October placebo diagnostics with bandwidth, weighting and cross-sectional dependence sensitivity. Publication target November 14, 2026 remains conditional.
