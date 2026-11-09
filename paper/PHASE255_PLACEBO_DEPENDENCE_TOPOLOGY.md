# Phase 255 — Placebo-window dependence topology (2026-11-08)

## Verified work
Reviewed the published Phase 244, 246, 247, 250, 253 and 254 code/reports. Phase 246 already counts pairwise overlap and greedily selects nonoverlapping windows; Phase 247 reports that overlap is not a statistical correction. This new standalone diagnostic adds *connected overlap components* and a tested maximum count of mutually disjoint equal-width windows, without calling either quantity an effective statistical sample size.

Five synthetic Python unittest cases passed locally (0 failures): chain-connected overlap, touching windows, exhaustive combinatorial comparison for three rosters, invalid bounds/duplicates, and boolean cut rejection. Example: cuts [5,8,11], half-width 3, 20 sessions form one connected overlap component, while a maximum of two windows can be chosen without shared sessions. This is synthetic combinatorics, not SEC data.

## Interpretation and restrictions
Overlapping placebo windows reuse dates; connected components quantify chains of shared observations. Nonoverlapping windows may still be correlated through persistent shocks, common security/exchange effects, and serial dependence. Neither component count nor maximum disjoint count is a number of independent hypothesis tests, a corrected p-value, or an estimator of effective sample size. No historical coefficients or figures were generated.

The substantial October 2025 placebo warning, September pretrends, treatment mapping, original SEC source authentication, weighting/matching sensitivity, security/exchange controls and common-date/serial-dependence-aware inference remain unresolved. The Phase 253/254 source and test files reported as locally retained were unavailable for verified import in this session. Historical ZIP inventory is incomplete. No causal effect is established.

## Reproduction
Place the published script in scripts/ and test in tests/, then run `PYTHONPATH=scripts python -m unittest discover -s tests -p 'test_phase255_placebo_effective_count.py' -v`. The isolated local run passed five tests; full-repository suite not run. Code publication is independently verifiable, but GitHub-published bytes were not executed as a checked-out repository.

## Next
Authenticate SEC files and treatment/calendar evidence; execute fixed-roster historical pretrend/placebo estimates with clustered or resampling-based inference that preserves date and security dependence. Publication target November 14 remains conditional.
