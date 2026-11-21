# Rapid baseline-matching sensitivity: recovered Phase 2 processed stock panel
**2026-11-20. Exploratory internal analysis, not authenticated SEC data, not a causal reform estimate.**

## Input and execution
Reanalyzed recovered Library file `roundlot_phase2_security_panel.csv`, 2,262 stocks (68 provisionally treated, 2,194 controls), SHA-256 `2ccb80427a765ca3858f11f2874d6f87a79a559ec1fdeafc34420e82840e5bbb`. The local analysis was executed with pandas, NumPy and SciPy cKDTree, and saved machine-readable aggregate results in `results/phase2_2026-11-20_baseline_matching.json`. The published script is a condensed reproducibility version of the local analysis. Eight elementary matching-invariant unit tests passed locally on deterministic constructed arrays; **the exact published checkout has not been executed**.

### Why this matters
The original unmatched stock-level descriptive treated-minus-control post-minus-pre difference was -3.4629 percentage points in hidden **trade count** rate and -2.5721 pp in hidden **share volume** rate. But the groups were sharply imbalanced before the event. Pooled-standard-deviation standardized mean differences (SMDs) in baseline hidden-trade rate, hidden-volume rate and log1p(baseline trade count) were **1.475, 1.936, and 1.088**, respectively. These are very large descriptive baseline gaps.

### Baseline matching, explicitly exploratory
Each of the 68 treated securities is paired with k nearest control securities **with replacement**, using Euclidean distance after scaling each baseline feature by its pooled sample standard deviation. Baseline features: hidden-trade rate, hidden-volume rate and log1p(pre-period trade count). No contemporaneous price-band, industry, exchange, or time-series controls are available in this processed stock-level file. Controls can recur across treated securities, so distinct matched controls are much fewer than the nominal 2,194.

| Baseline comparison | Distinct matched controls | Count change gap (pp) | Volume change gap (pp) |
|---|---:|---:|---:|
| Unmatched | 2,194 | -3.4629 | -2.5721 |
| k=1 | 39 | -1.1362 | -0.5746 |
| k=3 | 78 | -1.1410 | -0.6238 |
| k=5 | 107 | -0.9398 | -0.3602 |

At k=1, postmatch SMDs are **0.014, 0.025 and 0.084** in the same feature order. At k=3 they are **0.045, 0.063 and 0.103**; at k=5 they are **0.051, 0.074 and 0.117**. Five treated securities have a nearest-control standardized Euclidean distance exceeding 0.5 (none exceed 1). The maximum reuse of one control is 9 for k=1 and 14 for k=3 or k=5. All these results are conditional on the *provisional* treatment roster and the limited features in the processed input.

**Interpretation:** matching on observable baseline hidden-execution rates and baseline trade count attenuates both descriptive gaps considerably. This supports the prior warning that the original unmatched estimate is strongly sensitive to selection and weighting. It does **not** demonstrate that the reform has or has not caused a change. Matching on pre-event outcomes may also induce regression-to-the-mean and other biases; this is a diagnostic sensitivity exercise, not a prespecified causal identification strategy. The processed file cannot support calendar-date clustering, serial dependence, October placebos, September trends, or exchange effects.

## Source-authentication blocker
An attempted HTTPS retrieval of the original SEC 2025 Q3 individual-security-exchange ZIP on 2026-11-20 failed at DNS resolution for `www.sec.gov` before an HTTP response. Thus **no original SEC ZIP bytes, checksum, or raw-row reconciliation** were obtained. The published processed-panel SHA-256 identifies the local archived input only; it cannot establish provenance. Historical September 2025 Nasdaq stock-specific round-lot assignment remains unauthenticated. The October placebo warning and September pretrend evidence are not resolved by this matching analysis.

## Fastest responsible publication path
Draft the exploratory manuscript around the robustness/falsification findings and explicitly label the source-validation gates. Do not claim an identified causal treatment effect. Prioritize SEC source retrieval through an authorized reachable environment, verify ZIP hashes and metric definitions, reconstruct the 2025-11-03 treatment roster, then run common-date/security/exchange dependence-aware analyses. If these gates remain blocked, a public **provisional working paper** may present the descriptive diagnostics with transparent limitations, but it cannot be called source-verified or publication-certified.

The original November 14 deadline was missed. Phases 430/436 and 472 recovered historical archives remain unimported. No third-party raw data were redistributed. This project is strictly separate from GIG and other work.
