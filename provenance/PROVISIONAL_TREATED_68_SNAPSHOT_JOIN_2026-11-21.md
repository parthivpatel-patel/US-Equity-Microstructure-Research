# Provisional treatment roster versus historical third-party Nasdaq snapshots (2026-11-21)

**Evidence tier:** independent third-party listing cross-check; **not** Nasdaq-certified effective-date treatment and **not** SEC source authentication.

## Inputs and method

- Recovered processed panel `roundlot_phase2_security_panel.csv` (SHA-256 `2ccb80427a765ca3858f11f2874d6f87a79a559ec1fdeafc34420e82840e5bbb`), 2,262 rows, with 68 `treated=1` symbols. Its SHA identifies this processed file only.
- Third-party [2025-11-01 GitHub snapshot](https://github.com/datasets/nasdaq-listings/tree/441144e), `data/nasdaq-listed-symbols.csv`, Git blob `3d2e9fc6cc0e9394ce070af5bbbe115142ba9dd4`.
- Third-party [2025-12-01 GitHub snapshot](https://github.com/datasets/nasdaq-listings/tree/2ca384c), same path, Git blob `dfee5db8f575682248668cb36a9a2555ea1fc6eb`.
- Exact uppercase `Ticker` to `Symbol` match, RFC-style quoted CSV parsing, no fuzzy substitutions. Compare `Round Lot Size` as a literal field; no inference of a change in tier at November 3. Git blob hashes are not SEC ZIP SHA-256 values.

## Direct 68-name join

| Diagnostic | Count |
|---|---:|
| treated count | 68 |
| oct present | 68 |
| nov present | 68 |
| both | 68 |
| oct non100 | 68 |
| nov non100 | 68 |
| changed | 0 |

### Observed tier-pair distribution

- `40 → 40`: 64 symbols
- `10 → 10`: 4 symbols

### Exact provisional-treated roster join

| Provisional treated ticker | 2025-11-01 field | 2025-12-01 field |
|---|---:|---:|
| ADBE | 40 | 40 |
| ADP | 40 | 40 |
| ADSK | 40 | 40 |
| ALNY | 40 | 40 |
| AMGN | 40 | 40 |
| APP | 40 | 40 |
| APPF | 40 | 40 |
| AVAV | 40 | 40 |
| AVGO | 40 | 40 |
| AXON | 40 | 40 |
| BKNG | 10 | 10 |
| CACC | 40 | 40 |
| CASY | 40 | 40 |
| CDNS | 40 | 40 |
| CEG | 40 | 40 |
| CHTR | 40 | 40 |
| CME | 40 | 40 |
| COIN | 40 | 40 |
| COST | 40 | 40 |
| CRWD | 40 | 40 |
| CVCO | 40 | 40 |
| DASH | 40 | 40 |
| DJCO | 40 | 40 |
| DPZ | 40 | 40 |
| DUOL | 40 | 40 |
| ERIE | 40 | 40 |
| FCNCA | 10 | 10 |
| FFIV | 40 | 40 |
| HIFS | 40 | 40 |
| IDCC | 40 | 40 |
| IDXX | 40 | 40 |
| IESC | 40 | 40 |
| INTU | 40 | 40 |
| ISRG | 40 | 40 |
| ITIC | 40 | 40 |
| KLAC | 40 | 40 |
| LFUS | 40 | 40 |
| LPLA | 40 | 40 |
| MAR | 40 | 40 |
| MDB | 40 | 40 |
| MDGL | 40 | 40 |
| MEDP | 40 | 40 |
| MELI | 10 | 10 |
| META | 40 | 40 |
| MPWR | 40 | 40 |
| MSFT | 40 | 40 |
| MSTR | 40 | 40 |
| NFLX | 10 | 10 |
| PODD | 40 | 40 |
| POOL | 40 | 40 |
| POWL | 40 | 40 |
| REGN | 40 | 40 |
| ROP | 40 | 40 |
| SAIA | 40 | 40 |
| SITM | 40 | 40 |
| SNPS | 40 | 40 |
| STRL | 40 | 40 |
| TLN | 40 | 40 |
| TSLA | 40 | 40 |
| ULTA | 40 | 40 |
| UTHR | 40 | 40 |
| VRSK | 40 | 40 |
| VRSN | 40 | 40 |
| VRTX | 40 | 40 |
| WINA | 40 | 40 |
| WING | 40 | 40 |
| ZBRA | 40 | 40 |
| ZS | 40 | 40 |

## Interpretation and limitations

A non-100 entry in a third-party listing snapshot is **not** proof that the symbol's round lot changed on November 3. A `100` entry is not definitive proof of no reform exposure; snapshot timing, stale fields, mapping errors, corporate actions and tier boundaries may matter. The snapshot commits occur after the September 2025 price evaluation and do not provide an official historical effective-date roster. The market-wide SIP quotation-size reporting change also affected the broader market. The cohort remains **provisional**. Do not relabel controls as wholly unaffected or infer a causal hidden-execution effect from this table.

Next verification: acquire an official historical SIP Issue Symbol Directory and September reference-price evaluation, reconcile aliases/corporate actions and resolve each ambiguous/missing case. Separately obtain authenticated SEC Q3/Q4 ZIPs and replicate daily falsification with date-aware inference. No third-party raw files are redistributed here.
