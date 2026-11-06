# Phase 189: Two-way clustered variance failure modes (2026-11-06)

## Scope and provenance
This phase independently examined the exact published Phase 187 estimator and Phase 188 reference test using the connected GitHub repository. The new diagnostic script uses **constructed matrices only**, with no SEC observations or new empirical effect estimates. The local prototype passed five deterministic unittest checks on 2026-11-06. The published test imports the repository module under scripts/; fresh-checkout execution of that exact published test remains to be verified.

## Verified methodological result
The conventional two-way cluster inclusion–exclusion variance is not guaranteed nonnegative in finite samples. For the 2 × 2 constructed matrix [[1, -1], [-1, 1]], the group and date score sums are zero, while the intersection term is positive. Therefore the computed variance is negative and the standard error must be reported as undefined rather than silently truncated to zero. This is a mathematical/software diagnostic, **not a market-data finding**.

The diagnostic additionally checks a constant matrix (zero variance), additive group/date effects (positive variance), transposition invariance and rejection of unbalanced matrices. The Phase 187 implementation already flags negative variance; this adds an explicit reproducible failure-mode fixture and an independently coded calculation.

## Interpretation and unresolved threats
These tests do not establish validity of asymptotic inference with few clusters, overlapping windows, common calendar shocks or serially correlated observations. They do not authenticate the round-lot treatment assignment or SEC security/exchange daily panel. September pretrends and the substantial October 2025 placebo movement continue to preclude a defensible causal claim. Selection, weighting and historical placebo-date membership remain unverified.

## Publication and archive inventory
New: one standard-library diagnostic script, one unittest file and this report. No recovered historical ZIP, PDF, manuscript, chart, raw SEC panel or Nasdaq treatment snapshot was imported; source access, checksums and redistribution permissions remain unverified. Previously published artifacts are preserved.

## Next concrete task
Run both Phase 188 and Phase 189 tests from a clean checkout, then prioritize authenticated daily observations, matched roster and exact eligible placebo dates before producing any security/exchange-controlled empirical estimates. November 14, 2026 remains a conditional target, not a validated completion claim.
