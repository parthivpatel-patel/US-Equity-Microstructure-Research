# Phase 63 — Nonoverlapping calendar-boundary falsification

**Date:** October 31, 2026 (U.S. Eastern). **Cost:** $0. **Status:** reproducible, exploratory negative-control analysis; **no causal inference**.

## Research question and design

Prior analyses showed that the November 3, 2025 round-lot reform is confounded by an October placebo and unstable pretrends. This phase asks whether the November-minus-October change in the matched hidden-execution gap is unusually large relative to an **entirely pre-reform, adjacent-calendar-boundary contrast**. Unlike 45 overlapping historical paired-placebo windows, the four **raw** event windows below are disjoint in trading-day observations, although they use the same securities and are not statistically independent assignments.

The source is the inherited **SEC-derived** 580,715-row security/date/exchange panel, not original SEC Q3/Q4 ZIP files independently reconciled in this phase. The 68 treated and 204 matched-control labels remain **provisional**. The sample contains **50 treated-plus-three-control matched groups**, chosen using coverage through August 29, 2025, on the same ten venues (Arca, Bats-Y, Bats-Z, Boston, Edge-A, Edge-X, MEMX, NYSE, Nasdaq, Phlx). MIAX is excluded because NXT has no November 13 record there. All analyses use identical 50 groups across the ten venues.

For each venue, metric and boundary, calculate the mean over the ten trading days after the boundary minus the mean over the ten trading days before it, on each matched group, then equally average group changes. The matched daily gap is treated rate minus denominator-pooled three-control rate. Outcomes are on-exchange hidden trade-count rate, hidden share-volume rate and volume-minus-count wedge, in percentage points. A separate specification extrapolates the prior 20 trading days of a linear group-specific trend and compares post-event observations with the forecast. This latter specification uses overlapping lookback windows and is more model-dependent.

The four boundaries are August 1, September 2, October 1 and November 3, 2025. **Only September, October and November are after the August 29 cohort freeze.** The August negative control is useful descriptively but is selected using information that occurred after August 1, so it is *not* a strictly ex-ante placebo. The primary strict ex-ante falsification is **October minus September** versus **November minus October**. The raw ten-day pre/post windows for all four boundaries do not overlap.

## Main new results

Number of the ten venues where the **absolute October-minus-September pre-reform contrast** is at least as large as the **absolute November-minus-October contrast**:

| Outcome | Raw ten-day changes | 20-day linear pretrend-adjusted |
|---|---:|---:|
| Hidden trade-count rate | **8/10** | **4/10** |
| Hidden share-volume rate | **6/10** | **5/10** |
| Volume-minus-count wedge | **2/10** | **3/10** |

These are counts of descriptive magnitude comparisons, **not p-values**. With just one strictly ex-ante adjacent-month comparison, they cannot calibrate a null distribution or demonstrate the absence of a policy effect.

For hidden share-volume, selected raw ten-day changes (percentage points):

| Venue | September minus August | October minus September | November minus October |
|---|---:|---:|---:|
| Arca | +1.122 | **−2.973** | **+2.916** |
| Edge-X | −0.566 | **−2.756** | **+2.750** |
| Nasdaq | +1.724 | **−2.388** | **+0.926** |
| Boston | −0.589 | +0.015 | +1.613 |

**Arca:** The raw November-minus-October share-volume contrast of +2.916 pp is not larger in absolute magnitude than the fully pre-reform October-minus-September contrast of −2.973 pp. Moreover, the November boundary's own raw change is **+1.073 pp**, while the October boundary change is **−1.843 pp**. The positive November-minus-October comparison partly reflects the preceding negative October change. With 20-day trend extrapolation, Arca's November-minus-October contrast becomes +3.075 pp, exceeding its October-minus-September trend-adjusted comparison of −2.616 pp. Thus the apparent historical exception depends on the pretrend specification.

**Edge-X:** Raw October-minus-September share-volume is −2.756 pp versus November-minus-October +2.750 pp, nearly equal in magnitude with opposite signs.

**Across all ten venues:** The November raw share-volume *single-boundary change* is the largest absolute change among the four monthly boundaries in **3/10** venues; with 20-day pretrend adjustment, **2/10**. The August inclusion makes these supplementary descriptive comparisons, not strictly ex-ante tests.

