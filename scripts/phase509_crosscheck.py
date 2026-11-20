"""Internal consistency check, not SEC authentication."""
from collections import Counter
from datetime import date

def check_panel_coverage(panel, roster, coverage):
    if not isinstance(roster, dict) or not roster or any(
        not isinstance(k,str) or not k.strip() or v not in ('treated','control')
        for k,v in roster.items()):
        raise ValueError('invalid roster')
    def day(s):
        if not isinstance(s,str) or len(s)!=10:
            raise ValueError('invalid date')
        try: d=date.fromisoformat(s)
        except ValueError as exc: raise ValueError('invalid date') from exc
        if d.isoformat()!=s: raise ValueError('invalid date')
        return d
    actual=Counter()
    seen=set()
    for r in panel:
        try: sec,dt,ex,group=(r[k] for k in ('security','date','exchange','group'))
        except (KeyError,TypeError) as exc: raise ValueError('invalid panel row') from exc
        dt=day(dt)
        if sec not in roster or roster[sec]!=group or not isinstance(ex,str) or not ex.strip():
            raise ValueError('invalid panel identity')
        key=(sec,dt,ex)
        if key in seen: raise ValueError('duplicate panel key')
        seen.add(key)
        actual[(dt,ex,group)]+=1
    if not seen: raise ValueError('empty panel')
    declared={}
    for r in coverage:
        try:
            dt,ex=day(r['date']),r['exchange']
            te,to,ce,co=(r[k] for k in ('treated_eligible','treated_observed','control_eligible','control_observed'))
        except (KeyError,TypeError) as exc: raise ValueError('invalid coverage row') from exc
        if not isinstance(ex,str) or not ex.strip() or (dt,ex) in declared:
            raise ValueError('invalid or duplicate coverage key')
        if any(type(x) is not int or x<0 for x in (te,to,ce,co)) or to>te or co>ce or te+ce==0:
            raise ValueError('invalid counts')
        if 'period' in r and r['period']!=('pre' if dt<date(2025,11,3) else 'post'):
            raise ValueError('mislabeled period')
        declared[(dt,ex)]=(te,to,ce,co)
    if not declared: raise ValueError('empty coverage')
    unexpected=sorted(set((d,e) for d,e,g in actual)-set(declared))
    mismatches=[]
    for (dt,ex),(te,to,ce,co) in sorted(declared.items()):
        a,b=actual[(dt,ex,'treated')],actual[(dt,ex,'control')]
        if (a,b)!=(to,co):
            mismatches.append({'date':dt.isoformat(),'exchange':ex,'treated_declared':to,'treated_panel':a,'control_declared':co,'control_panel':b})
    return {'consistent':not mismatches and not unexpected,'panel_rows':len(seen),
            'coverage_cells':len(declared),'mismatches':mismatches,
            'unexpected_panel_cells':[{'date':d.isoformat(),'exchange':e} for d,e in unexpected]}
