# IFRS-AI Inspector Data and Evidence Sources

IFRS-AI Inspector is designed around evidence-grounded research. This file defines the provenance and rights boundary for standards content, regulatory material, company filings, research literature, and synthetic/digital-twin data.

## Core provenance rule

For every material source, record where applicable:

- source/provider;
- title or dataset/filing identifier;
- jurisdiction;
- version/effective date or filing date;
- acquisition date;
- source URL or controlled-access reference;
- rights/licence/permission status;
- transformations/chunking/extraction steps;
- integrity/hash information where feasible;
- evidence class;
- limitations and human-review status.

## 1. Accounting, auditing and sustainability standards

The architecture may reference IFRS/IAS, ISA, ISSB, ESRS, COSO, PCAOB or other professional/regulatory frameworks.

These references do **not** grant permission to redistribute protected standards text. Where full text is licensed or user-supplied, it should remain in approved local/controlled storage unless redistribution rights are explicit.

Repository artifacts should prefer lawful metadata, citations, identifiers, schemas, mappings, and synthetic examples rather than copying restricted source text.

## 2. Public company and regulatory data

Potential research evidence includes public company filings and structured reporting data such as SEC EDGAR/XBRL or other legally accessible filing systems. Each study should freeze issuer/filing identifiers, retrieval dates, source versions, transformations, and exclusions.

Public accessibility does not automatically mean unrestricted redistribution or that a source constitutes authoritative IFRS interpretation.

## 3. Academic and technical research

Peer-reviewed papers, working papers, preprints, technical documentation, and public research repositories may support method design, benchmarking, or evaluation. They remain scholarly/technical evidence rather than authoritative standards unless they separately carry such authority.

## 4. Synthetic and digital-twin data

Synthetic examples are appropriate for public demonstrations and controlled testing when clearly labelled. Record:

- generation method;
- planted conditions/anomalies;
- parameters/seeds where relevant;
- intended assertions or expected outcomes;
- whether any real confidential information contributed to generation.

Synthetic benchmark performance must not be presented as real-world assurance effectiveness.

## 5. Model-generated evidence

LLM or agent outputs are generated artifacts, not source evidence. Preserve them separately from the documents/data they cite and retain traceability from each material claim back to the underlying source.

## 6. Restricted and confidential data

Do not commit:

- confidential client information;
- credentials/API keys;
- licensed standards text without redistribution permission;
- restricted commercial datasets;
- personally identifiable information without appropriate authorization and controls;
- Blind Gold or protected evaluation answers intended to remain secret.

Use manifests, hashes, schemas, controlled references, or synthetic substitutes where appropriate.

## Publication/release gate

Before publishing a dataset, example, benchmark, or result, verify provenance, rights, jurisdiction, transformation lineage, evidence class, and whether the disclosure is compatible with the repository's public research status and IP policy.
