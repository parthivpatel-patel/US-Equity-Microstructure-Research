# Phase 316 — Frozen-summary identification gate (2026-11-12)

## Scope
Read the two already-public Phase 130 CSVs from the connected GitHub repository. Ran the new standard-library diagnostic script against local transcriptions of their relevant columns and executed six synthetic-fixture unit tests (6/6 passing). This is a consistency check of published aggregate output, **not** an independent SEC-data replication. The full repository suite was not run.

## New cross-checks

| Outcome | November–October (pp) | Leave-one-group-out range (pp) | LOO sign preserved? | Bootstrap 95% interval includes zero? | Historical placebo minimum–maximum (pp) | Descriptive absolute-extreme windows |
| --- | ---: | --- | --- | --- | --- | --- |
| Count | −0.7346606599 | [−0.9696093829, −0.3841068921] | Yes | Yes | [−1.4475738789, 1.0538523294] | 2/78 |
| Volume | +0.6265979998 | [0.3276885583, 0.8524315188] | Yes | Yes | [−1.8665501313, 1.4840122109] | 76/78 |

Both point estimates are within the historical placebo minimum–maximum, and neither reported group-bootstrap interval excludes zero. Removing one matched group at a time preserves the sign **within the published range**, but this does not establish robustness to group construction, sampling weights, exchange composition, or serial dependence. The count/volume sign reversal persists. Historical placebo-window frequencies are descriptive, not p-values; the 78 windows overlap and may have been selected post hoc. The October announcement and September trends remain important identification concerns.

## Reproduction

```bash
python -m unittest discover -s tests -p 'test_phase316_identification_gate.py'
python -m scripts.phase316_identification_gate results/phase130_summary.csv results/phase130_group_sensitivity.csv
```

The script rejects duplicate outcomes, impossible placebo frequencies, inconsistent historical ranges, and invalid leave-one-group-out ranges. Tests use explicitly synthetic fixtures. No data or images were generated or uploaded. No third-party licensed datasets were redistributed.

## Publication gate

Treatment classification and SEC source bytes are not authenticated. Historical ZIP contents, redistribution permissions and file-by-file inventory remain unreconciled. No fresh pretrend, pseudo-event, exchange fixed-effect, common-date cluster or serial-dependence-aware estimate was calculated. These require the authenticated underlying security-date-exchange panel. The November 14 manuscript target remains conditional; do not claim a causal effect or completed validation.
