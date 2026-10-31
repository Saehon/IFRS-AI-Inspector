import unittest
from portfolio_roles.anthropic_international_finance.demo import review_entity_launch, WORKSTREAMS

class TestInternationalFinance(unittest.TestCase):
    def setUp(self):
        self.case = {"entity_id": "E", "country": "IE", "program_owner": "p",
                     "launch_date": "2026-12-01", "risk_register_id": "SYN-R",
                     "workstream_signoffs": {k: True for k in WORKSTREAMS},
                     "critical_dependency_open": False, "human_final_approval": False}
    def test_complete_packet_ready_for_review(self):
        self.assertEqual(review_entity_launch(self.case)["state"], "READY_FOR_MANAGEMENT_REVIEW")
    def test_missing_tax_signoff_blocks(self):
        self.case["workstream_signoffs"]["tax"] = False
        self.assertIn("unsigned_tax", review_entity_launch(self.case)["blockers"])
    def test_open_dependency_blocks(self):
        self.case["critical_dependency_open"] = True
        self.assertEqual(review_entity_launch(self.case)["state"], "LAUNCH_HOLD")
    def test_missing_risk_register_blocks(self):
        self.case["risk_register_id"] = ""
        self.assertIn("missing_risk_register_id", review_entity_launch(self.case)["blockers"])

if __name__ == "__main__":
    unittest.main()
