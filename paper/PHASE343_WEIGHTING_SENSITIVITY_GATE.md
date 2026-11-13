# Phase 343: matched-cell weighting sensitivity gate

Date: 2026-11-13. Status: software validation only; not an empirical estimate.

## Estimands and support

For each matched-group, date, and exchange cell with both treatment arms, calculate the difference (percentage points) between arm-level ratios of summed hidden numerators to summed denominators. Exclude unsupported cells, recording their count. Compare (i) equal weight per matched group after averaging that group's paired cells, (ii) equal weight per paired cell, and (iii) paired-cell weight proportional to the sum of treated and control denominators. These are different descriptive aggregation rules and should not be conflated with an identified reform effect.

## Reproducibility

Run `python -m unittest discover -s tests -p 'test_phase343_weighting_sensitivity.py'` and `python scripts/phase343_weighting_sensitivity.py AUTHORIZED_PANEL.csv`. Input fields: security,date,exchange,treated,match_group,numerator,denominator. The script rejects duplicate security-date-exchange keys, assignment drift, invalid rates, nonfinite values, and invalid dates. Ten constructed-data tests passed locally on 2026-11-13 after correcting an erroneous expected value in a test fixture. In that constructed fixture, the three weighting schemes produce 36, 21.333333, and -3.809524 percentage points, respectively. These are deliberately synthetic numbers, **not SEC findings**.

## Publication gate

Source observations and historical treatment assignments have not been authenticated; no original SEC panel was run. This diagnostic does not correct September pretrends, the large October placebo break, the Phase 130 placebo count contradiction, selection into supported cells, or common-date/serial/group dependence. Confidence intervals and causal claims are intentionally absent. Historical research archives remain incompletely recovered and inventoried. Re-run on licensed/authenticated observations, compare estimand definitions, and report all unsupported cells and matching attrition before inclusion in the manuscript.
