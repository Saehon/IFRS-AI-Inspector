import hashlib
import unittest
from portfolio_roles.openai_grc_controls.demo import check_control

class TestGRCControls(unittest.TestCase):
    def setUp(self):
        payload = "synthetic event"
        self.case = {"control_id": "C1", "framework": "demo", "environment": "test",
                     "owner": "u1", "reviewer": "u2",
                     "evidence": {"source_id": "E1", "captured_at": "2026-10-01T00:00:00Z",
                                  "payload": payload, "sha256": hashlib.sha256(payload.encode()).hexdigest(),
                                  "control_id": "C1", "test_result": "pass"}}

    def test_valid_record_ready_for_review(self):
        self.assertEqual(check_control(self.case)["status"], "READY_FOR_HUMAN_REVIEW")

    def test_tampered_evidence_blocks(self):
        self.case["evidence"]["payload"] = "altered"
        self.assertIn("evidence_integrity_mismatch", check_control(self.case)["failures"])

    def test_wrong_scope_blocks(self):
        self.case["evidence"]["control_id"] = "OTHER"
        self.assertEqual(check_control(self.case)["status"], "BLOCKED")

    def test_nonindependent_reviewer_blocks(self):
        self.case["reviewer"] = self.case["owner"]
        self.assertIn("nonindependent_review", check_control(self.case)["failures"])

if __name__ == "__main__":
    unittest.main()
