# Phase 384 — Exact common-date circular-block resampling diagnostic

Date: 2026-11-15. Status: **methodology only; no authenticated market-data estimates**.

## Purpose and estimand
Phase 383 computes equal-matched-pair common-date gaps. Phase 384 introduces a small-sample, exactly enumerated circular-block resampling diagnostic for a *single date-level series* of those aggregated gaps. Each resampled index represents the entire common date, not an independently sampled security/exchange cell. Consequently it preserves contemporaneous cross-sectional dependence already aggregated into the date series and retains adjacent observations within a drawn block. It does **not** jointly resample matched pairs or fully solve two-way dependence.

For n ordered date-level values and block length L, let k=ceil(n/L). Enumerate all n^k ordered circular block-start combinations; concatenate k blocks, truncate to n observations, and compute each sample mean using Python Fraction. Equal-probability enumerated sequences yield exact frequencies and quantiles, with an explicit computational budget. Circular wrapping and block boundaries remain modeling assumptions, not validated features of SEC observations.

## Deterministic checks
Nine focused tests passed locally on constructed data (2026-11-15). A two-date series [0,2] with block length 1 yields means 0, 1, 2 with frequencies 1, 2, 1. With a three-date [0,1,2] series and block length 3, each circular rotation has mean 1. These are mathematical fixtures **not SEC estimates**.

Run from repository root: `python -m unittest tests/test_phase384_block_resampling.py` (or `python -m unittest discover -s tests -p 'test_phase384_block_resampling.py'`).

## Limits and mandatory gates
- Source panel, historical treatment roster, and matched groups must be authenticated before applying this to actual observations.
- Block length must be justified against observed serial correlation; sensitivity across L is mandatory. Circular blocks are not a universal solution to nonstationarity or structural breaks.
- The output is a resampling distribution of means, not automatically a valid confidence interval, null distribution, p-value, or causal estimate. A proper null-centering and interval design remains necessary.
- For pair/date two-way dependence, consider resampling pairs and common dates jointly or an appropriate multiway method, with documented finite-sample limitations.
- September pretrends and substantial October 2025 placebo effects remain unresolved; overlap between dated placebo windows precludes naive independent-placebo inference.
- Complete-case selection, exchange weighting, trade-count versus share-volume estimands, and treatment-authentication gaps remain unresolved.
- The November 14, 2026 publication target was missed. The paper is not certified or ready for causal claims.

## Recovery and provenance
This phase imports **zero** historical ZIPs, licensed data, prior paper versions, or empirical charts. Historical recovered archives remain unverified for repository inclusion; no inventory completeness is asserted. The next phase should locate authenticated raw observations and prior ZIP manifests, establish redistribution rights and hashes, and reconstruct the original 78 dated placebo estimates before applying block methods to actual data.
