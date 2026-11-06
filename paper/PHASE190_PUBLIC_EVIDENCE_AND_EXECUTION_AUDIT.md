# Phase 190 — Public repository evidence and execution audit (2026-11-06)

## Scope and source
Read the GitHub default-branch recursive tree at commit `cfe34640439dd9d2a3d3ee15d3635ac2e68081aa` using the connected GitHub API. This is a **repository inventory**, not a verification of source observations or an empirical re-estimation.

## Verified inventory
- Total tracked blobs: **140**.
- Paper markdown files: **58**.
- Test files: **45**.
- Script files: **10**.
- Provenance files: **5**.
- Results files: **10**.
- Tracked CSV files: **10**.
- Tracked ZIP, Parquet, PDF, PNG files: **0**.

### Tracked CSV inventory
- `results/phase130_group_sensitivity.csv` (Git blob 997785f33774b5d2ee1ea6f69d4f56ce59a3d988; 344 bytes)
- `results/phase130_summary.csv` (Git blob 22ec64f7089a2376b65280ecb35bbaa2185a1a4a; 398 bytes)
- `results/phase131_window_sensitivity.csv` (Git blob d85898449eff1edbf4b03abf63ebcb013301a816; 611 bytes)
- `results/phase133_event_group_diagnostics.csv` (Git blob 9ae99fcc9a082c494b8f38e400d6d232be3fb4fb; 623 bytes)
- `results/phase133_monthly_diagnostics.csv` (Git blob 279b6d4cececc90e609db4f2611bfd9a76b8fb6f; 530 bytes)
- `results/phase135_pretrend_hac_presentation.csv` (Git blob de1ffa1f3d68176c0faa8c781418721586a971a4; 625 bytes)
- `results/phase136_trend_uncertainty_presentation.csv` (Git blob e89016144b1b60079a4686c02a945009a2734c06; 1508 bytes)
- `results/phase137_block_bootstrap.csv` (Git blob b327230d5d28aeffd312d724a9fa88b9482aa529; 1706 bytes)
- `results/phase139_paired_october_shift_presentation.csv` (Git blob d15fc17c66d5e9f1a605714fd41b94a7b0041e6b; 876 bytes)
- `results/phase140_paired_interval_width_audit.csv` (Git blob 2d44f4b5c35a24938bafa47a0e960b6b84e0734a; 437 bytes)

## Evidence classification and blockers
The CSV filenames above identify result/presentation tables; they are **not authenticated SEC daily source observations** merely by appearing in the repository. No historical research ZIP, manuscript PDF, Parquet panel, or image artifact is tracked at this commit. This does **not** establish that those files are absent from prior conversation archives or external storage.

An attempted clean `git clone --depth 1` failed with `Could not resolve host: github.com` in the execution environment. Therefore **fresh-checkout tests were not run**, and Phase 188/189 execution remains unverified in that environment. This is a network-resolution failure, not a test failure.

## Identification and publication gate
Do not claim an identified causal effect. September pretrends and the October 2025 placebo warning remain material. Historical treatment assignment must be authenticated against UTP notices and contemporaneous closing prices; verify security identifiers, exchanges, trading dates, matching roster, source checksums, weighting, and overlap before any estimate is publication-ready. Two-way clustering of matched-group/date descriptive contrasts does not itself resolve serial dependence, small-cluster inference, or security/exchange confounding.

## Next actions
1. Recover and hash the previously located research ZIPs, subject to provenance and redistribution checks, and produce a complete contents manifest.
2. Authenticate the original daily SEC panel and historical treatment mapping; recover actual placebo-date membership and matched-group identifiers.
3. Run the exact published Phase 187–189 tests in a network-capable clean checkout; compare fixed-roster common-date estimates and September/October diagnostics with dependence-aware alternatives.
4. Keep the November 14 paper conditional until all validation gates pass.

No new empirical coefficients, confidence intervals, or treatment effects were calculated in this inventory audit.
