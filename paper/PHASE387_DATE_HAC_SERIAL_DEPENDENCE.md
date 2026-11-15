# Phase 387 — Exact Bartlett HAC on matched-pair date means

Date: 2026-11-15. **Methodology-only. No authenticated SEC observations were processed.**

## Motivation and estimator

Phase 386's two-way pair/date CR0 diagnostic does not account for serial dependence between different trading dates. This phase calculates a separate Bartlett heteroskedasticity/autocorrelation-consistent (HAC) variance diagnostic on the time series of equal-pair-weighted date means. For each trading session t, let m_t be the average matched-pair gap. Let u_t=m_t-mean(m). Define gamma_k = (1/T) sum from t=k+1 to T of u_t u_(t-k). For integer bandwidth L with 0<=L<T, report [gamma_0 + 2 sum from k=1 to L of (1-k/(L+1)) gamma_k]/T. All arithmetic is exact Fraction arithmetic; chronological ISO dates are validated, and lags refer to *observed trading sessions*, not calendar days.

The estimator requires a rectangular panel with at least two pairs and three dates; it rejects duplicate cells, missing cells, noncanonical dates and invalid bandwidths. It is a diagnostic, **not** joint pair/date clustering, a bootstrap, or a certified standard error. With a short sample, bandwidth choice and finite-sample bias can dominate. Common-date averaging does not fix cross-pair correlation, control reuse, selection or time-varying composition. Report bandwidth sensitivity and never use the result alone for publication inference.

## Local verification

Nine deterministic unittest cases passed locally on 2026-11-15 using constructed fixtures: constant series, lag-zero exact variance, lag-one Bartlett weighting, input order, fractional gaps, missing cell, duplicate cell, invalid bandwidth and invalid date. For date means [0,2,0,2], the exact variance-of-mean is 1/4 at L=0 and 1/16 at L=1. These are **not** empirical SEC results. Command from repository root: `PYTHONPATH=scripts python -m unittest discover -s tests -p 'test_phase387_date_hac.py'`. The published checkout and full repository suite remain untested.

## Identification and data gates

The November 14, 2026 target was missed and the manuscript is uncertified. The September pretrends, substantial October 2025 placebo warning, original 78 dated placebo estimates, historical treatment roster, raw SEC/Nasdaq source hashes, sample attrition, weighting sensitivity and historical archive access/licensing remain unresolved. No historical ZIP imported. Do not claim causal effects. Next: authenticate the historical panel and placebo records, compare bandwidths on actual matched-date series and combine serial-time sensitivity with matched-pair dependence-aware inference.
