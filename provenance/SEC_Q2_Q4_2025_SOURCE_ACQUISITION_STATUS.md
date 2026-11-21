# Primary SEC acquisition targets — verified landing-page links (2026-11-20)

The SEC publishes **Metrics by Individual Security and Exchange** with fields including Ticker, Date, Security, Trades, Hidden, TradesForHidden, HiddenVol, and TradeVolForHidden. Official landing page:
https://www.sec.gov/data-research/sec-markets-data/market-structure-data-security-exchange

| Quarter | Direct SEC ZIP target | Advertised approximate size | Verification |
|---|---|---:|---|
| 2025 Q2 | https://www.sec.gov/files/opa/data/market-structure/metrics-individual-security-exchange/individual_security_exchange_2025_q2.zip | 172.96 MB | Page link confirmed; byte retrieval **not completed** |
| 2025 Q3 | https://www.sec.gov/files/opa/data/market-structure/metrics-individual-security-exchange/individual_security_exchange_2025_q3.zip | 181.49 MB | Page link confirmed; byte retrieval **not completed** |
| 2025 Q4 | https://www.sec.gov/files/opa/data/market-structure/metrics-individual-security-exchange/individual_security_exchange_2025_q4.zip | 187.43 MB | Page link confirmed; byte retrieval **not completed** |

These files are **not downloaded, hashed or reconciled** in this session. In this execution environment direct binary transfer and container DNS were unavailable. Do not invent source SHA-256 values or imply a full SEC source audit.

After retrieval, log original URL, UTC retrieval time, HTTP status and headers, ZIP SHA-256, internal member names and member hashes, column definitions, provenance of cohort filter and matched joins, and row/venue/date reconciliation. Treat matched-control assignment as provisional until the September 2025 stock-specific round-lot rule is independently checked.

Nasdaq primary operational source for the reform: https://classic.nasdaqtrader.com/TraderNews.aspx?id=UTP2025-10 . The 2025-11-03 operative date is independently supported by that UTP Vendor Alert. A vendor alert confirms the **rule**, not the stock-by-stock historical treatment roster.

Distribution: this file records pointers and verification status only; no unlicensed raw source material is republished.


## November 21, 2026 — independently executed hosted acquisition attempt

A new GitHub Actions source-only acquisition workflow was published and executed on a GitHub-hosted Ubuntu runner. Unlike the local container's DNS failure, the hosted runner reached the SEC endpoint but received **HTTP 403 Forbidden** for **both Q3 and Q4 2025 ZIPs**, after three attempts per quarter. This is an access denial to the hosted client, **not** proof that the public archive links are invalid. The SEC public landing page still lists both files (2025 Q3: 181.49 MB; Q4: 187.43 MB). The correct direct download URLs are the ones linked above.

Evidence: [completed workflow run 44881411585](https://github.com/parthivpatel-patel/US-Equity-Microstructure-Research/actions/runs/44881411585) (failure, 2026-11-21 07:41 UTC); the job's printed JSON reports `HTTPError`, `HTTP Error 403: Forbidden` for both quarters. The workflow uploaded a provenance-only artifact containing failure details, and did not upload raw data. [Earlier run 44881353345](https://github.com/parthivpatel-patel/US-Equity-Microstructure-Research/actions/runs/44881353345) also failed; the later run adds explicit error diagnosis.

**Verified original SEC ZIP SHA-256: unavailable for Q3 and Q4. Verified member hashes: unavailable. Raw row reconciliation: not completed.** No publication-certification claim can be made from these attempts. Do not treat the GitHub Actions artifact's own SHA-256 as a hash of SEC data.

Next source-acquisition route: use an authorized, ordinary client/network with access to the SEC download links, observe SEC rate/access policies, and run the repository's probe locally with a properly identifying User-Agent; record original ZIP and member SHA-256 and compare security-date-exchange records against the research panel. Avoid repeated automated access from a client that the SEC rejects. This task does not require a paid data vendor.
