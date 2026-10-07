# Risk Assessment Findings

```
agent:        risk-assessment
status:       COMPLETE
confidence:   0.85
source:       RetailCorp_Annual_Report.pdf Section 3 (Operational Risk & Compliance), plus
              fin_audit_findings/audit_report.md and market_intelligence/market_report.md
missing:      carried from financial-audit: inventory value, interest expense, net income,
              total assets and equity. Carried from market-intelligence: competitor
              financials, e-commerce growth rate. Litigation and environmental disclosures
              are absent from the source, so regulatory risk is scored on what is present only.
escalate:     YES
```

**Company:** RetailCorp Inc.  **Fiscal year:** FY2025
**Upstream inputs:** financial-audit COMPLETE, market-intelligence PARTIAL

Scores from `skills/risk-assessment/scripts/risk_score.py`, bands from
`references/risk-scoring-policy.md`. Score = severity x probability.

## Risk register

| # | Category | Identified threat | Severity | Probability | Score | Tier | Mitigation | Approval |
|---|---|---|---|---|---|---|---|---|
| 1 | Financial | $12.5M revolver matures 30 Jun 2026 | Critical (5) | Near certain (5) | **25** | Critical | Refinance or extend before the covenant test | Within delegated authority |
| 2 | Financial | DSCR 1.15x against a 1.10x covenant floor | Critical (5) | Likely (4) | **20** | Critical | Negotiate waiver ahead of the test date | Within delegated authority |
| 3 | Strategic | E-commerce 12% against a 34% industry norm | High (4) | Near certain (5) | **20** | Critical | Digital platform pivot, $3.0M CAPEX | Within delegated authority ($3.0M < $5.0M) |
| 4 | Operational | Inventory turnover fell 4.2x to 3.1x | High (4) | Near certain (5) | **20** | Critical | Clear aged seasonal stock held in DCs | Within delegated authority |
| 5 | Market | Enclosed-mall foot traffic -18% YoY | High (4) | Near certain (5) | **20** | Critical | Shift footprint toward strip formats | Within delegated authority |
| 6 | Supply chain | 42% single-source vendor dependency | High (4) | Possible (3) | **12** | High | Dual-source the top categories | Within delegated authority |

Severity and probability rationale, per the policy bands:

- Rows 1, 3, 4 and 5 are **Near certain** because each is a dated obligation or an already-recorded
  movement, not a forecast. The policy sets dated obligations inside 12 months at Near certain by
  definition.
- Rows 1 and 2 are **Critical severity** under the covenant rule: a breach transfers control to the
  lender regardless of the sum involved.
- Row 6 is **Possible** rather than Likely because the document records the dependency and one Q3
  disruption, but gives no failure rate to support a higher band.

## Shared root causes

Six risks, but not six independent problems. Two clusters will arrive together.

- **Rows 1 and 2 share one cause: the EBITDA collapse.** EBITDA fell 34.1% to $28.0M, which is what
  pushed coverage down to 1.15x and what will be tested when the revolver is refinanced. They are
  listed separately because the policy requires it, but a lender will see one problem, not two. If
  the covenant trips before June 2026, the refinancing conversation starts from a materially weaker
  position.
- **Rows 3 and 5 share one cause: format and channel obsolescence.** The mall traffic decline and
  the digital deficit are the same customer migration observed from two ends. Fixing one without
  the other leaves the migration intact.

## Largest threat to continuity

The $12.5M revolver maturing on 30 June 2026 is the single largest threat, scoring 25 of a possible
25. It is the only risk in the register with a fixed date attached and no discretion over timing,
and cash of $13.8M covers it just 1.10x. What makes it the largest rather than merely the most
urgent is its interaction with row 2: the covenant is likely to be tested before or during the
refinancing, so the company may have to negotiate new terms at precisely the moment its coverage
ratio is weakest.

## Held for human approval

None in this run. The only costed mitigation is the $3.0M e-commerce transition CAPEX, which falls
below the $5.0M threshold in the orchestrator's group-level guardrails and therefore sits within
delegated authority. If the digital pivot is later rescoped above $5.0M, it stops for human
confirmation before it can be recommended.
