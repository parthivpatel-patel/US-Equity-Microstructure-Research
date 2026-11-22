# Exploratory release boundary: what the recovered evidence establishes (2026-11-22)

**Scope:** This is an interpretation and publication-boundary memo based on already published, internally checked outputs. It is **not** a new empirical estimate, source authentication, or causal certification. The study remains independent and zero-cost.

## Result hierarchy

1. **Directly recomputed from recovered processed Phase-2 security panel (not original SEC records):** 2,262 securities, including 68 provisionally treated. Equal-security mean post-minus-pre treated/control gaps are -3.4629 percentage points for hidden trade rate and -2.5721 for hidden volume rate. Pre-period trade-count weighting gives -2.7064 and -1.0065 respectively. These are different descriptive estimands, not alternative estimates of an identified treatment effect. Source: `paper/ACCELERATED_EVIDENCE_AUDIT_2026-11-20.md`.
2. **Numerical regression reproduction on that same processed file:** the unadjusted hidden-volume gap is -0.0257205; adjustment for baseline hidden-trade and hidden-volume rates yields +0.0147891. The sign reversal is a specification-sensitivity warning, not evidence of a beneficial or harmful reform effect. Baseline treated-minus-control gaps are +14.5672 pp for hidden trades and +20.1370 pp for hidden volume. Source: same audit.
3. **Previously published historical summaries, arithmetic checked but not source reconstructed:** 18/18 checked identities match at published precision. The reported July–September pretrend and October placebo shifts are material identification warnings. These are **inherited results**, not independently authenticated daily SEC observations. Source: same audit.
4. **Official operational rule verified, stock assignments unverified:** initial November 3, 2025 tiers derive from September 2025 primary-listing-exchange average closing prices; the production SIP Issue Symbol Directory is the preferred direct roster. Source: `provenance/NOVEMBER_2025_TREATMENT_AUTHENTICATION_PROTOCOL_2026-11-22.md`.
5. **Original SEC archive status:** official Q3/Q4 links are documented but the ZIP bytes, SHA-256 hashes, members, row counts and security/date/exchange joins remain unverified. GitHub-hosted HTTP 403 and local DNS failures do not establish invalidity of the official files. Source: `provenance/SEC_Q2_Q4_2025_SOURCE_ACQUISITION_STATUS.md`.

## What a public working paper may say now

The recovered security-level aggregates exhibit negative *unadjusted descriptive* changes in hidden-execution measures for a provisional cohort relative to a broad control universe, but those comparisons are sensitive to baseline adjustment and weighting. Inherited historical placebo/pretrend summaries further undermine a simple November 3 causal interpretation. The paper can contribute an openly falsification-oriented case study of why a plausible market-structure comparison fails to identify an effect with the currently verified evidence.

It must **not** claim that the reform reduced hidden liquidity, that the 68-name treatment list is authenticated, that SEC source rows were independently replicated, that the reported HC3 standard errors account for common-date serial dependence, or that a raw-data replication archive exists.

## Minimum release packaging without misrepresentation

- Label the manuscript **exploratory working paper / processed-data reanalysis; original source verification pending** on its title page, abstract, results tables, figure captions, and repository README.
- Keep direct processed-panel computations, internally checked historical summaries, constructed-fixture tests, and unverified source assumptions in visibly separate tables/sections.
- Include exact input-file SHA-256 and **explicitly state that this is a processed-file identity check only**. Do not redistribute third-party original data without authorization.
- Make the reproducibility command and expected outputs explicit for users who legitimately possess the recovered processed input; explain that public end-to-end reproduction is currently blocked by the missing original SEC ZIPs and historical roster.
- Treat September/October falsification as an adverse finding, not a footnote; do not present adjusted or unadjusted specification as a preferred causal estimate without a justified design.

## Next source-level gates

**A.** Obtain original Q3/Q4 SEC ZIP bytes through a permitted client, hash originals and members, inspect fields and trading-session coverage, and reconcile against the processed panel. **B.** Build November 3 production stock-level assignments or a September-primary-close reconstruction with symbol and corporate-action histories; retain unresolved names. **C.** Recompute September pretrends, October placebo, exchange/security-matched common-date comparisons and clustered or joint security/date bootstrap intervals on verified daily observations. **D.** Inventory missing Phase 430/436 and 472 packages, recording absence rather than inferring results.

**Decision:** A transparently qualified exploratory manuscript can be prepared from the existing processed evidence, but neither original-data replication nor a causal finding is certified. This memo does not assert that the manuscript is complete.
