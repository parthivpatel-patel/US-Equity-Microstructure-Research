# Phase 375 — Exact between/within weighting decomposition

**Status:** Mathematical methodology and deterministic fixture tests only; no authenticated SEC panel was used.

The pooled hidden-execution ratio and equal-observation mean differ whenever denominator weights and observation rates covary. This script decomposes their difference exactly using rational arithmetic, conditional on a supplied grouping (e.g. exchange or matched group).

For group g, let P_g be the pooled hidden/total ratio, E_g the equal-row mean, S_g its share of all denominators, and Q_g its share of rows. Then

P - E = sum_g (S_g - Q_g) E_g + sum_g S_g (P_g - E_g).

The first term is **between-group reweighting**; the second is **within-group denominator reweighting**. Both depend on the chosen grouping and are descriptive identities, not causal components.

A constructed two-row example [(A,0,1),(A,9,9)] gives pooled 9/10 and equal-row 1/2: the 2/5 difference is entirely within-group. Labeling the same two rows as distinct groups instead attributes 2/5 to between-group reweighting. Neither is a market observation.

Five deterministic unit tests passed locally with Python unittest, after correcting two test fixtures that inadvertently zeroed one component. The published checkout and full repository suite have not been executed. Reproduction from the repository: `PYTHONPATH=scripts python -m unittest discover -s tests -p 'test_phase375_weighting_decomposition.py'`.

**Empirical gate:** Run on authenticated security-date-exchange observations, separately for trade counts and share volume, by exchange and matched cohort; disclose zeros/missingness, group membership, calendar composition, pretrends, October placebo, treatment uncertainty, and clustered/common-date serial-dependence-aware uncertainty. The decomposition alone does not identify a November 2025 reform effect.

**Archive status:** No historical ZIPs or licensed source data were imported in this phase. The November 14 publication deadline was missed; manuscript not certified.
