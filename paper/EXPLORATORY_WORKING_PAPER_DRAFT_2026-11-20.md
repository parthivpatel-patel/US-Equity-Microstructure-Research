# Hidden Execution Around the November 2025 Round-Lot Reform: An Exploratory Falsification and Robustness Study

**Independent working-paper draft — November 20, 2026. NOT source-authenticated, NOT peer-reviewed, NOT publication-certified.**

## Abstract

The November 3, 2025 U.S. equity round-lot reform offers a natural setting for investigating how measured hidden execution depends on outcome definitions, treatment assignment, comparison securities, weighting and event windows. An archived, processed October–November stock-level panel includes 2,262 Nasdaq symbols, 68 provisionally treated and 2,194 provisional controls. Unmatched equal-security treated-minus-control changes are −3.46 percentage points for hidden-execution trade count and −2.57 pp for hidden share volume. Both attenuate sharply after baseline matching. A pre-trade-weighted volume comparison has a security-bootstrap interval spanning zero; a baseline-adjusted volume regression reverses sign. Earlier historical summaries also indicate substantial pre-reform September/October movements. These observations demonstrate **design sensitivity and identification risk**, not a causal effect of the reform. Original SEC source ZIPs, security-level effective-date round-lot assignments, and daily/exchange source joins are not yet independently authenticated.

## 1. Research question and data

The question is not simply whether hidden execution changes around November 3, but whether any measured change survives falsification and specification tests. SEC *Metrics by Individual Security and Exchange* reports Hidden, TradesForHidden, HiddenVol, TradeVolForHidden, Ticker, Date, Security and related fields. Trade-count and share-volume hidden rates measure different quantities. Primary source listing: https://www.sec.gov/data-research/sec-markets-data/market-structure-data-security-exchange . The 2025 Q3/Q4 ZIPs are listed there, but their original bytes and member hashes have **not** been obtained or authenticated in this research environment.

The recovered processed stock-level file is `roundlot_phase2_security_panel.csv`, SHA-256 `2ccb80427a765ca3858f11f2874d6f87a79a559ec1fdeafc34420e82840e5bbb`. This digest identifies the **recovered processed file only**, not its original SEC provenance. The 2,262 symbols comprise 68 provisionally affected and 2,194 provisional controls. Historical Nasdaq round-lot assignment and ticker continuity require independent verification. This file aggregates October pre-period and November post-period rates and has no daily/exchange rows. Consequently it cannot itself support September trends, October placebo-date regressions, venue effects, common-date clustering or serial-dependence-aware inference.

Separately, inherited historical security-date-exchange work reports 580,715 observations over 14 exchanges, with a distinct matched cohort of 68 treated and 204 controls. That is a **different sample and estimator**. Historical summary arithmetic was checked in prior sessions, but source-row authentication is outstanding. Do not merge results from these samples or describe the historical outputs as newly replicated from original SEC records.

## 2. Estimands and methods

For security i and period p, the count rate is the sum of hidden trades divided by the sum of eligible trades; the volume rate is the sum of hidden shares divided by the sum of eligible shares. Each security's period-level post-minus-pre change is compared between provisional treatment groups. The equal-security descriptive contrast is the difference in mean security changes; it is **not** a causally identified difference-in-differences estimand.

Exploratory robustness methods include baseline pre-trade-count weighting, baseline nearest-neighbor matching with replacement on pre-hidden-trade rate, pre-hidden-volume rate and log baseline trading activity, 5,000 within-group security bootstrap draws, leave-one-treated-security-out influence, and symmetric tail trimming within treatment groups. These approaches change assumptions or target populations and do not resolve omitted confounding or historical treatment uncertainty.

## 3. Descriptive findings

| Comparison | Hidden-trade count gap (pp) | Hidden-share-volume gap (pp) |
|---|---:|---:|
| Unmatched equal-security | −3.4629 | −2.5721 |
| Pre-period trade-count weighted | −2.7064 | −1.0065 |
| Exclude bottom pre-trade quartile within each arm | −4.1583 | −3.0891 |
| 1 nearest baseline control per treated name | −1.1362 | −0.5746 |
| 3 nearest baseline controls | −1.1410 | −0.6238 |
| 5 nearest baseline controls | −0.9398 | −0.3602 |

