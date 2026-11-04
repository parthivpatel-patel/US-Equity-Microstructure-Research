# Phase 144 — public reproducibility inventory (2026-11-04)

## Scope and verification

Read the GitHub recursive tree at `main`, commit `b2b371c5cc406639888d1d00bda734d27ed85040`, before making any changes. The tree contains **44 tracked blobs**. This is a *repository publication audit*, not a fresh SEC-data analysis or a claim of empirical replication.

| Category | Tracked files | GitHub tree byte sizes |
|---|---:|---:|
| paper/ | 14 | 42,184 |
| provenance/ | 3 | 2,071 |
| results/ | 10 | 7,658 |
| src/ | 7 | 18,420 |
| tests/ | 5 | 10,573 |
| root-level files | 5 | 10,363 |
| **Total** | **44** | **91,269** |

Counts and sizes are from the GitHub tree metadata, not estimates of local recovered material. The published `results/` files are small summaries, not the 14,416-row processed matched-group panel. No complete original SEC security/exchange source dataset, Nasdaq historical round-lot assignment file, or historical ZIP appears in the tracked tree. Absence from the tracked tree does not establish that an artifact was never produced elsewhere.

## Historical archive gap

The existing `provenance/ARCHIVE_STATUS.md` reports an earlier *local workspace* inventory of 129 ZIPs totaling 1,158,462,147 bytes. **Those ZIPs were not available for inspection in this session**, so neither their current existence, checksums, redistribution rights, nor per-file contents were reverified. The historical archive must not be described as imported. The GitHub 100 MB ordinary-file limit and third-party licensing constraints remain material.

## Empirical and identification status

Previously reported Phase 141 September breakpoints and Phase 139 October shifts remain exploratory. The Phase 143 whole-scan null implementation has only synthetic tests; no empirical maximum-statistic p-value was produced here. October 2025 information-event contamination, September pretrends, treatment classification, sample selection, weights, source authentication, and common-date plus group dependence remain open. No causal effect of the November 3, 2025 reform is established.

## Publication gate and next step

1. Recover the processed panel and verify its bytes against the archived SHA-256, then reconcile a reproducible security/date/exchange sample against SEC source releases.
2. Reconstruct and authenticate each affected security's historical round-lot size against dated Nasdaq/UTP alerts and historical prices.
3. Run the whole-scan null with matched-group and common-date resampling, serial-dependence sensitivity, alternative trend nulls, and explicit multiplicity treatment.
4. Inventory each historical ZIP by path, size, SHA-256, license status, and disposition; import only eligible code, original figures, and text in bounded batches.
5. Gate manuscript submission on external fresh-checkout reproduction and transparent noncausal interpretation.

This audit adds a precise public/private boundary; it does not resolve the data access blocker or replace empirical analysis.
