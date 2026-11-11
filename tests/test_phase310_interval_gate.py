import unittest
from scripts.phase310_interval_gate import strict_admitted_audit

S = ['2025-10-30', '2025-10-31', '2025-11-03']
GOOD = ('ABC', 'XNAS', '2025-10-31', '2025-11-03')
EMPTY = ('DEF', 'XNYS', '2025-09-01', '2025-09-02')

class TestStrictIntervalGate(unittest.TestCase):
    def test_complete(self):
        result = strict_admitted_audit([('ABC','XNAS',d) for d in S[1:]], [GOOD], S)
        self.assertEqual(result['expected_cells'], 2)
        self.assertEqual(result['missing'], [])
    def test_mixed_empty_interval_rejected(self):
        with self.assertRaisesRegex(ValueError, 'covers no supplied'):
            strict_admitted_audit([], [GOOD, EMPTY], S)
    def test_all_empty_rejected(self):
        with self.assertRaises(ValueError):
            strict_admitted_audit([], [EMPTY], S)
    def test_missing_not_zero(self):
        self.assertEqual(len(strict_admitted_audit([], [GOOD], S)['missing']), 2)
    def test_generators(self):
        self.assertEqual(strict_admitted_audit(iter([]), iter([GOOD]), iter(S))['expected_cells'], 2)
    def test_provenance_not_asserted(self):
        self.assertFalse(strict_admitted_audit([], [GOOD], S)['source_authenticated'])

if __name__ == '__main__': unittest.main()
