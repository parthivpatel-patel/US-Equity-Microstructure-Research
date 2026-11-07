"""Descriptive weighting sensitivity on a Phase 222-admitted complete panel.

No claim that the panel, calendar, treatment assignment or SEC source is authenticated.
"""
from scripts.phase222_panel_gate import audit_panel


def weighting_sensitivity(rows, sessions, treated, controls, exchanges):
    admission = audit_panel(rows, sessions, treated, controls, exchanges)
    index = {(r['date'], r['security'], r['exchange']): r for r in rows}
    result = []
    for day in sessions:
        group = {}
        for label, securities in (('treated', treated), ('control', controls)):
            cells = [index[(day, s, e)] for s in securities for e in exchanges]
            equal = sum(r['hidden_count']/r['total_count'] for r in cells)/len(cells)
            pooled = sum(r['hidden_count'] for r in cells)/sum(r['total_count'] for r in cells)
            security_equal = sum(sum(index[(day,s,e)]['hidden_count']/index[(day,s,e)]['total_count'] for e in exchanges)/len(exchanges) for s in securities)/len(securities)
            assert abs(equal-security_equal) < 1e-12
            group[label] = {'equal_cell_rate':equal, 'pooled_count_rate':pooled,
                            'denominator':sum(r['total_count'] for r in cells)}
        result.append({'date':day, 'equal_cell_contrast':group['treated']['equal_cell_rate']-group['control']['equal_cell_rate'],
                       'pooled_count_contrast':group['treated']['pooled_count_rate']-group['control']['pooled_count_rate'],
                       'treated':group['treated'], 'control':group['control']})
    return {'admission':admission, 'daily':result, 'interpretation':'descriptive only; weighting sensitivity is not a causal estimate'}
