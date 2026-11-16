# Phase 413: October placebo cutoff scan (methodology only)

The November 3, 2025 reform cannot explain changes occurring during October. A substantial historical October placebo signal remains an identification warning, not a finding to suppress.

This stdlib-only script requires security, match_group, exchange, date, treated, hidden_trades and total_trades. It validates duplicate security/exchange/date rows and integer count bounds. It retains only October matched-group/exchange/date cells containing both arms. Each cell computes treated minus control hidden-trade-count rates in percentage points. It then equal-weights cells within each date and compares mean daily gaps around October 8, 15 and 22. These are **different estimands** from pooled-denominator and cell-weighted contrasts.

For each fixed cutoff, a Bartlett/Newey-West score autocovariance estimate with maximum lag three provides a descriptive time-series standard error. This is **not** a valid simultaneous-inference or multiple-cutoff significance test, and a few October dates make asymptotic inference fragile. There are no p-values or claims of treatment effects. The script does not establish historical treatment assignment, data provenance, exchange-level stability, September pretrends, or the validity of matching. It cannot resolve selection induced by common support. Common-date shocks and matched-group dependence require stronger inference once authenticated panel data is recovered.

Run: `python scripts/phase413_placebo_scan.py /path/to/authorized_panel.csv`. Tests: `python -m unittest discover -s tests -p 'test_phase413_placebo_scan.py'`. Seven deterministic fixture tests passed on the locally tested implementation. No actual historical panel was executed in this session. The original ZIPs and restricted datasets remain unimported pending access and redistribution review.

**Publication gate:** November 14, 2026 deadline missed; November 30 provisional. Manuscript not certified. Next: authenticate historical source and original 68/204 treatment/control mapping, recover September, run this scan and compare weighting, pretrends and dependence-aware placebo inference on the same matched sample.
