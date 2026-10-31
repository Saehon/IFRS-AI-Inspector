"""Offline Evidence Passport metadata gates for accounting research.

This verifies an explicitly synthetic evidence packet; it never decides
accounting standards compliance or substitutes an external professional audit.
"""
from __future__ import annotations

import argparse
from datetime import date, datetime
import hashlib
import json
from pathlib import Path
import re


SHA = re.compile(r"^[0-9a-f]{64}$")
ASSERTIONS = {"existence", "completeness", "valuation", "rights", "presentation"}
RIGHTS = "original_synthetic_data"


def text(obj, key):
    val = obj.get(key)
    if not isinstance(val, str) or not val.strip():
        raise ValueError(f"missing {key}")
    if len(val) > 500:
        raise ValueError(f"{key} too long")
    return val


def day(val):
    if not isinstance(val, str) or len(val) != 10:
        raise ValueError("expected YYYY-MM-DD")
    try:
        return date.fromisoformat(val)
    except ValueError as exc:
        raise ValueError("invalid accounting date") from exc


def timestamp(val):
    if not isinstance(val, str) or not val.endswith("Z"):
        raise ValueError("timestamp must be UTC/Z")
    try:
        stamp = datetime.fromisoformat(val.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("invalid timestamp") from exc
    if stamp.utcoffset().total_seconds() != 0:
        raise ValueError("timestamp not UTC")
    return stamp


def local_path(root, relative):
    val = text({"path": relative}, "path")
    p = Path(val)
    if p.is_absolute():
        raise ValueError("absolute evidence paths are forbidden")
    loc = (Path(root) / p).resolve()
    if not loc.is_relative_to(Path(root).resolve()):
        raise ValueError("evidence path traversal")
    if not loc.is_file():
        raise ValueError("missing evidence file")
    if loc.stat().st_size > 100_000:
        raise ValueError("synthetic evidence file exceeds permitted size")
    return loc


def validate(packet, root):
    if not isinstance(packet, dict) or packet.get("schema_version") != "1.0":
        raise ValueError("invalid evidence passport schema")
    if packet.get("case_class") != "synthetic":
        raise ValueError("public demonstration accepts synthetic cases only")
    assertion_id = text(packet, "assertion_id")
    text(packet, "account")
    text(packet, "claim")
    prepared = text(packet, "prepared_by")
    if packet.get("assertion_type") not in ASSERTIONS:
        raise ValueError("unknown financial statement assertion")
    period = day(packet.get("reporting_date"))
    evidence = packet.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        raise ValueError("missing evidence records")
    if len(evidence) > 25:
        raise ValueError("excessive evidence records")
    seen, issues, receipts = set(), [], []
    for item in evidence:
        if not isinstance(item, dict):
            raise ValueError("evidence record must be an object")
        ident = text(item, "evidence_id")
        if ident in seen:
            raise ValueError("duplicate evidence ID")
        seen.add(ident)
        path = local_path(root, item.get("file"))
        declared_hash = text(item, "sha256")
        if not SHA.fullmatch(declared_hash):
            raise ValueError("invalid evidence SHA-256")
        actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        if declared_hash != actual_hash:
            issues.append("EVIDENCE_HASH_MISMATCH:" + ident)
        if item.get("source_rights") != RIGHTS:
            issues.append("SOURCE_RIGHTS_NOT_PERMITTED:" + ident)
        if day(item.get("effective_as_of")) > period:
            issues.append("LOOK_AHEAD_EVIDENCE:" + ident)
        timestamp(item.get("captured_at_utc"))
        receipts.append({"evidence_id": ident, "file_sha256_matches": declared_hash == actual_hash})
    cited = packet.get("supports_claim_with")
    if not isinstance(cited, list) or not cited or any(not isinstance(x, str) for x in cited):
        raise ValueError("missing claim evidence references")
    if not set(cited).issubset(seen):
        issues.append("UNREGISTERED_CLAIM_EVIDENCE")
    if len(set(cited)) != len(cited):
        issues.append("DUPLICATE_CLAIM_CITATION")
    conflicts = packet.get("unresolved_contradictions", [])
    if not isinstance(conflicts, list) or any(not isinstance(x, str) for x in conflicts):
        raise ValueError("invalid contradictions")
    if conflicts:
        issues.append("CONTRADICTORY_EVIDENCE_REQUIRES_REVIEW")
    reviewer = packet.get("reviewer")
    if reviewer is None or reviewer.get("decision") != "approve":
        issues.append("NO_DECLARED_HUMAN_APPROVAL")
    else:
        reviewed_by = text(reviewer, "reviewed_by")
        timestamp(reviewer.get("reviewed_at_utc"))
        if reviewed_by == prepared:
            issues.append("REVIEWER_NOT_INDEPENDENT_OF_PREPARER")
    return {
        "assertion_id": assertion_id,
        "evaluation_scope": "SYNTHETIC_EVIDENCE_METADATA_ONLY",
        "evidence_count": len(evidence),
        "evidence_file_receipts": receipts,
        "gate": "METADATA_PASSED" if not issues else "BLOCKED",
        "issue_codes": sorted(set(issues)),
        "human_review_identity_independently_verified": False,
        "financial_assertion_substantively_verified": False,
        "ifrs_compliance_certified": False,
        "audit_opinion_issued": False,
        "limitation": (
            "Metadata checks do not establish accounting evidence sufficiency, "
            "substantive truth, professional authorization or standard compliance."
        ),
    }


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--passport", default=str(here / "examples" / "synthetic_passport.json"))
    parser.add_argument("--out")
    args = parser.parse_args()
    source = Path(args.passport).resolve()
    data = json.loads(source.read_text(encoding="utf-8"))
    result = validate(data, source.parent)
    rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        p = Path(args.out)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(rendered, encoding="utf-8")
        print("Evidence passport metadata report:", p)
    else:
        print(rendered)


if __name__ == "__main__":
    main()
