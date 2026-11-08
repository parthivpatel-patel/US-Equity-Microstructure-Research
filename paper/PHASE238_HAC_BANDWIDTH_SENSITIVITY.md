# Phase 238 — HAC bandwidth sensitivity audit

Date: 2026-11-08. Independent November 2025 round-lot reform research.

## Source inspected
The published Phase 224 `common_date_hac` estimator calculates an early-versus-late difference and Bartlett HAC variance from the full sequence of daily contrasts. Phase 226 calls that estimator after constructing equal pair-exchange-weighted matched daily contrasts. The Phase 224 implementation supports integer bandwidths from zero through fewer than the total number of dates, but provides no systematic bandwidth comparison.

## Addition
`scripts/phase238_hac_bandwidth_sensitivity.py` runs the published Phase 224 estimator over an ordered, nonduplicate list of bandwidths and retains both estimator channels. It never changes the point estimates or labels source, calendar, or treatment as authenticated. The accompanying deterministic tests use synthetic observations and cover bandwidth invariance of point estimates, standard-error sanity, invalid bandwidths, and incomplete daily input.

## Interpretation and limitations
Bandwidth choices change estimated serial-dependence uncertainty, not the underlying early/late descriptive contrast. Short series and constant or nearly constant fixtures may produce misleadingly small HAC standard errors. This helper is not a substitute for matched-security clustering, common-date shocks, fixed-roster treatment validation, placebo-date inference, or source-data authentication. It makes **no** empirical claims about the November 3, 2025 reform. The October placebo warning and September pretrends remain unresolved. No causal effect has been established.

## Pending
Run against authenticated SEC historical inputs, assess bandwidth sensitivity alongside date-block and security-cluster methods, and inventory recovered historical archives when accessible. No licensed raw data or unverified figures are published here. November 14 target remains conditional.
