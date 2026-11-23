# Pre-reform trend gate for an exploratory manuscript (2026-11-23)

**Evidence status:** Direct review of already-published Phase 136 and Phase 139 numerical CSVs, **not** reconstruction from original SEC records. The 68 groups and treatment classifications remain provisional. This note does not claim independent reproduction of the original estimators, bootstrap draws, or source observations.

## Numerical comparison

The inherited Phase 136 `results/phase136_trend_uncertainty_presentation.csv` contains 64 July–September sessions and 23 October sessions (87 combined), with 68 groups. For the **July–September hidden-trade-count trend**, the reported slope is **+0.028607 percentage points per trading session**. Its reported two-way intervals at HAC lags **0, 3, 5, 10, 15** are respectively **[+0.011760,+0.045453]**, **[+0.007612,+0.049602]**, **[+0.006235,+0.050979]**, **[+0.004332,+0.052881]**, **[+0.003304,+0.053910]**. All five intervals exclude zero. The corresponding July–September hidden-volume slope is **−0.001464**, and all five reported intervals contain zero. These five lag variants are correlated analyses of the same observations, not five independent replications.

The inherited Phase 139 `results/phase139_paired_october_shift_presentation.csv` reports October count and volume slopes of **−0.141590** and **−0.157880** percentage points per session. Against July–September slopes of **+0.028607** and **−0.001464**, the October-minus-July–September contrasts are **−0.170197** and **−0.156416**, respectively. Four reported block-bootstrap intervals per outcome exclude zero; they are not source-certified. The October count slope changes sign relative to July–September; the volume slope becomes markedly more negative.

## Interpretation and manuscript placement

The positive July–September count trend is a **pre-reform trend**, not a September-specific estimate or a treated-versus-control parallel-trends test. It cannot be presented as proof that parallel trends failed without the actual matched-control comparison. The October slope break also predates November 3, 2025. Together they require that any November contrast be framed as descriptive and potentially confounded, not a clean causal reform effect.

For the shortest defensible public working paper, foreground a pre-reform diagnostic table with both outcomes, the July–September slope, October slope, their difference, and the explicit source-certification caveat. Place the adjusted-versus-unadjusted estimator sign reversal alongside it. Do not present these archived intervals as independently validated confidence statements.

## Required source-level follow-through

1. Retrieve original SEC Q3 and Q4 ZIP bytes, record archive and member SHA-256s, verify schema and calendar/venue coverage, and reconcile processed outcomes.
2. Freeze the September 2025 price-evaluation and symbol-history treatment roster; flag unresolved symbols.
3. Re-estimate **treated-minus-matched-control** daily pretrends on a common security/exchange/date support, with September-specific estimates, October placebo, changing membership and weighting, and dependence-aware clustered or date-block resampling.
4. Release genuine source-derived figures only after the corresponding inputs and transformation scripts can be reproduced.

**Decision:** evidence currently supports an explicitly unverified, exploratory falsification-focused manuscript, **not** a source-authenticated causal manuscript. No third-party raw data are redistributed. This project remains separate from all other research and software projects.
