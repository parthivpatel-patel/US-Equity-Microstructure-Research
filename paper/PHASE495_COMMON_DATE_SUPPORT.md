# Phase 495 — Common-date support is not guaranteed by full unit coverage

Date: 2026-11-20. This is a methodological validation, **not** an estimate from historical SEC data.

The Phase 493 auditor measures whether each security-exchange unit is fully observed on its *own* eligible dates. This is insufficient to certify that two fully observed units share any dates. A deterministic counterexample has A eligible/observed on October 1 and 3, 2025, and B eligible/observed on October 2 and 4. Both units pass full two-sided coverage around October 3, but their common observed-date intersection is empty. Thus neither common-date effects nor matched group comparisons are identified on that intersection.

The new auditor reports both the common eligibility-date intersection across paired units and the common observed-date intersection across fully covered paired units. Explicit zeros remain observations. The intersection is intentionally conservative; a practical regression can instead define and document a weaker minimum common-support threshold and exchange-specific samples.

## Limitations and admission gate

Inputs are not authenticated SEC historical data. This tool does not verify source lineage, round-lot treatment, pretrends, placebo dates, matched selection, serial dependence, or causal identification. It does not compute outcome estimates. Before interpreting the substantial October 2025 placebo or September pretrends, obtain independently authenticated observations and eligibility dates, report date support by treatment and exchange, and assess dependence-aware inference. File-byte SHA-256 alone does not authenticate provenance.

## Outstanding historical inventory

Previously recovered Phase 430/436 archives and Phase 472 executable artifacts have not been authenticated or imported. Do not imply they are published. The November 14, 2026 manuscript deadline was missed; publication certification remains blocked.
