# Phase 290 — Bootstrap percentile-index audit

Date: 2026-11-10. Scope: independent mathematical/code audit of the published Phase 289 implementation, not SEC historical inference.

## Verified observation
The published Phase 289 code sorts bootstrap means and selects positions `int(.025*(B-1))` and `int(.975*(B-1))`. At B=999 these are indices 24 and 973 (zero based); at B=99 they are 2 and 95. Both positions are floored rather than interpolated. A conventional linear-interpolation percentile rule can return different endpoints for finite B. Neither rule resolves identification failures, and no interval should be labeled as a causal confidence interval.

## Validation
An independent Python audit module and seven deterministic tests were executed locally on 2026-11-10, passing 7/7. The module exposes the actual Phase 289 index convention and a separately named linear-interpolation reference function. This is a numerical convention audit, not a replacement estimator or evidence that one interval convention is statistically superior. The exact published checkout has not been independently executed.

## Evidence boundaries and priorities
No authenticated historical SEC source files, fixed security treatment roster, official exchange calendar or historical placebo estimates were admitted in this session. The substantial October 2025 placebo warning, September pretrends, weighting/selection sensitivity, exchange controls and matched-security plus common-date serial-dependence-aware bootstrap remain unresolved. Phase 289 resamples common dates but does not resample matched security groups; do not describe it as two-way/hierarchical inference.

The historical archive inventory remains incomplete; no previously recovered ZIPs were imported in this session. Source hashes and licensing checks must precede any publication of recovered raw data. No causal effect of the November 3, 2025 round-lot reform has been established. November 14 remains a conditional manuscript target.

Next: authenticate original SEC observations and historical treatment assignments; then run fixed-roster September pretrends and October placebo diagnostics, both weighting schemes and common-date/HAC inference before considering November effects.
