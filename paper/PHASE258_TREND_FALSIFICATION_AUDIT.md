# Phase 258 — Synthetic trend falsification of circular-placebo interpretation

Date: 2026-11-09. Independent US equity microstructure project only.

## Reproducible result

The prior Phase 257 code was read from the repository before this additive diagnostic. A deterministic 12-date *linear trend* (values 0 through 11), with six dates on either side of an arbitrary cut and **no treatment or reform effect**, yields an observed post-minus-pre difference of 6.0. Its 12 cyclic-rotation statistics are [6,4,2,0,-2,-4,-6,-4,-2,0,2,4], with a two-sided tail fraction 2/12 = 1/6. A synthetic six-date step of magnitude four has a tail fraction of 1/6 as well. Thus this reference cannot distinguish a secular trend from an abrupt shift in these examples. The constant series has tail fraction 1.0. First differencing the linear series yields eleven ones, illustrating how a known deterministic linear trend can disappear under a difference transformation, **not** validating first differences as an estimator for the actual panel.

These are exact synthetic calculations, not historical SEC observations, p-values, power estimates, or evidence of a reform effect. A cyclic tail fraction is not a calibrated probability absent cyclic exchangeability; the seam disrupts dependence. No hypothesis test or inference is justified by this diagnostic.

## Verification

Seven Python unittest cases passed with zero failures in a local isolated run. To reproduce from the repository root: `PYTHONPATH=scripts python -m unittest discover -s tests -p 'test_phase258_trend_sensitivity.py' -v`; run `PYTHONPATH=scripts python scripts/phase258_trend_sensitivity.py` to print the three exact examples. The complete repository suite and historical estimator were not run.

## Historical research admission remains blocked

September 2025 pretrends and the substantial October placebo warning remain unresolved. Source files, exchange calendars, treatment assignments, frozen matching/weighting, security and exchange controls, common-date shocks, serial and cross-sectional dependence, and licensing require independent authentication. Historical recovered ZIPs, historical figures, and unpublished Phase 253–254 scripts were not available for verified import. No new historical coefficients or charts were produced. The November 14 manuscript target is conditional; **no causal effect has been established**.

Next: recover and authenticate source data and treatment roster; execute predeclared fixed-roster September trends and October placebo analyses with security/exchange and date effects and dependence-aware uncertainty. Do not use circular-rotation tail fractions as causal evidence.
