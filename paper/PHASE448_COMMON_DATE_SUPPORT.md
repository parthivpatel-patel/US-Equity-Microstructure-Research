# Phase 448 — Matched-group common-date support audit

Date: 2026-11-18. Status: software validation only; no authenticated SEC panel or historical effect estimation.

## Methodological finding

A placebo or reform comparison may be unsupported even when both treated and control securities appear somewhere in the panel: they must appear **on the same dates within the same exchange and matched group**. Pooling non-overlapping dates can confound calendar effects with treatment composition. Phase 448 reports common-date counts for September 2025, October 2025, pre/post October 1 placebo, and pre/post November 3 reform. The default two-common-date minimum is a **software smoke-test threshold, not an inferential adequacy threshold**. Actual estimation needs a prespecified and much stronger design-support policy.

## Reproduction

From the repository root:

```sh
PYTHONPATH=scripts python -m unittest discover -s tests -p 'test_phase448_calendar_support.py' -v
```

Ten deterministic tests passed in the local working copy on constructed observations. Exact published checkout and full repository suite have not been run. No source authentication, historical treatment verification, serial-dependence correction, or causal interpretation is supplied by this diagnostic.

## Limitations and next tasks

The audit requires preassigned exchange-specific matched groups; it does not validate how groups were chosen. It checks overlap, not missing-data mechanisms, date serial dependence, sufficient independent clusters, exchange fixed effects, or treatment stability. The October 2025 placebo warning and September pretrends remain substantive threats to identification. The November 14 manuscript deadline was missed and publication certification is withheld. Original SEC source data, authenticated treatment, recovered ZIP archives, and Phase 430/436 prototypes remain unavailable/unpublished in this session. Next: integrate source-bound validation, authenticate observations, and compute actual supported placebo/pretrend designs before inference.
