# Phase 313 — Source URL authority syntax audit (2026-11-12)

The published Phase 312 provenance wrapper parses HTTPS URLs but does not read the parsed port. Python's URL parser permits a parsed hostname while deferring invalid-port errors until the port property is accessed. The prior wrapper also did not explicitly reject URL backslashes, single-label hostnames or IP-literal authorities. These are metadata interpretation gaps, **not evidence of any SEC data tampering**.

Added an additive `verify_authorities` gate, which validates HTTPS authority syntax and ports, rejects backslashes, control characters, embedded credentials, nonstandard ports, IP literals and malformed DNS labels, then invokes the existing Phase 312 canonical-path and Phase 311 SHA-256 gates. This is a conservative policy: legitimate sources using nonstandard ports, IP addresses or internationalized hostnames will require separately reviewed exceptions. It does not establish that a hostname belongs to the SEC, that a response was retrieved from that host, or that a digest is independently trustworthy.

Ten deterministic tests passed locally with `python -W error -m unittest discover -s tests -v`, using textually reconstructed copies of the published Phase 311 and Phase 312 dependencies. The published checkout was not independently tested in this session. The synthetic three-byte fixture and illustrative SEC URL do not represent downloaded SEC observations.

**Empirical identification remains blocked:** no newly authenticated historical panel, treatment roster or independently checked trading calendar was available. The October placebo warning, September pretrends, selection and weighting sensitivity, exchange composition, and common-date serial dependence continue to preclude a causal interpretation. No new empirical estimates were computed.

**Archive status:** historical research ZIPs and recovered papers/charts have not been imported in this session; their comprehensive licensing and file inventory remains incomplete. Do not infer completeness from the repository's existing phase files.

Next: test the exact published checkout, reconcile recovered archive inventory and licensing, authenticate source bytes and treatment assignments, then run pretrends, October placebo, exchange and matched-group common-date/HAC sensitivity analyses. The November 14 manuscript deadline remains conditional on these requirements.
