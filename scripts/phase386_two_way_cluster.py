"""Two-way CR0 variance for a balanced matched-pair x date gap panel.

Methodology-only. Assumes independent pair and date clustering dimensions;
not a serial-correlation-robust time-series estimator.
"""
from fractions import Fraction


def two_way_cr0(rows):
    """Rows (pair, date, gap) with exactly one observation per cell.

    Returns mean, CGM inclusion-exclusion CR0 variance and components.
    No finite-cluster corrections or confidence interval are implied.
    """
    rows = tuple(rows)
    if not rows:
        raise ValueError('empty panel')
    cells = {}
    pairs, dates = set(), set()
    for row in rows:
        if len(row) != 3:
            raise ValueError('expected pair, date, gap')
        pair, date, value = row
        if not isinstance(pair, str) or not pair or not isinstance(date, str) or not date:
            raise ValueError('nonempty string keys required')
        if type(value) not in (int, Fraction):
            raise ValueError('integer or Fraction gap required')
        if (pair, date) in cells:
            raise ValueError('duplicate cell')
        cells[pair, date] = Fraction(value)
        pairs.add(pair)
        dates.add(date)
    if len(pairs) < 2 or len(dates) < 2 or len(cells) != len(pairs) * len(dates):
        raise ValueError('requires balanced panel with at least two pairs and dates')
    n = len(cells)
    mean = sum(cells.values(), Fraction()) / n
    residual = {k: v - mean for k, v in cells.items()}
    pair_scores = [sum((residual[p, d] for d in dates), Fraction()) for p in pairs]
    date_scores = [sum((residual[p, d] for p in pairs), Fraction()) for d in dates]
    pair_component = sum((x*x for x in pair_scores), Fraction()) / (n*n)
    date_component = sum((x*x for x in date_scores), Fraction()) / (n*n)
    cell_component = sum((x*x for x in residual.values()), Fraction()) / (n*n)
    variance = pair_component + date_component - cell_component
    return {'mean': mean, 'variance_cr0': variance, 'pair_component': pair_component,
            'date_component': date_component, 'intersection_component': cell_component,
            'n_pairs': len(pairs), 'n_dates': len(dates), 'n_cells': n,
            'negative_variance': variance < 0, 'causal_identification_established': False}
