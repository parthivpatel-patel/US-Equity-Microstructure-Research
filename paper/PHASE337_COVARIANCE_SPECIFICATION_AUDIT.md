# Phase 337 — Date-HAC versus two-way covariance sensitivity

Date: 2026-11-13. Input: existing public `results/phase136_trend_uncertainty_presentation.csv` (20 rows; source GitHub blob SHA `e89016144b1b60079a4686c02a945009a2734c06`). No underlying SEC observations were accessed or re-estimated. This is a descriptive audit of *reported* covariance estimates.

Run: `python scripts/phase337_covariance_comparison.py results/phase136_trend_uncertainty_presentation.csv`.

| Outcome | Period | Minimum two-way/date-HAC SE | Maximum two-way/date-HAC SE | Disagreement at illustrative 1.96 threshold |
|---|---|---:|---:|---|
| count | Jul–Sep | 1.164847 | 1.567858 | none of 5 lags |
| count | Jul–Oct | 1.073507 | 1.402513 | none of 5 lags |
| volume | Jul–Sep | 1.268347 | 1.422740 | none of 5 lags |
| volume | Jul–Oct | 1.169790 | 1.618377 | none of 5 lags |

In all 20 published cells, the two-way standard error exceeds the date-HAC standard error. This is an *observed property of these displayed results*, not a mathematical requirement of multiway clustering. At the purely illustrative absolute slope/SE > 1.96 cutoff, covariance choice alone does not reverse a classification for any of these 20 cells. July–September count and July–October volume exceed that cutoff under both published covariance choices for all five lags; the other two outcome-period combinations do not. The comparison does not establish valid finite-sample critical values, p-values, or causal identification.

Validation: nine deterministic unit tests passed locally. The script was also executed on a faithful local transcription of all 20 GitHub-fetched CSV rows; the source CSV was fetched via connected GitHub, not authenticated against the original SEC panel. The full published checkout regression suite was not run.

**Publication gate:** October 2025 placebo/break warnings and September pretrends remain material; Phase 130 five-day hidden-count placebo tail counts remain internally contradictory; original 78 dated placebo observations and producing code, treatment authentication, matching/weighting sensitivity, raw security-exchange controls and dependence-aware source-level inference are outstanding. Historical research ZIPs remain unverified and unimported. No causal reform claim is warranted, and the November 14 manuscript is not certified ready.
