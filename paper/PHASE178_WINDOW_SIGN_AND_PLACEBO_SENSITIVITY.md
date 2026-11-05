# Phase 178 — published window sensitivity audit (2026-11-05)

## Provenance and execution

Input: existing public `results/phase131_window_sensitivity.csv`, read from the connected GitHub repository on 2026-11-05. Ten rows (five windows per outcome). This is a secondary audit of *published summary data*, **not** independent replication from authenticated SEC daily observations. Window endpoints, sampling, historical placebo design, treatment assignments, source-data hashes and licensing have not been authenticated. No historical ZIP was imported.

A standalone Python audit is published at `scripts/phase178_window_audit.py`; run from repository root with:

```bash
python scripts/phase178_window_audit.py results/phase131_window_sensitivity.csv
python -m unittest discover -s tests -p 'test_phase178_window_audit.py' -v
```

Eight closely matching local fixture tests passed before publication. The exact GitHub checkout was not separately executed.

## Recomputed descriptive results

| Window (trading days) | Count Nov–Oct (pp) | Count absolute placebo fraction | Volume Nov–Oct (pp) | Volume absolute placebo fraction |
|---:|---:|---:|---:|---:|
| 3 | −0.682345 | 7/82 = 8.54% | +0.201918 | 71/82 = 86.59% |
| 5 | −0.734661 | 2/78 = 2.56% | +0.626598 | 76/78 = 97.44% |
| 7 | −0.122428 | 12/74 = 16.22% | +0.987253 | 64/74 = 86.49% |
| 10 | +0.337165 | 21/68 = 30.88% | +1.156684 | 47/68 = 69.12% |
| 15 | −0.118296 | 3/58 = 5.17% | +0.718230 | 9/58 = 15.52% |

Count differences are negative in four windows but **reverse sign at ten days**; range −0.734661 to +0.337165 pp. Volume differences are positive in all five windows; range +0.201918 to +1.156684 pp. Arithmetic reconciliation of November minus October with the displayed differences has maximum absolute discrepancy approximately 0.000001 pp, consistent with six-decimal rounding.

**These are not five independent estimates or five independent hypothesis tests.** Windows overlap, and placebo counts change by window. Fractions are descriptive ranks against previously published placebo comparisons, not calibrated randomization p-values. Choosing a favorable window after examining the results would invalidate nominal significance. No multiple-window-adjusted inference has been established.

## Identification implications

The count sign reversal, the near-zero count difference at seven and fifteen days, the much weaker volume placebo comparisons for short windows, the documented September pretrends and substantial October pre-reform slope shift all preclude a clean causal interpretation. Equal-weight versus alternative-weight estimates, security/exchange controls, fixed-roster attrition, common-date and matched-group dependence, serial correlation, and authenticated treatment classifications remain required before publication. A bootstrap confidence interval crossing zero in the existing group-sensitivity table is another warning, not evidence of no effect.

## Historical artifact inventory and next action

Phase 176 found ten CSVs but no ZIP/PDF/Parquet archives on the inspected public main branch; none were recovered or imported here. Next: authenticate and checksum original SEC security/exchange daily archives and historical round-lot classifications; construct a fixed matched roster and calendar; re-estimate all five window specifications plus September pretrends and October placebo with dependence-aware uncertainty, prespecified weights and sensitivity to exclusion of suspect treatment labels. November 14 remains conditional. **No causal effect established.**
