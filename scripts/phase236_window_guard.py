"""Strict pre-estimation window validation; does not authenticate trading calendars."""
from datetime import date

def validate_estimation_windows(sessions, early_dates, late_dates, calendar):
    """Reject malformed windows before downstream estimation."""
    def parse(seq, label):
        if not isinstance(seq, (list, tuple)) or not seq:
            raise ValueError(f'{label} must be a nonempty list or tuple')
        parsed = []
        for item in seq:
            if not isinstance(item, str):
                raise ValueError(f'{label} requires ISO date strings')
            try:
                d = date.fromisoformat(item)
            except ValueError as exc:
                raise ValueError(f'{label} has invalid ISO date') from exc
            if d.isoformat() != item:
                raise ValueError(f'{label} has noncanonical ISO date')
            parsed.append(d)
        if any(a >= b for a, b in zip(parsed, parsed[1:])):
            raise ValueError(f'{label} must be strictly increasing')
        return tuple(seq)
    roster = parse(calendar, 'calendar')
    requested = parse(sessions, 'sessions')
    early = parse(early_dates, 'early_dates')
    late = parse(late_dates, 'late_dates')
    if requested != early + late:
        raise ValueError('sessions must exactly concatenate early and late windows')
    if not set(requested).issubset(set(roster)):
        raise ValueError('requested sessions absent from supplied calendar')
    return {'n_early': len(early), 'n_late': len(late), 'n_sessions': len(requested),
            'calendar_independently_verified': False}
