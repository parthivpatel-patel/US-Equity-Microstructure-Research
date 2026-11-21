# Phase 2: Security-resampling uncertainty audit (2026-11-20)

## Scope and provenance
Reanalyzed the recovered `roundlot_phase2_security_panel.csv`, SHA-256 `2ccb80427a765ca3858f11f2874d6f87a79a559ec1fdeafc34420e82840e5bbb`. The input is a **processed stock-level panel**, not source-authenticated SEC daily security/exchange observations. It has 2,262 stocks, including 68 provisionally treated and 2,194 controls. The original SEC Q3/Q4 2025 ZIPs could not be retrieved here: container request failed with DNS resolution error for www.sec.gov. No new raw-data hash or original-source authentication is claimed.

## Newly executed analysis
Within each treatment arm, independently resampled securities with replacement 5,000 times, deterministic seed 20251103. The reported intervals are the 2.5th and 97.5th percentiles of security-resampling draws; point estimates are treated-minus-control mean security post-minus-pre rate changes in **percentage points**. Weighted comparisons use the **pre-period number of trades** as security weights, not share-volume weights. Also calculated exhaustive leave-one-treated-security-out influence. Seven local deterministic unit tests passed. This bootstrap does **not** handle serial dependence or common-date shocks, because the processed panel has no daily records.

| Descriptive gap | Point (pp) | Security-bootstrap percentile 95% (pp) | Largest leave-one-treated-out shift (pp) |
|---|---:|---:|---:|
| Hidden trade rate, equal security | -3.4629 | [-4.3093, -2.6101] | 0.1753 |
| Hidden trade rate, pre-trade weighted | -2.7064 | [-4.8825, -1.1598] | 1.0623 |
| Hidden volume rate, equal security | -2.5721 | [-3.3867, -1.7835] | 0.1374 |
| Hidden volume rate, pre-trade weighted | -1.0065 | [-3.4204, +0.6687] | 1.2693 |

**Finding:** under this narrow, independent-security resampling assumption, the weighted hidden-volume interval spans zero, while the other three do not. This is **not evidence of causal effects or valid event-study inference**. The treated group has only 68 provisional securities, strong baseline differences, extreme pre-trade weighting concentration, and large October placebo/September pretrend warnings. A security bootstrap cannot remove selection bias, time shocks, treatment misclassification, or serial dependence. Do not use these intervals as final paper inference.

## Publication and remaining tasks
The numerical results are in `results/phase2_2026-11-20_security_bootstrap.json`. The executable and tests were run locally, but publication status must be separately verified. Original SEC archive authentication, historical treatment assignment, common-date matched comparison, September/October falsification, and serial-dependence-aware inference remain **unresolved**. Phase 430/436 and 472 archives remain unimported. The November 14 deadline was missed; the manuscript is not publication-certified. Research is independent of GIG and other projects.
