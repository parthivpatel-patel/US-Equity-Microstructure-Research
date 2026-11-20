# Phase 501: coverage weighting and common-date support

This is a deterministic diagnostic for Phase 500 exchange/date/group eligibility and observation counts. It is not an estimate of the November 2025 round-lot reform effect.

For each exchange and pre/post period, report: (1) treatment/control coverage over all eligible dates, (2) number of dates with eligible observations in both groups, (3) equal-date-weighted mean treated-minus-control coverage gap on common support, and (4) difference of eligible-count-weighted coverage rates on the *same* common support. These generally differ because denominators vary across dates. Absent groups are never assigned zero coverage; they are excluded only from the common-support gap, while all eligible counts remain in group-wide summaries.

A constructed two-date fixture has treated/control counts (eligible, observed) of (1,1)/(1,0) on the first date and (9,0)/(1,1) on the second. Equal-date mean gap is 0, eligible-weighted common-date gap is -0.4. This is **not** a historical SEC result. Eight deterministic tests passed locally on November 20, 2026 against an equivalent implementation; the exact published checkout has not been executed.

Limitations: count records are assumed to have passed Phase 500 validation; this aggregator independently checks count integrity but does not reauthenticate securities, treatment labels, SEC source files, eligibility, or date-period mapping. It is descriptive and does not implement clustering or serial-dependence inference. No conclusion about the October 2025 placebo is warranted before authenticated observations, matched-group mappings, September pretrends, and date dependence are examined. The November 14, 2026 target was missed; the manuscript remains not publication-certified.

Reproduction: `PYTHONPATH=scripts python -m pytest -q tests/test_phase501_coverage_aggregation.py`. Function `aggregate_coverage(rows)` accepts dictionaries with Phase 500 count fields. No third-party market data are included.
