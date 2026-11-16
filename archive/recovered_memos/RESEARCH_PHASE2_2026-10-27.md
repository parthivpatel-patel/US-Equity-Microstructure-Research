# Round-lot reform study — Phase 2 research memo
Date: 2026-10-27

## Inputs and reproducibility
- Nasdaq historical symbol directory snapshots: `nasdaq_october_2025.csv`, `nasdaq_november_2025.csv(1).csv`.
- SEC individual-security daily data: `individual_security_2025_q4.zip`, member `q4_2025_all.csv`.
- Reproduction script: `roundlot_phase2.py` (run `python roundlot_phase2.py`; requires pandas, numpy, statsmodels).
- Outputs: `roundlot_phase2_security_panel.csv`, `roundlot_phase2_inference.csv`.

## Sample
Matched Nasdaq tickers with identical October and November snapshot lot sizes, `Security == Stock`, valid positive hidden-trade and hidden-volume denominators, and at least 10 observed days in each pre/post window. Pre: Oct 1–31, 2025. Post: Nov 3–28, 2025. 2,262 tickers; 68 reduced-lot, 2,194 100-share.

## Method
For each ticker and period, aggregate SEC counts and calculate hidden executions / eligible executions, and hidden volume / eligible volume. Compute post-minus-pre within ticker. Regress change on reduced-lot indicator with HC3 robust errors. Baseline-adjusted model adds both pre-period hidden-trade and hidden-volume rates. This is NOT a stock-and-date fixed-effects panel regression and does not establish causal identification.

## Estimates
- Trade rate unadjusted: -0.034629, HC3 SE 0.004418, p 4.56e-15, 95% CI [-0.043288,-0.025970].
- Trade rate baseline-adjusted: -0.010815, SE 0.005041, p 0.0319, CI [-0.020694,-0.000935].
- Volume rate unadjusted: -0.025721, SE 0.004213, p 1.03e-09, CI [-0.033978,-0.017463].
- Volume rate baseline-adjusted: +0.014789, SE 0.005569, p 0.00792, CI [+0.003874,+0.025704].
- Placebo: split October at Oct 15, comparing Oct 1–15 to Oct 16–31; trade rate -0.011703, SE 0.004424, p 0.00816. 2,258 tickers; 68 treated.

## Important limitations
1. Statistically significant October placebo differential is evidence against a simple parallel-trends assumption.
2. Baseline adjustment reverses volume-rate coefficient sign, signaling specification sensitivity.
3. Nasdaq snapshot lot sizes require independent validation as contemporaneous November 3 assignments. Ticker joins may be contaminated by ticker changes/reuse.
4. The comparison group differs structurally in price, capitalization and liquidity; cross-sectional HC3 errors do not address common market shocks or all time-series dependencies.
5. The sample is survivorship-filtered by agreement between snapshots and minimum valid-day requirements.
6. SEC daily statistics are not the same as a proprietary tick-by-tick time-and-sales feed; do not equate metrics without reading methodology.
7. Do not call these results causal, publication-ready, or proof of a reform effect.

## Next tests
Read SEC README definitions; event-time plots, placebo cut dates and pretrend; price-rank/turnover-rank controls; matched/near-threshold comparisons if contemporaneous September 2025 primary closing prices can be sourced; exchange-level heterogeneity; stable ticker and corporate-action audits; sensitivity to sample inclusion and denominator weighting; clustered inference and permutation tests.