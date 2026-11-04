# Phase 132 — Cross-phase numerical integrity and sign sensitivity audit

**November 3, 2026.** This audit uses the two **already published** frozen result CSVs from Phases 130 and 131. No SEC raw data or new treatment assignments were available in this session. The accompanying standard-library Python audit tests internal numerical consistency; it is **not** a rerun of the econometric estimator.

## Descriptive findings from the published ten-row Phase 131 table

- The November 3 **count** event-window change is negative in **all five** examined windows (3, 5, 7, 10, 15 trading days). This is a statement about a processed group-contrast series, **not a reform effect**.
- The November 3 **volume** event-window change is negative in **four of five** windows; the seven-day estimate is +0.089135 percentage points.
- The **count November-minus-October 6 difference** spans **-0.734661 to +0.337165 percentage points** and flips sign at the 10-day window. Thus a consistent negative November event estimate does **not** imply a consistently negative *incremental* November-versus-October contrast.
- The **volume November-minus-October 6 difference** is positive at all five windows, spanning **+0.201918 to +1.156684 percentage points**. That consistency does not resolve the choice of October comparator or confounding.
- Historical pseudo-event **absolute-extremeness** counts for count are **7/82, 2/78, 12/74, 21/68, 3/58** (W=3,5,7,10,15). For volume: **71/82, 76/78, 64/74, 47/68, 9/58**. These are *descriptive*, overlapping-window rankings, **not valid p-values**.
- The published Phase 130 five-day values match Phase 131's five-day values to the six-decimal precision of the latter, including November, October 6, their difference, and historical pseudo-event counts. The script explicitly checks these invariants and validates that placebo counts do not exceed denominators.

## Interpretive constraint

The all-negative count November event profile and the sign-changing count November-versus-October profile are **different estimands**. Reporting only the former would obscure the October warning. No additional statistical significance or causal claim can be inferred from these checks. In particular, comparing a reform date with an exploratory October 6 comparator is not a validated difference-in-differences design.

## Reproducibility

Run `python tests/audit_published_phase130_131.py` from the repository. No third-party packages are needed. The code is a deterministic table audit with exact-decimal arithmetic. It **does not** authenticate historical round-lot treatment, check raw SEC archives, address cross-date dependence, or establish reproducibility of the unpublished processed input.

## Blocking scientific work

Recover and publish the permitted Phase 130/131 input with SHA-256 validation; authenticate historical Nasdaq assignments and SEC source lineage; predefine matched security/venue weights; run event-study pre-trend and placebo plots; and perform matched-group/common-calendar-date block inference with serial dependence. Preserve the negative controls and avoid causal language until identification is defensible.
