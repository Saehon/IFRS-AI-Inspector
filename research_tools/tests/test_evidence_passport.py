import copy
import hashlib
import json
from pathlib import Path
import unittest
from tempfile import TemporaryDirectory

from research_tools.evidence_passport import validate


ROOT = Path(__file__).resolve().parents[1] / "examples"
BASE = json.loads((ROOT / "synthetic_passport.json").read_text(encoding="utf-8"))


class EvidencePassportTests(unittest.TestCase):
    def test_fixture_fails_closed(self):
        result = validate(copy.deepcopy(BASE), ROOT)
        self.assertEqual(result["gate"], "BLOCKED")
        self.assertIn("NO_DECLARED_HUMAN_APPROVAL", result["issue_codes"])
        self.assertIn("CONTRADICTORY_EVIDENCE_REQUIRES_REVIEW", result["issue_codes"])

    def test_local_source_hash_is_valid(self):
        result = validate(copy.deepcopy(BASE), ROOT)
        self.assertTrue(result["evidence_file_receipts"][0]["file_sha256_matches"])

    def test_no_assurance_assertion_even_when_passed(self):
        record = copy.deepcopy(BASE)
        record["unresolved_contradictions"] = []
        record["reviewer"] = {"decision": "approve", "reviewed_by": "reviewer_B",
                              "reviewed_at_utc": "2026-01-15T00:00:00Z"}
        result = validate(record, ROOT)
        self.assertEqual(result["gate"], "METADATA_PASSED")
        self.assertFalse(result["ifrs_compliance_certified"])
        self.assertFalse(result["audit_opinion_issued"])
        self.assertFalse(result["human_review_identity_independently_verified"])

    def test_mismatched_hash_blocks(self):
        record = copy.deepcopy(BASE)
        record["evidence"][0]["sha256"] = "0" * 64
        result = validate(record, ROOT)
        self.assertIn("EVIDENCE_HASH_MISMATCH:SYN-SOURCE-COUNT-001", result["issue_codes"])

    def test_temporal_leakage_blocks(self):
        record = copy.deepcopy(BASE)
        record["evidence"][0]["effective_as_of"] = "2026-01-01"
        result = validate(record, ROOT)
        self.assertIn("LOOK_AHEAD_EVIDENCE:SYN-SOURCE-COUNT-001", result["issue_codes"])

    def test_license_not_assumed(self):
        record = copy.deepcopy(BASE)
        record["evidence"][0]["source_rights"] = "unknown"
        result = validate(record, ROOT)
        self.assertIn("SOURCE_RIGHTS_NOT_PERMITTED:SYN-SOURCE-COUNT-001", result["issue_codes"])

    def test_missing_source_registration_blocks(self):
        record = copy.deepcopy(BASE)
        record["supports_claim_with"] = ["UNKNOWN"]
        result = validate(record, ROOT)
        self.assertIn("UNREGISTERED_CLAIM_EVIDENCE", result["issue_codes"])

    def test_reused_citation_blocks(self):
        record = copy.deepcopy(BASE)
        record["supports_claim_with"] = ["SYN-SOURCE-COUNT-001"] * 2
        result = validate(record, ROOT)
        self.assertIn("DUPLICATE_CLAIM_CITATION", result["issue_codes"])

    def test_self_review_blocks(self):
        record = copy.deepcopy(BASE)
        record["unresolved_contradictions"] = []
        record["reviewer"] = {"decision":"approve", "reviewed_by":"synthetic_preparer_A",
                              "reviewed_at_utc":"2026-01-15T00:00:00Z"}
        self.assertIn("REVIEWER_NOT_INDEPENDENT_OF_PREPARER", validate(record, ROOT)["issue_codes"])

    def test_external_source_path_blocks(self):
        record = copy.deepcopy(BASE)
        record["evidence"][0]["file"] = "../README.md"
        with self.assertRaises(ValueError):
            validate(record, ROOT)

    def test_duplicate_evidence_id_blocks(self):
        record = copy.deepcopy(BASE)
        record["evidence"] *= 2
        with self.assertRaises(ValueError):
            validate(record, ROOT)

    def test_rejects_real_data_class_in_public_fixture(self):
        record = copy.deepcopy(BASE)
        record["case_class"] = "real_client"
        with self.assertRaises(ValueError):
            validate(record, ROOT)

    def test_required_assertion_rejected(self):
        record = copy.deepcopy(BASE)
        record["assertion_type"] = "fake_assurance"
        with self.assertRaises(ValueError):
            validate(record, ROOT)

    def test_review_time_requires_utc(self):
        record = copy.deepcopy(BASE)
        record["reviewer"] = {"decision":"approve", "reviewed_by":"reviewer_B",
                              "reviewed_at_utc":"2026-01-15T02:00:00+02:00"}
        with self.assertRaises(ValueError):
            validate(record, ROOT)

    def test_invalid_sha_length_blocks(self):
        record = copy.deepcopy(BASE)
        record["evidence"][0]["sha256"] = "abc"
        with self.assertRaises(ValueError):
            validate(record, ROOT)

    def test_empty_evidence_blocks(self):
        record = copy.deepcopy(BASE)
        record["evidence"] = []
        with self.assertRaises(ValueError):
            validate(record, ROOT)

    def test_unknown_reporting_date_blocks(self):
        record = copy.deepcopy(BASE)
        record["reporting_date"] = "not-a-date"
        with self.assertRaises(ValueError):
            validate(record, ROOT)

    def test_material_file_tampering_detected(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp)
            (path / "inventory_evidence.txt").write_text("tampered\n", encoding="utf-8")
            result = validate(copy.deepcopy(BASE), path)
            self.assertTrue(any("HASH_MISMATCH" in x for x in result["issue_codes"]))


if __name__ == "__main__":
    unittest.main()
