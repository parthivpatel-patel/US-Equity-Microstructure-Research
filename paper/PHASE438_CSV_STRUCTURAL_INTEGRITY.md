# Phase 438 — Fail-closed CSV structural integrity (2026-11-17)

The Phase 437 source-byte-bound workflow uses Python DictReader, which can silently replace duplicate header names and place extra fields under a null key. A digest alone preserves the identity of malformed data; it does not establish that the parsed schema is usable. This phase adds an independent, standard-library-only structural audit before applying the historical support gates.

The audit rejects duplicate, missing, blank or padded column names, inconsistent row widths, empty fields, invalid UTF-8, NUL bytes, header-only inputs and malformed quoted records. It returns a SHA-256 digest, byte length, row count and exchange row counts for successfully parsed CSV. It does **not** validate numeric bounds, date parsing, security identifiers, treatment assignments, SEC provenance, exchange-level sampling, or inference. It must be composed with the stricter existing panel validators rather than used as a substitute.

Eleven deterministic constructed-data tests passed locally using `python -m unittest -v` in the isolated prototype directory. The published test file contains the same cases but the exact published checkout has not been independently executed. Run `python -m unittest discover -s tests -p 'test_phase438_csv_integrity.py' -v` from the repository root.

**Research status:** No authenticated original SEC panel or historical matching file was recovered. No September pretrend or October placebo estimate was generated. The substantial October placebo, September pretrends, treatment authentication, weighting sensitivity, fixed-security/common-date sample construction and dependence-aware uncertainty remain unresolved. November 14, 2026 publication target was missed; the manuscript is not publication-certified. Historical ZIP imports and unpublished Phase 430 and Phase 436 prototype/tests remain outstanding.

Next: integrate this structural gate at the source-byte entry point of Phase 437, run the exact repository tests, and authenticate original observations and treatment assignments before historical estimation.
