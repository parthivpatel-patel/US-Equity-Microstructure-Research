# Phase 331 — Cross-table joint feasibility gate (2026-11-13)

## Inputs and execution
Read existing public repository files `results/phase130_summary.csv`, `results/phase131_window_sensitivity.csv`, and `paper/PHASE330_WINDOW_ARITHMETIC_GATE.md` before adding new files. The Phase 331 script uses standard-library CSV and exact Decimal comparisons. Execute from repository root:

```sh
python scripts/phase331_cross_table_joint_gate.py results/phase130_summary.csv results/phase131_window_sensitivity.csv
python -m unittest discover -s tests -p 'test_phase331_cross_table_joint_gate.py' -v
```

The first command is **expected to exit 1** while the published count-row contradiction persists. This is a publication gate, not a broken implementation.

## Audited published aggregates
For the five-day hidden-count row, Phase 130 reports an event contrast of -0.7346606598677254 percentage points, 78 placebo windows, two negative-tail windows, two absolute-extreme windows, and a maximum placebo contrast of +1.0538523294152946. Because the event contrast is negative, each negative-tail observation is an absolute extreme; the positive maximum also exceeds the event's absolute magnitude and cannot be one of those negative-tail observations. Hence the minimum absolute-extreme count is **3**, contradicting the reported **2**.

The five-day Phase 131 row reproduces the same 78, 2, 2 counts and agrees with the Phase 130 event contrast within six-decimal rounding. It therefore propagates, rather than independently resolves, the contradiction.

For hidden volume, the reported event contrast is +0.626597999820323; the negative minimum of -1.8665501312689659 guarantees at least one absolute extreme. Its reported 76 absolute-extreme observations satisfy this *necessary* condition, but are not authenticated.

## Validation and limitations
Seven synthetic tests passed locally (zero failures). A local execution using manually transcribed rows from the fetched Phase 130 and 131 GitHub CSVs returned the expected fail-closed result for count and a passing necessary-condition result for volume. This is an aggregate consistency audit, **not** a fresh SEC-panel analysis. The complete published checkout regression suite was not executed. The original dated 78 placebo observations and generating code were not recovered.

September pretrends, the substantial October 2025 placebo warning, treatment authenticity, matched/security/exchange controls, selection and weighting sensitivity, common-date and serial-dependence-aware inference, and source-data provenance remain unresolved. No causal claim or calibrated p-value follows. Historical ZIPs remain unimported pending identification, licensing, and checksum verification.

## Publication decision
The November 14 target is **not certified**. Preserve all earlier results as provisional, block claims based on the inconsistent count-row tail statistic, and prioritize locating the Phase 130 producing code and dated observations. Next, run Phase 325–331 gates on authenticated observations and reconstruct all tail counts and extrema before estimating any new matched-panel effects.
