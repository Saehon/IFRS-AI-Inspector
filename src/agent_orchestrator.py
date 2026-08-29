import os
from typing import Dict, Any, List

from evidence_verifier import EvidenceItem, EvidenceVerifier, VerificationStatus


# --- The AI Technology Core (Hybrid Model Factory) ---
class HybridModelFactory:
    """Routes tasks to interchangeable model/tool capabilities."""

    @staticmethod
    def invoke_model(task_type: str, payload: Any):
        if task_type == "LANGUAGE_INTELLIGENCE":
            print("  [AI Core] Routing to ModernBERT/BERT for financial document understanding...")
        elif task_type == "GENERAL_REASONING":
            print("  [AI Core] Routing to LLM reasoning layer for complex accounting analysis...")
        elif task_type == "ACCOUNTING_SLM":
            print("  [AI Core] Routing to Accounting-Specific SLM for controlled IFRS interpretation...")
        elif task_type == "DETERMINISTIC_MATH":
            print("  [AI Core] Routing to Deterministic Python Engine for XBRL/Math reconciliation...")
        return "Model execution simulated."


# --- The Accounting & Audit Knowledge Core (Agents) ---
class BaseAssuranceAgent:
    def __init__(self, name: str, role: str, primary_model: str):
        self.name = name
        self.role = role
        self.primary_model = primary_model
        print(f"Initializing {self.name} - Role: {self.role} (Powered by {self.primary_model})")

    def execute_task(self, event_data: Dict[str, Any]):
        print(f"[{self.name}] Processing event...")
        HybridModelFactory.invoke_model(self.primary_model, event_data)
        return {
            "agent": self.name,
            "candidate_output": event_data.get(
                "candidate_output",
                "No professional conclusion generated in simulation mode.",
            ),
        }


class IFRS15Agent(BaseAssuranceAgent):
    def __init__(self):
        super().__init__("IFRS 15 Agent", "Accounting Reasoning Agent", "ACCOUNTING_SLM")


class IFRS16Agent(BaseAssuranceAgent):
    def __init__(self):
        super().__init__("IFRS 16 Agent", "Accounting Reasoning Agent", "ACCOUNTING_SLM")


class AuditReasoningAgent(BaseAssuranceAgent):
    def __init__(self):
        super().__init__("Audit Reasoning Agent", "Evaluates audit risks and evidence", "GENERAL_REASONING")


class PCAOBInspectionAgent(BaseAssuranceAgent):
    def __init__(self):
        super().__init__("PCAOB Inspection Agent", "Simulates regulatory inspection", "GENERAL_REASONING")


class ISAComplianceAgent(BaseAssuranceAgent):
    def __init__(self):
        super().__init__("ISA Compliance Agent", "Assesses auditing standard compliance", "ACCOUNTING_SLM")


class EvidenceVerificationAgent(BaseAssuranceAgent):
    def __init__(self):
        super().__init__("Evidence Verification Agent", "Validates audit documentation", "LANGUAGE_INTELLIGENCE")


class FraudIntelligenceAgent(BaseAssuranceAgent):
    def __init__(self):
        super().__init__("Fraud Intelligence Agent", "Detects anomalies/management override", "LANGUAGE_INTELLIGENCE")


class SustainabilityAssuranceAgent(BaseAssuranceAgent):
    def __init__(self):
        super().__init__("Sustainability Assurance Agent", "Evaluates ISSB/ESRS/ESG", "GENERAL_REASONING")


class DigitalTwinSimulationAgent(BaseAssuranceAgent):
    def __init__(self):
        super().__init__("Digital Twin Simulation Agent", "Scenario analysis within shadow ledger", "DETERMINISTIC_MATH")


