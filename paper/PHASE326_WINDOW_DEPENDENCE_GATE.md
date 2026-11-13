# Phase 326 — Placebo-window dependence and chronology gate (2026-11-12)

## Repository inspection and new check

Read the existing Phase 325 reconstruction script and report, and inspected the public repository's results directory. The latter contains aggregate CSVs such as `phase130_summary.csv`, `phase131_window_sensitivity.csv`, and `phase137_block_bootstrap.csv`; no dated 78-window placebo input was identified in that directory. This is a scoped inventory observation, **not** proof that the original observations do not exist elsewhere or in historical archives.

The new `scripts/phase326_window_dependence_gate.py` accepts the Phase 325 dated-window schema and checks historical chronology (end before 2025-11-03), duplicate outcome/window identifiers, invalid dates, and pairwise date overlap. It reports the overlap graph's connected components. Eight synthetic unit tests passed locally, including inclusive boundary overlap, disjoint windows, transitive overlap, invalid dates, duplicates, and separate outcomes.

## Identification significance

Seventy-eight overlapping historical windows must **not** be treated as 78 independent placebo experiments. The connected-component count is a descriptive overlap diagnostic, **not** an effective sample size, a p-value, or a valid replacement for block or date-cluster inference. Even disjoint windows may remain dependent through common securities, market regimes, and serial correlation.

## Unresolved publication gates

The original 78 dated placebo rows and their generating code were not recovered in this session, so the overlap statistics for the real historical windows **cannot be computed**. The Phase 130 hidden-count contradiction (two reported absolute-extreme windows despite two negative-tail windows and a separately positive extreme maximum) remains unresolved. September pretrends, October placebo contamination, treatment-roster authentication, weighting/selection sensitivity, source-data byte provenance, security/exchange controls, matched groups and common-date/serial-dependence-aware inference all remain publication blockers. Historical ZIPs were not imported because their bytes, hashes and redistribution permissions were not available for verification.

## Reproduce

```bash
python -m unittest discover -s tests -p 'test_phase326_window_dependence_gate.py'
python scripts/phase326_window_dependence_gate.py PATH_TO_DATED_WINDOWS.csv
```

This is a **synthetic validation of a new audit tool**, not a new estimate from authenticated SEC data. The November 14 publication deadline remains conditional, and no causal or paper-completion claim is supported.
