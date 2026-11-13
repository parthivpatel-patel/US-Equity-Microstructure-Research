# Phase 346: correction of zero-valued leave-out sign classification

Date: 2026-11-13. Independent U.S. equity round-lot reform study.

## Source-code audit and correction

The published Phase 344 diagnostic used `(v > 0) != (base > 0)` to count sign reversals. When the baseline is positive, a leave-one-group-out estimate of exactly zero was incorrectly counted as a reversal. A strict reversal requires opposite nonzero signs: `v * base < 0`. The implementation now uses that condition. This changes a descriptive influence diagnostic, **not** an empirical estimate.

A direct arithmetic check with baseline +10 and leave-out estimates [0, -5, +4] yields 2 counts under the previous expression but 1 strict reversal. A zero is a loss of directional sign, not a negative sign.

Three deterministic regression cases were added for positive-baseline/zero, negative-baseline/zero, and genuinely opposite-sign leave-out estimates. These are constructed software checks, not observations from the SEC panel. The exact published Python tests were **not executed in this session** because the working container could not resolve github.com for a fresh checkout. Do not describe them as passed without executing the published checkout.

## Outstanding gates

Original source authentication, dated placebo observations, Phase 130 count reconciliation, September pretrends, the substantial October placebo warning, treatment assignment, matched security-exchange support, common-date and serial-dependence-aware inference, weighting sensitivity, and historical ZIP inventory remain unresolved. This correction does not justify a causal claim or certify the manuscript.

## Reproduction

`python -m unittest discover -s tests -p 'test_phase346_zero_sign.py' -v`

Next: execute the published tests on a clean checkout and evaluate the corrected influence diagnostic on authenticated source observations.
