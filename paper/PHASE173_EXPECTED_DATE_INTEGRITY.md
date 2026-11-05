# Phase 173 — Expected trading dates versus observed zero coverage

Date: 2026-11-05. Independent U.S. equity microstructure research. **No SEC observations used.**

## Finding

The Phase 172 audit counts runs of zero coverage only among dates supplied to it. If an entire expected trading date is absent from the source extract, the date can disappear from the report. This is not equivalent to a verified date containing zero complete matched pairs.

This new fail-closed audit takes an externally supplied, sorted, unique expected trading-date calendar, validates observed daily matched-pair counts, and reports absent expected dates separately from observed zero coverage. It rejects duplicate dates, unexpected dates, invalid counts, noncanonical dates and cutoffs that do not split the expected calendar. An observed-only pooled coverage rate is explicitly labeled as such and is undefined when no dates are observed.

## Constructed counterexample

Expected dates: October 1, 2, 3 and 6, 2025. The observed extract contains October 1, 2 and 6, each with 2/2 complete pairs. October 3 is absent. The post-cutoff (October 3 onward) observed-only pooled coverage is 100%, but the post period is **not calendar complete**. If both October 3 and 6 are absent, the missing expected-date run is two and post observed-only pooled coverage is undefined.

The local extended prototype passed 12/12 unittest checks on deterministic fixtures. The repository implementation has the same named twelve scenarios; execute the published file in a fresh checkout to independently validate it. Neither implementation authenticates a trading calendar.

## Empirical gates

Before empirical use: independently authenticate the SEC daily source files, Nasdaq historical treatment assignment, the relevant exchange trading-day calendar and symbol/exchange universe. Quantify absent dates separately from zero matched pairs; report security-exchange and matched-group attrition; run September pretrends, multiple October placebo cutoffs, weighting and roster sensitivities, common-date and serial-dependence-aware inference. Existing October placebo and September pretrend warnings remain unresolved. No causal inference is justified. Historical ZIP and manuscript recovery remains incomplete. November 14 publication target is conditional.
