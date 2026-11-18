"""Circular moving-block bootstrap for fully balanced exchange/group/date gaps.

Descriptive sensitivity only. No source authentication or causal identification.
"""
from collections import defaultdict
from datetime import date
import math
import random

def analyze(rows, cutoff="2025-11-03", block_length=5, reps=999, seed=0):
    if type(block_length) is not int or block_length < 1: raise ValueError("invalid block_length")
    if type(reps) is not int or reps < 1: raise ValueError("invalid reps")
    boundary = date.fromisoformat(cutoff)
    cells = defaultdict(lambda: {True: [], False: []})
    seen = set(); assignment = {}; global_treatment = {}
    for row in rows:
        s, e, g = (row[k] for k in ("security", "exchange", "matched_group"))
        if not all(isinstance(v, str) and v.strip() for v in (s,e,g)): raise ValueError("invalid identifier")
        d = date.fromisoformat(row["date"])
        t, y = row["treated"], row["outcome"]
        if type(t) is not bool: raise ValueError("invalid treatment")
        if isinstance(y,bool) or not isinstance(y,(int,float)) or not math.isfinite(y): raise ValueError("invalid outcome")
        if (s,e,d) in seen: raise ValueError("duplicate observation")
        seen.add((s,e,d))
        if (s,e) in assignment and assignment[(s,e)] != (g,t): raise ValueError("unstable exchange assignment")
        assignment[(s,e)] = (g,t)
        if s in global_treatment and global_treatment[s] != t: raise ValueError("contradictory global treatment")
        global_treatment[s] = t
        cells[(e,g,d)][t].append(float(y))
    gaps = defaultdict(dict)
    for (e,g,d), arms in cells.items():
        if arms[True] and arms[False]:
            gaps[(e,g)][d] = sum(arms[True])/len(arms[True])-sum(arms[False])/len(arms[False])
    if not gaps: raise ValueError("no paired cells")
    common_dates = set.intersection(*(set(v) for v in gaps.values()))
    pre = sorted(d for d in common_dates if d < boundary)
    post = sorted(d for d in common_dates if d >= boundary)
    if len(pre) < 2*block_length or len(post) < 2*block_length:
        raise ValueError("insufficient balanced pre/post dates for block inference")
    strata = sorted(gaps)
    def average(values): return sum(values)/len(values)
    def statistic(a,b):
        return average([average([gaps[k][d] for d in b])-average([gaps[k][d] for d in a]) for k in strata])
    estimate = statistic(pre,post)
    rng = random.Random(seed)
    def draw(dates):
        n = len(dates); output=[]
        while len(output) < n:
            start = rng.randrange(n)
            output.extend(dates[(start+j)%n] for j in range(block_length))
        return output[:n]
    boot = sorted(statistic(draw(pre),draw(post)) for _ in range(reps))
    def quantile(p):
        z = (len(boot)-1)*p; lo=int(z); hi=min(lo+1,len(boot)-1)
        return boot[lo]+(boot[hi]-boot[lo])*(z-lo)
    return {"estimate":estimate,"percentile_95":[quantile(.025),quantile(.975)],
            "strata":len(strata),"balanced_pre_dates":len(pre),"balanced_post_dates":len(post),
            "excluded_unbalanced_calendar_dates":len({key[2] for key in cells}-common_dates),
            "block_length":block_length,"bootstrap_reps":reps,"seed":seed,
            "resampling":"circular moving blocks separately by period; synchronized across strata",
            "source_authenticated":False,"causal_identification_established":False,
            "inference_caveat":"descriptive sensitivity only; complete-case selection and short panels can bias intervals"}
