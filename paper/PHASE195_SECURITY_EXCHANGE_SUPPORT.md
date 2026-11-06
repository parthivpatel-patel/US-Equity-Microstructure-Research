# Phase 195 — Security/exchange-aware support audit

Date: 2026-11-06. Independent U.S. equity microstructure research.

## Correction implemented
Phase 194 correctly distinguished intentionally disjoint placebo dates from genuine unit-roster differences. This checkpoint implements a structural audit retaining security, exchange and matched-group identifiers. A shared group label alone is insufficient: the securities and exchanges may differ across windows.

The script reports exact within-window count/volume pairs, dates with roster drift, and cross-window overlap of (security, exchange, group) units. It does **not** require overlapping calendar dates across intentionally disjoint windows. Equal observation counts cannot establish equal underlying units.

## Validation
Ten constructed-data unit tests were executed locally on 2026-11-06 for an equivalent prototype and passed. The published implementation is a simplified adaptation of that prototype and requires fresh-checkout execution; its tests are published for that purpose. No test uses original SEC observations. These structural checks do not authenticate the source data, Nasdaq historical treatment assignments, trading calendars, or redistribution rights.

## Remaining empirical requirements
The substantial October 2025 placebo warning and September pretrends are not resolved. Treatment authentication, security/exchange controls in the statistical estimator, weighting sensitivity, matched-group/common-date inference, serial dependence, and historical SEC source verification remain outstanding. No historical coefficients or causal effects are reported.

Historical ZIPs, original daily SEC observations and treatment roster were not imported in this session. The archive inventory remains incomplete. The November 14 target is conditional.
