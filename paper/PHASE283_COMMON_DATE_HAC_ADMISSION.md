# Phase 283: Common-date HAC diagnostic admission

Date: 2026-11-10. This phase introduces a descriptive estimator operating on the strictly complete exchange/date panel admitted by Phase 282. It computes a pair-count-weighted or exchange-equal daily contrast, its time mean, and a Bartlett-kernel Newey-West standard error with a user-selected lag. It is **not** a causal estimator or an authentication procedure.

## Verification

Nine deterministic synthetic tests passed locally on 2026-11-10 (Python unittest; zero failures). Cases: both weightings, lag-zero arithmetic, lag-one arithmetic, invalid lag, missing exchange, duplicate date, nonfinite input, and false authentication assertion. The locally executed code was functionally identical; the published repository checkout has not been rerun. No historical SEC statistics are reported.

## Important limitations

The estimator requires `source_authenticated=False` as emitted by Phase 282, and returns `causal_inference_authorized=False`. It does **not** validate SEC source provenance, reconstruct the November 3 treatment roster, establish exchange calendars, estimate security-level fixed effects, perform matched-pair clustering, or supply a common-date block bootstrap. Newey-West inference on aggregated daily contrasts addresses one dimension of serial dependence, but does not resolve treatment-selection or common-shock identification.

The October 2025 placebo warning, September pretrends, treatment assignment uncertainty, and pair/exchange weighting sign sensitivity remain live threats to identification. No causal effect has been established.

## Reproduction

From repository root: `python -m unittest tests.test_phase283_common_date_hac -v`. Requires no third-party Python dependencies. The tests are synthetic and must not be described as empirical results.

## Provenance and missing artifacts

Previously recovered research ZIPs, historical papers, charts, raw SEC source manifests and treatment roster evidence remain unimported or unauthenticated in this phase. No claim is made that the historical archive inventory is complete. No licensed datasets or generated historical figures were added.

## Next task

Authenticate primary SEC files with hashes and download metadata; reconcile calendar and treatment roster; apply fixed matched security/exchange samples to September pretrends and October placebo dates; compare daily HAC estimates with matched-pair and common-date block bootstrap results before revising the manuscript. The November 14 manuscript target is conditional.
