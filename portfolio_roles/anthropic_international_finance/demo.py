"""Cross-functional entity setup gate; not a legal or tax opinion."""
import json

WORKSTREAMS = ("accounting", "tax", "treasury", "payroll", "finance_systems", "legal")

def review_entity_launch(record):
    blockers = []
    for key in ("entity_id", "country", "program_owner", "launch_date", "risk_register_id"):
        if not record.get(key):
            blockers.append("missing_" + key)
    signoffs = record.get("workstream_signoffs") or {}
    for key in WORKSTREAMS:
        if signoffs.get(key) is not True:
            blockers.append("unsigned_" + key)
    if record.get("critical_dependency_open") is not False:
        blockers.append("critical_dependency_unresolved")
    if record.get("human_final_approval") is True:
        blockers.append("demo_cannot_authorize_real_entity")
    return {"entity_id": record.get("entity_id"), "state": "READY_FOR_MANAGEMENT_REVIEW"
            if not blockers else "LAUNCH_HOLD", "blockers": sorted(set(blockers))}

if __name__ == "__main__":
    sample = {"entity_id": "SYN-IE-01", "country": "Ireland", "program_owner": "finance_pm",
              "launch_date": "2026-12-01", "risk_register_id": "SYN-RISK-01",
              "workstream_signoffs": {w: True for w in WORKSTREAMS},
              "critical_dependency_open": False, "human_final_approval": False}
    print(json.dumps(review_entity_launch(sample), indent=2))
