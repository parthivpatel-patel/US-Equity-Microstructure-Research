# Phase 421: September matched-cell pretrend diagnostic

This script computes a descriptive September 2025 slope in date-balanced treated-minus-control hidden-trade-count rates. It requires CSV fields `date,security,exchange,match_group,treated,hidden_count,total_count`. Within each date, exchange, and match group, it pools counts separately for treated and controls; it then equally weights matched cells on each date and fits a linear slope to September dates using calendar-day spacing.

Run: `python scripts/phase421_pretrend.py panel.csv --output pretrend.json`.

Validation: six deterministic local unit tests passed on constructed fixtures. No authenticated historical SEC panel or matching assignments were available, so no historical result was computed. The slope is descriptive and lacks cluster-robust, date-correlated, and serial-dependence-aware uncertainty; it is not a valid standalone parallel-trends test. Selection of surviving paired cells can itself induce bias. This script must not be used to assert a causal effect. October 2025 placebo warnings, round-lot treatment authentication, source provenance, weighting sensitivity, and licensed-data redistribution remain open gates.

Recovered historical ZIP inventory: none accessible in this run; none imported. Historical research papers/charts not newly published. November 14, 2026 target missed; manuscript not publication-certified.

Next: obtain authenticated panel and matching assignments, reconcile denominator definitions and September paired support, then evaluate multiple pretrends and October placebos with matched-group/common-date and serial-dependence-aware inference.
