import unittest
from phase333_pretrend_crosscheck import audit

class TestAudit(unittest.TestCase):
    def test_requires_both_outcomes(self):
        with self.assertRaises(StopIteration):
            audit([], [], [])
    def test_requires_complete_lags(self):
        with self.assertRaises(AssertionError):
            audit([{'outcome':'count'}], [], [])

if __name__ == '__main__':
    unittest.main()
