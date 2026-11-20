# Phase 504 — Common-date support attrition and coverage selection

Date: 2026-11-20. **Methodological diagnostic; synthetic validation only.**

## Identification issue
An exchange-period can contain eligible dates with treated observations but no eligible controls, or the reverse. Restricting coverage summaries to dates where both groups are eligible changes the target date population. This is not a causal effect and cannot be interpreted as reform-induced missingness. It is a selection diagnostic required before applying common-date estimators.

## New implementation
The Phase 504 local Python diagnostic measures the count and fraction of common-support dates, dates excluded for one-sided group eligibility, and eligible/observed units discarded in each group. It compares treated and control coverage in the full supplied universe against coverage on common dates. It rejects noncanonical dates, invalid counts, duplicate exchange-dates, and inconsistent period labels.

## Constructed counterexample
On October 1, treated and controls each have 2 eligible and 2 observed units. On October 2, treated have 2 eligible but zero observed units; controls have zero eligible units. Across both dates, treated coverage is 2/4 = 0.5, but on the sole common-support date it is 2/2 = 1.0. This demonstrates a possible selection-induced change in descriptive coverage without any historical SEC claim.

## Local validation and reproducibility gap
The retained local implementation and tests passed 11 synthetic regression cases in 0.07 seconds. This report alone does not establish publication of the executable or tests. They must be synchronized and independently verified before this phase is remotely reproducible.

## Empirical gates
Historical SEC source hashes, exchange identifiers, trading calendar, eligible security-date-exchange universe, treatment assignments, matched sets and redistribution permissions require authentication. The substantial October placebo warning and September pretrends remain unresolved. Do not infer causal reform effects; evaluate exchange/security controls, common-date support, selection/weighting sensitivity and dependence-aware uncertainty on authenticated data.

## Archive inventory and deadline
Recovered Phase 430/436 ZIPs and Phase 472 outputs remain unverified and unimported. The November 14, 2026 deadline has passed; the paper is **not publication-certified**.
