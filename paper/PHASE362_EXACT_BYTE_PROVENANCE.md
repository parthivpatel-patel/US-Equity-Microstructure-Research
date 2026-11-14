# Phase 362 — Exact-byte provenance verification (2026-11-14)

## Scope
The Phase 360/361 eligibility provenance gate checks the *format* of a SHA-256 declaration but does not compare the declared digest against actual source bytes. This new independent, local-only verifier reads files in bounded 1 MiB chunks, compares actual SHA-256 with the manifest, rejects duplicate and unsafe relative paths, and prevents symlink escape outside the supplied root. It deliberately returns `historical_source_authenticated: false` and `licensing_authenticated: false`: matching a manifest is necessary but not sufficient to establish that bytes came from the historical SEC source or may be redistributed.

## Verification
Seven deterministic tests passed in a local Python 3 unittest execution: matching digest, mismatching digest, traversal rejection, duplicate rejection, malformed digest rejection, empty manifest rejection, and symlink escape rejection. Constructed bytes only; no SEC observations processed. The locally tested script has the same algorithm and public interface as the published script, but exact published checkout/full-suite execution remains pending.

## Open empirical gates
Original 78 dated placebo observations; October placebo and September pretrend warnings; Phase 130 contradiction; treatment round-lot historical classification; exchange-eligibility history; matched-group/date and serial-aware inference; recovered historical ZIP inventory. No new effect estimates or causal conclusions. November 14 publication deadline not met. Next: locate permitted original SEC files, record trustworthy source URLs and acquisition timestamps, compute source-byte hashes, and run existing coverage and aggregation checks before placebo reconstruction.
