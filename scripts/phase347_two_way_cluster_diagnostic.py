"""Descriptive uncorrected two-way cluster variance; NOT calibrated inference."""
from collections import defaultdict
from math import isfinite

def variance_components(rows):
    rows = list(rows)
    if len(rows) < 2:
        raise ValueError('at least two observations required')
    seen = set()
    for g, d, y in rows:
        if not g or not d or not isfinite(y):
            raise ValueError('invalid row')
        if (g,d) in seen:
            raise ValueError('duplicate group-date: aggregate exchanges before use')
        seen.add((g,d))
    n=len(rows)
    mean=sum(y for _,_,y in rows)/n
    residuals=[(g,d,y-mean) for g,d,y in rows]
    def meat(index):
        sums=defaultdict(float)
        for g,d,e in residuals:
            key=(g,d) if index==2 else (g if index==0 else d)
            sums[key]+=e
        return sum(v*v for v in sums.values())/(n*n)
    group,date,intersection=(meat(i) for i in range(3))
    raw=group+date-intersection
    return {'n':n,'groups':len({g for g,_,_ in rows}),
            'dates':len({d for _,d,_ in rows}), 'mean_pp':mean,
            'group_component':group,'date_component':date,
            'intersection_component':intersection,
            'two_way_raw_variance':raw,
            'nonnegative_variance_certified':raw>=0,
            'warning':'Uncorrected two-way cluster sandwich; no finite-sample correction, p-value or CI. Requires enough independent clusters; equal-cell estimand only.'}
