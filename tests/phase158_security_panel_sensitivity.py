"""Phase 158: archived Phase 2 security-panel sensitivity audit.
Requires pandas, numpy, statsmodels and the private/locally retained
roundlot_phase2_security_panel.csv. No raw or derived market data is bundled.
Usage: python tests/phase158_security_panel_sensitivity.py /path/to/roundlot_phase2_security_panel.csv
"""
import sys
import numpy as np
import pandas as pd
import statsmodels.api as sm

def run(path):
    p = pd.read_csv(path)
    assert len(p) == 2262 and int(p.treated.sum()) == 68
    assert p.Ticker.is_unique and p.isna().sum().sum() == 0
    assert np.allclose(p.dr, p.r_post - p.r_pre)
    assert np.allclose(p.dv, p.v_post - p.v_pre)
    for c in ("r_pre", "r_post", "v_pre", "v_post"):
        assert p[c].between(0, 1).all()
    assert (p[["trades_pre", "trades_post"]] > 0).all().all()
    print("panel", len(p), "treated", int(p.treated.sum()), "controls", int((1-p.treated).sum()))
    for y in ("dr", "dv"):
        for spec in ("unadjusted", "baseline", "weighted", "trim_1pct", "trim_5pct"):
            q = p.copy()
            controls = ["r_pre", "v_pre"] if spec == "baseline" else []
            if spec.startswith("trim_"):
                cut = .01 if spec == "trim_1pct" else .05
                lo, hi = q[y].quantile([cut, 1-cut])
                q = q[q[y].between(lo, hi)]
            x = sm.add_constant(q[["treated"] + controls])
            if spec == "weighted":
                model = sm.WLS(q[y], x, weights=np.minimum(q.trades_pre, q.trades_post))
            else:
                model = sm.OLS(q[y], x)
            fit = model.fit(cov_type="HC3")
            print(y, spec, len(q), int(q.treated.sum()),
                  format(fit.params["treated"], ".8f"),
                  format(fit.bse["treated"], ".8f"),
                  format(fit.pvalues["treated"], ".8g"))
    print("baseline means by provisional treatment group")
    print(p.groupby("treated")[["r_pre", "v_pre", "trades_pre", "trades_post"]].mean())

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Pass local path to archived panel CSV")
    run(sys.argv[1])
