"""Exact within/between weighting decomposition. Constructed data only."""
from fractions import Fraction


def decompose(rows):
    """Rows are (group, hidden, total), integer-valued; positive totals required.

    Difference pooled minus equal-row mean = sum_i (w_i - 1/n) * rate_i.
    Also decomposes by group into between-group and within-group components.
    """
    rows = list(rows)
    if not rows:
        raise ValueError('empty panel')
    parsed = []
    for group, hidden, total in rows:
        if not isinstance(group, str) or not group:
            raise ValueError('invalid group')
        if type(hidden) is not int or type(total) is not int or total <= 0 or not 0 <= hidden <= total:
            raise ValueError('invalid counts')
        parsed.append((group, hidden, total))
    n = len(parsed)
    total_all = sum(t for _, _, t in parsed)
    pooled = Fraction(sum(h for _, h, _ in parsed), total_all)
    equal = sum((Fraction(h, t) for _, h, t in parsed), Fraction()) / n
    groups = sorted({g for g, _, _ in parsed})
    between = Fraction()
    within = Fraction()
    details = {}
    for group in groups:
        part = [(h, t) for g, h, t in parsed if g == group]
        ng = len(part)
        tg = sum(t for _, t in part)
        pg = Fraction(sum(h for h, _ in part), tg)
        eg = sum((Fraction(h, t) for h, t in part), Fraction()) / ng
        sw = Fraction(tg, total_all)
        ew = Fraction(ng, n)
        between += (sw - ew) * eg
        within += sw * (pg - eg)
        details[group] = {'rows': ng, 'total': tg, 'pooled': pg, 'equal': eg,
                          'denominator_weight': sw, 'row_weight': ew}
    assert pooled - equal == between + within
    return {'pooled': pooled, 'equal': equal, 'gap': pooled-equal,
            'between': between, 'within': within, 'groups': details}
