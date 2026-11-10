# Phase 281 — Identification and dependence audit (2026-11-10)

## Scope and evidence boundary
This is a mathematical and code-review audit, **not** a new estimate from authenticated SEC observations. Reviewed the existing `scripts/phase278_leave_exchange_out.py` from the public default branch (blob `8258d2600b48189441b82e9f2d35f7d280f415e8`). The script explicitly labels its inputs as admitted upstream and sets `source_authenticated=False` and `historical_inference_authorized=False`. No causal conclusion is warranted.

## Verified algebraic finding: exchange-equal and pair-weighted estimands
For exchange e and session t, let d[e,t] denote the admitted within-exchange matched-pair contrast, and n[e] the number of fixed matched pairs in that exchange. The script computes

- Pair-weighted session contrast: sum_e(n[e] * d[e,t]) / sum_e(n[e]).
- Exchange-equal session contrast: sum_e(d[e,t]) / E.

It then averages the session contrasts across observed dates. These coincide only under special conditions (e.g., equal n[e], or a contrast pattern orthogonal to the weighting difference). Thus they target different descriptive populations. A change in sign between them is **not** a software defect by itself; it is a substantive sensitivity result that must be reported.

### Hand-checkable counterexample (constructed, not SEC data)
With two exchanges, fixed pair counts n[A]=9, n[B]=1, and contrasts d[A]=+1 and d[B]=-3 on each of two dates, the pair-weighted contrast is (9*1+1*(-3))/10 = +0.6; exchange-equal is (1-3)/2 = -1. The sign reverses *without changing dates, treatment status, or observations*. The example proves that an aggregate sign alone cannot identify a reform effect.

## Newly identified guardrail
The Phase 278 function checks for duplicate dates but does not check that dates are sorted or authenticated against an external exchange-session calendar. It also computes mean contrasts, **not** HAC standard errors, simultaneous placebo inference, or a common-date block bootstrap. Upstream admission claims must be tested at the call site; passing an arbitrary dictionary directly to this function does not authenticate it. A leave-one-exchange-out sign flip is descriptive leverage, not a p-value or independent replication.

## Required historical analysis protocol
1. Authenticate original SEC source URLs, release versions, download timestamps, file hashes, units, numerator/denominator definitions, and any revisions; retain only redistributable materials in the public repository.
2. Reconstruct and independently authenticate the Nov. 3, 2025 round-lot treatment assignment with pre-specified closing-price reference dates and contemporaneous UTP notices. Freeze the affected-security roster and matching choices before estimating outcomes.
3. Join the full exchange-session calendar, enforce a complete common-date panel and stable security/exchange/pair roster, and separately report attrition, unmatched securities and nontrading sessions.
4. Estimate September pretrend diagnostics and the substantial October placebo on **the identical admitted panel**, then report the November contrast with pair-weighted and exchange-equal estimands and leave-one-exchange-out sensitivity.
5. For inference, retain the entire common-date vector across matched pairs and exchanges within each resampled block. Use predeclared block lengths and a moving-block or stationary bootstrap for serial dependence, plus full-series HAC sensitivity. Re-estimate every placebo and treatment contrast within each resample; do not independently resample exchanges or treat matched pairs as independent daily observations.
6. Preserve the adverse October placebo and September pretrend evidence in the manuscript even if a November estimate appears significant. Do not use a causal headline unless identification and falsification checks withstand scrutiny.

## Publication and archive status
This report contains no imported historical ZIP, authenticated historical coefficients, or newly generated empirical chart. Historical archives and earlier unpublished scripts/tests still require a source-by-source inventory, permission assessment, and file-size screening. The November 14 target remains conditional; an honest descriptive/limitations paper is preferable to an unsupported causal paper.

## Next reproducible deliverable
Add a fail-closed, externally supplied exchange-calendar and fixed-roster admission fixture to the estimation entry point; run the complete published repository test suite; then source-authenticate the historical panel and execute predeclared September/October/November contrasts.