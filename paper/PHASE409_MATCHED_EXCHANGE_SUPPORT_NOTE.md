# Phase 409 — matched-support identification note (2026-11-16)

## New audit and limitations

The recovered panel has not been made available in this session. No security-level empirical estimates are reported. Five locally executed deterministic fixture tests passed for a prototype matched-support audit (complete 1:3 roster, missing control, exchange mismatch, duplicate record, and empty input). Those tests **do not validate the historical data**.

A critical distinction: a matched group with simultaneous treated and control observations on a given date can still have **zero within-exchange overlap**. A common-date DiD may then mix changes in exchange composition with treatment contrasts. Report both matched-group-date and matched-group-exchange-date support, and explicitly define the estimand when dropping cells lacking within-exchange support.

A second distinction: 68 treated and 204 controls imply an intended 1:3 aggregate ratio, but **do not prove** that the original matching scheme had exactly three unique controls per treated security, that controls were unique across groups, or that historical treatment assignments were correct. A strict 1:3 check is a diagnostic only; failure is not proof the original design was invalid.

## Preregistered follow-up gates

1. Recover original security-exchange-day observations, source hashes and redistribution rights; verify numerator/denominator and security identity.
2. Authenticate the November 3 historical round-lot sizes independently of present-day classifications.
3. Recover the original treatment/control mapping; compare the unique roster to realized daily and exchange-level overlap.
4. Re-estimate September pretrends and October placebo dates under common-support restrictions, with explicit selection/weighting comparisons.
5. Report uncertainty with security-group clustering and common-date dependence, alongside serial-dependence-sensitive sensitivity analyses. Avoid causal language while placebo/pretrend warnings remain.

## Reproducibility

Prototype locally tested with Python standard-library unittest: five tests passed. Full repository test suite not executed; original SEC panel not executed. No recovered archives imported; source files and licensing status still unresolved. No numerical research outcomes are inferred from synthetic fixtures.

**Publication gate:** November 14 target missed. November 30 is provisional, not a certification.
