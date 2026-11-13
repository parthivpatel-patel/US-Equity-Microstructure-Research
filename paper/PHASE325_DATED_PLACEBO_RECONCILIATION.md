# Phase 325 — Dated placebo reconstruction gate (2026-11-12)

Read the published `results/phase130_summary.csv` and `scripts/phase324_placebo_partition_gate.py` before adding these new files.

## Reproducibility

The standard-library script accepts dated placebo rows with columns `outcome,window_id,start_date,end_date,placebo_pp`. It rejects duplicate identities, malformed dates, nonfinite values, outcome mismatches and missing windows. It reconstructs lower-tail counts, absolute-extreme counts, extrema, event ties, opposite-event ties and right-tail frequencies using exact decimal comparisons. Run `python scripts/phase325_placebo_row_reconciliation.py PATH_TO_WINDOWS.csv`; mismatches produce exit code 2. Run `python -m unittest discover -s tests -p 'test_phase325_placebo_row_reconciliation.py'`.

Seven analogous local synthetic reconciliation checks were executed successfully before publication. The repository module is additive; its contents were separately reviewed, but the exact repository checkout was not executed in this session.

## Findings and limitations

The Phase 130 count row remains inconsistent under the documented common-sample tail definitions: event contrast −0.7346606598677254, two lower-tail observations, two absolute-extreme observations and positive maximum +1.0538523294152946 imply at least three absolute extremes. This is a logical contradiction in published aggregates, not an SEC-panel result.

The original 78 dated placebo observations and their generating code were not recovered in this phase. Therefore this new gate has not been applied to actual SEC-derived observations. No historical ZIP archive was imported; archive permissions, hashes and completeness remain unverified.

## Next priority

Recover dated windows and their generating code, reconcile sample membership and filters, then authenticate original SEC bytes and historical treatment assignment. Re-run September pretrends, October placebo, weighting and security/exchange controls, and matched-group plus common-date and serial-dependence-aware inference. November 14 publication remains conditional; no causal or completion claim is warranted.
