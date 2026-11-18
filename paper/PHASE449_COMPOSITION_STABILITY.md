# Phase 449 — Common-date composition stability audit

Date: 2026-11-18. **Descriptive software diagnostic only.** The November 14 manuscript deadline was missed; publication certification is withheld.

## New methodological distinction

Phase 448 correctly requires treated and control observations on the same exchange/matched-group dates. That condition alone does not ensure that the **same securities** provide support across dates. A daily treated/control comparison may change composition completely across the event boundary even while common-date counts remain positive. Phase 449 therefore reports the number of securities in the union and intersection of each arm's observed security sets across supported dates, separately before and after a configurable cutoff, and whether each arm has at least one security observed on **every common date across both periods**. These counts reveal a composition threat; they do not correct it.

The global across-period flag is deliberately stringent and can fail in otherwise usable unbalanced panels. A false flag is not proof of bias; a true flag does not establish parallel trends or identify a causal effect. Within-exchange matched-group assignment is required to remain constant for each security. Cross-exchange group differences are allowed. No unverified treatment or source authentication is implied.

## Reproduce

```sh
PYTHONPATH=scripts python -m unittest discover -s tests -p 'test_phase449_composition_support.py' -v
```

Eight deterministic constructed-input tests are included. No historical SEC observations, real-world effect estimates, October placebo statistics, or September pretrend statistics are supplied here. The test suite must be executed in the published checkout before asserting a pass.

## Unresolved gates

Authenticate SEC source files and historical treatment/round-lot assignments; reconcile selection, weighting, September pretrends and the substantial October placebo warning; estimate with exchange/security controls, matched-group/common-date restrictions and common-date plus serial-dependence-aware inference. Recover prior ZIP archives and verify provenance and redistribution rights before importing. Phase 430/436 prototypes remain unpublished. Keep all work independent of GIG.
