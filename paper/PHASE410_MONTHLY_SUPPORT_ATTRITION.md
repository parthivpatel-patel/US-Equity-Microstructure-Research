# Phase 410 — Monthly common-date and same-exchange attrition audit (2026-11-16)

This standalone standard-library script quantifies how much of a proposed matched security panel survives two nested support restrictions: (1) treated/control securities observed in the same matched group and trading date; (2) treated/control observations on at least one shared exchange in that group-date. It partitions group-date attrition by month to expose changes in the comparison sample around the November 3 reform.

**Interpretation:** the same-exchange metric counts a group-date once when *any* exchange has both arms. The exchange-cell count uses a different denominator and must not be confused with the group-date count. The diagnostic does not estimate hidden execution, infer causal effects, validate historical round-lot sizes, or authenticate SEC provenance. The 1:3 roster check is informational only because aggregate 68:204 cohort sizes do not authenticate group assignments.

**Validation:** seven deterministic tests were executed locally against a structurally equivalent implementation (full overlap, exchange mismatch, date mismatch, duplicate, empty, roster caveat, month partition). They passed. No historical panel was accessible during this session; therefore **no empirical attrition percentages or research effect estimates are reported**. Full repository CI was not executed.

**Limitations:** A structurally complete group-date can still have severe differential missingness, time-varying exchange exposure, selection bias, or serial/common-date dependence. Matching, historical treatment, source rights and original panel authentication are unresolved. The substantial October placebo and September pretrend warnings remain. No original archives imported.

**Next:** recover and authenticate the original security–exchange–day panel and matched roster, run this audit on actual records, report month-specific attrition and weighting sensitivity, then run common-date and serial-dependence-aware placebo/pretrend inference.

**Publication:** November 14 deadline missed; November 30 provisional, not certified.
