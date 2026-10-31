"""Evidence integrity demonstration; not a certified compliance audit."""
import hashlib
import json

def check_control(control):
    failures = []
    for field in ("control_id", "framework", "environment", "owner", "reviewer", "evidence"):
        if not control.get(field):
            failures.append("missing_" + field)
    if control.get("owner") and control.get("owner") == control.get("reviewer"):
        failures.append("nonindependent_review")
    evidence = control.get("evidence") or {}
    for field in ("source_id", "captured_at", "payload", "sha256", "control_id", "test_result"):
        if not evidence.get(field):
            failures.append("evidence_missing_" + field)
    if evidence.get("control_id") != control.get("control_id"):
        failures.append("evidence_control_mismatch")
    if "payload" in evidence and "sha256" in evidence:
        observed_hash = hashlib.sha256(str(evidence["payload"]).encode("utf-8")).hexdigest()
        if observed_hash != evidence["sha256"]:
            failures.append("evidence_integrity_mismatch")
    if evidence.get("test_result") != "pass":
        failures.append("control_test_not_passed")
    return {"control_id": control.get("control_id"), "status": "READY_FOR_HUMAN_REVIEW" if not failures else "BLOCKED",
            "failures": sorted(set(failures))}

if __name__ == "__main__":
    payload = "synthetic cloud-access-log: user reviewed"
    control = {"control_id": "SYN-ACCESS-01", "framework": "SOC2-demo", "environment": "sandbox",
               "owner": "alice", "reviewer": "bob",
               "evidence": {"source_id": "SYN-EVID-01", "captured_at": "2026-10-01T12:00:00Z",
                            "payload": payload, "sha256": hashlib.sha256(payload.encode()).hexdigest(),
                            "control_id": "SYN-ACCESS-01", "test_result": "pass"}}
    print(json.dumps(check_control(control), indent=2))
