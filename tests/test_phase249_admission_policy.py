"""Synthetic admission-policy regression tests; no market observations."""
import unittest
from phase249_admission_policy import historical_estimation_allowed as allowed

class AdmissionTests(unittest.TestCase):
    def test_digest_alone_insufficient(self):
        self.assertFalse(allowed(True, False, False, False, False))

    def test_each_missing_attestation_rejects(self):
        for i in range(5):
            values = [True] * 5
            values[i] = False
            self.assertFalse(allowed(*values))

    def test_all_verified_passes_policy_only(self):
        self.assertTrue(allowed(True, True, True, True, True))

    def test_non_boolean_rejected(self):
        with self.assertRaises(TypeError):
            allowed(True, "yes", True, True, True)

if __name__ == "__main__":
    unittest.main()
