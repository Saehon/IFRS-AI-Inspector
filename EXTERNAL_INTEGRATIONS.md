# IFRS-AI Inspector — External Research Integrations

Owner: Saeid Homayoun  
ORCID: https://orcid.org/0000-0002-2536-0446

## Relevant integrations
- AuditData-API → `AuditDataAdapter` for structured financial/audit-data ingestion before IFRS rule and evidence evaluation.
- Financial Sentiment / BERT / FinBERT → `FinancialNLPAdapter` for narrative-disclosure classification and textual evidence benchmarking.
- fg-data-synthetic → `SyntheticDataAdapter` for privacy-safe IFRS scenarios, accounting-policy simulations and digital-twin stress tests.
- TimesFM → optional `TimesFMAdapter` for temporal accounting-risk, impairment/going-concern and control-risk research where forecasting is relevant.

## Design rule
External Data/Model → Rights Check → Adapter → Accounting Schema Validation → IFRS Knowledge/Evidence Layer → Verification → Human Professional Review

External projects retain their own authorship and licenses. IFRS-AI Inspector does not represent upstream code, models, standards or data as original NAAIL inventions.
