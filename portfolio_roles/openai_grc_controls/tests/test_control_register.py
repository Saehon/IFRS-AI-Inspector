import unittest
from portfolio_roles.openai_grc_controls.control_register import evaluate_register

class TestControlRegister(unittest.TestCase):
    def setUp(self):
        self.controls = [{"control_id": "SYN-C", "intent": "access review", "system": "sandbox",
                          "environment": "test", "owner": "IT", "risk_id": "SYN-R",
                          "framework_tags": ["SYN-ISO", "SYN-SOC2"]}]
        self.evidence = [{"evidence_id": "SYN-E", "control_id": "SYN-C",
                          "source_id": "synthetic-log", "owner": "IT",
                          "environment": "test", "captured_at": "2026-10-31", "result": "pass"}]
    def test_packet_ready_not_certified(self):
        x = evaluate_register(self.controls, self.evidence)
        self.assertEqual(x["status"], "REVIEW_PACKET_READY")
        self.assertFalse(x["human_certification"])
    def test_stale_environment_blocks(self):
        self.evidence[0]["environment"] = "prod"
        self.assertIn("SYN-E_environment_mismatch", evaluate_register(self.controls,self.evidence)["issues"])
    def test_framework_tag_not_approved_blocks(self):
        self.controls[0]["framework_tags"] = ["SOC2-REAL"]
        self.assertEqual(evaluate_register(self.controls,self.evidence)["status"], "BLOCKED")
    def test_missing_evidence_blocks(self):
        self.assertIn("SYN-C_no_evidence", evaluate_register(self.controls,[])["issues"])

if __name__ == "__main__":
    unittest.main()
