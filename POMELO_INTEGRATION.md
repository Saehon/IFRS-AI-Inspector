# POMELO Integration Contract

This repository is the IFRS specialist service for the IFRS HuggingFace / POMELO platform.

## Parent orchestration
`Saehon/pomelo-core/orchestration/ifrs-huggingface/`

## Required inputs
- Evidence Passport IDs
- jurisdiction and reporting period
- IFRS standard/paragraph scope
- entity/context metadata
- run manifest

## Required outputs
- finding_id
- assertion_or_question
- governing_source
- evidence_ids
- analysis_summary
- confidence
- severity
- counter_evidence
- human_decision_required
- remediation
- benchmark_trace

## Non-negotiable controls
No finding without source + evidence + trace. Effective dates must be explicit. Ambiguous or conflicting authoritative sources must be escalated rather than silently resolved.

## Release gate
Evidence -> reproducibility -> benchmark -> Blind Gold -> risk review -> human approval -> production.
