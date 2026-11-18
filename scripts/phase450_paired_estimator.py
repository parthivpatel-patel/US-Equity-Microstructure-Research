"""Phase 450: paired exchange/group/date descriptive estimator. NOT a causal estimate."""
from collections import defaultdict
from datetime import date
import math, random

def estimate(rows, cutoff="2025-11-03", bootstrap_reps=0, seed=0):
    boundary=date.fromisoformat(cutoff)
    if not rows: raise ValueError("empty observations")
    if type(bootstrap_reps) is not int or bootstrap_reps<0: raise ValueError("invalid bootstrap_reps")
    seen=set(); assignments={}; cells=defaultdict(lambda:{True:[],False:[]})
    for r in rows:
        d=date.fromisoformat(r["date"])
        s,e,g=(r[k] for k in ("security","exchange","matched_group"))
        if not all(isinstance(x,str) and x.strip() for x in (s,e,g)): raise ValueError("invalid identifier")
        t,y=r["treated"],r["outcome"]
        if type(t) is not bool: raise ValueError("treated must be bool")
        if isinstance(y,bool) or not isinstance(y,(int,float)) or not math.isfinite(y): raise ValueError("outcome must be finite numeric")
        if (s,e,d) in seen: raise ValueError("duplicate security-exchange-date")
        seen.add((s,e,d))
        if (s,e) in assignments and assignments[(s,e)]!=(g,t): raise ValueError("unstable assignment within exchange")
        assignments[(s,e)]=(g,t)
        cells[(e,g,d)][t].append(float(y))
    paired=defaultdict(dict)
    for (e,g,d),arms in cells.items():
        if arms[True] and arms[False]:
            paired[(e,g)][d]=sum(arms[True])/len(arms[True])-sum(arms[False])/len(arms[False])
    eligible={k:v for k,v in paired.items() if any(d<boundary for d in v) and any(d>=boundary for d in v)}
    if not eligible: raise ValueError("no stratum has paired pre/post common dates")
    def mean(v): return sum(v)/len(v)
    def effect(v): return mean([x for d,x in v.items() if d>=boundary])-mean([x for d,x in v.items() if d<boundary])
    out={"estimate":mean([effect(v) for v in eligible.values()]),"strata":len(eligible),"common_date_cells":sum(map(len,eligible.values())),"bootstrap_reps":bootstrap_reps,"source_authenticated":False,"causal_identification_established":False}
    if bootstrap_reps:
        pre=sorted({d for v in eligible.values() for d in v if d<boundary})
        post=sorted({d for v in eligible.values() for d in v if d>=boundary})
        rng=random.Random(seed); draws=[]
        for _ in range(bootstrap_reps):
            a=rng.choices(pre,k=len(pre)); b=rng.choices(post,k=len(post)); diffs=[]
            for v in eligible.values():
                x=[v[d] for d in a if d in v]; y=[v[d] for d in b if d in v]
                if not x or not y: break
                diffs.append(mean(y)-mean(x))
            if len(diffs)==len(eligible): draws.append(mean(diffs))
        out["valid_bootstrap_reps"]=len(draws)
        out["bootstrap_support_fraction"]=len(draws)/bootstrap_reps
        if len(draws)>=100 and len(draws)/bootstrap_reps>=.9:
            draws.sort()
            out["bootstrap_percentile_95"]=[draws[int(.025*(len(draws)-1))],draws[int(.975*(len(draws)-1))]]
    return out
