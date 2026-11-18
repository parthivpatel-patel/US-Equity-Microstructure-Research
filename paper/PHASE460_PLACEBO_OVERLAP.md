# Phase 460: Pre-reform placebo-window overlap audit

This diagnostic is **calendar-only** and does not estimate effects or authenticate SEC data. The November 3, 2025 reform boundary is held fixed. For illustrative placebo cutoffs September 1 and October 1, 2025, the July 1–November 3 analysis window has 125 calendar days, and 30 days change from the placebo post-window to the placebo pre-window. Thus the two placebo estimates reuse the same overall observations and cannot be interpreted as independent replication.

The script flags cutoffs with insufficient **calendar-day upper bounds**; passing that flag does not imply enough observed exchange sessions or matched security-exchange support. A verified exchange calendar and observed support checks are still mandatory.

The existing October placebo warning and September pretrends remain substantive threats to identification. This diagnostic neither resolves them nor supports a causal claim. Source provenance, round-lot treatment authentication, common-date and matched-group support, security/exchange assignment checks, weighting sensitivity, and serial-dependence-aware inference must precede any publication-grade estimate.

Test command from repository root: `python -m unittest tests/test_phase460_placebo_overlap.py`. Tests use synthetic date inputs only. No historical ZIPs were imported in this phase. The November 14, 2026 target has passed; the paper is not publication-certified.
