# Phase 286 — HAC descriptive-inference gate (2026-11-10)

## Scope and result
This session inspected the published Phase 283 common-date HAC implementation before extending it. Its output includes `n_dates`, `lag`, `weighting`, `mean`, `hac_standard_error`, and explicit unauthenticated/noncausal flags. The new gate checks those fields without reinterpreting them as authenticated observations.

The new code refuses inferential reporting if the common-date sample is shorter than a configurable threshold (default 20), the HAC lag exceeds a configurable fraction of the number of dates (default 0.25), or the standard error is zero/near zero (default floor 1e-12). It rejects nonfinite, negative, malformed, or contradictory input. Thresholds are **engineering defaults, not statistically validated critical values**; prespecification and sensitivity checks remain necessary. Even a passing gate does not authenticate data or license a causal interpretation.

## Reproduction
Run from the repository root:

```bash
PYTHONPATH=scripts python -m unittest -v tests/test_phase286_hac_inference_gate.py
```

Alternatively, from a directory containing both published Python files, run `python -m unittest -v test_phase286_hac_inference_gate.py`. Eleven deterministic synthetic tests passed in the local standalone implementation (11/11, 2026-11-10). The exact published checkout was not rerun; no historical SEC data were used.

## Identification and provenance limitations
* September 2025 pretrends and the substantial October 2025 placebo warning remain unresolved.
* Fixed treatment assignments, matched-security rosters, exchange calendars, source checksums and source redistribution rights require authentication.
* Exchange composition, estimator weighting, security/exchange controls, and joint matched-group/common-date serial-dependence-aware bootstrap remain to be executed on genuine historical observations.
* Phase 283's `source_authenticated=False` is a negative marker, not a data-authentication workflow.
* Previously recovered historical ZIPs, paper drafts and charts were not imported in this session; inventory remains incomplete. Do not represent those artifacts as published.

## Next work
Authenticate source files and exchange calendars; run the exact repository test suite; implement paired-security and common-date block resampling with prespecified lags; execute historical September pretrend and October placebo tests before interpreting November contrasts.

No reform-caused effect is established. The November 14 manuscript target is conditional on these unresolved checks.
