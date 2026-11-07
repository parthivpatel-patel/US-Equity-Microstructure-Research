# Phase 206: Fixed-roster admission before placebo and pretrend estimation

Date: 2026-11-06. This checkpoint is independent of all GIG projects.

## Verified local diagnostic

A standalone Python prototype `phase206_fixed_roster.py` was executed with ten deterministic unittest cases; all ten passed locally. It required a complete security × exchange × expected-session × outcome Cartesian product, stable matched-group/treatment labels, both treatment arms in each group, unique observation keys, finite values, and no unexpected dates/outcomes. The tests covered valid input, missing cell, duplicate cell, treatment switch, unmatched group, unexpected date, unexpected outcome, nonfinite value, empty panel and duplicate calendar. **This is software verification on constructed observations, not a result from SEC market data.**

## Why this matters

Phase 200's descriptive common-date contrasts reject group/date cells missing a treatment arm, but a stable security/exchange roster across all dates must also be enforced before using those contrasts as a fixed-support design. Otherwise, composition shifts can be mistaken for an event-time change. Separate count and volume measures must be jointly present without filling missing observations. An accepted structural panel is **not** evidence that treatment was historically authenticated.

## Empirical admission criteria

1. Preserve original raw source files and document retrieval URL, timestamp, SHA-256 and redistribution rights.
2. Authenticate historical treatment classifications from contemporaneous Nasdaq/UTP notices and price records, not today's classification.
3. Verify official market sessions, unexpected dates, duplicate panel keys and matched-group identity.
4. Hold the security/exchange roster and group weights fixed across September pretrend, October placebo and post-November windows. Report exclusions and alternative weightings.
5. Report the October 2025 placebo warning and September pretrends prominently. Estimate count and volume separately with common-date contrasts and multiple prespecified dependence-aware inference specifications; do not interpret a significant post-reform coefficient causally without a credible identification argument.

## Publication inventory and blockers

The verified Phase 206 prototype and tests are local only and are **not** represented as committed source files by this note. Historical SEC daily observations, historical Nasdaq treatment classifications, previously recovered ZIP archives and paper/chart artifacts remain unverified or unpublished here. No new historical coefficients, placebo statistics or causal claims are made. The November 14 target remains conditional.

Next: synchronize the executable prototype/tests, run the entire published suite from a clean checkout, then recover and authenticate original daily observations and historical treatment mapping before estimating fixed-roster pretrends/placebos.
