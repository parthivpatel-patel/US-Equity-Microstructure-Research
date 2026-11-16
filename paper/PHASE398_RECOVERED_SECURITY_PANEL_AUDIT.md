# Phase 398 — Recovered security-panel numerical audit (2026-11-15)

## Source and checks

Recovered Library file `roundlot_phase2_security_panel.csv` (345,329 bytes), SHA-256 `2ccb80427a765ca3858f11f2874d6f87a79a559ec1fdeafc34420e82840e5bbb`. The raw panel is **not republished** pending confirmation of its underlying SEC data provenance and redistribution terms. Read-only local analysis loaded 2,262 ticker rows, including 68 marked treated and 2,194 controls. Ticker identifiers are unique, all required fields nonmissing and finite, reported rate measures lie within [0,1], and `dr=r_post-r_pre`, `dv=v_post-v_pre` agree to machine precision. Pre-period days range 12–23, post-period days 12–19: exposure is **not uniform across the panel**.

## Actual panel computations (descriptive, not causal)

Unmatched equal-security-weighted treated-minus-control changes:

| Outcome | Treated mean | Control mean | Difference | Welch SE | 95% Welch CI | Two-sided Welch p |
| --- | ---: | ---: | ---: | ---: | --- | ---: |
| `dr` (trade-count-rate change) | -0.020946862 | 0.013682424 | **-0.034629286** | 0.004388763 | [-0.043355566, -0.025903006] | 9.50221e-12 |
| `dv` (share-volume-rate change) | -0.018781051 | 0.006939478 | **-0.025720529** | 0.004184797 | [-0.034047063, -0.017393995] | 2.83586e-8 |

Using **preperiod trade counts** as within-group weights, treated-minus-control differences become `dr=-0.027063922` and `dv=-0.010064732`. These are sensitivity diagnostics, **not share-volume-weighted estimands**: the weight is trade count, not executed share volume. The descriptive `dv` contrast shifts from -0.02572 to -0.01006 (absolute change 0.01566). This underscores composition/weighting sensitivity.

## Identification and inference limitations

The 2,194 controls are the recovered broad security panel, **not the separately documented 204 matched controls**. Welch inference assumes independent security observations and does not handle common-date shocks, exchange clustering, matched-pair structure, overlapping dates, serial dependence, pretrend violations or selection. It is **not valid causal or publication-grade uncertainty**. Panel rows contain pre/post aggregates rather than security-date-exchange histories, so this file alone cannot reconstruct September pretrends, October placebos, exchange fixed effects, or two-way/date-block inference. The 68 treatment flags are inherited from an unverified historical roster; they are not independently authenticated here.

## Reproduction

Run `python scripts/phase398_panel_audit.py /path/to/roundlot_phase2_security_panel.csv` after independently obtaining and authenticating the source file; requires numpy, pandas, scipy. The script emits only aggregate JSON. Local verification: seven focused fixture tests passed on a closely related implementation. The exact GitHub-published script and repository-wide suite have not been executed in this session. No original historical ZIPs imported, no causal claim. November 14 target missed; November 30 is provisional.

## Next

Recover the original daily SEC source, historical Nasdaq roster, and matched-control mapping; verify row lineage and period definitions, then rebuild pretrends/placebos and date-aware inference from authenticated security-date-exchange observations.
