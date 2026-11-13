# Phase 324 — Placebo partition feasibility and source-tracing status (2026-11-12)

## Exact public inputs
Read `results/phase130_summary.csv` and `scripts/phase323_placebo_joint_gate.py` before this additive change. This report does not alter or repair the source CSV. GitHub code-search attempts for `phase130_summary.csv`, `pre_placebo_at_least_as_negative`, and `pre_placebo_at_least_as_extreme_absolute` returned no matching indexed code; **absence from search is not evidence that the producer does not exist**. Original dated placebo windows and producer remain unverified.

## Necessary-condition derivation
Let n be the number of placebo observations, d the event contrast, L=#(x<=d), and A=#(|x|>=|d|). For negative d, every observation in the lower partition is an absolute extreme, so A>=L. If max(x)>=-d, the maximum is a distinct positive extreme, so A>=L+1. For positive d, all n-L observations in the upper partition x>d are absolute extremes; if min(x)<=-d, the minimum is an additional distinct negative extreme, giving A>=n-L+1. These are necessary bounds, not sufficient conditions for a jointly feasible dataset.

The frozen count row has d=-0.7346606598677254, L=2, A=2, max=1.0538523294152946, hence **A>=3 contradicts A=2**. The volume row has d=0.626597999820323, n=78, L=48, A=76, min=-1.8665501312689659, hence A>=31; it is not disproved by this necessary condition. In addition, A=76 means exactly two observations have |x|<|d| if the column definitions hold, but the identities and dates of those observations cannot be recovered from aggregates.

## Reproduction and limits
Run `python -m unittest tests/test_phase324_placebo_partition_gate.py` and `python scripts/phase324_placebo_partition_gate.py` from the repository root. The tests exercise published rows and synthetic edge cases. They do **not** authenticate SEC inputs, infer the placebo chronology, or calibrate p-values. The earlier Phase 322–323 count-row warning is retained, and all conclusions relying on the inconsistent count-row joint distribution must remain suspended.

## Publication gate
November 14, 2026 is a target, not a claim of completion. Before release, recover the dated 78 placebo observations and their generation code; check the October 2025 placebo and September pretrends; authenticate SEC source bytes and historical round-lot treatment; rerun security/exchange controls, matched-group and weighting sensitivity, common-date and serial-dependence-aware inference. Reconcile historical ZIP members, hashes, provenance, licensing, and publication inventory. No historical archive was imported in this phase. No causal claim is supported.
