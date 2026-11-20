# Security influence in recovered Phase-2 processed panel (2026-11-20)

**Evidence status: exploratory internal audit, not authenticated SEC-source data; no causal claim.**

A new leave-one-security-out analysis on the previously recovered 2,262-stock processed panel (68 provisional treated; 2,194 controls; input SHA-256 `2ccb80427a765ca3858f11f2874d6f87a79a559ec1fdeafc34420e82840e5bbb`) reveals substantial concentration in the baseline trade-weighted estimator.

## Computed findings
- Treated securities: largest single security contributes **26.21%** of all treated pre-period trade-count weight; largest five contribute **54.67%**. Controls: **5.89%** and **13.95%**, respectively.
- Hidden execution **count**: equal-security treatment-minus-control change **-3.4629 percentage points**; trade-weighted **-2.7064 pp**. Dropping any one treated stock changes equal-security estimate to **[-3.6249, -3.2876] pp**, but trade-weighted estimate to **[-3.7687, -2.3008] pp**. Removing TSLA alone shifts the weighted gap by **1.0623 pp**.
- Hidden execution **volume**: equal-security **-2.5721 pp**; trade-weighted **-1.0065 pp**. Leave-one-treated-out weighted range **[-2.2758, -0.6080] pp**; removing TSLA alone changes it by **1.2693 pp**, larger than the absolute original weighted estimate.
- Largest treated-stock influences in weighted count estimator: TSLA, NFLX, META, MSTR, AVGO. In weighted volume estimator: TSLA, META, NFLX, MSFT, DASH. These are mechanical sensitivity diagnostics on an old processed panel, **not verified contemporaneous treatment classifications**.
- The previous audit found a pretrade-weighted treated effective sample size of only **10.40** despite 68 nominal treated stocks.

## Interpretation
These results demonstrate a serious **concentration and influence problem** for a particular descriptive weighting choice. They do not establish a November 2025 reform effect. Removing a security changes the estimand, and the processed stock-level panel cannot supply daily serial dependence, exchange controls, or reliable September/October placebo estimates.

## Reproduction
`python scripts/phase2_influence.py path/to/roundlot_phase2_security_panel.csv > results.json`

The archived processed input is not redistributed; verify its SHA-256 against the hash above. Eight deterministic unit tests passed locally using the source program (in a flat temporary layout); the GitHub version adapts the test's import to the published scripts/tests layout and has not yet been executed as a remote checkout. The exact JSON result is committed under `results/phase2_2026-11-20_influence.json`.

## Blocking next step
Download and checksum the original SEC Q3/Q4 security-exchange ZIPs; direct SEC retrieval was blocked by network/proxy access in this run. Independently verify source records, September round-lot assignments, and calendar eligibility. Then run common-date September pretrends, October placebos, and dependence-aware inference before manuscript certification. Original November 14 deadline missed; manuscript not certified.