The treated-minus-control pre-period hidden-rate gaps are +14.57 pp by count and +20.14 pp by volume, showing serious initial imbalance. A later baseline-overlap audit reports treated versus control medians of **49.38% versus 32.72%** for pre-period hidden trade rates, **49.61% versus 27.55%** for pre-period hidden volume rates, and **312,932 versus 62,195** eligible pre-period trades. Its reported standardized differences are **+1.90**, **+2.49**, and **+1.34**, respectively (see `paper/BASELINE_OVERLAP_AUDIT_2026-11-21.md`). These are descriptive diagnostics, not a proof of common support or lack thereof. Pre-trade-weighted treated effective sample size is 10.40 despite 68 nominal treated names. The largest treated security accounts for 26.2% of treated pre-trade weight, and the largest five for 54.7%.

Security-bootstrap percentile 95% intervals from earlier recovered-panel analysis were: equal-security count [−4.31, −2.61] pp; equal-security volume [−3.39, −1.78]; pre-trade-weighted count [−4.88, −1.16]; and **pre-trade-weighted volume [−3.42, +0.67]**, crossing zero. These are independent-security bootstrap intervals, **not valid common-date/serial-dependence-aware event-study confidence intervals**. A cross-sectional HC3 regression of the volume change has a coefficient −0.02572 unadjusted and +0.01479 when adjusted for both baseline hidden rates: a substantive sign reversal, not a basis for selecting the more convenient estimate.

### Matched-overlap and estimand-selection sensitivity (November 21 follow-up)

The subsequent nearest-neighbor caliper analysis retains **68/68** provisional treated securities without a distance restriction, but only **49/68** at a **0.25 pooled-SD-scaled Euclidean caliper**. The unrestricted 1-neighbor design uses just **39 distinct controls** with replacement, and one control is reused **nine times**. This is not a 68-versus-68 independent matched sample. At the stricter 0.25 caliper, the descriptive count/volume change gaps are **−0.5166/−0.0412 pp** (49 treated, 31 unique controls), compared with **−1.1362/−0.5746 pp** without a caliper. At 0.50 they are **−1.0379/−0.4764 pp** (63 treated, 37 unique controls). These differences are not nested confidence intervals and **must not be interpreted as attenuation for a fixed treated population**: tighter calipers discard treated securities, change the target population, and can induce selection on measured characteristics. Nor do the low observed imbalances on the three matching covariates establish balance on price, exchange, capitalization, identity, or unmeasured shocks. See `paper/CALIPER_OVERLAP_SENSITIVITY_2026-11-21.md` and `results/phase2_caliper_overlap_2026-11-21.json`.

The later pre/post date-completeness audit found **68/68 treated** with the maximum observed **23 October pre-period and 19 November post-period days**, versus **2,162/2,194 controls**. The maximum-days restriction therefore removes 32 controls and zero treated securities. These are the processed panel's observed-day maxima, not independently verified market-calendar counts. The exclusion is a possible additional selection mechanism, not proof of selective reporting.

### Interpretation hierarchy

1. **Directly reanalyzed processed stock-level data:** descriptive gaps, trimming, matching, caliper attrition, weighting, influence and security-bootstrap results; integrity checks validate the recovered file internally but not SEC provenance.
2. **Historical inherited summaries:** September pretrends, October placebo and venue/date results; their reported arithmetic has been checked, but original source rows, treatment roster and analysis execution remain unverified.
3. **Unsupported as of this draft:** a causally identified round-lot treatment effect, stock-specific effective-date treatment certification, original SEC ZIP/member checksums, and dependence-aware inference from authenticated daily security-exchange observations.

This hierarchy is essential: agreement of numerical outputs with a processed CSV is **not independent replication** of SEC measurements.

### New robust-location sensitivity

Using the same recovered processed panel, trimming the lowest and highest 5%, 10% or 20% of security changes *within each group* gives:

| Fraction trimmed from each tail | Count gap (pp) | Volume gap (pp) |
|---|---:|---:|
| 0% | −3.4629 | −2.5721 |
| 5% | −3.5151 | −2.6334 |
| 10% | −3.5598 | −2.6428 |
| 20% | −3.4790 | −2.6183 |

Thus extreme individual change values alone do not explain the unmatched gap. This **does not counteract** matching, weighting, baseline-model and historical pretrend sensitivity, which diagnose different problems. The calculations use the archived processed file and are reproducible from the accompanying script and JSON, with no original-SEC authentication implied.

## 4. Falsification and interpretation

