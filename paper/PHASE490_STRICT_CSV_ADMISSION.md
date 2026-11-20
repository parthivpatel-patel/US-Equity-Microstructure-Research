# Phase 490 — Strict CSV admission gate (2026-11-19)

## Scope and result

Static inspection of the published Phase 488 auditor found that `csv.DictReader` places surplus CSV fields under a `None` key. Its row validation invokes `.strip()` on that list, potentially raising `AttributeError` instead of a controlled input-validation error. Phase 490 adds a standalone strict reader that rejects surplus and missing fields, duplicate keys, duplicate/mismatched headers, invalid/noncanonical dates, and nonfinite outcomes while preserving observed zeros.

The reader is **not yet wired into Phase 488**. The existing Phase 488 CLI remains vulnerable until it is refactored to use this admission gate. The new reader accepts exactly three eligibility fields or four observed-panel fields, and requires all cells nonblank. It does not verify historical exchange eligibility or SEC provenance.

## Reproducibility

From repository root:

```bash
python -m unittest discover -s tests -p 'test_phase490_strict_csv.py' -v
```

Eight tests passed locally against the development implementation on 2026-11-19. The GitHub-published files have not yet been independently executed from the exact commit; published test status is provisional. All fixtures are synthetic. No historical observations were processed.

## Empirical admission blockers

Before any reform inference: independently authenticate source panel bytes, security identifiers, historical round-lot assignments, security-exchange-date eligibility and the trading calendar; resolve September pretrends and the substantial October placebo; run fixed-composition and changing-composition comparisons with matched-group and common-date dependence-aware uncertainty, serial dependence sensitivity, and alternative weights. A SHA-256 digest demonstrates byte identity, not source authenticity.

## Historical archive inventory status

Previously mentioned Phase 430/436 recovered ZIP archives and Phase 472 executable artifacts have not been authenticated or imported in this phase. Their contents, licensing, and completeness remain unverified. No historical third-party data is redistributed.

## Publication status

The 2026-11-14 target was missed. Manuscript is not publication-certified. No causal effect estimate is asserted. This project remains separate from GIG.
