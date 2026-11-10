# Phase 285 — HAC inference admission audit (2026-11-10)

## Scope and inspected code
Inspected the published `scripts/phase282_calendar_admission.py` and `scripts/phase283_common_date_hac.py` directly through the connected GitHub service. Phase 282 validates completeness relative to a *caller-supplied* calendar and fixed exchange roster; it does not establish the historical provenance of either. Phase 283 computes a descriptive daily weighted contrast and Bartlett Newey–West standard error, but intentionally labels the result `source_authenticated=False` and `causal_inference_authorized=False`.

## Verified numerical and inference boundary
For a constant daily contrast series, centered residuals are all zero, so every sample autocovariance and the reported HAC standard error are exactly zero. Any downstream calculation dividing the estimated mean by this standard error is undefined (if the mean is zero) or divergent (if nonzero). This is a mathematical property of the published formula, **not an empirical SEC observation**. A downstream diagnostic must fail closed rather than report a finite t-statistic or a misleading significance claim.

Additional admission criteria for later inference: (1) reject nonfinite estimates or negative standard errors, (2) flag zero or near-zero standard errors, (3) flag short common-date series, (4) flag lags large relative to the sample, (5) never convert these checks into historical or causal authorization. A local Python diagnostic prototype implementing these checks passed **10 deterministic unittest cases** on 2026-11-10. Its exact source and tests were executed locally but are **not part of this published report** and require separate repository synchronization.

## Outstanding empirical requirements
No authenticated SEC security-date-exchange observations were available in this session. No historical coefficients, confidence intervals, figures, or causal estimates were computed. The substantial October 2025 placebo warning, September pretrends, treatment classification and historical round-lot authentication, security/exchange confounding, weighting and selection sensitivity, common-date serial dependence, and matched-group bootstrap remain unresolved. Earlier recovered ZIPs, manuscript drafts and charts have not been inventoried or imported.

## Next gate
Authenticate source-file hashes and permitted redistribution, source metadata, session calendar, treatment assignments and fixed matched security/exchange roster. Rerun repository tests on the published checkout; then estimate September pretrends and multiple October placebo cutoffs using identical panels, exchange leave-one-out and alternative weighting, prespecified HAC lags, and matched-group/common-date block resampling. The November 14, 2026 manuscript target remains conditional; no causal conclusion is authorized.
