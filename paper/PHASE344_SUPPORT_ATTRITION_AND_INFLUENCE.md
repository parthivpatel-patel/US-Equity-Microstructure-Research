# Phase 344: matched-support attrition and cluster influence audit

## Scope
This adds a descriptive audit to the existing Phase 340–343 validation sequence. The input must be a separately authenticated, authorized security-date-exchange panel with columns security, date, exchange, treated, match_group, numerator, denominator. The script itself **does not authenticate any source**.

The program aggregates arm-specific numerators and denominators within each matched-group × date × exchange cell; a cell is paired only if both arms occur. It reports treated-only and control-only cells, paired-cell fraction, supported groups and dates, and the equal-group average of paired-cell rate differences in percentage points.

Leave-one-matched-group-out and leave-one-calendar-date-out recalculations expose sensitivity to concentrated support. Undefined deletions are counted rather than silently discarded. Sign-reversal counts are descriptive and not p-values. The date deletion is not a serial-dependence-aware bootstrap; it is an influence diagnostic.

## Validation
A local prototype implementing the same arithmetic and checks passed seven synthetic unittest cases (paired support and influence, duplicates, assignment drift, invalid quantity, empty input, no paired support, undefined single-date deletion). The exact GitHub-published script still requires a fresh-checkout execution test. **No SEC panel observations were processed in this phase.** No empirical estimates, standard errors or causal effects are claimed.

## Research gates still open
The original 78 dated placebo observations and producing code are missing; Phase 130 count-tail summaries conflict; September pretrends and the substantial October 2025 pre-reform placebo break remain unresolved. Treatment definitions, source provenance, exchange support, weighting and selection sensitivity, joint matched-group/date dependence, and historical ZIP recovery require authentication. November 14 manuscript certification is not warranted on this evidence.

## Next action
Run the Phase 340–344 sequence on authenticated observations, reconcile placebo counts from dated raw rows, then construct serial-dependence-aware common-date and matched-group inference. Preserve all historical archives only after access, licensing, and checksums are established.
