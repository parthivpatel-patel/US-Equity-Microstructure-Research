# Caliper overlap and matched-population sensitivity — 2026-11-21

**Exploratory analysis only. Original SEC source and effective-date treatment roster NOT authenticated.**

Input is the archived processed Phase-2 2,262-security panel, SHA-256 `2ccb80427a765ca3858f11f2874d6f87a79a559ec1fdeafc34420e82840e5bbb` (68 provisional treated, 2,194 provisional controls). No underlying SEC rows or licensed material redistributed.

The previously published one-nearest-neighbor baseline matching was replicated with replacement using Euclidean distance on pooled-standard-deviation-scaled pre-period count hidden rate, volume hidden rate, and log1p(pre-period eligible trades). We additionally **discard treated names without a nearest control within the stated caliper**; caliper selection changes the treated population and therefore the descriptive estimand.

| Caliper (scaled Euclidean distance) | Retained treated | Unique controls | Max control reuse | Count gap (pp) | Volume gap (pp) |
|---|---:|---:|---:|---:|---:|
| None | 68 | 39 | 9 | -1.1362 | -0.5746 |
| 0.25 | 49 | 31 | 6 | -0.5166 | -0.0412 |
| 0.50 | 63 | 37 | 8 | -1.0379 | -0.4764 |
| 0.75 | 68 | 39 | 9 | -1.1362 | -0.5746 |

The uncalipered matched control group consists of just **39 distinct names** with replacement (one name reused nine times). At caliper 0.25, **19 of 68 treated names are excluded** and the hidden-volume change gap approaches zero. This is not evidence of a causal null; it demonstrates that the descriptive contrast depends on the population with available baseline comparators. The full-sample-SD-scaled post-match differences at no caliper are 0.0144 (pre count rate), 0.0252 (pre volume rate), and 0.0837 (log trades); at 0.25 they are 0.0090, 0.0118, and 0.0171. Small balance differences on three chosen covariates do **not** establish exchange, liquidity, price-band, identity, or unobserved-factor comparability.

All results come from a locally executed Python analysis of actual recovered processed rows. Script and aggregate JSON are published. **No raw SEC archive was obtained**: direct HTTPS request to the SEC Q3 ZIP failed DNS resolution in this run. No Q3/Q4 source ZIP or member hashes, SEC row-level checks, historical Nasdaq effective treatment authentication, September/October source-level pretrends/placebos, or common-date serial-dependence inference were completed. These are still blocking full empirical certification.

**Manuscript implication:** the draft should explicitly flag reuse concentration and caliper-dependent sample attrition alongside baseline imbalance and the October placebo. The best near-term release is a transparent falsification/robustness working paper, not a claimed reform effect. November 14, 2026 deadline passed. Strictly independent of all other projects.
