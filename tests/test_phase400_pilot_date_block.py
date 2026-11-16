"""Fixture-only tests; no private SEC data required."""
import unittest
import pandas as pd
from phase400_pilot_date_block import audit, run

class TestPilot(unittest.TestCase):
    def setUp(self):
        rows = []
        for date in [20251001, 20251002, 20251016, 20251017, 20251103, 20251104]:
            for tier in [10, 40, 100]:
                rows.append({'Date': date, 'lot': tier, 'Hidden': tier + (date % 10),
                             'TradesForHidden': 200, "HiddenVol('000)": tier,
                             "TradeVolForHidden('000)": 200})
        self.data = pd.DataFrame(rows)

    def test_valid(self):
        audit(self.data)

    def test_duplicate(self):
        with self.assertRaises(ValueError):
            audit(pd.concat([self.data, self.data.iloc[:1]]))

    def test_missing_tier(self):
        with self.assertRaises(ValueError):
            audit(self.data[self.data.lot != 10])

    def test_negative_numerator(self):
        x = self.data.copy()
        x.loc[0, 'Hidden'] = -1
        with self.assertRaises(ValueError):
            audit(x)

    def test_determinism(self):
        self.assertEqual(run(self.data, reps=20), run(self.data, reps=20))

    def test_eight_results(self):
        self.assertEqual(len(run(self.data, reps=10)), 8)

if __name__ == '__main__':
    unittest.main()