The wedge's raw November-minus-October comparison exceeds the pre-reform October-minus-September magnitude in 8/10 venues, but this was one of several metrics and specifications explored after inspecting data. This is a lead for further validation, not a new confirmatory discovery.

## Why this matters

The significant October placebo warning is reinforced: in a common matched-security cohort, large month-to-month hidden-execution differences are often present entirely before November 3. These data do **not** support an assertion that the reform caused the observed changes. The October-to-November difference can be driven in part by the October baseline movement rather than a uniquely large November jump. The results also caution against presenting the exploratory matched-group bootstrap intervals from Phases 61–62 as causal confidence intervals.

## Data and inference limitations

1. Original SEC Q3/Q4 2025 archive ZIPs have **not** been reconciled to the inherited panel in this run. The official source is publicly listed, but a direct request from this environment failed with `NameResolutionError` for `www.sec.gov`. A source-extract hash is supplied; this is **not** proof of original-archive authenticity.
2. Nasdaq October/November lot snapshots and the 68 treatment labels remain provisional; historical September primary-listing-exchange average closing prices and production November 3 SIP directory records have not been authenticated.
3. Ten-day raw windows are disjoint but the same securities recur and market dynamics may persist. One pre-reform adjacent-month contrast is not an inferential reference distribution. August has lookahead cohort selection; 20-day trend windows overlap. Calendar boundaries differ in weekday and market context.
4. Metric definitions are **exchange-reported executions against hidden orders**, not order-level fills, all dark-pool executions, or a demonstrated trading signal. Missing venue-day records may reflect no eligible activity rather than a corrupted source.
5. The choice of ten venues, outcomes, pretrend models, and comparison families follows extensive exploratory analyses. No confirmatory p-values, statistical power or causal identification is claimed.
6. Existing Nasdaq (December 4, 2025) and NYSE (February 2, 2026) analyses study the reform. Publication-level originality has not been established.

## Reproducibility and outputs

- `phase63_month_boundary_falsification.py`: executable original analysis; outputs 240 monthly-step records, 60 venue/outcome/specification summaries and 2,910 daily matched-gap records.
- `phase63_plot.py`: renders **two actual charts from the CSV output**, not generated or illustrative imagery.
- `test_phase63.py`: 16 automated checks for cohort, dates, nonmissing metrics, group counts, step algebra, negative-control bounds and outputs.
- `results/monthly_boundary_falsification.csv`: exact venue-level comparisons; `results/monthly_boundary_steps.csv`: all four boundary steps; `results/daily_common_cohort_gaps.csv`: underlying daily gaps.
- `source_checksums.sha256`, `output_checksums.sha256`, `clean_rerun_verification.log`: source and deterministic clean-rerun evidence.

Run `python phase63_month_boundary_falsification.py`, `python phase63_plot.py`, `python -m unittest -v test_phase63` from the extracted folder. Python 3, NumPy, pandas, matplotlib required. **No paid resources**.

## Next concrete research task

Authenticate the September 2025 unadjusted primary-exchange daily closing prices and November 3 production round-lot assignments for the matched cohort, including corporate-action/ticker-history handling. Obtain the original SEC Q3/Q4 ZIPs and reconcile individual source rows, especially NXT/MIAX on November 13. Then prespecify a design and repeat the negative controls with authenticated treatment groups. Continue the novelty audit. **November 14, 2026** remains the target for a validated manuscript and reproducible code package, not a claim that the paper is ready.

## Official sources

- SEC, *Metrics by Individual Security and Exchange*: https://www.sec.gov/data-research/sec-markets-data/market-structure-data-security-exchange
- SEC 2025 Q3 archive: https://www.sec.gov/files/opa/data/market-structure/metrics-individual-security-exchange/individual_security_exchange_2025_q3.zip
- SEC 2025 Q4 archive: https://www.sec.gov/files/opa/data/market-structure/metrics-individual-security-exchange/individual_security_exchange_2025_q4.zip
- Nasdaq UTP Vendor Alert #2025-10 (May 7, 2025): https://www.nasdaqtrader.com/TraderNews.aspx?id=UTP2025-10
- Nasdaq reform research (December 4, 2025): https://www.nasdaq.com/articles/new-round-lots-helped-decrease-spreads
- NYSE reform research (February 2, 2026): https://www.nyse.com/research/insights/smaller-round-lots-tighter-spreads-but-thinner-liquidity

**Separate from all GIG and other projects.**