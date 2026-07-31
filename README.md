# IFRS-AI Inspector 🔍
**A Hybrid Multi-Agent Digital Twin Framework for Autonomous Continuous IFRS Assurance**

*Created by [Saeid Homayoun](https://github.com/Saehon), Senior Lecturer in Accounting at [University of Gävle, Sweden](https://www.hig.se/engelska/university-of-gavle/research/researchers/aue/saeid-homayoun) | [Google Scholar](https://scholar.google.com/citations?user=1PKckooAAAAJ&hl=en).*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Compliance: EU AI Act](https://img.shields.io/badge/Compliance-EU_AI_Act-green.svg)](#eu-ai-act-compliance)

## Abstract
This study proposes the **IFRS-AI Inspector**, a next-generation Hybrid Multi-Agent Digital Twin Framework designed for autonomous, continuous financial assurance. The framework integrates Google’s agentic orchestration principles (inspired by Co-Scientist and Antigravity) alongside MiroFlow hierarchical workflows, live shadow-ledger technology, and Retrieval-Augmented Generation (RAG). It provides standards-aware assurance across IFRS Accounting Standards, auditing requirements, and sustainability reporting frameworks.

To address the complexities of modern financial compliance and algorithmic transparency, the IFRS-AI Inspector is structured around a novel **Dual-Core Architecture**:
1. **Accounting & Audit Knowledge Graph Core**: The immutable foundation of the system. Based strictly on IFRS standards, this core represents the absolute accounting truths and rules. It does not change with technology upgrades.
2. **Technology Knowledge Graph Core**: The upgradable, intelligent engine of the system. This core utilizes a **Co-Scientist Inspired Multi-Agent** framework and leverages state-of-the-art AI models, such as the **Mango** foundation model published by Meta, ensuring the architecture can evolve with future AI breakthroughs.

## The Dual-Core Architecture

### 1. Accounting & Audit Knowledge Graph Core (Immutable)
This core introduces an **IFRS-as-Agent architecture**, where each IFRS Accounting Standard (such as IFRS 15) is represented as a specialized, grounded knowledge node. This core encapsulates the rigid, unchangeable rules of accounting interpretation, compliance assessment, and audit procedure support. These agents are strictly bound to authoritative knowledge sources, including IFRS, IAS, ISA, PCAOB, ISSB, ESRS, and COSO frameworks.

### 2. Technology Knowledge Graph Core (Upgradable)
This modular core is designed to be fully swappable and upgradable as AI advances, operating as a **Co-Scientist Inspired Multi-Agent** ecosystem. It adopts a hybrid multi-model architecture:
*   **General Reasoning Engines**: Integrates advanced foundation models like **Mango** (published by Meta) and the LLaMA-family for complex accounting analysis and strategic audit decisions.
*   **Language Intelligence Layer**: Specialized ModernBERT/BERT models for financial document understanding, semantic similarity, and evidence identification from SEC EDGAR filings.
*   **Small Language Models (SLMs)**: Efficient, locally deployable models for targeted execution.

## Repository Structure

```text
IFRS-AI-Inspector/
├── docs/
│   ├── 01_ontology_and_personas.md     # Definition of the Assurance Graph and expanded Agent Roles
│   ├── 02_architecture_design.md       # System blueprints detailing the Dual-Core architecture
│   └── 03_data_engineering.md          # Strategy for SEC data ingestion and RAG chunking
├── src/
│   ├── agent_orchestrator.py           # The primary MiroFlow hierarchical routing logic (incorporating all specialized agents)
│   └── edgar_pipeline.py               # The SEC EDGAR data ingestion script
├── LICENSE
└── README.md
```

## The Principle of Deterministic Mathematics and Grounded Narration
AI models in this framework retrieve, interpret, classify, reason, and explain accounting information, while **deterministic engines** independently perform calculations, reconciliations, accounting identity tests, XBRL validation, and rule-based compliance verification.

## Standard Example: IFRS 15
The core codebase and prototype simulations are anchored around **IFRS 15 (Revenue from Contracts with Customers)**. This acts as the standard example to demonstrate the framework's capability to process complex revenue recognition schedules, performance obligations, and varying transaction prices using simulated SEC EDGAR 10-K data.

## EU AI Act Compliance
IFRS-AI Inspector is designed with a strict focus on the **EU AI Act**, specifically addressing the requirements for High-Risk AI Systems (which may encompass AI used for critical financial infrastructure and auditing). The Dual-Core architecture guarantees:
*   **Transparency & Traceability**: The separation of the AI narrative engine from the deterministic mathematical engine ensures every algorithmic decision has a clear, non-opaque audit trail.
*   **Human Oversight**: Workflow orchestration necessitates human-in-the-loop approvals for material judgments.
*   **Data Governance**: RAG grounds the models strictly in authoritative accounting standards, minimizing hallucination risks and satisfying data quality mandates.

## License
This project is dual-licensed under the **MIT License** and the **Apache License 2.0** - see the [LICENSE-MIT](LICENSE-MIT) and [LICENSE-APACHE](LICENSE-APACHE) files for details.

## Citation
If you use this framework in your research, please cite it as follows:

> **Homayoun, S. (2026).** *A Hybrid Multi-Agent Digital Twin Framework for Autonomous Continuous IFRS Assurance.* GitHub repository. https://github.com/Saehon/IFRS-AI-Inspector
