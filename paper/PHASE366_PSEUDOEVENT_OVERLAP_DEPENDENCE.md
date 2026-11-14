# Phase 366 — five-day pseudo-event overlap dependence (2026-11-14)

## Motivation and provenance
Read `paper/PHASE130_REPORT.md` and `paper/PHASE365_CROSS_REPORT_ARITHMETIC_AUDIT.md` before this analysis. Phase 130 reports a five-trading-day post-minus-pre contrast across 78 prior pseudo-event dates, with overlapping windows. The archived 2/78 and 48/78 counts are descriptive rankings, **not calibrated p-values**. The underlying dated pseudo-event estimates and SEC source observations remain unauthenticated.

## Exact constructed null benchmark
For a candidate event at index t, define D_t = (sum of Y on t..t+4 minus sum of Y on t-5..t-1)/5. Suppose for illustration only that Y_t are independent, equal-variance daily shocks with zero mean. The 10 nonzero contrast weights are five negatives followed by five positives. Consequently, the lag-k correlation is the dot product of the shifted weight vectors divided by their squared norm. The exact values for k=0..10 are:

| Trading-session lag | Correlation under white-noise benchmark |
|---:|---:|
| 0 | 1 |
| 1 | +0.7 |
| 2 | +0.4 |
| 3 | +0.1 |
| 4 | -0.2 |
| 5 | -0.5 |
| 6 | -0.4 |
| 7 | -0.3 |
| 8 | -0.2 |
| 9 | -0.1 |
| 10 | 0 |

Adjacent five-day contrasts are mechanically correlated at **+0.7** even when the underlying daily series has **zero serial correlation**. The sign becomes negative at lags four through nine because one window's post-period overlaps another's pre-period. This exact arithmetic is a methodological counterexample to treating 78 scanned dates as independent draws; it is **not** an estimate of the true dependence in the SEC panel.

## Replication
`python scripts/phase366_window_overlap.py` prints exact rational values. From the repository root, `PYTHONPATH=scripts python -m unittest discover -s tests -p 'test_phase366_window_overlap.py' -v` runs five deterministic tests. Local prototype execution on 2026-11-14: **5 tests passed**. Exact published checkout and full repository test suite remain untested.

## Interpretation and next tasks
The benchmark alone does not determine an effective sample size or corrected significance level: common-date shocks, security/exchange composition, calendar gaps, autocorrelation, cohort matching, and exploratory October 6 selection can all change dependence. Recover the 78 dated outputs and original authenticated panel, enforce eligibility and source-byte checks, and run calendar-aligned pretrend/placebo inference with common-date and matched-group block resampling. Do not interpret the Phase 130 descriptive 2/78 count as a 2.56% hypothesis-test p-value. Historical original SEC ZIPs, Nasdaq snapshots, Phase 2 code/CSVs, and the reported historical research ZIP inventory remain unrecovered/unpublished in this session. No third-party market data or fabricated figure is published.

**November 14 deadline not met. Manuscript uncertified; no causal reform effect established.**
