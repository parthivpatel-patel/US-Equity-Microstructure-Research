# Phase 253 — Executed evidence-ledger regression audit (2026-11-08)

Nine deterministic Python unittest cases passed locally (9/9, 0 failures) for an offline structural ledger prototype. Cases: consistent bytes still do not establish authentication, tampering, traversal, naive timestamp, boolean size, missing category, duplicate category, rights-type mismatch and malformed digest.

The prototype requires SEC observations, exchange calendar and treatment roster categories, UTC acquisition timestamps, HTTPS source URLs, byte size and SHA-256 consistency, and distinct analysis and redistribution rights. It explicitly sets independently_authenticated, historical_inference_authorized and redistribution_authorized to false even when all structural checks pass. The code was executed in an isolated temporary directory; this was not a complete repository checkout or a historical SEC analysis.

**Critical limitation:** A caller can create self-consistent hashes and metadata for unauthentic files. This gate cannot establish original SEC provenance, exchange sessions, treatment classification, or legal reuse rights. It is not appropriate to override this safeguard with caller-supplied booleans.

No historical coefficients, pretrend estimates, placebo results or figures were produced. September pretrends, October 2025 placebo warning, treatment classification, matching and weighting sensitivity, common-date and serial dependence remain unresolved. No causal effect is established.

Historical research ZIP inventory/import remains incomplete because the recovered archives were unavailable in this execution environment. Do not infer they are absent from earlier work.

Next: independently authenticate original SEC source downloads and calendar/treatment sources; execute exact repository suite; freeze treatment/matching and run historical placebo/pretrend estimates with security/exchange controls and date/dependence-aware inference.

Local prototype source and nine tests were executed but are **not included in this commit**; they must be imported and independently verified in the repository in a subsequent session.