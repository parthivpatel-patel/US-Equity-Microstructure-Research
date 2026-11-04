# U.S. Equity Market Microstructure Research

**Independent exploratory research** into the November 3, 2025 U.S. equity round-lot reform and exchange-reported hidden-order execution.

> **Research status:** Working paper in progress. Results are preliminary and **do not establish a causal effect** of the reform. Historical Nasdaq round-lot assignments and source-level SEC reconciliation remain outstanding.

## Research question

How much do measured changes in hidden-order execution depend on outcome definitions, matched-security cohorts, exchange composition, weighting, event windows, historical placebo dates, and inference procedures?

## Scope

The inherited processed SEC-derived research panel has been reported as containing **580,715 security-date-exchange observations**, **408 securities**, **14 exchanges**, and **106 trading dates**. Provisional assignments contain **68 treated securities and 204 matched controls**. A complete-case subset has **52 treated securities and 156 controls**. These are inherited dataset counts, not newly authenticated raw SEC records.

## Main identification and reproducibility warnings

- Large September/October pre-reform movements challenge a simple reform-date causal interpretation.
- October 1 was an announced publication date for future round-lot assignments; it is not a pure no-information placebo.
- Hidden execution measured by trade count and by share volume can yield different signs.
- Venue weighting, eligibility thresholds, matching, time-trend modeling, and selection of event windows materially change estimates.
- Historical placebo windows overlap, and post hoc selection/multiple tests prevent treating their empirical ranks as calibrated p-values.
- Earlier complete-case filters disproportionately exclude matched-control observations at thin venues.
- A public repository does **not** establish that the manuscript, treatment assignments, or complete raw-data lineage are verified.

## Public contents and replication status

- `paper/PHASE130_REPORT.md` — historical pseudo-event results and limitations.
- `src/phase130_analysis.py` — original recovered Phase 130 analysis code. It expects `daily_group_contrasts.csv` **beside the script**, along with pandas and numpy; a validated processed input must be supplied separately.
- `results/phase130_summary.csv` and `results/phase130_group_sensitivity.csv` — frozen reported Phase 130 outputs.
- `provenance/ARCHIVE_STATUS.md` — inventory of recovered archival packages and materials **not yet present on GitHub**.

**Important:** This initial published checkpoint is only a *subset* of recovered work. Do not claim all prior phase ZIPs, research figures, or raw source datasets are uploaded until they are independently verified in the repository.

## Research publication

Target date: **November 14, 2026**, contingent on validation. The defensible current manuscript path is exploratory and falsification-focused. The project is independent of GIG Quant Terminal and all other projects.

## Data and licensing

Review the SEC, Nasdaq, NYSE and third-party data-use terms before redistributing any original archives. Source files may be documented by hashes and acquisition instructions rather than republished. Code and manuscript remain without an explicit reuse license until their rights and attribution are reviewed.
