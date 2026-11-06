# Phase 184: matched-group identity is not matched-group count

2026-11-06 (America/New_York). Independent U.S. equity round-lot reform research. No GIG assets or code.

## Finding and correction to the research workflow

Phase 183's row-level contract records only `matched_groups`, a count, for each date/window/outcome. Equal counts do not imply equal constituent securities or matched-group identities. For example, two outcomes can each report two groups but refer to {A,B} and {A,C}; accepting those as a fixed matched panel would silently change the estimand. Phase 183 also returns count-outcome means only, omitting volume means despite validating volume date coverage. This phase adds a strict group-identity audit and reports both outcomes.

The new CSV contract is `window_days,placebo_date,outcome,matched_group_id,contrast_pp`. The validator rejects duplicate group records, nonfinite contrasts, malformed dates, missing outcome-date pairs, count/volume identity mismatch, and any group roster drift across the common dates and five windows. It reports equal-group-date descriptive means for both outcomes, only after establishing a balanced roster. These strict checks may exclude otherwise usable unbalanced observations; that exclusion and its selection consequences must be disclosed rather than hidden.

## Local verification

A closely corresponding standard-library prototype passed 8/8 deterministic unit tests locally. Synthetic balanced observations produce count=1 and volume=3 percentage points for every window. These are software fixtures, **not SEC estimates**. Published-version fresh-checkout execution is not yet verified.

## Identification and provenance limits

No original SEC daily panel, historical Nasdaq treatment snapshot, authenticated group IDs, original placebo date memberships, or recovered historical ZIP/PDF was imported this session. The September pretrends, October 2025 placebo warning, treatment misclassification, weighting/selection sensitivity, common-date dependence, serial correlation, and security/exchange controls remain unresolved. No causal effect is claimed. A group ID must ultimately be linked to authenticated security and exchange membership, and source hashes and licensing status must be recorded.

Next: recover authenticated daily source data and historical archives; verify source rights; build the dated matched-group roster; run this identity audit, then pretrend/placebo models with calendar-date and matched-group clustered or appropriate block-bootstrap inference. The November 14 publication goal remains conditional.
