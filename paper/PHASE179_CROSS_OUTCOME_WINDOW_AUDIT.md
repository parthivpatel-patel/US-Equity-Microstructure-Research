# Phase 179 — Cross-outcome window consistency audit (2026-11-05)

## Source and scope

Read the public repository's `results/phase131_window_sensitivity.csv` and the Phase 178 audit script/report before adding new files. The input is an existing ten-row **summary table**, not authenticated SEC source observations. This report does not re-estimate the reform effect or treat placebo ranks as calibrated p-values. Historical treatment assignments, exchange-level source records, dates, and matching remain unauthenticated.

## New descriptive cross-outcome comparison

| Window, trading days | Count Nov–Oct, pp | Volume Nov–Oct, pp | Volume minus count, pp | Opposite signs? |
|---:|---:|---:|---:|:---:|
| 3 | -0.682345 | +0.201918 | +0.884263 | Yes |
| 5 | -0.734661 | +0.626598 | +1.361259 | Yes |
| 7 | -0.122428 | +0.987253 | +1.109681 | Yes |
| 10 | +0.337165 | +1.156684 | +0.819519 | No |
| 15 | -0.118296 | +0.718230 | +0.836526 | Yes |

Count and volume contrasts have opposite signs in **four of five** window specifications. Count changes sign twice as window length increases (negative to positive at 10, then positive to negative at 15); volume remains positive in all five. The largest cross-outcome gap is **1.361259 percentage points**, in the five-day specification. These are differences between distinct outcome definitions, **not** estimates of a single causal quantity, and do not establish an economic mechanism.

## Interpretation and constraints

Count-based and volume-based hidden execution statistics have different denominators and may reflect different composition, size, and venue effects. Cross-outcome divergence cannot be attributed to the November 3, 2025 round-lot change without authenticating the underlying SEC observations and treatment definitions. The documented September pretrends and substantial October pre-reform shift remain direct warnings against causal claims. All five windows overlap; neither the five windows nor their placebo rank fractions constitute independent tests. No familywise or dependence-aware p-value can be inferred from the summary table alone.

## Reproduction and testing

```bash
python scripts/phase179_joint_window_audit.py results/phase131_window_sensitivity.csv
python -m unittest discover -s tests -p 'test_phase179_joint_window_audit.py' -v
```

Seven closely corresponding deterministic tests were executed locally and passed before publication. The exact GitHub checkout has **not** been executed; that verification remains outstanding. The script rejects incomplete paired windows, duplicate outcomes, nonfinite effects, and invalid placebo counts.

## Source recovery and inventory

The Phase 176 inventory reported no historical ZIP/PDF/Parquet archives on the inspected public main branch. No new historical ZIP, paper, chart, or authenticated raw SEC file was imported in this session; the previous archive inventory is not a complete inventory of private or local historical recoveries. Source redistribution permissions must be checked before importing.

## Next empirical action

Recover original SEC security-date-exchange records with checksums and provenance, authenticate Nasdaq historical round-lot classifications and the trading calendar, then re-estimate the five windows under fixed matched rosters, prespecified weighting, security/exchange controls, matched-group and common-date dependence, and serial-dependence-aware inference. Reassess September trends and October placebo before interpreting November contrasts. The November 14 publication target is conditional. **No causal effect has been established.**
