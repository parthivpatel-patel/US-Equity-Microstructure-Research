# Phase 442 — assignment scope reconciliation

The Phase 432 daily support audit tracks membership by security alone, potentially rejecting a security with different *matching groups* on separate exchanges. Phase 441 distinguishes security-wide treatment from exchange-specific matching. This standalone fail-closed gate implements that distinction without modifying prior code.

**Rules:** treatment arm must remain identical for a security across exchanges; within each (security, exchange), both treatment and matching group must remain stable. Different matching groups across exchanges are permitted and reported. Duplicate (date, security, exchange) observations, missing identifiers, invalid arms, weekends, and empty panels are rejected.

**Validation:** ten deterministic tests were exercised in a local prototype using Python unittest on 2026-11-17, all passed. The committed implementation is logically equivalent but the exact published checkout and full repository suite were not run; do not treat this as historical SEC validation.

**Limitations:** no authenticated SEC panel, treatment source, matched controls, placebo effects, September pretrends, or serial-dependence-aware estimates were used. A pass only establishes internal structural consistency, not treatment authenticity or identification. The Phase 432 historical integration remains pending. The October 2025 placebo warning and September pretrend warning prohibit causal conclusions.

**Outstanding archive inventory:** previously recovered historical ZIPs are not accessible in this session; no archives imported. Phase 430 and Phase 436 local prototypes remain uncommitted. Do not infer that existing repository files constitute complete historical recovery.

**Next:** run the exact repository checkout's tests; reconcile this gate with the Phase 435/439 source-bound pipeline; recover authenticated observations and treatment assignments before empirical re-estimation.
