# IFRS-AI Inspector: Phase 3 - Data Engineering

With our vision reaffirmed and our architecture defined, we now enter the **Data Engineering Phase**. An AI assurance system is only as good as the data it reasons over. In this phase, we establish the two critical data pillars for the IFRS-AI Inspector:

1.  **The Rulebook**: The RAG knowledge base of IFRS Standards.
2.  **The Environment**: The simulated enterprise data (ERP and telemetry) to populate the Shadow Ledger.

---

## 3.1 IFRS Knowledge Base Construction (RAG)

To enable the *Scholar Sub-Agent* to perform tool-assisted reasoning on accounting treatments, we must structure the IFRS standards into a queryable vector database.

### The Ingestion Pipeline

1.  **Source Material**: We will utilize the public text of IFRS Accounting Standards (e.g., IFRS 9, 15, 16) and IAS standards.
2.  **Document Parsing (MiroFlow Reading Server)**: The text is parsed to maintain its hierarchical structure (Standard $\rightarrow$ Part $\rightarrow$ Section $\rightarrow$ Paragraph).
3.  **Semantic Chunking**: 
    *   *Granularity*: Paragraph-level chunking is preferred for IFRS standards because individual paragraphs often contain specific, atomic rules (e.g., "An entity shall recognize revenue to depict the transfer of promised goods...").
    *   *Metadata*: Each chunk is tagged with metadata: `{"standard": "IFRS 15", "topic": "Revenue", "paragraph_id": "31"}`.
4.  **Embedding**: We will use a financial domain-specific embedding model (e.g., a fine-tuned BERT or a specialized commercial model) to capture the nuanced legal and accounting terminology.
5.  **Vector Store**: The embeddings are stored in a vector database (e.g., Pinecone, Milvus, or a local ChromaDB for our prototype).

### Retrieval Strategy
When a transaction occurs, the agent will construct a query. Instead of a simple keyword search, we will use a **Hybrid Search** approach:
*   **Semantic Search**: Finding paragraphs conceptually related to the transaction description.
*   **Metadata Filtering**: Restricting the search space if the router agent has already identified the relevant standard (e.g., `filter = {"standard": "IFRS 16"}`).

---

## 3.2 Simulated ERP Data Generation

Because we cannot immediately connect to a live corporate SAP/Oracle system for our prototype, we must build a realistic generator to feed our Digital Twin (Shadow Ledger).

### The Data Generator (Python)

We will create a Python module that procedurally generates a stream of complex corporate events and their corresponding accounting entries.

#### Example Scenario: SaaS Revenue (IFRS 15)
The generator will emit the following linked data points for a single event:

1.  **Operational Event**: A new enterprise customer signs a 3-year SaaS contract for \$360,000, paid annually in advance.
2.  **Source Document (Synthetic)**: A JSON representation of the contract terms.
3.  **ERP Transactions**:
    *   *Day 1*: Invoice issued for \$120,000.
    *   *Day 2*: Cash received for \$120,000.
4.  **General Ledger Entries**:
    *   *Debit*: Cash (\$120,000)
    *   *Credit*: Deferred Revenue (\$120,000)
5.  **Telemetry Data**: The IP address of the sales rep who closed the deal, the timestamp of the signature, and the approval routing metadata.

### The "Anomaly" Injection
To test our *Auditor* and *Quant* sub-agents, the generator will occasionally inject intentional errors into the data stream:
*   **Accounting Error**: Recognizing the full \$360,000 as immediate revenue instead of deferring it.
*   **Vouching Error**: The ERP transaction shows \$150,000, but the underlying synthetic contract document says \$120,000.
*   **Telemetry Anomaly**: A journal entry posted at 3:00 AM on a Sunday by an inactive user ID.

This continuous, slightly noisy data stream will serve as the perfect testing ground for our MiroFlow orchestrated agents.
