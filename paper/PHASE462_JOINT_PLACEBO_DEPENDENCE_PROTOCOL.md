# Phase 462 — Joint placebo dependence and support protocol (2026-11-18)

## Verified prior implementation
Reviewed `scripts/phase461_observed_overlap.py` and `scripts/phase459_placebo_grid.py` directly from the public repository. Both explicitly report unauthenticated sources and treatment. Phase 461 measures observed-date overlap; Phase 459 computes equal-group placebo contrasts, but neither supplies joint uncertainty for overlapping cutoffs.

## New validation in this session
Developed a standalone Python joint placebo bootstrap prototype and ran eight deterministic unit tests locally: all eight passed. The prototype enforces complete exchange–matched-group × session support; rejects duplicate/unsorted sessions, invalid cutoffs, nonfinite gaps and invalid block lengths; resamples matched groups and common contiguous session blocks using the same resampled dates for every placebo boundary. It returns observed contrasts and exploratory percentile intervals, with a count of draws retaining pre/post support. The prototype and tests have **not** been imported into this repository in this commit; their local working copies are not represented as published code.

For a constructed six-session, two-group example, the observed treated-minus-control gap shift was 2.25 at each of two illustrative September placebo cutoffs. This is synthetic verification only, not an SEC result.

## Important inference limits
1. Resampling the same date indices across groups preserves common-date shocks and cutoff dependence within draws. Independently resampling each cutoff would destroy that dependence.
2. Ordinary moving blocks over a supplied session list are only meaningful if the calendar is authenticated and complete. Observed-date adjacency alone is insufficient.
3. Requiring a complete group-session panel changes the target sample; quantify exclusions and compare with locally paired support before using any interval.
4. Percentile intervals from a naive resampling of the observed series can be inappropriate for testing a structural break under the null. A null-centered or restricted bootstrap, or a suitable dependent multiplier design, is needed for calibrated placebo hypothesis tests.
5. The group bootstrap is not automatically valid if matching creates dependence across groups or securities appear in multiple exchange strata. Resampling should respect the original matching units and security-level cross-exchange dependence.
6. Report the joint covariance of placebo contrasts and simultaneous, rather than separately interpreted, uncertainty bands when multiple cutoffs are examined.
7. No treatment authentication, source provenance, September pretrend resolution, October placebo resolution, or causal identification is established here.

## Publication gate
November 14, 2026 target missed. Manuscript remains NOT PUBLICATION-CERTIFIED. No authenticated historical SEC effect estimate was produced. Historical ZIP recovery and Phase 430/436 import remain outstanding.

## Next work
Publish the tested prototype and tests once their exact bytes can be transferred into the GitHub workflow; integrate the authenticated session calendar and matched-unit identifiers, add null-centered joint inference and empirical placebo sensitivity. No proprietary raw observations should be committed without redistribution authorization.
