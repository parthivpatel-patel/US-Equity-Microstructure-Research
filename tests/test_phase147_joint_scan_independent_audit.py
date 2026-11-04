"""Independent Phase 146 numerical audit; synthetic fixtures only."""
import importlib.util
from pathlib import Path
import numpy as np

def reference_scan(y, window):
    changes = []
    for boundary in range(window, len(y) - window + 1):
        left = np.polyfit(np.arange(window), y[boundary-window:boundary], 1)[0]
        right = np.polyfit(np.arange(window), y[boundary:boundary+window], 1)[0]
        changes.append(right - left)
    return np.array(changes)

def test():
    spec = importlib.util.spec_from_file_location(
        "phase146", Path(__file__).with_name("test_phase146_joint_scan.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rng = np.random.default_rng(147)
    count = 0
    for length in (40, 41, 65, 87):
        for window in (3, 5, 10, 20):
            if length < 2 * window:
                continue
            for _ in range(25):
                y = rng.normal(size=length) + .12 * np.arange(length)
                np.testing.assert_allclose(module.scan(y, window),
                                           reference_scan(y, window), atol=1e-12)
                count += 1
    assert count == 400
    gi, ti = module.joint_indices(9, 87, 5, np.random.default_rng(147))
    assert len(gi) == 9 and len(ti) == 87
    for start in range(0, 87, 5):
        segment = ti[start:start+5]
        np.testing.assert_array_equal(segment,
                                      (segment[0] + np.arange(len(segment))) % 87)
    x = np.arange(87)
    panel = np.stack([i + (.01*i)*x for i in range(1, 10)])
    observed, null, p = module.simulate(panel, block=5, draws=50, seed=147)
    assert abs(observed) < 1e-12 and np.max(np.abs(null)) < 1e-12
    assert 1/51 <= p <= 1
    with np.errstate(divide="ignore", invalid="ignore"):
        bad_observed, bad_null, _ = module.simulate(panel, window=1, draws=5)
    assert np.isnan(bad_observed) and np.isnan(bad_null).all()
    print("PASS: 400 independent comparisons, calendar blocks, linear null")
    print("KNOWN BUG: window=1 silently returns nonfinite statistics")

if __name__ == "__main__":
    test()
