# Phase 483: Source authentication and coverage gates

**Status:** methodological validation only; no historical SEC observations analyzed.

The existing Phase 482 calendar audit was inspected before this report. Its cutoff check rejects the first calendar date but permits the final date, leaving no post-cutoff observations after the cutoff. That is an invalid design for a two-sided placebo contrast. The proposed stricter gate is `cutoff in dates[1:-1]`, with the cutoff date assigned to the post-period.

A local standalone implementation of this stricter gate and SHA-256 input fingerprinting passed six deterministic tests: coverage versus observed zeros, digest sensitivity to byte changes, rejection of final-date cutoff, duplicate keys, nonfinite values, and off-calendar rows. The implementation is retained as a local artifact pending publication; **these tests do not certify the previously published Phase 482 script**.

The supplied trading calendar is not an authenticated market calendar. A SHA-256 digest establishes identity of supplied bytes, not SEC provenance or redistribution permission. The observed union of security-exchange units is not an independently authenticated listing universe. Missing rows must not be recoded as zero outcomes. All historical results remain blocked on source verification, treatment authentication, and September/October placebo and pretrend resolution.

**Reproducibility note:** This report records the discovered edge case and exact local test scope; it does not report historical estimates or claim causal identification. Phase 430/436 recovered archives and Phase 472 executable package remain unimported. Publication deadline November 14, 2026 was missed.
