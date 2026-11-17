import unittest
from phase434_common_date_gate import gate

class GateTests(unittest.TestCase):
    def unit(self, name, dates, period='pre'):
        return {'match_group': name, 'exchange': 'X', 'period': period,
                'paired_date_values': dates}

    def test_missing_unit_fails_closed(self):
        r = {'by_unit': [self.unit('A', ['2025-10-30']), self.unit('B', [])]}
        self.assertFalse(gate(r, 'pre')['pass'])
        self.assertEqual(gate(r, 'pre')['zero_paired_units'], 1)

    def test_disjoint_dates_fail(self):
        r = {'by_unit': [self.unit('A', ['2025-10-30']), self.unit('B', ['2025-10-31'])]}
        self.assertFalse(gate(r, 'pre')['pass'])

    def test_shared_dates_pass(self):
        r = {'by_unit': [self.unit('A', ['2025-10-30', '2025-10-31']), self.unit('B', ['2025-10-31'])]}
        self.assertEqual(gate(r, 'pre')['common_dates'], ['2025-10-31'])
        self.assertTrue(gate(r, 'pre')['pass'])

    def test_no_units_fail(self):
        self.assertFalse(gate({'by_unit': []}, 'post')['pass'])

if __name__ == '__main__':
    unittest.main()
