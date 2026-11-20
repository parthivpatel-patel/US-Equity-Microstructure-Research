# Phase 491 — strict CSV composition integration

Date: 2026-11-19. Status: methodological/data-quality integration, **not historical empirical inference**.

Phase 488's composition auditor has an input-admission defect: extra CSV fields can yield an unexpected AttributeError. Phase 490 introduced a strict reader but did not connect it to Phase 488. The new `scripts/phase491_strict_composition.py` invokes the existing Phase 488 summary routine while temporarily replacing its input reader with Phase 490's `read_strict`; it restores the original reader in a `finally` clause. The original scripts remain unchanged. The entry point supports `--eligibility`, `--panel`, `--cutoff`, and optional `--output`.

## Validation and limitations

Seven integration tests passed in a local reconstructed environment using the source-equivalent Phase 488 audit body and Phase 490 reader. Cases include an explicitly observed zero, missing eligible observation, exchange-level missingness, malformed extra fields in either input, missing outcome, duplicate key, nonfinite outcome, and repeated invocation. The exact published GitHub checkout has **not** been executed; tests must be rerun from the published repository before certification. The local reconstruction was not a byte-identical clone of the published dependencies.

The temporary module-level reader replacement is **not thread-safe**. Do not call the Phase 491 audit concurrently in one Python interpreter. A future refactor should inject the reader as a parameter instead. The validator verifies CSV structure and fingerprints, not historical SEC authenticity, treatment status, eligibility accuracy, or redistribution permission.

## Empirical gate

No historical SEC observations were analyzed here. September pretrends, substantial October 2025 placebo effects, treatment authentication, changing security/exchange composition, matched-group weighting, common-date shocks, and serial-dependence-aware uncertainty remain unresolved. Do not interpret composition counts as causal reform effects.

The November 14, 2026 publication target was missed; the manuscript remains **not publication-certified**.

## Historical artifact inventory (known pending, not recovered or authenticated this phase)

- Phase 430 and 436 recovered ZIP archives: not imported; verify availability, content, licensing and file sizes before publishing.
- Phase 472 executable artifacts: not imported or validated.
- Phase 487 original local prototype: not byte-for-byte recovered; later Phase 488 implementation is available.
- Historical SEC panel and date-specific eligibility source: not authenticated or processed in this phase.

Next: run published checkout tests; inspect input source manifests; authenticate and apply eligibility coverage to the October placebo period before further estimands.
