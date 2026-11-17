# Phase 433 — Common-date matched-cell support audit (2026-11-17)

## Question and new diagnostic

Earlier fixed-security and within-unit daily pairing gates (Phases 431–432) do not establish that different matched-group/exchange units are simultaneously observed. This matters for common-date inference and pooled placebo/pretrend comparisons: a collection of individually paired units can have **zero common paired dates**. The new script counts paired dates by matched group, exchange and pre/post period, then reports both the union and intersection of paired dates across eligible units. It also detects duplicate security/exchange/date records, invalid treatment labels, weekend dates and changing group/treatment assignments within security/exchange identifiers.

## Reproducible check

Run from the repository root with `PYTHONPATH=scripts python -m unittest -v tests/test_phase433_calendar_support.py` (or from a local directory containing both files). The implementation and eleven deterministic tests were executed together locally: 11 passed, 0 failures. A constructed example with two individually paired groups on October 30 and October 31 respectively produces zero common paired dates. Another constructed example with overlapping October 31 support produces one common paired date. These are **synthetic validation cases**, not empirical observations.

The audit defines common dates over units with at least one paired date; units with no paired dates are excluded from the intersection and must be inspected separately. It does not require that securities remain fixed across dates (use Phase 432 for that), authenticate the SEC source, identify exchange holidays, infer treatment, estimate any effect, or provide serial-/matched-group-/date-dependence-aware uncertainty. The distinction between ticker and stable security identifier requires upstream authentication. No source-data figures are produced.

## Status and next action

No original authenticated SEC daily panel, historical treatment mapping, or recovered licensed ZIP archive was imported. The Phase 430 prototype/tests remain unpublished. The substantial October placebo, September pretrends, selection/weighting sensitivity, and causal identification warnings remain fully in force. The November 14 publication deadline was missed and the manuscript is **not publication-certified**.

Next: run the published tests from the exact checkout; locate and authenticate original SEC daily records and treatment assignments; quantify common-date and fixed-security support before estimating September trends and October placebo with exchange controls and dependence-aware inference. Independent of GIG and other projects.
