"""Deterministic contract tests; downstream estimator intentionally stubbed."""
import importlib.util
import pathlib
import sys
import types
import unittest
from unittest.mock import Mock

HERE = pathlib.Path(__file__).resolve().parent.parent / 'scripts'

def load(name):
    spec = importlib.util.spec_from_file_location(name, HERE / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class WindowBridgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.guard = load('phase236_window_guard')

    def setUp(self):
        self.downstream = Mock(return_value={'estimate': 2.0, 'calendar_authenticated': True})
        sys.modules['phase236_window_guard'] = self.guard
        sys.modules['phase235_structural_preflight'] = types.SimpleNamespace(
            structurally_gated_matched_hac=self.downstream)
        self.bridge = load('phase237_window_integrated_preflight')
        self.kw = dict(calendar=['2025-09-02', '2025-09-03'],
                       source_url='https://example.org/calendar',
                       retrieved_at='2026-11-08T09:00:00+00:00',
                       raw_sha256='a'*64, source_authenticated=True)

    def tearDown(self):
        sys.modules.pop('phase235_structural_preflight', None)
        sys.modules.pop('phase236_window_guard', None)

    def run_bridge(self, sessions=None, early=None, late=None):
        return self.bridge.window_gated_matched_hac(
            [], [], sessions if sessions is not None else ['2025-09-02','2025-09-03'],
            [], early if early is not None else ['2025-09-02'],
            late if late is not None else ['2025-09-03'], 2, **self.kw)

    def test_valid_forwards_and_scrubs(self):
        out = self.run_bridge()
        self.assertEqual(out['estimate'], 2.0)
        self.assertTrue(out['window_contract_validated'])
        self.assertEqual((out['window_n_early'], out['window_n_late']), (1, 1))
        self.assertFalse(out['calendar_independently_verified'])
        self.assertNotIn('calendar_authenticated', out)
        self.downstream.assert_called_once()

    def test_empty_early_rejected_before_estimation(self):
        with self.assertRaises(ValueError): self.run_bridge(early=[])
        self.downstream.assert_not_called()

    def test_noncanonical_date_rejected_before_estimation(self):
        with self.assertRaises(ValueError): self.run_bridge(sessions=['2025-9-2','2025-09-03'])
        self.downstream.assert_not_called()

    def test_unsorted_rejected_before_estimation(self):
        with self.assertRaises(ValueError): self.run_bridge(sessions=['2025-09-03','2025-09-02'])
        self.downstream.assert_not_called()

    def test_absent_roster_date_rejected_before_estimation(self):
        with self.assertRaises(ValueError): self.run_bridge(late=['2025-09-04'], sessions=['2025-09-02','2025-09-04'])
        self.downstream.assert_not_called()

    def test_generator_rejected_before_estimation(self):
        with self.assertRaises(ValueError): self.run_bridge(sessions=iter(['2025-09-02','2025-09-03']))
        self.downstream.assert_not_called()

if __name__ == '__main__': unittest.main()
