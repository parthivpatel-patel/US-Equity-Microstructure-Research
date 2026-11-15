# Phase 373 — Combined structural and exact-integer panel gate

Date: 2026-11-14. Status: software validation only; no authenticated SEC data processed.

## Motivation

Phase 371 checks security-date-exchange uniqueness, cohort stability and count consistency using binary floating-point conversions. Phase 372 separately checks exact integer counts using decimal arithmetic. Running only Phase 371 leaves a precision-sensitive numerator/denominator comparison vulnerable above 2^53. This wrapper requires **both** checks to pass and their row counts to agree.

## Reproduction

Run `python scripts/phase373_combined_panel_gate.py path/to/canonical_panel.csv --output gate.json`. The command returns exit code 2 for a failed gate. Run `python -m unittest discover -s tests -p 'test_phase373_combined_panel_gate.py' -v` for six constructed-fixture tests.

Six focused tests passed in a local Python environment against faithful local copies of the previously fetched Phase 371 and 372 modules. The exact published checkout and complete repository regression suite have not been run. Test inputs are synthetic, never represented as SEC observations.

## Limits and publication gate

A passing structural check is **not** evidence that source bytes came from the SEC, that the round-lot treatment was correctly assigned historically, or that the event study is identified. September pretrends, the large October placebo, original 78 dated pseudo-events, Phase 130 contradictions, selection/weighting sensitivity, common-date shocks and serial dependence all remain open. No causal claim is warranted.

Next: run the exact published checkout, inventory and authenticate recoverable original archives and source transformations, then reconstruct placebo estimates and dependence-aware inference. The November 14 manuscript deadline was not met; the manuscript remains uncertified.
