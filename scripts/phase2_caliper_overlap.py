#!/usr/bin/env python3
"""Descriptive 1-nearest-neighbor caliper sensitivity on archived processed Phase-2 panel.
NOT raw SEC authentication or causal inference. Requires pandas, numpy, scipy.
Usage: python scripts/phase2_caliper_overlap.py path/to/roundlot_phase2_security_panel.csv
"""
import hashlib
import json
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

EXPECTED_SHA = "2ccb80427a765ca3858f11f2874d6f87a79a559ec1fdeafc34420e82840e5bbb"
FEATURES = ["r_pre", "v_pre", "log_trades_pre"]

def analyze(path):
    digest = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    if digest != EXPECTED_SHA:
        raise ValueError("Archived processed input SHA-256 mismatch")
    d = pd.read_csv(path)
    if len(d) != 2262 or d.Ticker.duplicated().any() or d.treated.sum() != 68:
        raise ValueError("Archived sample membership changed")
    if not (d.trades_pre > 0).all():
        raise ValueError("Nonpositive baseline trade count")
    d["log_trades_pre"] = np.log1p(d.trades_pre)
    if not np.isfinite(d[FEATURES + ["dr", "dv"]].to_numpy()).all():
        raise ValueError("Nonfinite input")
    sd = d[FEATURES].std(ddof=1).to_numpy()
    if np.any(sd <= 0):
        raise ValueError("Zero covariate scale")
    t = d.loc[d.treated == 1].reset_index(drop=True)
    c = d.loc[d.treated == 0].reset_index(drop=True)
    distances, indexes = cKDTree(c[FEATURES].to_numpy()/sd).query(t[FEATURES].to_numpy()/sd, k=1)
    cases = []
    for cap in (None, 0.25, 0.5, 0.75):
        keep = np.ones(len(t), dtype=bool) if cap is None else distances <= cap
        tt = t.loc[keep]
        cc = c.iloc[indexes[keep]]
        if len(tt) == 0:
            raise ValueError("No matched treated securities")
        reuse = cc.Ticker.value_counts()
        cases.append({
            "caliper": "none" if cap is None else cap,
            "n_treated": len(tt),
            "n_distinct_controls": cc.Ticker.nunique(),
            "max_control_reuse": int(reuse.max()),
            "trade_gap_pp": float(100*(tt.dr.mean()-cc.dr.mean())),
            "volume_gap_pp": float(100*(tt.dv.mean()-cc.dv.mean())),
            "post_match_smd": {k: float((tt[k].mean()-cc[k].mean())/sd[i]) for i,k in enumerate(FEATURES)},
            "max_distance": float(distances[keep].max()),
        })
    return {
        "input_sha256": digest,
        "source_authentication": "NOT VERIFIED",
        "method": "1-NN with replacement; pooled-SD-scaled baseline covariates; post-match SMD uses full-sample SD",
        "distance_quantiles": {str(q):float(np.quantile(distances,q)) for q in (0,.25,.5,.75,.9,.95,1)},
        "cases": cases,
    }

if __name__ == "__main__":
    print(json.dumps(analyze(sys.argv[1]), indent=2, sort_keys=True))
