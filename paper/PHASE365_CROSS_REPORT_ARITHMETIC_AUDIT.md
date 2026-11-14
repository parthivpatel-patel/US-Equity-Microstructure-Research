# Phase 365 — archival placebo arithmetic audit (2026-11-14)

Sources inspected at parent commit f7f181eaee819b2d181f50d99b68786e162bee76: paper/PHASE130_REPORT.md and paper/PHASE157_ARCHIVE_EVIDENCE_RECONCILIATION.md.

Exact decimal cross-checks of the **reported** Phase 130 five-day contrasts: hidden-trade -1.335781 - (-0.601120) = **-0.734661 percentage points**; hidden-volume -0.006939 - (-0.633537) = **+0.626598 percentage points**. The contrasts have opposite signs. The reported prior pseudo-events equally or more negative number **2/78 (2.5641%)** for trade count and **48/78 (61.5385%)** for volume. These descriptive ranks are **not p-values**: scanned windows overlap, October 6 was selected exploratorily, and calendar dependence has not been calibrated.

Separately, the Phase 157 archival Phase 2 adjusted-versus-unadjusted hidden-volume coefficient shift is +0.014789 - (-0.025721) = **+0.040510 rate units = 4.051 percentage points**. Phase 2's 2,262-ticker cohort and Phase 130's 68 matched groups are distinct; do not pool these figures.

Reproduce the arithmetic with `python scripts/phase365_cross_report_arithmetic.py` (standard library). This is **not an independent SEC re-estimation**. The original dated 78-placebo series, source bytes, historical round-lot treatment, September pretrends, substantial October placebo, security/exchange coverage and dependence-aware inference remain unverified. No historical ZIP or licensed market data was imported. Historical original SEC ZIPs, Nasdaq snapshots, Phase 2 code/CSVs and reported 129 research ZIPs remain unpublished/unverified in this phase; the Phase 157 memo reports recovery of two archival text references only.

**November 14, 2026 deadline not met; manuscript uncertified.** Next: recover and authenticate source bytes and dated placebo outputs, then rerun pretrends and placebo tests under matched-group and common-date/serial-dependence-aware inference. No causal effect asserted.
