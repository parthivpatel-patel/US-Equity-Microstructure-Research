# Phase 164 — Joint-support counterexample

Date: 2026-11-05. Independent research into the November 3, 2025 U.S. equity round-lot reform.

## Verified diagnostic

Six deterministic standard-library unittest cases passed locally. The fixture has treated baseline outcome pairs (0,0), (1,1) and comparison pairs (0,1), (1,0). Both groups have **identical marginal ranges [0,1] in each outcome**. All four observations fall inside the other group's two-dimensional bounding box. Nevertheless, there are **zero cross-group pairs** within an L-infinity distance of 0.49; at distance 1.0 there are four cross-group pairs. This establishes that marginal range overlap, and even bounding-box inclusion, do not guarantee nearby observations in the *joint* baseline outcome space.

This is a mathematical construction, **not** an estimate from SEC market observations. A distance threshold must be justified relative to the outcome scales and declared in advance; raw nearest-neighbor counts are not themselves causal identification tests.

## Implications for the empirical paper

Before any matched treatment-effect estimate, compute and disclose joint baseline distances between treated and control securities, matched-group support, fraction of securities without adequate neighbors, effective sample size and maximum weight shares. Examine sensitivity to prespecified distance tolerances and trimming. Assess September pretrends and the substantial October placebo separately, using common-date and serial-dependence-aware inference. Overlap alone does not establish parallel trends or treatment validity.

## Provenance and inventory

The preceding Phase 163 memo was read from the public repository before writing. This phase adds only this report and an executable constructed-data test; it does not overwrite prior research. The original SEC daily archive, authenticated historical Nasdaq round-lot snapshots, recovered 2,262-security analytical panel and historical ZIP collection were not available for fresh empirical execution or redistribution review. No original market observations, charts or causal estimates were produced or published. Source authentication, treatment classification, pretrend/placebo re-estimation and historical archive inventory remain outstanding.

Publication target November 14, 2026 is provisional. No causal effect has been established.
