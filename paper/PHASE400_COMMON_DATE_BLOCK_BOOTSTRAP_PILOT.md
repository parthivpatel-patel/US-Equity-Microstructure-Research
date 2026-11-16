# Phase 400 — Recovered daily pilot: common-date block-bootstrap sensitivity

Date: 2026-11-15. **Exploratory, descriptive; not causal.** Source is recovered Library file `roundlot_pilot_daily.csv`, SHA-256 `9cd1e7f9fc89a2254211868e1a82cf97fd243bc860ad03eefa99409f94086bba` (126 tier-date records, 42 dates, three tiers 10/40/100). Underlying SEC ZIP, historical tier assignment and redistribution permissions remain unauthenticated. Source CSV deliberately not redistributed.

Method: sum numerators and denominators by tier and date period, combine 10/40 into a denominator-pooled reduced tier, compare reduced-minus-100 hidden trade and volume rates across early October (Oct 1–15), late October (Oct 16–31) and November (Nov 3–28). For a sensitivity interval, resample **entire common dates** across tiers together using circular five-session blocks *within each period*, with 1,000 deterministic bootstrap replicates (seed 400). Report 2.5/97.5 percentiles, not a confirmatory 95% confidence interval. Separate periods are sampled independently; repeated dates within periods and finite short windows limit interpretation. Tier aggregates cannot represent matched securities, exchange effects, or security-level serial dependence.

| Metric / contrast | October placebo (pp) | November vs late October (pp) |
|---|---:|---:|
| Trade count: pooled 10/40 minus 100 | -0.942 [-1.729, -0.219] | -2.148 [-3.387, -0.825] |
| Share volume: pooled 10/40 minus 100 | +1.162 [+0.026, +2.419] | -2.727 [-4.254, -0.934] |
| Trade count: 10 minus 100 | -4.345 [-5.775, -2.863] | -12.388 [-16.999, -2.359] |
| Share volume: 10 minus 100 | -2.756 [-4.680, -0.430] | -12.406 [-15.091, -4.835] |

Intervals are **date-block-bootstrap sensitivity ranges** conditional on this aggregate pilot and bootstrap scheme, not valid evidence for causal identification or population coverage. In particular, October placebo changes are not zero; different tier contrasts show different directions, reinforcing the placebo and weighting warning. The pooled 10/40 tier is denominator-weighted, not an equal-security average. No inference about the matched 68/204 panel is warranted.

Verification: six local deterministic unit tests passed. The source was a recovered Library CSV, not a newly authenticated SEC archive. Run `python scripts/phase400_pilot_date_block.py <local-private-pilot.csv> --reps 1000`; `PYTHONPATH=scripts python -m unittest discover -s tests -p 'test_phase400_pilot_date_block.py'`. The published script and full repository suite still require a clean-checkout rerun.

Release gate remains closed: original SEC archives and 78 placebo windows, historical November 3 lot assignments, September daily security-exchange pretrends, matched-group/common-date and serial-dependence-aware inference unresolved. November 14 deadline missed; November 30 is a provisional target, not certification.