# --- MiroFlow Orchestration + Phase 2 Verify & Evidence Gate ---
class MiroFlowLeadRouter:
    def __init__(self):
        self.agents: List[BaseAssuranceAgent] = []
        self.verifier = EvidenceVerifier()
        print("\n--- Booting MiroFlow Lead Router ---")

    def register_agent(self, agent: BaseAssuranceAgent):
        self.agents.append(agent)

    @staticmethod
    def _load_evidence(event_data: Dict[str, Any]) -> List[EvidenceItem]:
        items: List[EvidenceItem] = []
        for raw in event_data.get("evidence", []):
            try:
                items.append(EvidenceItem(**raw))
            except TypeError as exc:
                raise ValueError(f"Invalid Phase 2 evidence object: {raw}") from exc
        return items

    def _verify_before_downstream(
        self,
        candidate_output: str,
        event_data: Dict[str, Any],
        producing_agent: str,
    ) -> Dict[str, Any]:
        report = self.verifier.verify(
            agent_output=candidate_output,
            evidence=self._load_evidence(event_data),
            context={
                "producing_agent": producing_agent,
                "force_human_gate": bool(event_data.get("force_human_gate", False)),
            },
        )
        payload = report.to_dict()
        print(
            f"[Phase 2 Verify] agent={producing_agent} status={payload['status']} "
            f"evidence={payload['evidence_coverage']:.0%} "
            f"citations={payload['citation_coverage']:.0%} "
            f"unsupported={payload['unsupported_claim_rate']:.0%}"
        )
        return payload

    def route_event(self, event_data: Dict[str, Any]):
        print("\n[Lead Router] --- NEW SHADOW LEDGER EVENT DETECTED ---")
        print(
            f"[Lead Router] Event Source: {event_data.get('form_type', 'Unknown')} | "
            f"Target: {event_data.get('ticker', 'Unknown')}"
        )
        print("[Lead Router] Delegating to candidate-producing agents under Phase 2 governance...")

        run_results: List[Dict[str, Any]] = []
        for agent in self.agents:
            if not isinstance(agent, (IFRS15Agent, PCAOBInspectionAgent)):
                continue

            candidate = agent.execute_task(event_data)
            verification = self._verify_before_downstream(
                candidate_output=candidate["candidate_output"],
                event_data=event_data,
                producing_agent=agent.name,
            )

            if verification["status"] == VerificationStatus.BLOCK.value:
                print(f"[Lead Router] BLOCKED: {agent.name} output cannot flow downstream.")
            elif verification["status"] == VerificationStatus.REVIEW.value:
                print(f"[Lead Router] HELD: {agent.name} output requires Human Gate review.")
            else:
                print(f"[Lead Router] VERIFIED: {agent.name} output may flow downstream.")

            run_results.append(
                {
                    "agent": agent.name,
                    "candidate_output": candidate["candidate_output"],
                    "verification": verification,
                }
            )

        return {
            "phase": 2,
            "phase_name": "Verify & Evidence",
            "results": run_results,
            "downstream_allowed": bool(run_results)
            and all(r["verification"]["status"] == VerificationStatus.PASS.value for r in run_results),
        }


def initialize_inspector_framework():
    """Initializes the complete Dual-Core architecture with Phase 2 gating."""
    print("--- Booting IFRS-AI Inspector (Dual-Core) ---")
    router = MiroFlowLeadRouter()
    router.register_agent(IFRS15Agent())
    router.register_agent(IFRS16Agent())
    router.register_agent(AuditReasoningAgent())
    router.register_agent(PCAOBInspectionAgent())
    router.register_agent(ISAComplianceAgent())
    router.register_agent(EvidenceVerificationAgent())
    router.register_agent(FraudIntelligenceAgent())
    router.register_agent(SustainabilityAssuranceAgent())
    router.register_agent(DigitalTwinSimulationAgent())
    print("--- Framework Initialized Successfully ---")
    return router


if __name__ == "__main__":
    import json

    inspector_router = initialize_inspector_framework()
    try:
        with open("MSFT_10K_sample.json", "r") as f:
            sec_event = json.load(f)
        result = inspector_router.route_event(sec_event)
        print(json.dumps(result, indent=2))
    except FileNotFoundError:
        print("Please run edgar_pipeline.py first to generate the MSFT_10K_sample.json file.")
