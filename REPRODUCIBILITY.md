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
7. Verify full manuscript, code, figures and all uploaded archive hashes. The November 14, 2026 target has passed; no new publication date is certified.

## Scientific conclusion

No causal effect of the November 3, 2025 round-lot reform has been established. The existing analysis is an exploratory, falsification-focused working paper, not a peer-reviewed or fully verified release.


## Recovered Phase-2 processed-panel reproduction route (status: November 21, 2026)

The older Phase-130 instructions above describe a **different** 14,416-row daily matched-group input, which is still missing. Do not confuse that input with the recovered Phase-2 stock-level file `roundlot_phase2_security_panel.csv` (2,262 securities; 68 provisional treated; 2,194 provisional controls). The recovered file's reported SHA-256 is `2ccb80427a765ca3858f11f2874d6f87a79a559ec1fdeafc34420e82840e5bbb`. That digest fingerprints a **processed artifact**, not the original SEC ZIPs. The Phase-2 file is not distributed in this public repository; users must supply an authorized copy to reproduce the processed-panel calculations.

For the published robust-location sensitivity, execute:

```bash
python scripts/phase2_robust_location.py /path/to/roundlot_phase2_security_panel.csv --expect-sha256 2ccb80427a765ca3858f11f2874d6f87a79a559ec1fdeafc34420e82840e5bbb
python -m unittest discover -s tests -p 'test_phase2_robust_location.py'
```

For other processed-panel sensitivity analyses, inspect the corresponding scripts and results under `scripts/` and `results/` and their input assumptions before comparing numerical output. A unit test passing on fixtures, or reproducing a table from the recovered CSV, is **not** authentication of the upstream SEC source or historical Nasdaq classification.

### Source and treatment evidence status

- SEC's 2025 Q3/Q4 individual-security-and-exchange ZIP URLs are recorded in `provenance/SEC_Q2_Q4_2025_SOURCE_ACQUISITION_STATUS.md`. The original bytes and SHA-256s are **not yet obtained**. GitHub-hosted acquisition returned HTTP 403 for both quarters (run 44881411585); a local request failed DNS resolution. Neither is evidence that SEC removed the archives.
- The historical third-party Nasdaq snapshot audit found 84 valid non-100-share securities per snapshot, of which 68 matched the provisional treated cohort; 16 others did not match the processed panel under identical symbols. See `provenance/NASDAQ_SNAPSHOT_FULL_UNIVERSE_CORRECTION_2026-11-21.md`. This is **not** official September price-evaluation or November 3 effective-date roster certification.
- The Phase-2 panel contains period-level October/November aggregates, **not daily exchange-level observations**. It cannot be used to independently reproduce September pretrends, October within-month placebo, common-calendar clustering or serial-dependence-aware inference. Historical summaries of those analyses remain inherited, not independently source-row replicated.

**Fastest honest release boundary:** a clearly labeled exploratory methodological preprint can expose the processed-panel estimates, sensitivity analyses, source-acquisition failures and falsification warnings. It must not claim source-authenticated causal estimates, a completed full reproduction package or publication certification. The missing Phase 430/436/472 archives remain unverified and are not silently replaced by newly generated fixtures.
