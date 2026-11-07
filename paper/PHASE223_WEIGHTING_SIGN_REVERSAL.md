# Phase 223: weighting sensitivity can reverse a descriptive treatment contrast

Status: synthetic methodological counterexample, **not** historical SEC evidence. November 7, 2026.

## Design

After the Phase 222 rectangular-panel gate admits a complete security × exchange × date panel, compute two daily treated-minus-control hidden-execution rates: (1) arithmetic mean of security/exchange cell rates within each group, and (2) group pooled hidden-count divided by group pooled total-count. Both use the same observations but answer different descriptive questions. They must be reported side by side, not selected based on significance.

## Deterministic counterexample

For each of two constructed dates, treated exchange X has 9/10 hidden executions and treated exchange Y has 10/100. Control X has 4/10 and control Y has 40/100. Equal-cell treated-minus-control is (0.9+0.1)/2 - (0.4+0.4)/2 = **+0.10**. Count-pooled treated-minus-control is (19/110)-(44/110) = **-25/110 = -0.2272727...**. The sign reverses solely because the estimand's weights differ. These are fabricated integer fixtures for software testing, not estimated market statistics.

## Verification and limits

Six Python unittest cases passed locally, including sign reversal, two dates, permutation invariance, duplicate-cell rejection, missing-cell rejection and preservation of unauthenticated-source flags. The integration used a locally reconstructed copy of the Phase 222 module transcribed from the GitHub file fetched this session. The *exact published Phase 222 module* has not been executed in a clean checkout; that remains a required independent reproduction step. The new module itself is published separately under `scripts/` and imports the repository Phase 222 module.

No SEC observations, historical treatment labels, authenticated exchange sessions, matched-group weights, or archive ZIPs were available to this run. No historical coefficients, significance claims, empirical plots or causal claims are produced. Phase 222 complete-case selection may itself change the sample. The substantial October placebo warning and September pretrends remain open.

## Next empirical admission gates

Authenticate SEC file hashes, acquisition URLs and observation schema; authenticate the November 2025 treatment roster from historical Nasdaq notices and prices; authenticate the actual exchange-session calendar; preserve a matched security/exchange roster; report complete-case attrition and available-case sensitivity; calculate both weighting estimands on common dates; then apply dependence-aware inference and placebo-date sensitivity. The November 14 target is conditional on these gates.

## Historical archive inventory for this phase

Historical ZIPs, original manuscript drafts, empirical figures and prior code bundles: **not accessible in this session; not imported or re-published**. Redistribution permission and integrity hashes have not been verified. Existing public repository files are preserved unchanged.
