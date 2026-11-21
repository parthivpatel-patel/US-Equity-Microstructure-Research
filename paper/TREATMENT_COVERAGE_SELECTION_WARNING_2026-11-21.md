# Provisional cohort coverage and potential treatment leakage (2026-11-21)

**Status:** arithmetic audit of already published third-party snapshot counts, **not** a newly authenticated Nasdaq treatment roster or SEC data analysis.

## Observed counts and bounded interpretation

The published [snapshot audit](../provenance/NASDAQ_GITHUB_SNAPSHOT_CROSSCHECK_2026-11-21.md) reports **86** non-100-share round-lot records in each of the November 1 and December 1 third-party Nasdaq-listed snapshots. The [68-name join](../provenance/PROVISIONAL_TREATED_68_SNAPSHOT_JOIN_2026-11-21.md) reports **68 of 68** provisional treated tickers with non-100 fields in both. Arithmetic leaves **18 snapshot non-100 entries not accounted for by the provisional treated roster in each snapshot** (86 − 68 = 18); the roster covers **79.07%** (68/86) of each snapshot's non-100 entries.

**Crucial distinction:** this is a comparison between a 68-name *study subset* and an 86-entry *third-party Nasdaq-listed snapshot*. It does **not** establish 18 omitted eligible treated stocks, 18 contaminated controls, or an 79% treatment recall rate. The 18 could fall outside the 2,262-security processed panel, be ineligible, be listed under different identities, or be classified differently for valid reasons. Moreover, the two snapshots need not have the same 18 unmatched names; only their counts are established by the published audits. No individual identity or overlap is asserted here.

## Identification consequence

Before calling the 2,194 provisional controls “no-tier-change” securities, reconcile **all** 86 snapshot non-100 symbols separately against **all** 2,262 processed-panel tickers, not just the 68 treated names. Report a mutually exclusive audit with (i) provisional treated, (ii) provisional control, (iii) absent from panel, (iv) duplicate/alias/ambiguous and (v) unresolved source field. Repeat on each snapshot and track listing entry/exit and symbol changes. Only a contemporaneous official November 3 directory plus September evaluation can establish actual treatment. The market-wide SIP quotation-size reporting change also means that even a verified no-tier-change comparison group was not wholly unexposed to the implementation.

Until that full-universe join is executed, **potential control-group tier misclassification is an open risk, not an observed error**. Do not reweight, remove 18 symbols, or recompute the causal contrast on the basis of the aggregate subtraction. This note adds no new empirical effect estimate or confidence interval.

## Reproducibility

Inputs are the two linked, already published audits. Reproduce the only new arithmetic with `86-68` and `100*68/86`. Original snapshot CSVs are linked in the snapshot audit, but not redistributed. The recovered processed panel is not authenticated against original SEC ZIPs. Next substantive action is the **full 86-by-2,262 membership cross-tab** with exact symbol and alias handling, followed by original-source verification and pre-reform falsification on daily observations.
