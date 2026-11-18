"""Descriptive pre-reform placebo-date grid; historical inputs unauthenticated."""
from collections import defaultdict
from datetime import date
from math import isfinite

def placebo_grid(rows, boundaries, reform="2025-11-03", min_dates=2):
    reform_day=date.fromisoformat(reform)
    if type(min_dates) is not int or min_dates<2: raise ValueError("invalid minimum dates")
    cuts=[date.fromisoformat(x) for x in boundaries]
    if not cuts or len(set(cuts))!=len(cuts) or any(c>=reform_day for c in cuts):
        raise ValueError("invalid placebo boundaries")
    seen=set(); assignments={}; global_treatment={}
    cells=defaultdict(lambda:{True:[],False:[]})
    for row in rows:
        s,e,g=(row[k] for k in ("security","exchange","matched_group"))
        if not all(isinstance(v,str) and v.strip() for v in (s,e,g)): raise ValueError("invalid identifier")
        d=date.fromisoformat(row["date"]); t=row["treated"]; y=row["outcome"]
        if type(t) is not bool or type(y) not in (int,float) or not isfinite(y): raise ValueError("invalid outcome or treatment")
        if (s,e,d) in seen: raise ValueError("duplicate observation")
        seen.add((s,e,d))
        if (s,e) in assignments and assignments[(s,e)]!=(g,t): raise ValueError("unstable assignment")
        assignments[(s,e)]=(g,t)
        if s in global_treatment and global_treatment[s]!=t: raise ValueError("cross-exchange treatment conflict")
        global_treatment[s]=t
        if d<reform_day: cells[(e,g,d)][t].append(float(y))
    gaps=defaultdict(dict)
    for (e,g,d),arms in cells.items():
        if arms[True] and arms[False]:
            gaps[(e,g)][d]=sum(arms[True])/len(arms[True])-sum(arms[False])/len(arms[False])
    results=[]
    for cut in sorted(cuts):
        group_results=[]
        for (e,g),dated in sorted(gaps.items()):
            pre=[v for d,v in dated.items() if d<cut]
            post=[v for d,v in dated.items() if cut<=d<reform_day]
            if len(pre)>=min_dates and len(post)>=min_dates:
                group_results.append({"exchange":e,"matched_group":g,"pre_dates":len(pre),
                                      "post_dates":len(post),"difference":sum(post)/len(post)-sum(pre)/len(pre)})
        results.append({"placebo_date":cut.isoformat(),"eligible_groups":len(group_results),
                        "paired_groups_total":len(gaps),
                        "equal_group_effect":sum(z["difference"] for z in group_results)/len(group_results) if group_results else None,
                        "groups":group_results})
    supports=[set((z["exchange"],z["matched_group"]) for z in r["groups"]) for r in results]
    common=set.intersection(*supports)
    for r in results:
        values=[z["difference"] for z in r["groups"] if (z["exchange"],z["matched_group"]) in common]
        r["fixed_support_effect"]=sum(values)/len(values) if values else None
        r["fixed_support_groups"]=len(common)
    return {"placebos":results,"paired_cells":sum(map(len,gaps.values())),
            "unpaired_cells":len(cells)-sum(map(len,gaps.values())),
            "source_authenticated":False,"treatment_authenticated":False,
            "serial_dependence_inference_performed":False}
