# Uploaded SEC archive row audit (2026-11-25)
User supplied Q3/Q4 archives after hosted acquisition failed. Official landing page: https://www.sec.gov/data-research/sec-markets-data/market-structure-data-security-exchange . Independent official byte comparison remains outstanding.
SHA256 Q3: c41f8ac7befaf45c5065061145997329b1166a9057bc8785d698a72f16c7b2aa
SHA256 Q4: 5f7b515f1804f10d6365a0d071d43a30f100453aee7eaa8929ac58400cea2188

| Month | All rows | Stock rows | Missing pairs (each metric) | Dates |
|---|---:|---:|---:|---:|
| Jul | 2342597 | 1186095 | 80398 | 22 |
| Aug | 2249311 | 1128423 | 76386 | 21 |
| Sep | 2275530 | 1127622 | 76388 | 21 |
| Oct | 2515842 | 1231709 | 83395 | 23 |
| Nov | 2087406 | 1008873 | 68870 | 19 |
| Dec | 2435045 | 1157071 | 79618 | 22 |

Method: pandas read_csv in 250000-row chunks from each ZIP CSV. Filter Security == 'Stock'. For each pair (Hidden, TradesForHidden) and (HiddenVol('000), TradeVolForHidden('000)), count rows with either value missing; among complete pairs count negative numerator or denominator or numerator exceeding denominator by more than 1e-8. Zero violations for both metrics in every month. Missing counts coincide but rowwise coincidence not tested. Date counts are distinct observed dates, not independent calendar certification. No treatment effect estimated. Historical panel reconciliation and 68 provisional assignments remain outstanding.
