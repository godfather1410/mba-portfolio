# Workflow: 360-degree turnaround audit

## Trigger
A request to audit a company from its annual report ahead of a turnaround or strategy decision.

## Architecture
Parallel fan-out, then fan-in. This mirrors the real process: the financial position and the
market position are independent readings of the same document and can be taken at the same
time, but the risk model is only meaningful once both are known.

```
                    Data/AnnualReport.pdf
                             |
             +---------------+---------------+
             |                               |
      financial-audit               market-intelligence      <- Phase 1, parallel
             |                               |
      fin_audit_findings/            market_intelligence/
             |                               |
             +---------------+---------------+
                             |
                     risk-assessment                          <- Phase 2, fan-in
                             |
                      risk_assessment/
                             |
                  Orchestrator synthesis                      <- Phase 3
                             |
              Summary/executive_turnaround_report.md
```

## Phase 1, parallel
Dispatch financial-audit and market-intelligence against `Data/`. Neither may read the other's
output. Both must return a status block.

## Phase 2, fan-in
Dispatch risk-assessment with three inputs: the source document and both Phase 1 reports. It
scores risks using `skills/risk-assessment/scripts/risk_score.py` rather than by judgement alone.

## Phase 3, synthesis
The orchestrator merges the three reports into an executive turnaround report containing:
1. The headline diagnosis in two sentences.
2. A financial position summary.
3. A market position summary.
4. The risk register, ordered by score.
5. A decision matrix comparing at least three strategic options.
6. A recommendation, with any item above the $5M human-approval threshold marked as pending.

## Failure handling
If a specialist returns BLOCKED, the workflow continues but the summary opens with what could
not be established and why. A missing input is reported, never estimated.
