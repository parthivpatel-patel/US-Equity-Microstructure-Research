# Phase 333: Cross-table pretrend and October-break audit

Date: 2026-11-13. Scope: existing published aggregate tables only. No new SEC panel estimates.

## Sources
- `results/phase135_pretrend_hac_presentation.csv` (blob `de1ffa1f3d68176c0faa8c781418721586a971a4`)
- `results/phase136_trend_uncertainty_presentation.csv` (blob `e89016144b1b60079a4686c02a945009a2734c06`)
- `results/phase139_paired_october_shift_presentation.csv` (blob `d15fc17c66d5e9f1a605714fd41b94a7b0041e6b`)

These are published presentation summaries, not authenticated underlying observations. The accompanying script accepts the original CSV files as positional arguments and fails on missing outcomes, incomplete lag/block grids, incompatible sample sizes, or inconsistent displayed slopes/differences.

## Cross-table findings

| Outcome | Jul–Sep slope (pp/day) | Jul–Oct slope (pp/day) | October slope (pp/day) | October minus Jul–Sep (pp/day) |
|---|---:|---:|---:|---:|
| Hidden count | +0.028607 | −0.004083 | −0.141590 | −0.170197 |
| Hidden volume | −0.001464 | −0.027276 | −0.157880 | −0.156416 |

The Phase 136 two-way 95% interval excludes zero at all published lags (0, 3, 5, 10, 15) for Jul–Sep **count**, but at none for Jul–Sep **volume**. For Jul–Oct, the pattern reverses: volume excludes zero at all five lags; count at none. The Phase 139 October-minus-Jul–Sep block-bootstrap intervals exclude zero for both outcomes at all four reported block lengths (3, 5, 10, 15). All eight displayed shift arithmetic identities agree within six-decimal rounding.

This is a **pre-reform regime-change warning**: October 2025 exhibits a negative within-preperiod slope shift for both outcomes. Post-November comparisons against October can inherit pre-existing dynamics. Interval exclusion describes reported intervals, not newly validated inference. Joint security/date resampling, multiplicity, selection, serial dependence, and source provenance remain unresolved. No authenticated significance test or causal effect is claimed.

## Validation and limits

Two minimal failure-path unit tests passed locally. A separate cross-table audit directly on the GitHub-fetched CSV text confirmed the slopes, eight shift arithmetic identities and interval-exclusion patterns. The script itself could not run against freshly downloaded GitHub CSVs locally because DNS resolution failed. These checks do not validate underlying SEC observations.

The Phase 130 five-day placebo-count contradiction remains open. The original 78 dated placebo observations and producer code are unrecovered. Historical ZIPs and papers/code/charts have not been imported or fully inventoried. Treatment membership and source authentication, September pretrends, security/exchange controls, matched/common-date inference and weighting sensitivity remain publication gates.

## Next action

Recover Phase 130 dated observations and producer, execute Phase 325–328 checks, and rebuild October-break and post-event estimates from authenticated daily security-by-exchange data using matched groups and dependence-aware inference. The November 14 target is conditional on scientific validation.
