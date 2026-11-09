# Phase 272 — Historical pretrend admission requirements (2026-11-09)

This audit follows Phase 271. The placebo-grid implementation accepts sorted observed dates, but does not authenticate the expected trading-session calendar, original SEC observations, or the externally fixed treatment roster. Consequently its numerical results, if supplied with an incomplete panel, could appear valid while silently excluding missing sessions or never-observed matched groups.

## New verified software test
A local Python prototype of a fixed-window descriptive pretrend audit passed **10/10 deterministic synthetic unit tests** on 2026-11-09. Tests covered calendar-day linear slopes, adjacent-window mean differences, explicit nonauthorization, duplicate and reversed dates, nonfinite values, overlapping windows, empty windows, invalid minimum dates, and sparse dates. These are **synthetic** checks; the prototype was not imported into the repository in this session, and the complete repository suite was not run.

## Required historical analysis protocol
1. Independently retrieve original SEC market-structure security/exchange observations; record canonical source URLs, retrieval dates, SHA-256 hashes, licenses, and row-level parsing checks.
2. Authenticate the November 3, 2025 round-lot treatment assignment using contemporaneous UTP alerts and closing-price inputs, documenting exceptions.
3. Freeze a security/exchange matched-pair roster and independently authenticated expected session calendar **before** filtering observed outcomes.
4. Require every expected date × matched pair observation, or explicitly document and predefine treatment of gaps.
5. On the identical admitted sample, estimate September 2025 pretrends, multiple predeclared October placebo cutoffs, and November estimates. Include security/exchange controls and common-date shocks where identified.
6. Report pair-equal and alternative bounded weights; full-series HAC with cross-period covariance, lag sensitivity, and serial-dependence-aware bootstrap. Report failed placebo/pretrend diagnostics rather than filtering them away.

## Current publication limitations
No authenticated historical SEC data, treatment roster, historical coefficients, or genuine research figures were analyzed or generated in Phase 272. The substantial October placebo signal and September pretrend warnings remain unresolved. Prior recovered historical ZIPs, unpublished Phase 252–254 artifacts, and a complete publication inventory remain outstanding and were not imported. **No causal effect is established.** November 14, 2026 is a conditional target, not a verified publication date.
