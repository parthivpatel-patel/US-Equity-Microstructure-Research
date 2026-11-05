# Phase 169 — Matched-arm missingness and fixed-roster coverage audit

Date: 2026-11-05. Independent research project. No historical SEC data analyzed in this phase.

## Source-code observation

Read the existing Phase 168 script before preparing this addition. Its `paired_contrasts` constructs matched pairs only when both arms exist, and rejects a date only if it contains **no** complete matched pair. It does not report incomplete treatment-arm cells or the share of a prespecified group roster represented on each date. Thus a date with one complete group and many partial groups can pass its admission rule. This is a verified property of the published code, **not** a finding that the SEC data have such missingness.

## New reproducible diagnostic

`tests/test_phase169_pair_coverage.py` reports complete, partial, and wholly absent matched groups for each observed calendar date. The denominator is either the observed union of groups (a descriptive lower-bound diagnostic) or a separately supplied fixed roster (preferred for selection diagnostics). It rejects duplicate cells, noncanonical dates, invalid arms/outcomes, duplicate roster members, and unknown groups. The denominator must not be interpreted as the full historical eligible population unless the external roster is authenticated.

Illustrative constructed data: on 2025-10-02, group A has both arms and group B only its control arm. Complete = 1, partial = 1, coverage = 1/2. A missing group B on every date is invisible without an independently defined expected roster. No historical coefficients or confidence intervals are claimed.

## Verification status

Nine unittest cases are included in the published source, but execution could not be completed in this run because the local execution environment returned a session-limit error. **Do not report 9/9 passing.** GitHub publication and fetch-back, if successful, establish source availability, not test execution or empirical validation.

## Identification and data gates

The October 2025 placebo signal and September pretrends remain substantial warnings. The 68 provisionally treated securities require historical Nasdaq round-lot authentication. Security/exchange controls, matched-group composition, common-date support, serial dependence, cluster-aware inference, alternative weighting, and selection sensitivity must be applied to authenticated SEC daily observations. Neither balanced-roster restriction nor observed-roster coverage independently solves missing-not-at-random selection.

## Archive inventory / publication boundary

Previously named but not authenticated this session: `roundlot_phase2.py`, `roundlot_phase2_security_panel.csv`, `roundlot_pilot_daily.csv`. Historical research ZIPs, Nasdaq snapshots, and original SEC daily archives were not accessible for import in this run. Redistribution rights and checksums remain unverified. No archives, licensed datasets, synthetic charts, or invented statistics were published.

## Next action

Recover and hash original SEC/Nasdaq source files and the historical ZIP inventory, authenticate treatment rules, define the expected security/exchange/matched-group roster, compute daily pair coverage, and then estimate September pretrends and October placebo contrasts with common dates and matched-group plus serial-dependence-aware uncertainty. The November 14 target remains conditional. No causal effect established.
