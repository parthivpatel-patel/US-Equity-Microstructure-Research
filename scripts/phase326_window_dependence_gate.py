"""Audit dated historical placebo-window chronology and overlap; no independence claims."""
import csv
import datetime as dt
import json
import sys
from collections import defaultdict

REQUIRED = {'outcome','window_id','start_date','end_date','placebo_pp'}

def audit(rows):
    groups = defaultdict(list)
    seen = set()
    for row in rows:
        if not REQUIRED.issubset(row):
            raise ValueError('missing required columns')
        name, wid = row['outcome'].strip(), row['window_id'].strip()
        if not name or not wid or (name,wid) in seen:
            raise ValueError('empty or duplicate outcome/window_id')
        seen.add((name,wid))
        start = dt.date.fromisoformat(row['start_date'])
        end = dt.date.fromisoformat(row['end_date'])
        if start > end:
            raise ValueError('reversed interval')
        if end >= dt.date(2025,11,3):
            raise ValueError('historical placebo reaches reform date')
        groups[name].append((wid,start,end))
    if not groups:
        raise ValueError('no observations')
    result = {}
    for name, intervals in groups.items():
        graph = {wid:set() for wid,_,_ in intervals}
        overlap_count = 0
        for i in range(len(intervals)):
            for j in range(i+1,len(intervals)):
                a,b = intervals[i],intervals[j]
                if max(a[1],b[1]) <= min(a[2],b[2]):
                    overlap_count += 1
                    graph[a[0]].add(b[0])
                    graph[b[0]].add(a[0])
        visited = set()
        components = []
        for wid in graph:
            if wid in visited:
                continue
            stack=[wid]
            visited.add(wid)
            component=[]
            while stack:
                u=stack.pop()
                component.append(u)
                for v in graph[u]:
                    if v not in visited:
                        visited.add(v)
                        stack.append(v)
            components.append(component)
        n=len(intervals)
        result[name] = {
            'n_windows':n,
            'overlapping_pairs':overlap_count,
            'total_pairs':n*(n-1)//2,
            'overlap_connected_components':len(components),
            'largest_component_windows':max(map(len,components)),
            'all_windows_pairwise_disjoint':overlap_count==0,
            'warning':'Overlap components are not effective independent sample sizes.'
        }
    return result

if __name__=='__main__':
    if len(sys.argv)!=2:
        sys.exit('usage: python scripts/phase326_window_dependence_gate.py dated_windows.csv')
    with open(sys.argv[1],newline='') as f:
        print(json.dumps(audit(list(csv.DictReader(f))),indent=2,sort_keys=True))
