# Phase 412 — October within-preperiod placebo audit (2026-11-16)

This script constructs matched-group × exchange × date treated-minus-control hidden-trade-count rate gaps, then calculates a difference in equal-cell average gaps on either side of an October 15, 2025 placebo cutoff. It requires contemporaneous treated/control observations in the **same exchange** and matched group, rejects duplicate security/exchange/day records, and blocks missing paired observations on either side. All rates are percentages of trades, not share volume.

**Interpretation:** This is a pre-reform falsification diagnostic, not an effect estimator. October 15 is a diagnostic choice, not an authenticated event date. Testing many cutoffs requires multiplicity controls. Equal-cell averaging is not denominator pooling; composition may change across the cutoff. The statistic has no standard error or p-value, and cannot establish parallel trends.

**Validation:** A locally executed seven-test structurally richer prototype passed, including a constructed −50 percentage-point placebo difference. The simplified published implementation and six published tests are provided for reproducibility but were not independently executed as the exact published checkout in this session. The −50 figure is fixture-only, **not SEC data**.

**Critical blockers:** Historical security/exchange/day observations and original matched assignments were not available to this session. Source and historical treatment authentication are outstanding; the September pretrend and substantial October placebo warnings remain. Do not use this script to claim causality. No raw data or historical ZIP imported. The Nov 14 deadline was missed; Nov 30 is provisional, manuscript not publication-certified.

Run from repository root: `python -m unittest tests.test_phase412_october_placebo` and `python scripts/phase412_october_placebo.py PATH_TO_AUTHENTICATED_PANEL.csv`.
