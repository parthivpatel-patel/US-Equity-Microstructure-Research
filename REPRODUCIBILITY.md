# Reproducibility and release gates

## What has been published

The recovered Phase 130 exploratory analysis script, two frozen result tables, and a report with uncertainty and identification warnings are on GitHub. See `provenance/PHASE130_INPUT_AND_OUTPUT_HASHES.json` for the archived input and output file digests.

## Requirements to run end-to-end

The **processed 14,416-row matched-group input** named `daily_group_contrasts.csv` must be placed in `src/` next to `phase130_analysis.py`; it has **not yet been uploaded**. Install the packages in `requirements.txt` and execute `python src/phase130_analysis.py`. Compare the resulting SHA-256 digests with the archived manifest. The pinned dependency environment, automated tests, raw SEC source provenance and historical Nasdaq classifications are **not yet certified**. The script's exact row/group assertions do not themselves establish data authenticity.

## Source-data and treatment checks still open

1. Reconcile original SEC quarterly archives and version/checksum history.
2. Authenticate September 2025 Nasdaq round-lot production assignments using the applicable price-based classification rules and corporate-action/identity history.
3. Document all included/excluded 68 matched groups and 14 venues, especially complete-case selection and thin-trading venue missingness.
4. Freeze outcome definition, horizons, weights, and estimators; distinguish exploratory from confirmatory analyses.
5. Implement matched-group and common-calendar-date inference with serial dependence and pre-reform placebo checks.
6. Review data redistribution rights before uploading raw SEC/Nasdaq/NYSE or third-party materials.
7. Verify full manuscript, code, figures and all uploaded archive hashes. Until then the November 14 date is a target only.

## Scientific conclusion

No causal effect of the November 3, 2025 round-lot reform has been established. The existing analysis is an exploratory, falsification-focused working paper, not a peer-reviewed or fully verified release.
