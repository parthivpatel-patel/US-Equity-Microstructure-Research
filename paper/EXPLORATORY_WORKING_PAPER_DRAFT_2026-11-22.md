# Round-Lot Reform and Hidden Execution: An Exploratory Reanalysis of U.S. Equity Market-Structure Metrics

**Working manuscript draft — 22 November 2026. Processed-data reanalysis; original SEC source verification and effective-date stock assignments pending. Not a causal estimate.**

## Abstract

The November 3, 2025 U.S. equity round-lot reform provides a natural occasion to examine whether changes in displayed quotation conventions coincide with changes in hidden execution. This exploratory study revisits a recovered stock-level processed panel containing 2,262 securities, of which 68 are provisionally classified as affected. In equal-security comparisons, the treated-minus-control difference in post-minus-pre hidden-trade rate is −3.4629 percentage points, and the corresponding hidden-volume rate difference is −2.5721 percentage points. These associations are not stable across reasonable estimands: pre-period trade-count weighting changes the respective gaps to −2.7064 and −1.0065 percentage points; a reported hidden-volume regression coefficient reverses from −0.0257205 without baseline controls to +0.0147891 with baseline hidden-trade and hidden-volume controls. Baseline differences and inherited September pretrend and October placebo warnings make an effect of the November rule change unidentifiable from the currently verified evidence. The original SEC quarterly archives have not been authenticated, and the stock-level treatment roster remains provisional. The contribution is therefore a transparent examination of estimation and falsification risk, not evidence that reform increased or decreased hidden liquidity.

## 1. Institutional setting and research question

The operative round-lot change took effect November 3, 2025. The initial stock-specific tiers were based on average September 2025 primary-listing-exchange closing prices. That operational definition matters: later listing snapshots or October 31 prices alone cannot authenticate treatment status. A market-wide quotation-size change also occurred, so treated/control comparisons should not be interpreted as isolating every simultaneous market-structure change.

The question is whether hidden-trade and hidden-volume measures shift differentially around implementation, and whether those patterns survive plausible falsification and specification checks. The question is **not** answered causally by the available processed aggregates.

## 2. Data and provenance

The recovered Phase-2 processed security panel contains 2,262 securities and 68 provisionally treated names. Its recorded SHA-256 is `2ccb80427a765ca3858f11f2874d6f87a79a559ec1fdeafc34420e82840e5bbb`. This digest identifies the recovered processed file only; it does not authenticate SEC provenance or certify the original transformation. The SEC's official individual-security-and-exchange Q3 and Q4 2025 ZIP links are recorded in `provenance/SEC_Q2_Q4_2025_SOURCE_ACQUISITION_STATUS.md`; original ZIP bytes, member hashes and source-row reconciliation remain unavailable. The effective November 3 production Issue Symbol Directory and symbol histories have not been authenticated. Accordingly, all treatment labels and source-derived claims in this draft are provisional.

## 3. Descriptive estimands and specification sensitivity

For a hidden-execution rate `Y`, define a security-level change `ΔY_i = Y_i,post − Y_i,pre`. The unweighted descriptive gap is `mean(ΔY_i | provisional treated) − mean(ΔY_i | controls)`. This is a comparison of observed processed-panel changes, not a difference-in-differences causal estimand unless further identification assumptions hold. Trade-count weighting instead answers a different question about the contribution of securities with more baseline trading activity.

| Processed-panel comparison | Hidden-trade rate (percentage points) | Hidden-volume rate (percentage points) |
|---|---:|---:|
| Equal-security mean gap | −3.4629 | −2.5721 |
| Pre-period trade-count-weighted gap | −2.7064 | −1.0065 |

The treated-minus-control **pre-period level** gaps are +14.5672 percentage points for hidden trades and +20.1370 for hidden volume, indicating major imbalance before the event. The hidden-volume regression's unadjusted coefficient of −0.0257205 changes sign to +0.0147891 after baseline hidden-trade and hidden-volume controls. These estimates are specification-sensitive descriptive associations. Do not compare their numerical magnitudes without noting the regression coefficient's unit scale and model differences.

A separate processed-panel leave-one-treated-security-out audit reports negative unadjusted gaps for all 68 deletions, but this does not address calendar dependence, treatment misclassification, omitted covariates, or pretrend failures. See `results/PHASE2_TREATED_INFLUENCE_AUDIT_2026-11-22.md`.

## 4. Falsification and inference limits

Previously published September pretrend and October placebo summaries raised substantial warnings. Their arithmetic was checked against inherited reports, but the underlying daily SEC observations have not been reconstructed from original files. Therefore the historical falsification evidence must be labeled **inherited and not source-replicated**. It cannot be presented as a new verified event-study estimate. Similarly, heteroskedasticity-robust standard errors do not by themselves account for common-date dependence or security-level serial correlation. Joint security/date resampling and appropriate clustered inference require verified daily observations, common calendars and confirmed exchange/security joins.

## 5. Interpretation

The direction of the unadjusted comparisons is negative in the recovered panel, but the baseline imbalances, weighting changes, adjusted sign reversal, and inherited placebo/pretrend warnings prevent attributing the differences to the round-lot reform. The strongest supported result is methodological: apparently straightforward before/after comparisons in market-structure data can change materially with estimand choice and adjustment, even before historical source provenance and treatment assignment are established. This paper neither estimates a reliable reform effect nor establishes that hidden liquidity changed because of the rule.

## 6. Reproducibility and release boundaries

The currently public repository includes processed-panel reanalysis code and internally checked numerical outputs, but not a certified raw-data replication package. A reproducibility release must distinguish (a) code tests on constructed fixtures, (b) computations performed on the recovered processed panel, (c) inherited historical summaries, and (d) original-source verification. The panel's recorded SHA-256 must be checked against a legitimately obtained copy before re-running its analysis. No proprietary or restricted raw data should be redistributed without permission.

**Outstanding evidence gates:** (1) download and hash the SEC Q3/Q4 ZIP originals and members, and reconcile source rows with trading sessions; (2) authenticate the November 3 stock-specific production roster or reconstruct September average primary closing prices with symbol/corporate-action histories; (3) re-estimate September pretrends and October placebos on common-date, exchange/security-matched daily observations; (4) run dependence-aware inference and composition/weighting sensitivity on verified observations; (5) inventory/recover historical Phase 430/436/472 packages where legitimately available. Until then, this is an exploratory draft, not a source-certified publication.

## Source and calculation pointers

- SEC market-structure source landing page: https://www.sec.gov/data-research/sec-markets-data/market-structure-data-security-exchange
- UTP operational notice: https://classic.nasdaqtrader.com/TraderNews.aspx?id=UTP2025-10
- `paper/ACCELERATED_EVIDENCE_AUDIT_2026-11-20.md`
- `paper/EXPLORATORY_RELEASE_BOUNDARY_2026-11-22.md`
- `provenance/NOVEMBER_2025_TREATMENT_AUTHENTICATION_PROTOCOL_2026-11-22.md`
- `scripts/phase2_sensitivity_reaudit.py`, `results/phase2_2026-11-20_sensitivity_reaudit.json`

*No new numerical estimates were computed in preparing this draft; all reported numbers are drawn from previously published processed-panel audits.*
