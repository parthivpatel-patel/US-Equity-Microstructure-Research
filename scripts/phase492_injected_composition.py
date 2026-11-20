"""Strict composition audit with explicit reader dependency; no global monkeypatch."""
import hashlib
from datetime import date
from pathlib import Path
from phase490_strict_csv import read_strict

def audit(eligibility, panel, cutoff, *, reader=read_strict):
    try:
        d = date.fromisoformat(cutoff)
    except ValueError as exc:
        raise ValueError('invalid cutoff') from exc
    if d.isoformat() != cutoff:
        raise ValueError('noncanonical cutoff')
    e = reader(eligibility, observed=False)
    o = reader(panel, observed=True)
    if not e:
        raise ValueError('empty eligibility')
    if set(o) - set(e):
        raise ValueError('observation outside eligibility')
    days = sorted({k[2] for k in e})
    if not (days[0] < cutoff <= days[-1]):
        raise ValueError('cutoff requires eligible dates on both sides')
    result = {'cutoff': cutoff, 'provenance_status': 'UNAUTHENTICATED_INPUTS'}
    for name, selected in [('pre', lambda day: day < cutoff), ('post', lambda day: day >= cutoff)]:
        ek = {k for k in e if selected(k[2])}
        ok = {k for k in o if selected(k[2])}
        eu, ou = {k[:2] for k in ek}, {k[:2] for k in ok}
        result[name] = {
            'eligible_cells': len(ek), 'observed_cells': len(ok),
            'missing_eligible_cells': len(ek - ok),
            'observed_zero_cells': sum(o[k] == 0 for k in ok),
            'eligible_units': len(eu), 'observed_units': len(ou),
            'by_exchange': {x: {'eligible': sum(k[1] == x for k in ek),
                                'observed': sum(k[1] == x for k in ok),
                                'missing': sum(k[1] == x for k in ek - ok)}
                            for x in sorted({k[1] for k in ek})},
        }
    for kind, source in [('eligible', e), ('observed', o)]:
        a = {k[:2] for k in source if k[2] < cutoff}
        b = {k[:2] for k in source if k[2] >= cutoff}
        result[kind + '_unit_composition'] = {
            'both': len(a & b), 'pre_only': len(a - b), 'post_only': len(b - a)}
    result['sha256'] = {name: hashlib.sha256(Path(path).read_bytes()).hexdigest()
                        for name, path in [('eligibility', eligibility), ('panel', panel)]}
    return result
