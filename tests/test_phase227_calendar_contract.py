"""Deterministic 2025 NYSE session admission contract; not historical data authentication."""
import datetime
import unittest

# Explicit known full-day NYSE closures within the diagnostic interval.
# This narrow contract is not a substitute for a sourced complete exchange calendar.
KNOWN_CLOSED = frozenset({'2025-09-01', '2025-11-27', '2025-12-25'})

def validate_sessions(sessions, closed=KNOWN_CLOSED):
    if not sessions or len(set(sessions)) != len(sessions) or list(sessions) != sorted(sessions):
        raise ValueError('sessions must be nonempty, ordered, unique')
    for value in sessions:
        day = datetime.date.fromisoformat(value)
        if day.isoformat() != value or day.weekday() >= 5 or value in closed:
            raise ValueError('nontrading date in supplied sessions')
    return tuple(sessions)

class CalendarContract(unittest.TestCase):
    def test_weekday_session_admitted(self):
        self.assertEqual(validate_sessions(['2025-09-02','2025-09-03']), ('2025-09-02','2025-09-03'))
    def test_labor_day_rejected(self):
        with self.assertRaises(ValueError): validate_sessions(['2025-09-01'])
    def test_weekend_rejected(self):
        with self.assertRaises(ValueError): validate_sessions(['2025-09-06'])
    def test_duplicate_rejected(self):
        with self.assertRaises(ValueError): validate_sessions(['2025-09-02','2025-09-02'])
    def test_out_of_order_rejected(self):
        with self.assertRaises(ValueError): validate_sessions(['2025-09-03','2025-09-02'])
    def test_noncanonical_rejected(self):
        with self.assertRaises(ValueError): validate_sessions(['2025-9-2'])
    def test_thanksgiving_rejected(self):
        with self.assertRaises(ValueError): validate_sessions(['2025-11-27'])

if __name__ == '__main__': unittest.main()
