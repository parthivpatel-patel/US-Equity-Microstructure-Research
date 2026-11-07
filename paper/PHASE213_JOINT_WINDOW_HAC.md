# Phase 213: joint-window HAC implementation (2026-11-07)

This phase publishes executable code and ten deterministic tests for a descriptive late-minus-early pre-reform contrast. Unlike the separate-window variance shortcut warned about in Phase 212, the implementation computes a single full-sequence Newey–West long-run variance of influence scores, retaining cross-window lag products. Zero scores for observations between windows preserve the supplied observation-index distance. The returned lag-dependent standard errors are **diagnostics**, not validated confidence intervals.

## Local verification
`python -m unittest -v test_phase213_joint_hac.py`: 10/10 tests passed locally using constructed observations. The constructed series includes weekends and is **not** an authenticated U.S. trading-session calendar or SEC evidence. No historical estimate was produced.

## Limitations
The caller must independently authenticate SEC observations, treatment assignments, exchange calendar and date coverage. Date ordering is checked but the code cannot prove missing-session completeness. The procedure assumes a stable, prespecified contrast series; it does not itself implement security/exchange fixed effects, matched-pair construction, cross-sectional clustering, trend adjustment, small-sample corrections or multiplicity adjustment. The HAC score approach does not solve September pretrends or the substantial October placebo signal. Its lag bandwidth must be prespecified and robustness reported. No causal effect is established.

## Archive inventory
Previously recovered ZIPs, papers, charts and historical panel files were not accessible in this session and were not imported. Their contents, redistribution rights and completeness remain unverified; this is not a complete archive inventory.

## Next
Run clean-checkout tests; authenticate the source panel and trading sessions; freeze security/exchange matched rosters; compute September pretrends and multiple October placebo contrasts with joint-window HAC, trend sensitivity and dependence-preserving resampling.