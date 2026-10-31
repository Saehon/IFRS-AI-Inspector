# Evidence Passport — Accounting and AI Assurance Research

**Executable synthetic research demonstration, Python 3.11 standard library.** This code validates provenance metadata for a claimed financial-statement assertion. It does **not** evaluate the substance of an audit, confirm IFRS treatment, attest actual human sign-off, or issue any assurance opinion.

## Reproduce

```bash
python -m research_tools.evidence_passport --out reports/synthetic_evidence_passport.json
python -m unittest discover -s research_tools/tests -p 'test_*.py' -v
```

The fixture is a fully hand-written **synthetic inventory discrepancy** with one synthetic source file. It is deliberately **BLOCKED** because the variance remains unresolved and human approval is absent. In this example, a blocked result demonstrates fail-closed metadata validation, *not discovery of an actual misstatement*.

## Validation dimensions

- **Source provenance:** source file SHA-256 must match the declared digest; IDs must be unique; file paths must remain in the fixture directory.
- **Legal rights:** sample accepts original synthetic material only; no copyrighted IFRS text or client records are included.
- **Temporal integrity:** a source effective after the reporting date triggers a `LOOK_AHEAD_EVIDENCE` issue.
- **Support mapping:** supporting source IDs must be registered and should not be duplicated.
- **Contradiction handling:** unresolved disagreements prevent approval.
- **Human gate:** missing reviewer approval or a reviewer identical to the preparer prevents approval.
- **Claim boundary:** even `METADATA_PASSED` never implies true evidence sufficiency, independent review, regulatory compliance or authorization to deploy.

The script validates declaration formats, file integrity and explicit conflicts. It does **not** validate the truth of an assertion, resolve differences between accounting methods, or authenticate a reviewer or file source.

## Scientific evaluation standards

This is a domain-specific implementation of a verification layer complementary to [the IFRS-AI Inspector research evaluation card](../RESEARCH_EVALUATION_CARD.md), [the NAAIL evidence-grounded financial AI evaluator](https://github.com/Saehon/Saeid-Homayoun/tree/main/research/ai_evidence_evaluation), and documented evaluation methodology from OpenAI, Anthropic, Google and the UK AI Security Institute.

**No LLM services are called. No actual corporate data, restricted accounting standards or confidential POMELO artifacts are distributed.**