An inherited October-only placebo split (October 1–15 versus October 16–31) reports a hidden-trade differential of −0.011703 in fractional rate units (−1.1703 pp), HC3 p = 0.00816, for 2,258 provisional securities. The October 1 date may also carry assignment-information/anticipation effects, so this is a warning rather than a clean no-information placebo. In separately inherited historical summaries, the July–September count pretrend HAC-lag-5 interval is [0.006235, 0.050979] pp per trading session; reported October-minus-July/September slope changes are −0.170197 pp/session (count) and −0.156416 pp/session (volume). These summaries are **not** source-row replicated and their estimands differ from the October–November stock-level panel. Overlapping historical pseudo-event windows and post hoc specification searches prevent interpreting their apparent ranks or p-values as final calibrated inference.

A November 3 reform-date dummy cannot by itself distinguish treatment from contemporaneous shocks, anticipation, selection, changes in venue coverage or structural pretrends. The evidence therefore supports a narrower finding: **provisional hidden-execution comparisons are sensitive to baseline comparability, weighting, specification and pre-reform patterns**. It does not establish that the round-lot reform caused an increase or decrease in hidden execution.

## 5. Required verification and limitations

Outstanding gates: (1) obtain and hash original SEC 2025 Q3/Q4 ZIP bytes and internal CSV members; (2) reconcile security-date-exchange keys, eligible denominators, date calendar and venue coverage; (3) authenticate stock-specific round-lot assignments effective November 3 using contemporaneous September reference prices and symbol/corporate-action history; (4) freeze eligible treated/control and matched rosters; (5) rerun September pretrends, October falsification, exchange/security/common-date comparisons and serial-dependence-aware joint inference on authenticated daily data; (6) reproduce all results from a clean checkout; (7) recover and inventory prior Phase 430/436/472 archives where authorized. No original third-party source ZIPs are redistributed.

## 6. Reproducibility and release decision

Archived processed input SHA-256: `2ccb80427a765ca3858f11f2874d6f87a79a559ec1fdeafc34420e82840e5bbb`. Run `python scripts/phase2_robust_location.py /path/to/roundlot_phase2_security_panel.csv --expect-sha256 2ccb80427a765ca3858f11f2874d6f87a79a559ec1fdeafc34420e82840e5bbb`; run `python -m unittest discover -s tests -p 'test_phase2_robust_location.py'`. Prior matching, influence, bootstrap and panel-validation scripts/results are published separately with their own caveats. A SHA-256 match is **not** original-source authentication.

**Publication status:** exploratory working-paper draft only. This document integrates follow-up baseline-overlap and caliper findings through November 21, 2026, but no new SEC raw-data authentication is claimed. The November 14, 2026 target was missed. A public provisional methodological preprint can explicitly report these limitations, but the paper cannot be described as source-verified, causally identified or publication-certified until the gates above are met. The project is strictly independent of GIG and other work.


## 7. Source-acquisition escalation (November 21, 2026)

Direct local acquisition of the original SEC Q3 archive failed at DNS resolution on November 21, 2026 (three attempts). This is an environment connectivity failure, **not evidence that the SEC archive is missing**. To avoid repeating the same local failure, the repository now includes `scripts/sec_archive_provenance_probe.py` and `.github/workflows/sec-2025-provenance.yml`. The latter is designed to attempt retrieval on a GitHub-hosted Ubuntu runner and upload **only** a metadata JSON artifact containing ZIP and member SHA-256 values, member names and headers, or explicit HTTP/DNS failures. Original SEC ZIPs are deleted before the job finishes and are not committed or attached as artifacts. A successful ZIP download would establish a reproducible byte fingerprint and member inventory; **it would not by itself** validate source row transformations, the historical Nasdaq roster, or causal identification.

**Verification boundary:** the workflow and script were published and retrieved from GitHub; no successful hosted execution or resulting SEC ZIP/member SHA-256 was verified at the time of this update. The action must be inspected for a real completed run and a valid metadata artifact before updating the provenance table or manuscript claims. This is a source-recovery mechanism, not a new empirical finding.

### Release criteria and fallback

- A fully source-verified empirical paper requires actual original Q3/Q4 ZIP fingerprints and row reconciliation, a historical stock-specific effective-date treatment roster, common-date September/October falsification, and dependence-aware inference.
- A faster **explicitly provisional exploratory methodological release** can present the recovered processed-panel sensitivity and inherited historical warning signs with separate evidence tiers, direct code links, known non-replication and the caveat that the historical SEC-derived inputs have not been independently authenticated. It must **not** be advertised as a validated event-study result or final causal paper.
- If the hosted SEC probe also fails, preserve the failure logs and seek another legitimate network environment rather than asserting success or endlessly generating small synthetic-only modules.


