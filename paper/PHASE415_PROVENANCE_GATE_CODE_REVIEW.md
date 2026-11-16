# Phase 415 — Source provenance gate code review (2026-11-16)

Scope: independent November 3, 2025 U.S. equity round-lot reform research. This is a static review of the published Phase 414 script, **not** an execution on historical SEC data.

## Verified implementation observations

The Phase 414 audit resolves each manifest path against the root, rejects absolute paths and paths escaping the root, and checks SHA-256 digests. It records duplicates using `str(rel)` rather than the resolved path. Consequently, two syntactically different relative paths that resolve to the same file (e.g. `data/../panel.csv` and `panel.csv`) can evade the duplicate-path check. This is a *code-level* observation; no historical archive was examined.

The required `source_url`, `retrieved_utc`, and `grain` fields are checked only for nonempty strings. A manifest can therefore pass the gate with a non-URL source identifier, a non-date retrieval timestamp, or an unspecified observational grain. A correct file hash confirms byte identity relative to the supplied digest; it cannot authenticate the original publisher or a claim of redistribution permission.

The audit deliberately allows `redistribution=restricted` and `redistribution=unknown` while returning `PASS`. This is appropriate only if PASS is interpreted as **local file integrity**, never publication clearance. Downstream publication gates must separately require affirmative, documented redistribution permission for every source to be distributed.

## Recommended regression cases before reliance

1. Reject canonical-path aliases within a single manifest, even when literal path strings differ.
2. Validate retrieval timestamps as timezone-aware ISO 8601 and require supported HTTPS source URLs (or a documented non-URL provenance exception).
3. Require a controlled vocabulary for grain and validate the corresponding data keys separately.
4. Report two independent statuses: integrity verified and redistribution cleared; restricted/unknown rights must block data publication.
5. Preserve the current fail-closed behavior for missing files, digest mismatches and paths outside the root.
6. Distinguish user-entered provenance metadata from independently authenticated source records.

## Research implications and limits

These gaps affect reproducibility and evidence provenance, not the sign or magnitude of a reform effect. They do not resolve the substantial October placebo warning, September pretrends, treatment assignment uncertainty, matching selection, estimand weighting, or common-date/serial-dependence inference. The original security–exchange–date panel and historical archives were not recovered in this review; **no new empirical estimate** is reported.

The November 14, 2026 publication target was missed. Publication certification remains blocked pending authenticated sources, reconstructed matching assignments, pretrend/placebo reconciliation, and dependence-aware sensitivity analysis. No raw or licensed third-party data is included here.
