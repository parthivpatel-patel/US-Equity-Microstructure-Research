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
