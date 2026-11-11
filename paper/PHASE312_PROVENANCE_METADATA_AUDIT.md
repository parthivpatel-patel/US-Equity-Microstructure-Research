# Phase 312 — Provenance metadata and canonical identity gate (2026-11-11)

## Verified implementation-level findings

Read the published Phase 311 source gate and tests at commit `22f157ef5a5c68b7828a3cea6dc60e613e870891`. Its timestamp regex accepts calendar-impossible strings (e.g., February 30 or hour 25), its URL prefix test accepts `https://` without a host, and its duplicate check compares literal path strings rather than resolved file identities. These are metadata-validation weaknesses, not demonstrated tampering of historical SEC data.

Added `scripts/phase312_provenance_metadata.py` as a fail-closed wrapper that parses UTC timestamps, requires a syntactically valid HTTPS host without embedded credentials, rejects duplicate canonical file targets including symlink aliases, and then delegates byte hashing to Phase 311. No existing script was overwritten.

Seven deterministic tests passed in an isolated local workspace with a textually reconstructed copy of the published Phase 311 implementation: `python -W error -m unittest discover -s tests -v`. This is not a test of the final published checkout, nor an authentication of SEC provenance. The illustrative SEC URL is not evidence of an actual download. A valid HTTPS host is not evidence of an authentic SEC source; an independently trusted source manifest is still necessary.

## Empirical and release status

No authenticated SEC historical observations were available in this session. Therefore no September pretrend, October placebo, treatment-effect, weighting, exchange, or serial-dependence estimate was calculated. Prior October placebo warning and September pretrends remain material; no causal conclusion is supported. Historical research ZIPs remain unimported and the complete inventory remains outstanding.

Next: execute the published checkout regression suite; obtain and independently authenticate source SEC panel files, treatment roster and trading calendars; then estimate placebo and pretrend diagnostics using matched security groups, common dates and serial-dependence-aware inference. The November 14 target is conditional on these gates.
