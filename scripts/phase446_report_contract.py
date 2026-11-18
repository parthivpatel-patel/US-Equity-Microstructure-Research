"""Validate internal consistency of source-bound assignment reports; not SEC authentication."""
import re

HEX = re.compile(r'^[0-9a-f]{64}$')

def audit(report):
    if not isinstance(report, dict):
        raise ValueError('report must be a dictionary')
    digest = report.get('source_sha256')
    size = report.get('source_bytes')
    if not isinstance(digest, str) or not HEX.fullmatch(digest):
        raise ValueError('invalid SHA-256')
    if type(size) is not int or size <= 0:
        raise ValueError('invalid byte length')
    daily, calendar, assignment = (report.get(k) for k in ('daily','calendar','assignment_scope'))
    if any(not isinstance(x, dict) for x in (daily, calendar, assignment)):
        raise ValueError('missing diagnostic')
    n = report.get('observations')
    if type(n) is not int or n <= 0:
        raise ValueError('invalid observation count')
    for label, sub in (('daily',daily),('calendar',calendar),('assignment_scope',assignment)):
        if sub.get('source_sha256') != digest or sub.get('source_bytes') != size:
            raise ValueError(f'{label}: source mismatch')
        if type(sub.get('observations')) is not int or sub['observations'] != n:
            raise ValueError(f'{label}: observation count mismatch')
    if type(report.get('pass')) is not bool or type(assignment.get('pass')) is not bool:
        raise ValueError('invalid pass flag')
    for key in ('global_treatment_conflicts','within_exchange_treatment_conflicts','within_exchange_group_changes','permitted_cross_exchange_group_variation'):
        value = assignment.get(key)
        if not isinstance(value,list) or any(not isinstance(s,str) or not s for s in value) or len(set(value)) != len(value):
            raise ValueError(f'invalid {key}')
    conflicts = any(assignment[key] for key in ('global_treatment_conflicts','within_exchange_treatment_conflicts','within_exchange_group_changes'))
    if assignment['pass'] == bool(conflicts):
        raise ValueError('assignment pass contradicts conflicts')
    if report['pass'] and not assignment['pass']:
        raise ValueError('top-level pass contradicts assignment failure')
    if report.get('treatment_authenticated') is not False or report.get('historical_effect_estimated') is not False:
        raise ValueError('unsupported authentication or estimation claim')
    return {'pass': True, 'source_sha256':digest, 'source_bytes':size, 'observations':n,
            'contract_valid':True, 'sec_origin_authenticated':False,
            'historical_effect_estimated':False}
