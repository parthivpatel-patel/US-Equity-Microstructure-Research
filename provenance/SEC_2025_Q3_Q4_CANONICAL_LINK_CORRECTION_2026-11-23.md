# SEC 2025 Q3/Q4 canonical archive URL correction (2026-11-23)

## Verified discrepancy

The earlier repository acquisition manifest `provenance/SEC_Q2_Q4_2025_SOURCE_ACQUISITION_STATUS.md` recorded URLs with directory `metrics-individual-security-and-exchange`. **That directory is not the path linked by the SEC's current official landing page for the 2025 files.** This correction does not assert that all historical HTTP 403 responses were caused by the wrong path; hosted access policy may independently block downloads.

The SEC's current [Metrics by Individual Security and Exchange landing page](https://www.sec.gov/data-research/sec-markets-data/market-structure-data-security-exchange) links the following URLs:

| Quarter | Canonical SEC landing-page download URL | Listed size |
| --- | --- | --- |
| 2025 Q2 | https://www.sec.gov/files/opa/data/market-structure/metrics-individual-security-exchange/individual_security_exchange_2025_q2.zip | 172.96 MB |
| 2025 Q3 | https://www.sec.gov/files/opa/data/market-structure/metrics-individual-security-exchange/individual_security_exchange_2025_q3.zip | 181.49 MB |
| 2025 Q4 | https://www.sec.gov/files/opa/data/market-structure/metrics-individual-security-exchange/individual_security_exchange_2025_q4.zip | 187.43 MB |

The [U.S. Data.gov SEC dataset catalog](https://catalog.data.gov/dataset/metrics-by-individual-security-and-exchange) independently lists the same 2025 directory structure. On 2026-11-23, following the Q3 and Q4 links from the SEC landing page through a web text retrieval client returned **unsupported binary content-type `application/octet-stream`** rather than downloaded ZIP bytes. This is **not** a successful local download, ZIP validation, HTTP status proof, or archive authentication. It does show that the source landing-page links are distinct from those recorded in the earlier acquisition manifest.

## Immediate corrective action

1. Use the exact canonical URLs above for any future authorized binary transfer. Do not continue retrying the old `-and-exchange` URLs.
2. Obtain the actual bytes, then log UTC acquisition time, final response URL/status, response headers, byte count, SHA-256, ZIP integrity, member names/member hashes and dataset schema.
3. Reconcile security/exchange/date rows and calendar coverage against the historical processed panel. Keep historical treatment assignment provisional until independently validated.
4. Treat the 2026-11-21 GitHub-hosted HTTP 403 evidence as a failure **of the earlier URL requests**; it does not certify access behavior for these corrected URLs.

**Evidence status:** Verified official source-link correction only. No original ZIP bytes, hashes, numerical estimates or causal results have been established by this note. No raw third-party data redistributed.
