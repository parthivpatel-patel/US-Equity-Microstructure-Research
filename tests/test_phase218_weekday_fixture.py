import unittest
from datetime import date
from scripts.phase218_weekday_fixture import weekday_fixture

class WeekdayFixtureTests(unittest.TestCase):
    def test_weekends_excluded(self):
        rows, days, early, late = weekday_fixture()
        self.assertEqual(len(days), 24)
        self.assertTrue(all(date.fromisoformat(d).weekday() < 5 for d in days))
        self.assertEqual([r['date'] for r in rows], days)
        self.assertEqual(early, (days[0], days[9]))
        self.assertEqual(late, (days[14], days[23]))

    def test_determinism(self):
        self.assertEqual(weekday_fixture(), weekday_fixture())

    def test_invalid_count(self):
        for n in (0, 11, 2.5, True):
            with self.subTest(n=n), self.assertRaises(ValueError):
                weekday_fixture(count=n)

    def test_reform_intrusion(self):
        with self.assertRaises(ValueError):
            weekday_fixture('2025-10-31', 24)

    def test_no_holiday_authentication(self):
        _, days, _, _ = weekday_fixture('2025-09-01', 12)
        self.assertIn('2025-09-01', days)  # Labor Day: deliberately NOT exchange-authenticated

if __name__ == '__main__':
    unittest.main()
