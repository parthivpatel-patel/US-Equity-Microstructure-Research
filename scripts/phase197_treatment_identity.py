"""Conservative treatment identity audit; structural consistency is not authentication."""
from collections import defaultdict
from datetime import date

REQUIRED = ('window','date','security','exchange','group','treated','outcome')

def audit(rows):
    seen=set(); groups=defaultdict(set); treatments=defaultdict(set); pairs=defaultdict(set); windows=set()
    for row in rows:
        missing=[k for k in REQUIRED if k not in row]
        if missing: raise ValueError('missing fields: '+','.join(missing))
        if type(row['treated']) is not bool: raise ValueError('treated must be boolean')
        if row['outcome'] not in ('count','volume'): raise ValueError('invalid outcome')
        try: day=date.fromisoformat(row['date'])
        except (TypeError,ValueError) as exc: raise ValueError('invalid ISO date') from exc
        if day.isoformat()!=row['date'] or day.weekday()>=5: raise ValueError('noncanonical or weekend date')
        for k in ('window','security','exchange','group'):
            if not isinstance(row[k],str) or not row[k].strip(): raise ValueError('empty identifier')
        key=tuple(row[k] for k in ('window','date','security','exchange','group','outcome'))
        if key in seen: raise ValueError('duplicate panel key')
        seen.add(key)
        entity=(row['security'],row['exchange'])
        groups[entity].add(row['group']); treatments[entity].add(row['treated'])
        pairs[key[:-1]].add(row['outcome']); windows.add(row['window'])
    return {'observations':len(seen),'windows':sorted(windows),
            'treatment_switches':[list(k) for k,v in sorted(treatments.items()) if len(v)>1],
            'group_switches':[list(k) for k,v in sorted(groups.items()) if len(v)>1],
            'unpaired_keys':[list(k) for k,v in sorted(pairs.items()) if v!={'count','volume'}],
            'treatment_authenticated':False}
