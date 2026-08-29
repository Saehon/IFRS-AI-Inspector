from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any, Dict, Iterable, List, Optional
import hashlib
import json
import re


class VerificationStatus(str, Enum):
    PASS = "PASS"
    REVIEW = "REVIEW"
    BLOCK = "BLOCK"


@dataclass
class EvidenceItem:
    evidence_id: str
    source_type: str
    source_uri: str
    excerpt: str
    authority: str = "unknown"
    retrieved_at: Optional[str] = None
    sha256: Optional[str] = None

    def normalize(self) -> "EvidenceItem":
        if not self.sha256:
            payload = f"{self.source_uri}|{self.excerpt}".encode("utf-8")
            self.sha256 = hashlib.sha256(payload).hexdigest()
        return self


@dataclass
class ClaimCheck:
    claim: str
    supported: bool
    evidence_ids: List[str]
    citation_present: bool
    risk: str
    reason: str


@dataclass
class VerificationReport:
    status: VerificationStatus
    evidence_coverage: float
    citation_coverage: float
    unsupported_claim_rate: float
    hallucination_risk: str
    materiality_risk: str
    human_gate_required: bool
    checks: List[ClaimCheck]
    exceptions: List[str]
    evidence_graph: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        payload = asdict(self)
        payload["status"] = self.status.value
        return payload


