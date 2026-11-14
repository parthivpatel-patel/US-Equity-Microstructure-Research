"""Fail-closed coverage gate for security-date exchange aggregation; no source authentication."""
from collections import defaultdict
from math import isfinite

ALLOWED = {'observed', 'source_missing', 'not_listed', 'not_trading', 'exchange_not_applicable'}

def aggregate_complete_cells(rows, exchanges):
    """Sum only security-date cells with all declared exchanges observed; never impute."""
    exchanges = list(exchanges)
    if not exchanges or any(not isinstance(e, str) or not e.strip() for e in exchanges) or len(set(exchanges)) != len(exchanges):
        raise ValueError('invalid exchanges')
    cells = defaultdict(dict)
    for security, day, exchange, status, value in rows:
        if not isinstance(security, str) or not security.strip() or not isinstance(day, str) or not day.strip():
            raise ValueError('invalid key')
        if exchange not in exchanges or status not in ALLOWED:
            raise ValueError('invalid exchange/status')
        if exchange in cells[(security, day)]:
            raise ValueError('duplicate cell')
        if status == 'observed':
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value) or value < 0:
                raise ValueError('invalid observed metric')
        elif value is not None:
            raise ValueError('nonobserved metric must be None')
        cells[(security, day)][exchange] = (status, value)
    if not cells:
        raise ValueError('empty rows')
    complete = {}
    excluded = {}
    for key, exchange_cells in sorted(cells.items()):
        missing = sorted(set(exchanges) - set(exchange_cells))
        nonobserved = sorted(e for e, (status, _) in exchange_cells.items() if status != 'observed')
        if missing or nonobserved:
            excluded[key] = {'undeclared_exchanges': missing, 'nonobserved_exchanges': nonobserved}
        else:
            total = sum(exchange_cells[e][1] for e in exchanges)
            if not isfinite(total):
                raise ValueError('nonfinite aggregate')
            complete[key] = total
    return {'complete': complete, 'excluded': excluded, 'status': 'COVERAGE_GATED_DESCRIPTIVE_NO_CAUSAL_CLAIM'}
