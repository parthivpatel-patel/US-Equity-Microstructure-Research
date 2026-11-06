"""Validate count/volume assignment consistency without claiming treatment authentication."""
from collections import defaultdict
from datetime import date

def audit(rows):
    by_key = defaultdict(dict)
    seen = set()
    for row in rows:
        required = ('window','date','security','exchange','outcome','group','treated')
        if any(k not in row for k in required): raise ValueError('missing required field')
        if row['outcome'] not in ('count','volume') or type(row['treated']) is not bool:
            raise ValueError('invalid outcome or treatment')
        try: d = date.fromisoformat(row['date'])
        except (TypeError,ValueError) as exc: raise ValueError('invalid date') from exc
        if d.isoformat() != row['date'] or d.weekday() >= 5: raise ValueError('noncanonical or weekend date')
        if any(not isinstance(row[k],str) or not row[k].strip() for k in ('window','security','exchange','group')):
            raise ValueError('invalid identifier')
        key = tuple(row[k] for k in ('window','date','security','exchange'))
        obs_key = key + (row['outcome'],)
        if obs_key in seen: raise ValueError('duplicate outcome for entity/date')
        seen.add(obs_key)
        by_key[key][row['outcome']] = (row['group'],row['treated'])
    unpaired=[]; conflicts=[]
    for key,outcomes in sorted(by_key.items()):
        if set(outcomes) != {'count','volume'}: unpaired.append(list(key))
        elif outcomes['count'] != outcomes['volume']: conflicts.append(list(key))
    return {'entity_dates':len(by_key),'unpaired_entity_dates':unpaired,
            'within_pair_assignment_conflicts':conflicts,'treatment_authenticated':False}
