import unittest
from scripts.phase309_admission import admitted_audit

S = ['2025-10-30', '2025-10-31', '2025-11-03']
I = [('ABC', 'XNAS', S[1], S[2])]

class TestAdmission(unittest.TestCase):
    def test_complete(self):
        r = admitted_audit([('ABC', 'XNAS', d) for d in S[1:]], I, S)
        self.assertEqual(r['expected_cells'], 2)
        self.assertEqual(r['missing'], [])
    def test_empty_sessions(self):
        with self.assertRaisesRegex(ValueError, 'empty trading-session'):
            admitted_audit([], I, [])
    def test_empty_intervals(self):
        with self.assertRaisesRegex(ValueError, 'empty eligibility'):
            admitted_audit([], [], S)
    def test_no_eligible_cells(self):
        with self.assertRaisesRegex(ValueError, 'cover no supplied'):
            admitted_audit([], [('ABC', 'XNAS', '2025-09-01', '2025-09-02')], S)
    def test_missing_not_zero(self):
        self.assertEqual(len(admitted_audit([], I, S)['missing']), 2)
    def test_generators(self):
        self.assertEqual(admitted_audit(iter([]), iter(I), iter(S))['expected_cells'], 2)
    def test_malformed_row(self):
        with self.assertRaisesRegex(ValueError, 'three fields'):
            admitted_audit([('ABC', 'XNAS')], I, S)
    def test_malformed_interval(self):
        with self.assertRaisesRegex(ValueError, 'four fields'):
            admitted_audit([], [('ABC', 'XNAS', S[0])], S)
    def test_invalid_identifier_type(self):
        with self.assertRaisesRegex(ValueError, 'nonempty strings'):
            admitted_audit([(42, 'XNAS', S[1])], I, S)
    def test_duplicate_preserved(self):
        self.assertEqual(len(admitted_audit([('ABC','XNAS',S[1])]*2, I, S)['duplicates']), 1)
    def test_unverified_flags(self):
        r = admitted_audit([], I, S)
        self.assertFalse(r['source_authenticated'])
        self.assertFalse(r['causal_inference_authorized'])

if __name__ == '__main__': unittest.main()
