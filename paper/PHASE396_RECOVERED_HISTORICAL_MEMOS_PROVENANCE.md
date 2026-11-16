# Phase 396 — Historical memo recovery and evidence triage (2026-11-15)

Two previously produced research memos were located through the user's file collection and restored **as historical documents**, without changing their original claims:

- `archive/recovered_memos/RESEARCH_PHASE2_2026-10-27.md` (source file title: `RESEARCH_PHASE2_2026-10-27.md`; 33 lines reported by file reader; archived research text).
- `archive/recovered_memos/RESEARCH_PHASE63_2026-10-31.md` (source file title: `RESEARCH_PHASE63_2026-10-31.md`; 80 lines reported by file reader; archived research text).

## Recovered evidence — NOT newly recomputed

**Phase 2 (October 27, 2026)** reports 2,262 stocks (68 reduced-lot and 2,194 100-share); a pre-reform October placebo trade-rate coefficient of -0.011703 with HC3 SE 0.004424 and p=0.00816; and a volume-rate coefficient reversal from -0.025721 unadjusted to +0.014789 baseline-adjusted. Those are **historical memo-reported statistics**, not independently reproduced in this recovery session. Phase 2 explicitly warns that its Nasdaq snapshot-based treatment labels and cross-sectional HC3 inference are insufficient for causal identification.

**Phase 63 (October 31, 2026)** describes a common 50-matched-group, 10-venue design with ten-day calendar-boundary contrasts. It reports that, across the ten venues, the absolute pre-reform October-minus-September contrast is at least as large as the November-minus-October contrast in 8/10 venues for raw hidden-trade-count rate, 6/10 for raw hidden-share-volume rate and 2/10 for the raw volume-minus-count wedge. These counts are **descriptive, not p-values**, and the original SEC ZIPs were not independently reconciled to the inherited panel in that analysis. The memo also notes the August placebo's post-boundary cohort-selection lookahead.

## Why recovery matters

The original texts preserve the magnitude and design of a **substantial pre-reform falsification warning**. Later fixture-only software tests must not be described as resolving it. Phase 2 and Phase 63 use different populations and estimands and their reported numbers must not be pooled as if from one prespecified analysis.

## Not yet recovered or published by this recovery

The underlying Phase 2 script, raw Nasdaq snapshots, SEC Q4 ZIP and output CSVs; the Phase 63 source panel, script, tests, plots, CSV outputs and checksum logs; the original 78 dated placebo records; and the reported historical research ZIP collection were **not** recovered in this session. The user's file collection may contain additional material not yet exhaustively inventoried. Do not infer any raw-data rights or authenticity from memo recovery.

## Release decision and next action

Historical documents are suitable for publication as **clearly labeled research archives**, but their empirical claims remain **unverified in this session**. Next recover executable source and hashed inputs, verify raw SEC rows and round-lot assignment provenance, then rerun Phase 2 and Phase 63 with matched/common-date and serial-dependence-aware uncertainty. November 14, 2026 deadline was missed; November 30 is a provisional target, not certification.
