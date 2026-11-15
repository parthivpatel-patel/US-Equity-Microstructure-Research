# Phase 380: Roster-anchored exchange attrition

Phase 379 infers candidate pairs and exchanges from observed rows and takes their Cartesian product. This can overstate missing observations when a matched pair is not assigned to every exchange, while entirely unobserved pair-exchange units cannot be discovered from observed rows.

Phase 380 accepts an explicit independent pair-exchange roster and constructs expected cells only for listed pair-exchange units, both arms, and all declared pre/post dates. Missing cells and exact exchange-level retention fractions are reported. Unexpected observations, duplicate keys, duplicate roster entries, invalid windows, and invalid integer counts fail closed.

In a constructed two-pair, two-exchange fixture with each pair assigned to exactly one exchange and two dates, the correct expected count is eight rows, not sixteen. Seven deterministic tests passed locally. This is a software validation, not an SEC empirical finding.

**Critical limitations:** The supplied roster is not authenticated by this script. A fabricated or incomplete roster still gives misleading retention. Source files, historical round-lot assignments, and treatment labels remain unauthenticated. No historical placebo, pretrend, or causal estimate is produced. Phase 379 remains unchanged for reproducibility; Phase 380 is an alternative with a stricter roster contract.

Next: authenticate the original security/exchange roster and source observations, then quantify observed attrition and re-estimate dated placebos with matched-pair and date-dependent uncertainty.
