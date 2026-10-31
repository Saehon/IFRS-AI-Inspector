"""Versioned, synthetic control-to-framework mapping with evidence scoping.

No proprietary standards text and no assertion of actual compliance.
"""
from __future__ import annotations
import hashlib
import json

def evaluate_register(register, evidence):
    issues = []
    identifiers = set()
    mapped = set()
    for control in register:
        cid = control.get("control_id")
        if not cid or cid in identifiers:
            issues.append("missing_or_duplicate_control_id")
        identifiers.add(cid)
        for required in ("intent", "system", "environment", "owner", "risk_id"):
            if not control.get(required):
                issues.append(f"{cid}_missing_{required}")
        frameworks = control.get("framework_tags") or []
        if not frameworks:
            issues.append(f"{cid}_unmapped")
        for fw in frameworks:
            if not isinstance(fw, str) or not fw.startswith("SYN-"):
                issues.append(f"{cid}_unreviewed_framework_tag")
            mapped.add(fw)
    evidence_ids = set()
    for row in evidence:
        eid = row.get("evidence_id")
        if not eid or eid in evidence_ids:
            issues.append("missing_or_duplicate_evidence_id")
        evidence_ids.add(eid)
        cid = row.get("control_id")
        if cid not in identifiers:
            issues.append(f"{eid}_orphan_evidence")
        if row.get("environment") != next((r["environment"] for r in register if r.get("control_id") == cid), None):
            issues.append(f"{eid}_environment_mismatch")
        if row.get("result") not in ("pass", "fail"):
            issues.append(f"{eid}_invalid_result")
        if not row.get("owner") or not row.get("captured_at") or not row.get("source_id"):
            issues.append(f"{eid}_untraceable")
        if row.get("result") == "fail":
            issues.append(f"{eid}_failing_test")
    for cid in identifiers:
        if cid and not any(e.get("control_id") == cid for e in evidence):
            issues.append(f"{cid}_no_evidence")
    return {"control_count": len(register), "evidence_count": len(evidence),
            "framework_tag_count": len(mapped), "status": "REVIEW_PACKET_READY" if not issues else "BLOCKED",
            "issues": sorted(set(issues)), "human_certification": False}

if __name__ == "__main__":
    control = [{"control_id": "SYN-ACCESS-01", "intent": "review temporary privileged access",
                "system": "synthetic-idp", "environment": "sandbox", "owner": "IT",
                "risk_id": "SYN-R1", "framework_tags": ["SYN-SOC2-ACCESS", "SYN-ISO-ACCESS"]}]
    evidence = [{"evidence_id": "SYN-E1", "control_id": "SYN-ACCESS-01", "source_id": "sandbox-log",
                 "owner": "IT", "environment": "sandbox", "captured_at": "2026-10-31T00:00:00Z",
                 "result": "pass"}]
    print(json.dumps(evaluate_register(control, evidence), indent=2))
