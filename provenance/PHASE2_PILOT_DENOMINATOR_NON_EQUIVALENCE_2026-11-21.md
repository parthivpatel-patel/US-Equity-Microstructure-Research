# Historical pilot versus Phase-2: denominator-selection non-equivalence (2026-11-21)

**Evidence class:** direct comparison of recovered historical source-code text in the research Library. **Not** an execution on authenticated SEC source rows, a new empirical estimate, or proof of source provenance.

## Verified implementation difference

The recovered `roundlot_pilot.py` reads `individual_security_exchange_2025_q4.zip` members `oct25.csv` and `nov25.csv`, restricts to stock rows, exact-symbol stable-lot matches and the October 1–November 28 interval, and **filters only `TradesForHidden > 0`** before aggregating. It then computes both `Hidden / TradesForHidden` and `HiddenVol('000) / TradeVolForHidden('000)` from group totals.

The recovered `roundlot_phase2.py` instead reads `individual_security_2025_q4.zip` member `q4_2025_all.csv`, and **requires both `TradesForHidden > 0` and `TradeVolForHidden('000) > 0`** before security-period aggregation. It additionally requires at least ten distinct observed dates in each period for its final paired-security sample.

Consequently the pilot and Phase-2 output are **not interchangeable** even if the two source ZIPs were later proven byte-equivalent. Rows with positive eligible trade counts but zero eligible volume are retained by the pilot and excluded by Phase-2; the pilot also aggregates across securities into date-by-lot groups, whereas Phase-2 computes security-period rates before equal-security comparisons. Any numerical difference could reflect denominator filtering, aggregation weighting, sample-selection rules, or source-member differences.

## Required empirical reconciliation once original ZIP bytes are available

1. Record both original ZIP SHA-256s, member lists, member hashes, row counts and date ranges. Do not assume matching filenames or CSV columns prove identical observations.
2. Count rows with positive `TradesForHidden` and zero/nonpositive/missing `TradeVolForHidden('000)`, by month, date, exchange and provisional lot category. Record nonfinite ratios and any negative or impossible numerator/denominator values.
3. Reconstruct both filters on **the same authenticated source rows**; quantify the number of excluded records and differences in count- and volume-weighted rates, keeping numerator and denominator sums explicit.
4. Separately apply the Phase-2 ten-observed-day inclusion rule and its security-level equal-weight estimand; document how sample and weighting alter the comparison.
5. Report source-identity, filter, sample-selection and weighting effects separately; do not claim any of these effects is zero without observed data.

**Status:** original Q3/Q4 SEC bytes remain unavailable in the current execution environment; local Q3 retrieval still fails DNS resolution, and previously recorded hosted Q3/Q4 requests returned HTTP 403. No new raw-data or inference result is claimed. This document isolates a concrete historical-code discrepancy that must be resolved before describing the pilot as independent replication of Phase-2.