### Hosted source-retrieval outcome (verified November 21, 2026)

The GitHub-hosted provenance workflow **did execute**, but both 2025 Q3 and Q4 SEC archive requests returned **HTTP 403 Forbidden** after retries ([workflow run 44881411585](https://github.com/parthivpatel-patel/US-Equity-Microstructure-Research/actions/runs/44881411585)). The local container independently failed at DNS resolution. Thus neither execution environment has obtained original SEC ZIP bytes or member hashes. This materially limits source certification; it does **not** invalidate the official SEC archive listing or justify replacing source observations with invented data. The manuscript remains an explicitly exploratory, processed-data-based methodological draft. See `provenance/SEC_Q2_Q4_2025_SOURCE_ACQUISITION_STATUS.md`.


## 8. Identification and falsification decision (November 21, 2026)

### What is and is not identified

Let \(H_{i,p}^{(m)}\) denote the security-level period-aggregate hidden rate for metric \(m\) (eligible hidden trade count or eligible hidden share volume), and let \(D_i\) be the **provisional** treatment label. The principal processed-panel descriptive contrast is

\[
\widehat{\Delta}_m =
\frac{1}{n_1}\sum_{i:D_i=1}(H_{i,post}^{(m)}-H_{i,pre}^{(m)})
-
\frac{1}{n_0}\sum_{i:D_i=0}(H_{i,post}^{(m)}-H_{i,pre}^{(m)}).
\]

It is a difference of *observed changes*, not a causal effect. For a causal interpretation one would additionally need a correct historical assignment roster, stable measurement and coverage, a defensible untreated counterfactual trend (including anticipation effects), and uncertainty accounting for common calendar shocks. The currently recovered stock-level data do not permit these conditions to be tested directly.

**Selection/measurement mechanisms requiring separation:** September 2025 price levels determine the reform's size bands and are correlated with security capitalization, activity and baseline hidden-execution rates; October announcements and anticipatory order routing can move behavior before November 3; changes in market-wide volatility or exchange composition affect both groups; ticker joins and corporate actions can alter roster membership; eligibility denominators and security inclusion can shift across periods. These mechanisms can generate a treated/control change difference even with zero reform effect. Conditioning on pre-period hidden rates may reduce observed imbalance but can also change the estimand and induce regression-to-the-mean artifacts. Matching on baseline observables cannot solve unobserved or date-common confounding.

### Falsification decision rule

The October-only placebo differential, inherited September trend results and large baseline imbalance jointly make an unqualified parallel-trends story **unacceptable on current evidence**. A statistically nonzero placebo is not automatically a proof of an invalid design, particularly if the announcement or assignment information arrived during the placebo window. It does require a model of information timing, independent source replication, and a transparent assessment of whether a meaningful causal comparison remains plausible. No post hoc choice of placebo dates or favorable weighting is permitted to erase this concern.

The 2025 Q3/Q4 original SEC ZIP acquisition remains a separate **source-integrity gate**: a 403 from GitHub-hosted runners and a local DNS failure prevent hashing and reconciling the actual source bytes. No original-source claim follows from a processed-panel checksum. Similarly, the historical NYSE reference file cannot establish a Nasdaq-specific effective-date roster; the recovered Nasdaq 2026 reference file is not a 2025 historical assignment source.

### Release decision

**Provisional methodological preprint: permissible with prominent evidence-tier disclosures.** The defensible contribution is a reproducible demonstration that provisional hidden-execution comparisons are highly sensitive to baseline balance, control reuse, caliper attrition, trade weighting, and regression specification, while inherited pre-reform summaries motivate falsification. The paper should avoid causal language in title, abstract, charts, conclusions, or social summaries; distinguish *recomputed processed-panel estimates* from *inherited, unreplicated daily-panel summaries*; link executable code and input digest; disclose that the original processed input is not distributed in the repository; and state that a clean third-party reproduction requires the exact input or a documented rebuild from authenticated sources.

**Source-verified empirical paper: not yet eligible.** It additionally requires original Q3/Q4 ZIP and member hashes, security-date-exchange reconciliation, September price-band/round-lot roster and ticker continuity, independently rerun October placebo and September pretrends, and date-/security-dependent uncertainty. These are substantive gates, not cosmetic editorial tasks.

**Research integrity note:** No figure derived from unverified raw SEC observations should be labeled as a direct SEC replication. A visual of the already-computed processed-panel sensitivity is allowable only if it is generated from its published numerical table and labeled accordingly.

## 8. Corrected historical listing-snapshot reconciliation (November 21, 2026)

The initial [historical snapshot audit](../provenance/NASDAQ_GITHUB_SNAPSHOT_CROSSCHECK_2026-11-21.md) inadvertently counted a file-creation trailer and an empty row as securities in each third-party CSV. The [subsequent direct reparse and full-universe reconciliation](../provenance/NASDAQ_SNAPSHOT_FULL_UNIVERSE_CORRECTION_2026-11-21.md) supersedes those counts: the November 1 and December 1 Git-commit snapshots contain **5,159** and **5,222 valid security rows**, respectively, with **84** non-100-share securities in each (80 at 40 shares, 4 at 10 shares). Their non-100 symbol sets and sizes agree across the snapshots.

All **68/68 provisionally treated symbols** in the recovered 2,262-security processed panel match non-100-share fields in both third-party snapshots (64 at 40 shares, 4 at 10 shares). The **16 additional non-100 symbols** are `ARGX, ASML, BRKRP, CYBR, EQIX, ESLT, LIN, NVMI, ONC, QQQ, RTH, SMH, SOXX, VONE, VTHR, WTW`; none matches an exact `Ticker` entry in the processed panel. Thus **no exact-symbol provisional-control overlap was found for those 16**, although symbol aliases, eligibility, and corporate actions have not been resolved. The provisional treated roster covers **68/84 = 80.95%** of the snapshots' non-100 entries, *not* 68/86.

These are third-party Git history snapshots, not authenticated Nasdaq effective-date records. Commit dates do not establish the actual directory observation date or the September price-evaluation input. Agreement of two post-assignment snapshots cannot certify the November 3 assignment, confirm pre-reform status, or establish a causal treatment effect. Official Nasdaq September reference prices, November 3 directory records, and symbol-history verification remain outstanding. The original SEC Q3/Q4 ZIPs and the processed-panel provenance also remain unauthenticated. The previously published 86/18 counts and statement that the 68-name join was not yet performed are **superseded**; earlier audit files are preserved as an error trail.

## 8. Treatment-versus-market-wide implementation distinction (primary-source audit, November 21)

The May 7, 2025 [Nasdaq UTP Vendor Alert #2025-10](https://classic.nasdaqtrader.com/TraderNews.aspx?id=UTP2025-10) identifies **two different changes** effective November 3: (a) a security-specific round-lot tier based on the **average primary-listing-exchange closing price over all September 2025 trading days** (100 shares through $250, 40 above $250 through $1,000, 10 above $1,000 through $10,000, and 1 above $10,000), and (b) a **market-wide SIP quotation-size representation change** from numbers of lots to actual shares. Nasdaq's alert explicitly gives a 100-share-round-lot example where the disseminated quote-size field changes from 3 to 300 for a 300-share quotation. Thus a stock retaining a 100-share round lot is **not necessarily untreated by every contemporaneous market-data change**. This is a concrete threat to a simple treated-versus-control causal interpretation, even if the round-lot tier roster were authenticated.

The design must define treatment narrowly as **change in assigned round-lot size relative to the previous regime**, not exposure to the overall November 3 implementation. A 100-share comparator may be a valid control for the *differential tier assignment* under additional assumptions, but not an unexposed control for all simultaneous SIP representation changes. The SEC hidden-execution fields are trade/volume metrics rather than SIP quote-size fields; the alert does **not** establish that those SEC fields themselves were rescaled. Any measurement-discontinuity claim requires separate field-level verification. The Nasdaq notice also states that the daily Issue Symbol Directory Message (Category A, Type B) disseminates assigned sizes; this is a candidate **primary treatment-verification record**, not evidence that the third-party November/December listing snapshots reproduce the September assignment accurately.

**Required empirical consequence:** freeze a security-level September average-price/tier roster with source provenance; label the 100-share group as *no tier change / market-wide implementation exposed* rather than *unaffected*; verify hidden-trade denominator definitions across November 3; and interpret any difference-in-differences estimate as a differential association conditional on common implementation effects, anticipation, baseline imbalance and pretrend tests. This audit adds primary-source design clarification, **not** new verified stock assignments, SEC ZIP hashes or causal estimates.
