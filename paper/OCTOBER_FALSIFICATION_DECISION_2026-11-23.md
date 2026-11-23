# October pre-reform falsification: publication decision (2026-11-23)

**Status:** audit of previously published numerical summaries, **not** a rerun on authenticated SEC source records. The November 3, 2025 round-lot change cannot explain an October 2025 movement as a post-treatment effect.

## Existing evidence examined

Source files in this repository: `results/phase136_trend_uncertainty_presentation.csv`, `results/phase139_paired_october_shift_presentation.csv`, and `results/phase140_paired_interval_width_audit.csv`. These outputs have not been source-replicated from original SEC Q3/Q4 ZIP archives; stock-specific treatment assignment also remains provisional.

* The Phase 136 July–September count slope is **+0.028607 percentage points per session** (68 groups, 64 sessions). Its lag-5 two-way interval is **[+0.006235, +0.050979]**. The corresponding volume slope is **-0.001464**, interval **[-0.021680, +0.018752]**.
* Phase 139 reports October slopes of **-0.141590** (count) and **-0.157880** (volume) percentage points per session, versus July–September slopes of **+0.028607** and **-0.001464**, respectively. October-minus-July–September slope differences are **-0.170197** (count) and **-0.156416** (volume).
* Across the four reported bootstrap block lengths (3, 5, 10, 15 sessions; 2,000 draws each), **all eight** Phase 139 intervals for the October-minus-July–September difference lie below zero. For count, the intervals are [-0.276633, -0.061064], [-0.276373, -0.061328], [-0.295482, -0.049174], [-0.299240, -0.047068]. For volume: [-0.252181, -0.046798], [-0.250259, -0.054541], [-0.254761, -0.059799], [-0.257065, -0.061678]. These are *inherited exploratory intervals*, not independently certified uncertainty statements.

## Consequences for the manuscript

1. **Do not present November changes as a clean reform-induced effect.** The reported October shift predates implementation and is quantitatively substantial; it may reflect changing composition, seasonal trends, exchange behavior, measurement, or other confounders. The existing summaries cannot adjudicate these explanations.
2. **Do not interpret the eight bootstrap intervals as eight independent confirmations.** They reuse the same underlying data and differ only in block length; source provenance and bootstrap implementation must still be checked.
3. **Treat September pretrends and October falsification as primary results**, not robustness footnotes. Report descriptive associations and estimator sensitivity alongside these threats.
4. **Release decision:** a transparent exploratory working paper can present these inherited results explicitly as unverified, but a source-replicated or causal claim is not defensible until raw SEC archives, historical stock-specific assignment, and common-calendar source-level falsification are verified.

## Remaining source requirements

The SEC Q3 and Q4 original archive bytes and SHA-256 values remain unavailable in this research environment; previously documented GitHub-hosted requests returned HTTP 403. An ordinary authorized client should obtain the ZIPs, record original and member hashes, and reconstruct daily security–exchange observations with a common trading calendar. Authenticate the September 2025 price-evaluation treatment roster and symbol history before recomputing pretrends, placebo tests, matched comparisons, and dependence-aware inference. The Phase 430/436 and 472 packages are not yet recovered.

No third-party raw data are redistributed here. This note is independent of other projects.
