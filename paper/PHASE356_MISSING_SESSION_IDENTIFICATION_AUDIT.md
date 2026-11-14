# Phase 356 — Missing-session identification audit (2026-11-14)

## Scope and source inspected
Read `scripts/phase352_calendar_serial.py` and `tests/test_phase355_calendar_properties.py` on the repository default branch. This audit concerns the *interpretation* of the existing descriptive diagnostic, not a new SEC estimate.

## Verified implementation behavior
The implementation builds `scores=[ds.get(d,0.) for d in sessions]`. Consequently, an authenticated calendar session absent from **all** input observations is assigned a zero aggregate score for the lag calculation. This is a computational convention, **not evidence that the unobserved day's economic score was zero**. It also computes each group's weight as `1/(G*n_g)` using its *observed* dates. If missingness is nonrandom, the descriptive estimand is conditional on observed support, not a balanced-panel estimand.

## Exact constructed counterexample
For the hypothetical observed date-score sequence `[+1,-1]`, lag-zero score product is 2 and lag-one score product is -1. With Bartlett maximum lag 1, the serial component is `2 + 2*(1/2)*(-1) = 1`. If the supplied trading calendar contains an unobserved intermediate session, the implementation uses `[+1,0,-1]`, yielding lag-zero 2, lag-one 0, and serial component 2. The *same observed scores* produce different diagnostics solely because the calendar support changes. These are exact arithmetic examples, not observations, standard errors, or estimates of treatment effects.

## Implications for the paper
1. Report missing-session counts and group-date coverage beside any descriptive serial diagnostic. Do not interpret zero-filled sessions as verified zero market activity.
2. Distinguish (a) true market closure, (b) source data missing for an open session, (c) security nonlisting/nontrading, and (d) group-specific incomplete exchange coverage before drawing inference.
3. Require sensitivity analyses on complete-case common-date support and explicitly authenticated calendar support; disclose changes in group composition and weighting.
4. Preserve the substantial October 2025 placebo warning, September pretrends, treatment classification uncertainty, and Phase 130 count contradiction as open identification blockers.
5. Do **not** attach calibrated confidence intervals or causal language to Phase 352's raw covariance quantities. Serial-date score construction alone does not validate the intersection correction under cross-group and temporal dependence.

## Verification and provenance
The arithmetic above was independently checked with Python using two explicitly constructed score vectors. The inspected source contains the zero-fill expression and observed-support weights quoted above. No SEC data, historical ZIPs, or licensed data were acquired or published in this session. No repository-wide test run is claimed.

## Next reproducible empirical gate
Recover the original dated placebo inputs and authenticated security-date-exchange panel with source hashes and coverage records; implement a coverage matrix separating absent source records from genuine zero-valued observations. Only then evaluate common-support pretrends, October placebo dates, and dependence-aware uncertainty.
