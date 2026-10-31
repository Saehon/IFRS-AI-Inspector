# Research Evaluation Card — IFRS-AI Inspector

**Status:** scientific research prototype; benchmark design and evaluation requirements documented; **no production financial-reporting assurance, audit opinion or regulatory certification**.

**Investigator:** Saeid Homayoun · [ORCID](https://orcid.org/0000-0002-2536-0446) · [University of Gävle](https://www.hig.se/)

## Research question and scope

Can standards-aware retrieval, multi-agent analysis and a deterministic control layer help identify accounting evidence gaps and support **human-reviewed** judgments more reliably than an unguided model?

**Scope of this card:** research protocol; it is not a completed real-model head-to-head trial. IFRS standards, professional audit material and audited financial-reporting records must be licensed and version-controlled before tests based on their text are published.

## Evaluation dimensions, pre-registration and failure conditions

| Dimension | Example failure | Proposed observable | Gate |
|---|---|---|---|
| Accounting calculation | Wrong currency, denominator, fiscal period, unit or sign | Absolute/relative tolerance with units and period validation | Deterministic test |
| Evidence provenance | Cited evidence does not support accounting assertion | Source ID validity **plus independent evidence entailment** | Source-passport + independent reviewer |
| IFRS judgment | Model treats an accounting choice as universally determined | Annotated permitted alternatives, uncertainty and rationale | Qualified accountant review |
| Audit internal controls | Missing segregation of duties, conflicting control owner or stale evidence | Environment, identity, timestamp and owner checks | Fail closed |
| Agent tool use | Invalid tool calls or tool result fabricated | Allowed scope, traces, missing-call and error counts | Tool-integrity gate |
| Human oversight | AI outputs a final audit approval without authorized reviewer | Signoff evidence and escalation | Human Gate, never self-approved |
| Model reliability | Changes in model/version produce unknown error patterns | Paired case-level comparisons, ablations, coverage and abstention | Frozen evaluation protocol |
| Data protection | Client data sent to model without permission | Data flow rights, retention, approved endpoint and consent | Block deployment |

## Reproducibility and study design

1. Freeze a protocol with tasks, case IDs, sampling frame, legal rights, reviewer roles, model-configuration hashes and prespecified metrics.
2. Independently create and blind gold labels; record inter-rater disagreement and allowed IFRS professional-judgment alternatives.
3. Evaluate at least two genuinely executed model configurations with identical licensed evidence and materially equivalent tasks.
4. Report denominators, coverage/abstention, numerical errors, evidence-grounding, human agreement, error taxonomy, sampling uncertainty and cost.
5. Inspect wrong answers by **account** (e.g., inventory, goodwill, revenue), standard, company-year and industry rather than reporting only average accuracy.
6. Preserve signed scientific review, code commit SHA, source versions, model IDs and run artifact checksums.

## Benchmark anchors and licensing

- [OpenAI — evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices): evaluator calibration; human/metric/model grades
- [Anthropic — evaluation methodology](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests): task-specific and edge-case evaluations
- [Google — Gen AI evaluation](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/evaluation-overview): rubrics and comparable model metrics
- [UK AI Security Institute — Inspect](https://inspect.aisi.org.uk/): tool/agent traces and composable scorers
- [Patronus AI — FinanceBench](https://huggingface.co/datasets/PatronusAI/financebench): finance QA; public 150-example sample under **CC BY-NC 4.0**
- [NAAIL — comprehensive benchmark crosswalk](https://github.com/Saehon/Saeid-Homayoun/blob/main/research/LLM_BENCHMARKS_AND_EVALUATION.md)

**No FinanceBench samples, restricted IFRS standard passages, audit-firm proprietary methods or client financial files are embedded by this card.** Referenced frameworks are independent third-party contributions and are not endorsed or authored by this project.

## Reproducible public examples and limits

The [NAAIL financial evidence grader](https://github.com/Saehon/Saeid-Homayoun/tree/main/research/ai_evidence_evaluation) demonstrates offline case scoring with deliberately synthetic examples and regression tests. It provides **internal software-test evidence, not validation of IFRS AI decision quality or externally measured model correctness**.

The specialist evidence/control tests in [the IFRS-AI Inspector PR #3](https://github.com/Saehon/IFRS-AI-Inspector/pull/3) remain in an **open, unmerged** pull request and should be examined at their exact commit before research findings are attributed to the default branch.

## Known limitations and release decision

This repository does not establish standards compliance, completed independent replication, a statistically representative sample or production audit effectiveness. An actual assurance claim requires lawful evidence and appropriately qualified human auditors; model outputs are not professional signatures. Research findings should only be released with reproducible data permissions, independent review and explicit uncertainty.
