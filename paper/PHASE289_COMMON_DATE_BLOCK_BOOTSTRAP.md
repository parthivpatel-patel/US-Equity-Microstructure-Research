# Phase 289 — Common-date circular block bootstrap: implementation and limits

Date: 2026-11-10. Scope: **software/methodology verification only**. No historical SEC data were authenticated or estimated.

## New work
Added `scripts/phase289_common_date_block_bootstrap.py` and `tests/test_phase289_common_date_block_bootstrap.py`. The estimator uses fixed positive matched-pair counts, constructs one treated-minus-control exchange-weighted contrast per date, and resamples **the same circular blocks of dates across every exchange**. This preserves contemporaneous exchange co-movement in the resampled aggregate and short-run temporal structure up to the chosen block length. Pair-count and exchange-equal weights are separate sensitivity estimands. The random seed and block length are explicit.

The local implementation of the same algorithm passed 11 deterministic tests on 2026-11-10 (zero failures): constant series, deterministic seed, weighting contrast, missing exchange, duplicate date, nonfinite contrast, provenance flag, invalid block length, invalid repetitions, one-date sample, and boolean pair count. The exact published checkout has **not** been executed; the test file in this commit should be rerun independently.

## Limits and admission requirements
- The input flag `source_authenticated=False` is a *negative* provenance declaration, not a verification of SEC provenance.
- This is a **date-block-only** bootstrap, **not** the full matched-group plus common-date hierarchical bootstrap. It keeps fixed exchange weights and does not resample matched securities or account for matching uncertainty.
- Circular wrapping can join distant calendar endpoints; report block-length sensitivity and compare with noncircular stationary/moving-block methods before empirical inference.
- The percentile interval is descriptive; its coverage under treatment selection, exchange heterogeneity, cross-sectional clustering, and structural breaks is not established.
- Input date ordering is checked lexicographically; a separate authoritative trading-calendar and source-file manifest admission step remains mandatory.
- No p-values, treatment effects, or causal interpretation are authorized.

## Identification and historical status
September 2025 pretrends, the substantial October 2025 placebo warning, fixed treatment-roster authentication, selection and weighting sensitivity, security/exchange controls, and dependence-aware historical inference remain unresolved. **No reform effect is established.** Previously recovered ZIPs/papers/charts are not yet inventoried completely or imported. No proprietary source data are published.

## Next tasks
Run the exact committed tests, authenticate the SEC source files and official exchange sessions, freeze pre-reform security treatment assignments, and implement matched-group resampling nested with common-date blocks. Apply to genuine September/October data *before* interpreting November contrasts. The November 14 manuscript target remains conditional on validation.
