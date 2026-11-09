# Phase 256 — Exact date-block sign-flip diagnostic (2026-11-09 UTC)

## Verified execution
Created an exact enumeration diagnostic for already constructed, date-indexed treated-minus-matched-control contrasts. Eight deterministic Python unittest cases passed locally (0 failures), including small-sample exact probabilities, zero contrasts, malformed observations and enumeration limits. For synthetic values [1,1,1], the two-sided sign-flip tail fraction is 2/8 = 0.25. This is **not** an estimate from SEC data.

The script enumerates 2^n joint date-sign assignments (maximum 18 dates by default) and computes the two-sided absolute-sum tail fraction. It does not independently construct matching groups, authenticate observations, estimate security/exchange effects, or adjust for multiplicity. One aggregate contrast per date must already be defined using frozen, documented weights and a common observation roster.

## Identification and inference warning
A date-level sign-flip test is exact only under the required joint sign-symmetry/randomization null. Common-date shocks, serial correlation, heteroskedasticity, overlapping placebo windows and data-driven treatment selection do **not** automatically satisfy this assumption. In particular, flipping individual dates independently can break serial dependence. Therefore this is a software diagnostic and conditional reference calculation, **not a validated historical p-value**. The earlier Phase 255 overlap component count is not an effective sample size and cannot justify sign-flip exchangeability. For historical inference, specify a defensible dependence-preserving design (e.g., sufficiently long block resampling with appropriate sensitivity checks), fixed security/exchange controls and family-wise placebo handling before interpreting significance.

## Reproduction
Run `PYTHONPATH=scripts python -m unittest discover -s tests -p 'test_phase256_date_signflip.py' -v`. The isolated local test execution passed eight cases. A complete repository checkout and full suite were not executed.

## Outstanding evidence and publication inventory
No authenticated SEC historical observations, September pretrend coefficients, October 2025 placebo estimates or reform causal effects were produced. Treatment classification and SEC source/calendar authentication remain open; selection and weighting sensitivity remain unresolved. Previously recovered research ZIPs and unpublished Phase 253/254 scripts/tests were not accessible for authenticated import. This phase adds only the listed script, tests and report; it does not claim a complete historical artifact inventory. November 14, 2026 publication remains conditional.

## Next
Authenticate original source files and treatment mapping; recover and inventory historical archives where permitted; run fixed-roster September/October placebo and pretrend models with security/exchange effects and serial/cross-sectional dependence-aware inference. Do not interpret this conditional sign-flip reference as valid inference without verifying its null assumptions.
