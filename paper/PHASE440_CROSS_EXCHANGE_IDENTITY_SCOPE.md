# Phase 440: cross-exchange identity scope audit

Source inspection of the published Phase 432 implementation shows that `membership[s].add((g,a))` aggregates assignments by security alone, whereas Phase 433 uses `identities[(s,e)].add((g,a))`. This discrepancy can falsely label a security as unstable when it belongs to different matched groups on different exchanges, even if each security/exchange assignment is stable. The Phase 435 gate treats the Phase 432 warning as a failure.

The new Phase 440 diagnostic reports within-security/exchange instability separately from multi-exchange presence. Six deterministic constructed-data unit tests passed locally on November 17, 2026; no authenticated SEC panel was used. This is a diagnostic module, **not** a patch to Phase 432 or a demonstration that any historical sample is affected.

Next: reconcile the intended treatment/matching identity definition, integrate a validated identity scope into the Phase 432/435 gates, execute exact published checkout tests, then apply to authenticated historical data. The October 2025 placebo and September pretrend warnings remain unresolved. No causal interpretation is warranted. The November 14 publication target was missed. Historical recovered archives and Phase 430/436 prototypes remain unimported.
