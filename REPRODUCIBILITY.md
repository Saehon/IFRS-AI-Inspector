# IFRS-AI Inspector Reproducibility Contract

IFRS-AI Inspector treats reproducibility as a prerequisite for stronger scientific claims. A generated explanation, agent trace, or one-off notebook result is not sufficient evidence of a reproducible accounting or assurance result.

## Current maturity

The repository is a **Research Prototype**. Architecture and research workflows are more mature than the software packaging, and no claim of production deployment, regulator approval, or professional certification is made.

## Minimum run record

For each material experiment or benchmark, preserve where applicable:

- Git commit SHA;
- research question and treatment definition;
- source/standards evidence version and provenance;
- model/provider/model-version identifier;
- prompt, policy, agent, and configuration version;
- deterministic calculation/rule-engine version;
- dataset or filing identifiers and acquisition date;
- transformations, chunking, retrieval, and exclusion rules;
- random seeds or sampling configuration;
- benchmark/gold definition and leakage controls;
- evaluation rubric and metrics;
- raw or governed output references;
- contradiction/failure records;
- human-review status and final release decision.

## Environment status

There is currently no root `requirements.txt` or `pyproject.toml` that fully freezes the software environment for this repository. Therefore the repository should **not** be described as environment-reproducible end to end until dependencies are explicitly inventoried and pinned.

Future executable releases should add a documented environment manifest and automated tests.

## Evidence separation

Keep the following evidence classes distinct:

1. authoritative or licensed accounting/auditing standards and interpretations;
2. public regulatory or enforcement materials;
3. public company filings and XBRL/iXBRL evidence;
4. peer-reviewed academic research;
5. working papers/preprints;
6. synthetic/digital-twin evidence;
7. model-generated interpretations or labels.

Model output, academic literature, or synthetic evidence does not become authoritative IFRS guidance merely because it is retrieved through RAG or processed by multiple agents.

## Restricted content

Do not commit licensed IFRS/IAS/ISA or other restricted standards text unless redistribution is expressly permitted. Reproducibility may instead use:

- source identifiers and version metadata;
- paragraph/reference identifiers where permitted;
- hashes;
- retrieval manifests;
- user-supplied/licensed local corpora;
- synthetic examples.

## Validation expectation

A stronger result should be recoverable from a frozen commit and governed inputs and should include, where appropriate:

**evidence retrieval → deterministic checks → agent/model reasoning → evaluation → adversarial review → robustness → human review**.

Passing software tests alone does not establish accounting correctness or professional assurance validity.
