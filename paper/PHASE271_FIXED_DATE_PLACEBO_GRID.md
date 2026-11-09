# Phase 271: fixed-date placebo and lag-grid diagnostic

The new diagnostic enumerates predeclared placebo cutoffs and HAC lag choices on the same input date series. It calls the existing Phase 269 full-series HAC implementation. It reports the descriptive contrast, HAC standard error, and the cross-cutoff covariance contribution without claiming significance or causal identification.

**Validation:** Ten deterministic synthetic cases passed locally against an algorithm-equivalent standalone implementation (not the exact published import layout). The published tests have not been rerun byte-for-byte; the complete repository suite has not been run. No historical SEC data were analyzed, and no historical effect estimates or figures were generated.

**Critical prerequisites:** The input series must first pass Phase 263 fixed-roster, Phase 264 assignment-integrity, and Phase 270 expected-session checks. Those structural gates do not authenticate the SEC source, exchange calendar, or historical treatment assignment. Cutoffs and lags must be fixed before outcome inspection. This module does not correct multiple testing, model security/exchange fixed effects, or provide finite-sample bootstrap inference.

**Interpretation:** A sizeable October 2025 placebo signal and September pretrends remain serious threats to identification. Weighting and selection sensitivity also remain unresolved. No causal effect of the November 3, 2025 round-lot reform has been established.

**Unpublished inventory:** Previously recovered research ZIPs and Phase 252–254 implementations have not been authenticated or imported. The full archive inventory is incomplete. No licensed third-party datasets were added.

**Next:** Authenticate the original SEC files, exchange sessions, and fixed treatment roster; run the predeclared September and October historical sensitivity grid and common-date dependence-aware inference.
