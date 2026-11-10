# Phase 280 — Temporal exchange influence: executable prototype and admission audit (2026-11-09)

## Local execution
Implemented a standalone Python diagnostic for predeclared early/late windows using a fixed pair-count roster by exchange, pair-weighted and exchange-equal contrasts, and leave-one-exchange-out late-minus-early comparisons. Nine deterministic unittest cases passed locally (9/9, zero failures). The prototype and tests were executed in the session workspace but are **not included in this commit**; the published repository checkout has not been tested. No historical SEC observations were used.

Constructed fixture: exchange X contains two pairs and exchange Y one pair. Two early dates use X=-2 and Y=5; two late dates use X=1 and Y=-1. The full pair-weighted mean is 1/3 in both windows, so its change is zero. Excluding Y gives an early mean of -2 and a late mean of 1, a change of +3. This is synthetic arithmetic, not a historical estimate.

## Audit and limits
The prototype checks strictly increasing ISO dates, duplicate dates, fixed exchange coverage, finite outcomes, positive integer (not Boolean) pair counts, valid cutoff and nonempty windows. Cutoff observations belong to the late window. It does **not** independently authenticate the exchange-session calendar, pair identities, source files or treatment assignments; a stable pair-count vector alone cannot establish a stable matched-security roster. Exchange-equal weights are a sensitivity estimand, not a causal adjustment. No inferential p-values or confidence intervals are authorized.

## Historical admission requirements
1. Obtain original SEC security-date-exchange observations, source URLs, file checksums, schemas and redistribution permission.
2. Authenticate the historical exchange-session calendar and verify missing/extra sessions; freeze treatment and matched-security assignments using independent contemporaneous sources.
3. Join security/exchange records to fixed matched pairs and verify identity persistence, not just counts.
4. Predeclare September trend and October placebo windows, cutoff rules, missingness, weighting and exclusion rules.
5. Estimate pair- and exchange-weighted contrasts with security/exchange controls; use matched-group and common-date resampling and full-series HAC lag sensitivity. Account for cross-cutoff covariance and report multiple placebo comparisons.
6. Treat the substantial October 2025 placebo and September pretrend warning as identification failures until convincingly resolved. No causal conclusion is currently warranted.

## Publication inventory
The Phase 280 prototype and its nine tests remain **unpublished**. Previously recovered historical ZIPs, papers, charts and earlier unpublished Phase 279 prototype/tests remain unimported and are not fully inventoried. No source-authenticated historical coefficient, figure or manuscript result was produced. Next priority: publish the tested code and tests, run the full repository suite, and authenticate SEC source data before historical inference.
