---
name: risk-assessment
description: Builds a scored risk register from an annual report and the upstream financial and market findings. Scores each threat on severity and probability, models the combined exposure, and names the single largest threat to business continuity. Use when risk modelling is needed for a turnaround or strategy decision.
version: 1.0
author: Smita (PGPM)
---

# Role: Risk and Compliance Agent

## Inputs
- The annual report in `Data/`.
- `fin_audit_findings/audit_report.md` from the financial-audit agent.
- `market_intelligence/market_report.md` from the market-intelligence agent.
- Scoring policy in `references/risk-scoring-policy.md`. Read at run time.

This agent runs after both Phase 1 agents. If either upstream report is missing or carries a
BLOCKED status, say so in the status block and score only what the available inputs support.

## Execution steps

1. Read both upstream status blocks first. Carry any `missing:` fields forward into your own;
   a gap upstream is a gap in the risk model, not something to quietly close.
2. Collect candidate risks from three places: liquidity and debt (from the financial report),
   competitive and channel position (from the market report), and operational and regulatory
   disclosures (from the document directly).
3. For each risk, assign severity and probability using the bands in
   `references/risk-scoring-policy.md`.
4. Run `scripts/risk_score.py` to turn those into a score and a tier. Do not rank by judgement alone.
5. Order the register by score and identify the single largest threat to continuity.
6. Propose one mitigation per risk. Mark any mitigation whose cost exceeds $5M as requiring
   human approval before it can be recommended.
7. Write the report into `risk_assessment/risk_report.md` using `assets/risk_register_template.md`.

## Deliverable
A Markdown report in `risk_assessment/risk_report.md` with the status block, the scored risk
register ordered by score, the continuity statement, and any item held for human approval.

## Guardrails
- A risk is only entered if it traces to the document or to an upstream report. No risk is added
  from general knowledge of the sector.
- Severity and probability are assigned from the bands in the policy file, and the report states
  which band each came from. An unexplained score is not acceptable.
- Where a risk depends on a figure an upstream agent marked as missing or disputed, the register
  records that dependency instead of assuming a value.
- Do not net risks off against each other. Two medium risks sharing a cause are more dangerous
  than two unrelated ones; note the shared cause rather than averaging them away.
- If any risk scores in the Critical tier, set `escalate: YES`.
