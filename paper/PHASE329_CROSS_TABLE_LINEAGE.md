# Phase 329 — Cross-table lineage and window-sign audit (2026-11-13)

## Inputs and verification
Read existing public repository files `results/phase130_summary.csv` and `results/phase131_window_sensitivity.csv` without modifying them. The 5-day Phase 131 rows reproduce Phase 130's placebo denominator and both tail counts exactly for count and volume; event contrasts agree to within 0.000001 percentage points (rounding). This means Phase 131's five-day summary is **not an independent replication** of the questionable Phase 130 count row. Shared numerical fields do not prove shared raw data or identical generating code.

## Observed descriptive window sensitivity
Count November-minus-October contrast (percentage points): 3 days −0.682345; 5 days −0.734661; 7 days −0.122428; 10 days +0.337165; 15 days −0.118296. The sign reverses at 10 days. Volume: 3 days +0.201918; 5 days +0.626598; 7 days +0.987253; 10 days +1.156684; 15 days +0.718230; all positive. These are previously published aggregate numbers, not new authenticated SEC estimates. Window selection must not be optimized ex post.

## Checks
The new cross-table script was executed locally against a minimal transcription of the two retrieved CSV tables (the relevant columns only); all four 5-day checks passed for each outcome. Five synthetic unit tests passed locally (0 failures) for matching, mismatch, missing/duplicate windows and sign changes. Full repository checkout tests and independent reproduction from underlying daily security-exchange observations were not performed.

## Publication gate
The Phase 130 count row remains internally inconsistent under the documented common-population tail definitions (negative-tail 2, absolute-extreme 2, positive maximum above the absolute event threshold). Because Phase 131 repeats the suspect five-day counts, it cannot resolve that contradiction. Original dated placebo observations, the producer, source-data authentication, September pretrends, substantial October placebo, treatment assignments, matched security/exchange controls, weighting, common-date and serial-dependence-aware inference remain required. Historical recovered ZIPs remain unverified and unimported. No causal interpretation or completed-paper certification is warranted.
