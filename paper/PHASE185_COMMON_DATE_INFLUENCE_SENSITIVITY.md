# Phase 185 — common-date group/date influence sensitivity (2026-11-06)

## Contribution
Phase 184 established matched-group identity checks. Phase 185 adds descriptive leave-one-matched-group-out and leave-one-common-date-out influence diagnostics for both outcomes and all five window lengths. A single influential group or date can reverse the sign of an equal-group-date mean, even with an unchanged fixed roster. The script fails closed on duplicate rows, nonfinite contrasts, malformed dates, mismatched outcome dates, and changes to group identity across common dates/windows. At least two common dates and two groups are required.

## Reproducibility
Run `python scripts/phase185_influence_audit.py group_contrasts.csv` using the same five-column contract as Phase 184: `window_days,placebo_date,outcome,matched_group_id,contrast_pp`. Output contains baseline means, deletion ranges, maximum absolute changes and sign-flip flags. A closely corresponding local prototype passed eight deterministic unit tests on constructed observations on November 6, 2026. The exact published version still requires fresh-checkout testing and authenticated inputs.

## Identification and source limits
This is a **methodological diagnostic, not a new SEC historical estimate**. No original daily SEC panel, historical Nasdaq treatment assignments, fixed historical roster or recovered research ZIP/PDF was authenticated or imported. Deletion statistics are neither calibrated p-values nor serial-dependence-aware confidence intervals. Historical placebo-date membership and date-level contrasts remain missing, so the script cannot currently produce defensible empirical numbers. September pretrends, substantial October 2025 pre-reform placebo, selection/weighting sensitivity and security/exchange dependence must be resolved before any causal claim. Do not treat sign stability as evidence of causality.

## Next work
Recover original SEC daily security/exchange observations and source metadata (URL, retrieval date, checksum, schema, row counts, redistribution rights), historical treatment snapshots and matched-roster definitions. Build the group/date contrasts, rerun Phase 184 and Phase 185, then estimate security/exchange-controlled models with common-date and serial-dependence-aware inference. November 14, 2026 publication target remains conditional. **No causal effect established.**
