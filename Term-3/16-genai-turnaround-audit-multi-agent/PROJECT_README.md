# Turnaround Audit Assistant

A multi-agent personal assistant that produces a 360-degree business audit from a company's
annual report: financial ratio analysis, competitor benchmarking and risk modelling, consolidated
into one turnaround briefing.

Built for the classwork brief: *Smita, an MBA student preparing a turnaround strategy
presentation on an underperforming retail company, needs a 360-degree audit from a 100-page
annual report.*

## How to run it

1. Put the annual report in `Data/`.
2. Point your agent at this folder and give it the orchestrator instructions:
   `Read Agents.md and run the turnaround audit on the document in Data/.`
3. The orchestrator reads `SkillRegistry.md`, dispatches the three specialists, and writes each
   stage output to its own folder.

## Architecture

Parallel fan-out, then fan-in. Financial and market readings are independent and run together;
risk modelling needs both, so it runs after. See `workflows/turnaround-audit.md`.

```
financial-audit  ─┐
                  ├─> risk-assessment ─> Summary
market-intelligence ─┘
```

## Folder map

| Path | What it holds |
|---|---|
| `Agents.md` | Orchestrator instructions and the group-level guardrails |
| `SkillRegistry.md` | Directory of the three specialists and what each is for |
| `workflows/` | The execution flow and failure handling |
| `Data/` | Input document |
| `skills/<name>/SKILL.md` | One specialist's instructions |
| `skills/<name>/references/` | Thresholds, benchmarks and policies, read at run time |
| `skills/<name>/scripts/` | Deterministic calculations |
| `skills/<name>/assets/` | Output templates |
| `fin_audit_findings/` | Financial audit output |
| `market_intelligence/` | Market intelligence output |
| `risk_assessment/` | Risk register output |
| `Summary/` | Consolidated turnaround report |

## Design notes

**Policies live in `references/`, not in instructions.** Thresholds and benchmarks change; the
procedure for applying them does not. Editing `audit-thresholds.md` changes the audit without
touching any SKILL.md.

**Deterministic maths lives in `scripts/`.** Ratios and risk scores are computed, not narrated,
so two runs on the same document produce the same numbers.

**Guardrails are set at three levels.** Individual agents carry their own rules in each SKILL.md.
The handoff between agents is a structured status block, defined in `Agents.md`, so a downstream
agent receives confidence and gaps rather than just a conclusion. Group-level rules that no single
agent owns, such as the $5M human-approval gate, sit in `Agents.md`.

## Current outputs

The four output folders contain a completed run against `Data/RetailCorp_Annual_Report.pdf`.
Every figure in them traces to that document or to one of the scripts.
