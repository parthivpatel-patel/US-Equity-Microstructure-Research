# Baseline overlap and sample-coverage audit (November 21, 2026)

This is an **exploratory reanalysis of an archived processed panel**, not an authentication of SEC raw data or effective-date round-lot treatment. Input: `roundlot_phase2_security_panel.csv`, SHA-256 `2ccb80427a765ca3858f11f2874d6f87a79a559ec1fdeafc34420e82840e5bbb`, 68 provisional treated and 2,194 controls.

## Actual computed results

| Baseline covariate | Treated median | Control median | Standardized mean difference | Controls inside treated min-max |
|---|---:|---:|---:|---:|
| Hidden trade rate | 0.493823 | 0.327206 | +1.9026 | 819/2194 |
| Hidden volume rate | 0.496139 | 0.275512 | +2.4943 | 751/2194 |
| Pre-period eligible trades | 312,931.5 | 62,195 | +1.3391 | 990/2194 |

Standardized differences use pooled within-arm standard deviations; pre-period trades are log1p-transformed **only for the standardized difference**, not the displayed medians or range test. All 68 treated observations lie inside each control covariate's **univariate** observed min-max range; that does not demonstrate **joint** common support. There are 68/68 treated and 2,162/2,194 controls with the full observed 23 pre-period and 19 post-period dates; therefore requiring full observed days would selectively drop 32 controls and no treated securities. Calendar completeness is inferred from the processed panel's maxima, **not independently reconciled to an official trading calendar**.

These large baseline standardized differences demonstrate poor unmatched comparability. The baseline matching attenuation reported in the working-paper draft should be presented as a specification sensitivity rather than evidence that matching fully solves confounding. Joint overlap, post-match balance, controls reused under matching, and raw-data authentication remain unresolved.

## Reproduction and limitations

`python scripts/phase2_overlap_audit.py /path/to/roundlot_phase2_security_panel.csv --expect-sha256 2ccb80427a765ca3858f11f2874d6f87a79a559ec1fdeafc34420e82840e5bbb`. Dependencies: Python, pandas, numpy. Five deterministic fixture tests passed locally on a development copy; the published checkout has not been executed. Raw SEC Q3 ZIP retrieval again failed locally due to DNS resolution; original SEC ZIP and member hashes are **not available**. Historical Nasdaq treatment authentication, September/October falsification, date-dependent inference, and archive recovery remain open. No third-party raw data redistributed. The November 14 target has passed; no causal or publication-certification claim.
