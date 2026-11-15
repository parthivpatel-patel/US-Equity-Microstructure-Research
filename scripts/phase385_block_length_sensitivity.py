"""Exact circular-block length sensitivity audit; diagnostics, not inference."""
from fractions import Fraction

def audit_block_lengths(values, lengths, enumerator, max_draws=100000):
    """Compare exact Phase 384 resampled mean distributions over block lengths."""
    values = tuple(values)
    lengths = tuple(lengths)
    if not values or any(type(x) not in (int, Fraction) for x in values):
        raise ValueError('invalid date-level values')
    if not lengths or any(type(x) is not int or not 1 <= x <= len(values) for x in lengths):
        raise ValueError('invalid block lengths')
    if len(set(lengths)) != len(lengths):
        raise ValueError('duplicate block length')
    rows = []
    for length in sorted(lengths):
        result = enumerator(values, length, max_draws=max_draws)
        dist = result['distribution']
        draws = result['draws']
        if sum(c for _, c in dist) != draws:
            raise ValueError('enumerator frequencies do not sum to draws')
        mean = sum((x * c for x, c in dist), Fraction()) / draws
        variance = sum(((x - mean) ** 2 * c for x, c in dist), Fraction()) / draws
        observed = result['observed_mean']
        if mean != observed:
            raise ValueError('unexpected bootstrap mean shift')
        rows.append({'block_length': length, 'draws': draws,
                     'distinct_means': len(dist), 'minimum': dist[0][0],
                     'maximum': dist[-1][0], 'resampling_variance': variance,
                     'degenerate': len(dist) == 1, 'observed_mean': observed})
    return {'n_dates': len(values), 'results': tuple(rows),
            'confidence_interval_validated': False,
            'null_distribution_validated': False,
            'two_way_dependence_handled': False,
            'causal_identification_established': False}
