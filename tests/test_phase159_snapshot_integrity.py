"""Phase 159: fail-closed Nasdaq snapshot join integrity checks.
Synthetic fixtures only; run: python -m unittest -v tests/test_phase159_snapshot_integrity.py
"""
import unittest

ALLOWED = {1, 10, 40, 100}

def validate_snapshot(rows):
    result = {}
    for symbol, lot in rows:
        if not isinstance(symbol, str) or not symbol.strip() or symbol != symbol.strip():
            raise ValueError("missing/noncanonical symbol")
        if type(lot) is not int or lot not in ALLOWED:
            raise ValueError("invalid round-lot size")
        if symbol in result:
            raise ValueError("duplicate symbol, including conflicting duplicate")
        result[symbol] = lot
    return result

def stable_cohort(oct_rows, nov_rows):
    october = validate_snapshot(oct_rows)
    november = validate_snapshot(nov_rows)
    return {s: lot < 100 for s, lot in october.items()
            if s in november and lot == november[s]}

class SnapshotIntegrity(unittest.TestCase):
    def test_stable_treatment(self):
        self.assertEqual(stable_cohort([("A", 40), ("B", 100), ("C", 10)],
                                       [("A", 40), ("B", 100), ("C", 100)]),
                         {"A": True, "B": False})
    def test_duplicate_identical_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate"):
            stable_cohort([("A", 40), ("A", 40)], [("A", 40)])
    def test_duplicate_conflicting_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate"):
            stable_cohort([("A", 40), ("A", 100)], [("A", 40)])
    def test_duplicate_november_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate"):
            stable_cohort([("A", 40)], [("A", 40), ("A", 40)])
    def test_invalid_lot_rejected(self):
        for lot in [0, 50, None, "40", True]:
            with self.subTest(lot=lot), self.assertRaises(ValueError):
                validate_snapshot([("A", lot)])
    def test_invalid_symbol_rejected(self):
        for symbol in ["", None, " A", "A "]:
            with self.subTest(symbol=symbol), self.assertRaises(ValueError):
                validate_snapshot([(symbol, 40)])
    def test_does_not_impute_missing(self):
        self.assertEqual(stable_cohort([("A", 40)], [("B", 40)]), {})
    def test_disagreement_excluded_not_recoded(self):
        self.assertEqual(stable_cohort([("A", 10)], [("A", 100)]), {})

if __name__ == "__main__":
    unittest.main()
