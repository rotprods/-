import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("render_budget_estimator", ROOT / "tools" / "render_budget_estimator.py")
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


class RenderBudgetTests(unittest.TestCase):
    def test_weighting(self):
        r = MOD.estimate(20, 30, 8, 14, 30, workers=4, parallel_efficiency=.85, device_hour_rate=1.8)
        self.assertEqual(r["frames"], 600)
        self.assertAlmostEqual(r["benchmark_seconds_per_frame"]["expected_weighted"], 16.0)
        self.assertAlmostEqual(r["compute"]["single_device_equivalent_hours"], 8 / 3)
        self.assertAlmostEqual(r["cost"]["render_compute"], 4.8)

    def test_workers_reduce_wall_not_total_compute(self):
        a = MOD.estimate(10, 24, 5, 10, 20, workers=1, parallel_efficiency=1)
        b = MOD.estimate(10, 24, 5, 10, 20, workers=8, parallel_efficiency=1)
        self.assertAlmostEqual(a["compute"]["single_device_equivalent_hours"], b["compute"]["single_device_equivalent_hours"])
        self.assertAlmostEqual(a["compute"]["estimated_wall_hours"] / 8, b["compute"]["estimated_wall_hours"])

    def test_fail_closed_inputs(self):
        with self.assertRaises(ValueError):
            MOD.estimate(0, 24, 1, 1, 1)
        with self.assertRaises(ValueError):
            MOD.estimate(1, 24, 1, 1, 1, workers=0)
        with self.assertRaises(ValueError):
            MOD.estimate(1, 24, 1, 1, 1, parallel_efficiency=1.5)


if __name__ == "__main__":
    unittest.main()
