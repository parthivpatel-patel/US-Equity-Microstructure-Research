# Phase 188 — Independent covariance cross-check and execution provenance (2026-11-06)

## Verified repository inspection

Read the exact public contents of `scripts/phase187_cluster.py`, `tests/test_phase187_cluster.py`, and `paper/PHASE187_CLUSTER_IMPLEMENTATION.md` using the connected GitHub service. Phase 187 computes an intercept-only, balanced matched-group × date, two-way clustered descriptive variance with group, date, and singleton-intersection terms. It does not estimate a security/exchange-adjusted difference-in-differences coefficient.

## New audit artifact

`tests/test_phase188_cluster_reference.py` supplies a separately expressed intercept-OLS sandwich-score reference calculation, scaling and label-permutation checks, and a constructed-data fixture. It contains no market observations and must not be described as an empirical result. The new reference test has been published but **not executed against a fresh checkout**. The previously reported Phase 187 ten-test run is not a substitute for execution of this exact new test.

## Execution environment blocker

Attempted to retrieve the public raw GitHub script and test files into a clean local directory for a fresh-checkout-style run. The attempt failed because this execution container could not resolve `raw.githubusercontent.com` (DNS error). The GitHub connector did successfully fetch their contents, but no local test execution is claimed for Phase 188. Re-run from an environment with repository checkout:

```bash
python -m unittest discover -s tests -p 'test_phase187_cluster.py' -v
python -m unittest discover -s tests -p 'test_phase188_cluster_reference.py' -v
```

## Statistical interpretation

The Phase 187 formula is for a balanced intercept-only mean, not a regression with security and exchange fixed effects. Its cluster correction is one particular CR1-style convention; alternative finite-sample corrections, few-cluster methods, serially dependent overlapping windows, and non-nested date membership can materially affect uncertainty. A two-way clustered standard error alone does not resolve the substantial October 2025 pre-reform shift, September pretrends, treatment misclassification, matching sensitivity, or source authentication.

## Source and publication inventory

This phase did not import original SEC data, treatment snapshots, or historical ZIPs, PDFs, figures, and manuscripts. Existing archives cannot be certified as published without file-by-file access, checksums, and redistribution review. No causal reform effect is established.

## Next action

Run the exact new test from a clean checkout; authenticate and checksum the security-date-exchange SEC panel and round-lot historical classification; preserve a fixed matched-group roster and actual placebo-date memberships; only then run common-date, September pretrend, October placebo, security/exchange-controlled and serial-dependence-aware estimators. The November 14 target remains conditional.
