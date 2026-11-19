# Phase 465 — Executable exact placebo-support enumeration (2026-11-18)

This is an independent deterministic audit of the Phase 462 moving-block resampling algorithm. It does not use SEC data and does not estimate a market-reform effect.

The script enumerates all possible ordered block-start sequences, truncating concatenated blocks to the original sample length, exactly as the reviewed Phase 462 code does. It counts eligibility for each placebo boundary and jointly. A hard path-count ceiling prevents accidental exponential workloads.

For six synthetic sessions, length-three blocks, and cutoffs before indices 1 and 3, enumeration yields 16 total ordered paths, 7 eligible for the first cutoff, 14 for the second, and 6 eligible jointly. Therefore joint eligibility is 37.5%. Eight deterministic unit tests passed locally on 2026-11-18.

Run from the repository root with `PYTHONPATH=scripts python -m unittest discover -s tests -p 'test_phase465_support_enumeration.py'`. The script is not a null-centered inference method; it does not fix cross-exchange security clustering, serial dependence, authenticated trading-session calendars, or sample-selection bias. Exact enumeration is feasible only for small panels; the path ceiling explicitly rejects larger configurations.

**Research status:** November 14 target missed; manuscript not publication-certified. September pretrends, the substantial October placebo warning, source and treatment authentication, alternative weighting, and historical recovery remain unresolved. Phase 430/436 archives have not been imported. Next: incorporate per-cutoff rejection diagnostics in the empirical bootstrap, then investigate a support-preserving design under dependence.
