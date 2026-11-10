# Phase 276: integrated pretrend admission and estimation

This release composes the already-published Phase 275 exchange-session window audit with the Phase 274 fixed-window descriptive pretrend estimator. It materializes input iterables once, verifies endpoint membership and excluded-session counts, and checks that admitted and estimated window sample sizes agree. An optional contiguous-partition mode rejects unreported gaps between windows.

## Reproduction

From the repository root:

```bash
PYTHONPATH=scripts python -m unittest -v tests/test_phase276_integrated_pretrend.py
```

Nine deterministic synthetic tests passed in a local working directory using locally transcribed equivalent Phase 274 and 275 dependencies. The exact published checkout has not been rerun. No historical SEC observations were used; the synthetic numerical contrast is not an empirical estimate.

## Research admission and outstanding evidence

This is a descriptive software integration only. All source, calendar, treatment, and historical-inference authorization flags remain false. The supplied session calendar is not independently authenticated. The substantial October 2025 placebo warning, September pretrends, matched-roster and treatment authentication, selection and weighting sensitivity, security/exchange controls, and common-date serial-dependence-aware historical inference remain unresolved. No causal conclusion is warranted.

Recovered historical ZIPs, unpublished earlier implementations, and their complete license/provenance inventory were not accessible for verified import during this phase. The next step is to authenticate source files and exchange sessions, freeze a security/exchange matched roster, then execute historical September pretrends and October placebos with full-series HAC and bootstrap sensitivity checks. November 14, 2026 remains a conditional target, not a validated completion date.
