"""Constructed-data regression checks only; no SEC observations."""
import hashlib
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from phase437_source_bound_gate import evaluate_bytes

HEADER = "date,security,exchange,match_group,treated,hidden_count,total_count\n"
def panel():
    return (HEADER + "".join(
        f"{d},{s},X,G,{a},1,10\n"
        for d in ("2025-10-30", "2025-11-04")
        for s, a in (("T", 1), ("C", 0))
    )).encode()

class SourceBoundTests(unittest.TestCase):
    def test_valid_common_support(self):
        raw = panel()
        result = evaluate_bytes(raw)
        self.assertTrue(result["pass"])
        self.assertEqual(result["source_sha256"], hashlib.sha256(raw).hexdigest())
        self.assertEqual(result["daily"]["source_sha256"], result["calendar"]["source_sha256"])
        self.assertFalse(result["historical_effect_estimated"])

    def test_same_size_mutation_changes_digest(self):
        first = evaluate_bytes(panel())
        second = evaluate_bytes(panel().replace(b",1,10\n", b",2,10\n"))
        self.assertEqual(first["source_bytes"], second["source_bytes"])
        self.assertNotEqual(first["source_sha256"], second["source_sha256"])

    def test_missing_post_fails(self):
        raw = (HEADER + "2025-10-30,T,X,G,1,1,10\n2025-10-30,C,X,G,0,1,10\n").encode()
        self.assertFalse(evaluate_bytes(raw)["pass"])

    def test_unpaired_fails(self):
        raw = (HEADER + "2025-10-30,T,X,G,1,1,10\n2025-10-30,C,X,G,0,1,10\n2025-11-04,T,X,G,1,1,10\n").encode()
        self.assertFalse(evaluate_bytes(raw)["pass"])

    def test_duplicate_rejected(self):
        with self.assertRaises(ValueError):
            evaluate_bytes(panel() + b"2025-11-04,T,X,G,1,1,10\n")

    def test_empty_rejected(self):
        with self.assertRaises(ValueError):
            evaluate_bytes(b"")

    def test_invalid_utf8_rejected(self):
        with self.assertRaises(ValueError):
            evaluate_bytes(b"\xff")

if __name__ == "__main__":
    unittest.main()
