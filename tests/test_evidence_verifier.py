import unittest

from src.evidence_verifier import EvidenceItem, EvidenceVerifier, VerificationStatus


class EvidenceVerifierTests(unittest.TestCase):
    def setUp(self):
        self.verifier = EvidenceVerifier()

    def test_supported_and_cited_claim_passes(self):
        output = "Revenue recognition is based on transfer of control under the customer contract [EVID-001]."
        evidence = [
            EvidenceItem(
                evidence_id="EVID-001",
                source_type="filing",
                source_uri="local://filing",
                excerpt="Revenue recognition is based on transfer of control under the customer contract.",
                authority="issuer filing",
            )
        ]
        report = self.verifier.verify(output, evidence)
        self.assertEqual(report.status, VerificationStatus.PASS)
        self.assertFalse(report.human_gate_required)
        self.assertEqual(report.evidence_coverage, 1.0)
        self.assertEqual(report.citation_coverage, 1.0)

    def test_material_unsupported_claim_blocks(self):
        output = "The company committed fraud and must restate revenue by $20 million."
        evidence = [
            EvidenceItem(
                evidence_id="EVID-002",
                source_type="filing",
                source_uri="local://filing",
                excerpt="The annual report describes revenue recognition policies.",
            )
        ]
        report = self.verifier.verify(output, evidence)
        self.assertEqual(report.status, VerificationStatus.BLOCK)
        self.assertTrue(report.human_gate_required)
        self.assertEqual(report.hallucination_risk, "HIGH")

    def test_supported_but_uncited_claim_requires_review(self):
        output = "Revenue recognition is based on transfer of control under the customer contract."
        evidence = [
            EvidenceItem(
                evidence_id="EVID-003",
                source_type="contract",
                source_uri="local://contract",
                excerpt="Revenue recognition is based on transfer of control under the customer contract.",
            )
        ]
        report = self.verifier.verify(output, evidence)
        self.assertEqual(report.status, VerificationStatus.REVIEW)
        self.assertTrue(report.human_gate_required)

    def test_graph_contains_claim_evidence_edge(self):
        output = "Lease liabilities are measured from contractual lease payments [EVID-004]."
        evidence = [
            EvidenceItem(
                evidence_id="EVID-004",
                source_type="contract",
                source_uri="local://lease",
                excerpt="Lease liabilities are measured from contractual lease payments.",
            )
        ]
        report = self.verifier.verify(output, evidence)
        self.assertTrue(any(edge["relation"] == "SUPPORTS" for edge in report.evidence_graph["edges"]))


if __name__ == "__main__":
    unittest.main()
