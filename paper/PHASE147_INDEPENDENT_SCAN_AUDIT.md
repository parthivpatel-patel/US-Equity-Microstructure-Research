# Phase 147 — independent breakpoint scan audit (2026-11-04)

## Scope and verification

Read the published Phase 146 implementation and methodology before creating a new file. Executed a local independent OLS-versus-convolution test with 400 seeded synthetic comparisons spanning series lengths 40, 41, 65 and 87 and window sizes 3, 5, 10 and 20. All 400 agreed within absolute tolerance 1e-12. Additional executed tests confirmed a single common calendar-block index sequence and a near-zero maximum breakpoint statistic for a nine-group panel with heterogeneous linear trends. The published test is a cleaned, equivalent version of the locally executed audit; it has not yet been rerun from a fresh checkout.

**New code-quality finding:** Phase 146 accepts `window=1`, despite an undefined OLS slope denominator. The result is NaN-valued observed and bootstrap statistics, potentially yielding a misleading finite-simulation tail probability. The audit reproduces this invalid-input behavior; Phase 146 itself was deliberately not overwritten. Future production inference should reject noninteger or <2 windows, empty groups, invalid block sizes, noninteger draw counts, and all nonfinite outputs before reporting a p-value.

## Inference limitations

This is numerical software verification, **not** new SEC market-data analysis. The group-level residual-block bootstrap's null detrending, stationary-residual assumptions, cross-group dependence, and treatment composition remain unvalidated. The September pretrends and October 2025 information-event/placebo warning prevent a causal interpretation. A maximum-statistic bootstrap handles scanning multiplicity only if its null distribution is itself credible.

## Data and publication status

The repository's Phase 144 inventory documents missing original SEC security/exchange observations, authenticated Nasdaq treatment assignments, and the Phase 131 processed panel. Historical ZIP archives were not available for inspection or licensing verification in this run; none were imported. No empirical p-values, new market estimates, or figures were generated.

## Reproduce and next gate

With NumPy installed, run `python tests/test_phase147_joint_scan_independent_audit.py`. It imports the existing Phase 146 test file by path. Next: add fail-closed input validation to a separately reviewed version of the bootstrap, verify the published test from a fresh checkout, then recover and authenticate the empirical panel and source records before any whole-scan inference.