class EvidenceVerifier:
    """POMELO Phase 2 Verify & Evidence gate.

    This module is deliberately model-neutral. It evaluates whether an agent
    output is traceable to supplied evidence before that output can be used by
    downstream accounting, audit, IFRS, PCAOB, or forensic agents.
    """

    CLAIM_SPLIT = re.compile(r"(?<=[.!?])\s+")
    CITATION_PATTERN = re.compile(r"\[(?:EVID|EV|SRC)-?[A-Za-z0-9_.:-]+\]")

    def __init__(
        self,
        min_evidence_coverage: float = 0.80,
        min_citation_coverage: float = 0.80,
        max_unsupported_claim_rate: float = 0.20,
    ) -> None:
        self.min_evidence_coverage = min_evidence_coverage
        self.min_citation_coverage = min_citation_coverage
        self.max_unsupported_claim_rate = max_unsupported_claim_rate

    @staticmethod
    def _tokenize(text: str) -> set[str]:
        return {
            token.lower()
            for token in re.findall(r"[A-Za-z0-9%$€£._-]+", text)
            if len(token) > 2
        }

    @staticmethod
    def _material_claim(claim: str) -> bool:
        triggers = (
            "material", "misstatement", "fraud", "violation", "non-compliance",
            "impairment", "revenue", "liability", "asset", "control deficiency",
            "restatement", "going concern", "pcaob", "ifrs", "isa", "%", "$", "€", "£",
        )
        low = claim.lower()
        return any(t in low for t in triggers)

    def _support_score(self, claim: str, evidence: EvidenceItem) -> float:
        c = self._tokenize(claim)
        e = self._tokenize(evidence.excerpt)
        if not c:
            return 0.0
        return len(c & e) / max(1, len(c))

    def _match_evidence(self, claim: str, evidence: Iterable[EvidenceItem]) -> List[str]:
        matches: List[tuple[float, str]] = []
        for item in evidence:
            score = self._support_score(claim, item)
            if score >= 0.28:
                matches.append((score, item.evidence_id))
        matches.sort(reverse=True)
        return [evidence_id for _, evidence_id in matches[:3]]

    def verify(
        self,
        agent_output: str,
        evidence: List[EvidenceItem],
        context: Optional[Dict[str, Any]] = None,
    ) -> VerificationReport:
        context = context or {}
        normalized = [item.normalize() for item in evidence]
        claims = [c.strip() for c in self.CLAIM_SPLIT.split(agent_output.strip()) if c.strip()]

        checks: List[ClaimCheck] = []
        for claim in claims:
            matched = self._match_evidence(claim, normalized)
            citation_present = bool(self.CITATION_PATTERN.search(claim))
            supported = bool(matched)
            material = self._material_claim(claim)
            if supported and citation_present:
                risk = "LOW"
                reason = "Claim is evidence-linked and explicitly cited."
            elif supported:
                risk = "MEDIUM"
                reason = "Evidence match exists but explicit evidence citation is missing."
            elif material:
                risk = "HIGH"
                reason = "Material accounting/audit claim is unsupported by supplied evidence."
            else:
                risk = "MEDIUM"
                reason = "Claim is not supported by supplied evidence."
            checks.append(
                ClaimCheck(
                    claim=claim,
                    supported=supported,
                    evidence_ids=matched,
                    citation_present=citation_present,
                    risk=risk,
                    reason=reason,
                )
            )

        total = max(1, len(checks))
        supported_count = sum(1 for c in checks if c.supported)
        cited_count = sum(1 for c in checks if c.citation_present)
        unsupported_rate = 1 - (supported_count / total)
        evidence_coverage = supported_count / total
        citation_coverage = cited_count / total

        material_exceptions = [c for c in checks if c.risk == "HIGH"]
        exceptions: List[str] = []
        if evidence_coverage < self.min_evidence_coverage:
            exceptions.append("Evidence coverage below policy threshold.")
        if citation_coverage < self.min_citation_coverage:
            exceptions.append("Citation coverage below policy threshold.")
        if unsupported_rate > self.max_unsupported_claim_rate:
            exceptions.append("Unsupported-claim rate above policy threshold.")
        if material_exceptions:
            exceptions.append("One or more material claims lack evidence support.")

        if material_exceptions or unsupported_rate > 0.40:
            status = VerificationStatus.BLOCK
        elif exceptions:
            status = VerificationStatus.REVIEW
        else:
            status = VerificationStatus.PASS

        human_gate_required = status != VerificationStatus.PASS or bool(context.get("force_human_gate"))
        hallucination_risk = "HIGH" if status == VerificationStatus.BLOCK else "MEDIUM" if status == VerificationStatus.REVIEW else "LOW"
        materiality_risk = "HIGH" if material_exceptions else "MEDIUM" if any(self._material_claim(c.claim) for c in checks) else "LOW"

        nodes = [
            {
                "id": item.evidence_id,
                "type": "evidence",
                "source_type": item.source_type,
                "source_uri": item.source_uri,
                "authority": item.authority,
                "sha256": item.sha256,
            }
            for item in normalized
        ]
        edges: List[Dict[str, str]] = []
        for idx, check in enumerate(checks, start=1):
            claim_id = f"CLAIM-{idx:03d}"
            nodes.append({"id": claim_id, "type": "claim", "text": check.claim, "risk": check.risk})
            for evidence_id in check.evidence_ids:
                edges.append({"from": evidence_id, "to": claim_id, "relation": "SUPPORTS"})

        return VerificationReport(
            status=status,
            evidence_coverage=round(evidence_coverage, 4),
            citation_coverage=round(citation_coverage, 4),
            unsupported_claim_rate=round(unsupported_rate, 4),
            hallucination_risk=hallucination_risk,
            materiality_risk=materiality_risk,
            human_gate_required=human_gate_required,
            checks=checks,
            exceptions=exceptions,
            evidence_graph={"nodes": nodes, "edges": edges},
        )


def verify_agent_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    verifier = EvidenceVerifier()
    evidence = [EvidenceItem(**item) for item in payload.get("evidence", [])]
    report = verifier.verify(
        agent_output=payload.get("agent_output", ""),
        evidence=evidence,
        context=payload.get("context", {}),
    )
    return report.to_dict()


if __name__ == "__main__":
    sample = {
        "agent_output": "Revenue recognition appears inconsistent with the contract evidence [EVID-001].",
        "evidence": [
            {
                "evidence_id": "EVID-001",
                "source_type": "filing",
                "source_uri": "local://sample",
                "excerpt": "Revenue recognition is based on transfer of control under the customer contract.",
                "authority": "issuer filing",
            }
        ],
    }
    print(json.dumps(verify_agent_payload(sample), indent=2))
