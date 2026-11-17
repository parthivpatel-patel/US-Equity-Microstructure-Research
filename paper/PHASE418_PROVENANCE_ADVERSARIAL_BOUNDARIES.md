# Phase 418 — Provenance-gate adversarial boundary review (2026-11-16)

## Scope and reproducibility
Reviewed the exact published source of `scripts/phase417_provenance_gate.py` and its 13 published tests via the connected GitHub repository reader. A direct Git clone was attempted in the execution environment and failed because `github.com` DNS resolution was unavailable. Consequently the repository's exact test suite was **not executed** in this session.

Independently executed the published `valid_https` and `valid_utc` function bodies in Python 3 against five adversarial/positive examples. The observed outputs are shown below. These are synthetic boundary checks, **not SEC market observations**.

| Input | Function | Observed result | Interpretation |
|---|---|---|---|
| `https://localhost/data.csv` | `valid_https` | True | HTTPS syntax does not establish a public authoritative source |
| `https://127.0.0.1/data.csv` | `valid_https` | True | Loopback URLs accepted |
| `https://example.com/fake-sec.csv` | `valid_https` | True | Any syntactically valid hostname accepted |
| `https://www.sec.gov@evil.example/a` | `valid_https` | False | Userinfo spoofing rejected |
| `2099-01-01T00:00:00Z` | `valid_utc` | True | UTC syntax passes despite a future retrieval date |

## Findings
The Phase 417 audit is a **local manifest consistency gate**, not a proof of upstream data authenticity. It verifies supplied digests against local bytes, but both the source URL and expected digest can be self-asserted by the same manifest author. The future-dated timestamp case demonstrates that temporal plausibility is not yet enforced. No network retrieval or trusted publisher checksum is verified by the gate. Its `publication_clearance=NOT_ESTABLISHED` output is appropriate and must remain unchanged.

A future hardening change should: (1) distinguish syntax validation from independent publisher authentication; (2) reject retrieval timestamps later than a caller-supplied reproducible as-of time, with explicit clock tolerance; (3) flag local/private/reserved URL hosts where a public authoritative source is claimed, without assuming that a hostname allowlist alone proves authenticity; (4) require a separate provenance attestation recording the independent upstream artifact identifier, retrieval method, original URL, immutable digest and redistribution determination; and (5) add regression tests for these cases.

## Empirical and publication status
No authenticated security–exchange–date panel or original 204-control mapping was available. No new empirical estimates were generated. The September pretrends, substantial October placebo, treatment assignment, weighting sensitivity, matched-date/exchange support and dependence-aware inference remain unresolved. November 14, 2026 was missed; the paper is not publication-certified. Historical ZIP recovery and license review remain outstanding. Do not present these five checks as empirical findings or as execution of the published repository test suite.
