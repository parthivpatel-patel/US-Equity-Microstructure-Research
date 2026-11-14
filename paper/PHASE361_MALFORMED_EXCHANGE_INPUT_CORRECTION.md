# Phase 361 — Malformed exchange evidence input correction (2026-11-14)

## Reproduced defect
The Phase 360 metadata gate was inspected directly from the published repository. Its exchange-policy validation invoked `tuple(exchanges)` without first establishing that the value was an iterable collection. With a policy value of `None` or an integer it raised `TypeError`, rather than the documented `ValueError` rejection. Nested lists in either policy or evidence also triggered `TypeError: unhashable type: 'list'` during set conversion.

## Correction and verification
The validator now checks that policy exchange collections are list, tuple, or set, and checks that every element is a nonblank string *before* deduplication. Evidence exchange elements are checked before set conversion as well. The previous provenance flags remain false, because metadata validation does not authenticate source bytes.

Locally reconstructed Phase 360 code reproduced the three exception failure patterns. The corrected implementation passed five new deterministic unittest methods (including three noniterable subcases) using `python -m unittest discover -s tests -v` in an isolated test directory. The tests are constructed fixtures, not market-data observations. Full published-checkout and repository-wide tests remain outstanding.

## Research implications and limitations
This is a defensive software correction, not new empirical evidence. No authenticated SEC panel, historical eligibility source, treatment assignment, September pretrend, October placebo, or original 78 dated placebo observations was evaluated. The Phase 130 contradiction and dependence-aware inference remain unresolved. No causal effect is claimed.

**Deadline status:** November 14, 2026 publication target not met; manuscript not certified. Historical ZIP and paper/code/chart recovery inventory remains incomplete and no archive was imported this session.

**Next:** execute the exact published tests and integrated suite; authenticate original source bytes and historical exchange eligibility; reconstruct placebo/pretrend evidence and sensitivity analyses before manuscript certification.
