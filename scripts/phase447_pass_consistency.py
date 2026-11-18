"""Check pass-flag coherence across source-bound panel reports.

This validates report logic only, not provenance, treatment, or effect estimation.
"""
from phase446_report_contract import audit as audit_contract


def audit(report):
    audit_contract(report)
    labels = ('daily', 'calendar', 'assignment_scope')
    for label in labels:
        flag = report[label].get('pass')
        if type(flag) is not bool:
            raise ValueError(f'{label}: missing or non-Boolean pass flag')
    expected = all(report[label]['pass'] for label in labels)
    if report['pass'] is not expected:
        raise ValueError('top-level pass flag disagrees with component conjunction')
    return {'contract_valid': True, 'pass_consistent': True,
            'panel_pass': expected, 'sec_origin_authenticated': False,
            'historical_effect_estimated': False}
