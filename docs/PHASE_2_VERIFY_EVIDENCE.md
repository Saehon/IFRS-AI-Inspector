# Phase 2 — Verify & Evidence

## Objective
Phase 2 turns the IFRS-AI-Inspector into an evidence-gated accounting and audit system. No agent conclusion is trusted merely because a model produced it. Every material claim must be linked to traceable evidence, checked for citation coverage, assessed for hallucination/materiality risk, and routed through a Human Gate when policy requires it.

## Position in the POMELO architecture

Phase 1 — Knowledge Engine  
→ **Phase 2 — Verify & Evidence**  
→ Phase 3 — Eval & Benchmark  
→ Agent/Dataset Hub  
→ Co-Scientist & Evolution  
→ Enterprise / Marketplace / Global Ecosystem

Phase 2 is model-neutral and therefore works with LLMs, SLMs, deterministic tools, retrieval systems, or external agents.

## Phase 2 pipeline

1. Agent produces a candidate output.
2. Evidence objects are normalized and hashed with SHA-256.
3. Output is segmented into claims.
4. Each claim is matched against supplied evidence.
5. Explicit Evidence IDs/citations are checked.
6. Unsupported claims are detected.
7. Material accounting/audit claims receive elevated risk treatment.
8. An EvidenceGraph is produced linking evidence nodes to claim nodes.
9. Policy thresholds generate PASS, REVIEW, or BLOCK.
10. REVIEW/BLOCK invokes the Human Gate.
11. Only PASS output may flow downstream automatically.

## Required evidence object

```json
{
  "evidence_id": "EVID-001",
  "source_type": "filing|contract|xbrl|audit_workpaper|standard|regulator|dataset",
  "source_uri": "https://... or internal://...",
  "excerpt": "verifiable evidence text",
  "authority": "IASB|PCAOB|SEC|issuer|auditor|other",
  "retrieved_at": "ISO-8601 timestamp",
  "sha256": "computed automatically when absent"
}
```

## Verification output

The verifier returns:

- `status`: PASS / REVIEW / BLOCK
- `evidence_coverage`
- `citation_coverage`
- `unsupported_claim_rate`
- `hallucination_risk`
- `materiality_risk`
- `human_gate_required`
- claim-level checks and reasons
- exception log
- EvidenceGraph nodes and SUPPORTS edges

## Gate rules

### PASS
Evidence and citation thresholds are met, unsupported-claim rate is within tolerance, and there are no unsupported material conclusions. Downstream automation is allowed.

### REVIEW
Evidence may exist but citations or coverage are incomplete. Output is held for professional review.

### BLOCK
A material claim is unsupported or the unsupported-claim rate is severe. Output cannot reach downstream decision agents without a human override.

## Accounting and audit safety rule

Phase 2 must never infer that a model-generated statement is authoritative simply because it is fluent. Professional conclusions concerning material misstatement, fraud, IFRS/ISA/PCAOB compliance, restatement, going concern, control deficiencies, or quantitative impacts require evidence support and appropriate human review.

## Management panel contract

The management panel should expose the following Phase 2 fields:

- verification status
- evidence coverage %
- citation coverage %
- unsupported claim %
- hallucination risk
- materiality risk
- exception count
- Human Gate state
- EvidenceGraph link/view
- run/report identifier

Recommended route: `/phases/2/verify-evidence`.

## Phase 2 Definition of Done

Phase 2 is complete when:

- evidence intake schema exists;
- SHA-256 provenance hashing exists;
- claim-level support checking exists;
- citation checking exists;
- unsupported-claim/hallucination controls exist;
- materiality-sensitive risk logic exists;
- EvidenceGraph output exists;
- PASS/REVIEW/BLOCK policy exists;
- Human Gate behavior exists;
- unit tests cover pass, review, block, and graph linkage;
- the agent orchestrator can invoke the verifier before downstream routing;
- Phase 3 can consume the Phase 2 report as benchmark input.

## Phase 3 hand-off metrics

Phase 3 should benchmark at minimum:

- Evidence Coverage
- Citation Coverage
- Unsupported Claim Rate
- Material Unsupported Claim Rate
- Hallucination Risk distribution
- Human Review Rate
- False-PASS rate
- False-BLOCK rate
- Agent Alone vs Agent + POMELO delta

These become part of POMELO Eval and ΔPOMELO.
