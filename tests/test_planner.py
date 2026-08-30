import json
import unittest
from pathlib import Path

from migrationforge.planner import assess


ROOT = Path(__file__).parents[1]


class PlannerTests(unittest.TestCase):
    def setUp(self):
        self.estate = json.loads((ROOT / "examples/vmware-to-azure/250-vm-estate.json").read_text())

    def test_estate_totals(self):
        report = assess(self.estate)
        self.assertEqual(report["estate_summary"]["virtual_machines"], 250)
        self.assertEqual(report["estate_summary"]["applications"], 40)

    def test_latency_sensitive_factory_stays_on_prem(self):
        decisions = {item["group"]: item for item in assess(self.estate)["decisions"]}
        self.assertEqual(decisions["manufacturing-control"]["strategy"], "retain")
        self.assertEqual(decisions["manufacturing-control"]["status"], "blocked")

    def test_container_ready_apps_replatform(self):
        decisions = {item["group"]: item for item in assess(self.estate)["decisions"]}
        self.assertEqual(decisions["customer-portals"]["target"], "Azure Kubernetes Service")

    def test_dependency_waves_are_ordered(self):
        waves = assess(self.estate)["migration_waves"]
        positions = {name: wave["wave"] for wave in waves for name in wave["workloads"]}
        self.assertLess(positions["landing-zone"], positions["shared-services"])
        self.assertLess(positions["shared-services"], positions["order-processing"])

    def test_economics_are_explicit(self):
        economics = assess(self.estate)["economics"]
        self.assertEqual(economics["simple_payback_months"], 12.0)
        self.assertEqual(economics["modeled_outage_exposure_reduction_usd"], 150000.0)

    def test_never_auto_executes(self):
        self.assertFalse(assess(self.estate)["production_control"]["auto_execute"])

    def test_receipt_is_deterministic(self):
        self.assertEqual(assess(self.estate)["receipt_sha256"], assess(self.estate)["receipt_sha256"])

    def test_dependency_cycle_rejected(self):
        self.estate["dependencies"].append({"dependency": "order-processing", "workload": "landing-zone"})
        with self.assertRaises(ValueError):
            assess(self.estate)


if __name__ == "__main__":
    unittest.main()
