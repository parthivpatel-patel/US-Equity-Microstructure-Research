# Phase 157 — Archival empirical-evidence reconciliation (2026-11-04)

## Scope and newly located source

A search of the user's historical research file library recovered a **text memo**, `RESEARCH_PHASE2_2026-10-27.md`, and an earlier pilot memo, `RESEARCH_PROGRESS_2026-10-27.md`. These are archival *reports*, not the underlying original SEC data or verified Nasdaq assignment files. The Phase 2 memo identifies its required original inputs as `individual_security_2025_q4.zip` (member `q4_2025_all.csv`) and October/November 2025 Nasdaq snapshots, and identifies the missing replication program `roundlot_phase2.py` and outputs `roundlot_phase2_security_panel.csv`, `roundlot_phase2_inference.csv`. These files were **not recovered** in this session. No ZIP was imported. No rights to redistribute raw archives were established.

The archival Phase 2 sample is **2,262 tickers**, comprising **68 provisionally reduced-lot** and **2,194 100-share** tickers, with October 1–31 before and November 3–28 after, at least ten observed days each period. This is **not** the later matched sample of 68 provisional treated and 204 matched controls described in the repository README. Mixing these denominators would misstate the estimator and sample.

## Arithmetic audit of archived coefficients

The accompanying executable test independently recalculates rounded Wald 95% intervals and z ratios from coefficients and HC3 standard errors *transcribed from the archived memo*. Differences of approximately one millionth in some published interval endpoints are consistent with rounded reported inputs. This is **not an independent re-estimation**.

| Phase 2 model | Archived coefficient | Archived HC3 SE | Recalculated z |
|---|---:|---:|---:|
| Hidden-trade rate, unadjusted | -0.034629 | 0.004418 | -7.83816 |
| Hidden-trade rate, baseline-adjusted | -0.010815 | 0.005041 | -2.14541 |
| Hidden-volume rate, unadjusted | -0.025721 | 0.004213 | -6.10515 |
| Hidden-volume rate, baseline-adjusted | +0.014789 | 0.005569 | +2.65559 |
| October split placebo, trade rate | -0.011703 | 0.004424 | -2.64534 |

Baseline adjustment changes the archived hidden-volume coefficient by **+0.040510 rate units (4.051 percentage points)**, reversing its sign. This is a *difference between model coefficients*, not a treatment-effect estimate. The archived October placebo remains nonzero on its reported HC3 scale, but this inference does not account for common-date dependence or all sample-selection mechanisms. October 1 also coincides with publication of future round-lot assignments and is not a pure no-information placebo.

The earlier pilot memo reports **5,110 stable Nasdaq symbol matches** across snapshots and pooled October/November rate comparisons on a different cohort. These figures are not interchangeable with Phase 2 or later matched-panel results.

## Evidence status and publication inventory

- **Now recovered as accessible historical text references:** October 27 pilot memo and October 27 Phase 2 memo; the latter's numeric statements were audited arithmetically. These are source *summaries*, not authenticated primary observations.
- **Published in this phase:** this reconciliation note and its executable arithmetic test. The archival memos themselves were **not copied** to GitHub; exact original content remains in the user's historical file library.
- **Still not recovered or published:** original SEC Q3/Q4 ZIP contents; original Nasdaq snapshots; `roundlot_phase2.py`; Phase 2 panel and inference CSV; the complete 129 historical phase ZIPs (~1.16 GB previously inventoried); complete source hashes/permissions.
- **Still unresolved:** historical operative treatment authentication, September pretrends, October placebo identification, security/exchange missingness and composition, denominator weighting, group and calendar-date dependence, whole-scan bootstrap calibration.

## Scientific interpretation

The earlier Phase 2 volume sign reversal and October placebo reinforce **identification failure for simple causal claims**, rather than confirm a reform effect. Neither the archived HC3 p-values nor the synthetic bootstrap calibrations are sufficient for a publication-grade causal claim. The November 14 target is contingent on source authentication and a reproducible manuscript.

## Next specific task

Locate the original `roundlot_phase2.py` and source/panel artifacts through historical files, verify hashes and redistribution rights, reconcile keys to original SEC security-date-exchange rows and Nasdaq assignments, then re-estimate pretrend/placebo models with explicit exchange composition and common-date/serial dependence. Preserve raw restricted data outside the public repository.
