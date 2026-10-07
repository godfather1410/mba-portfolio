# Risk scoring policy

Policy file, read at run time. Changing these bands changes the model without touching instructions.

## Severity bands

| Band | Score | Meaning |
|---|---|---|
| Critical | 5 | Threatens continuity within 12 months, or breaches a covenant |
| High | 4 | Material hit to earnings or liquidity, recoverable but painful |
| Medium | 3 | Contained impact on one segment or function |
| Low | 2 | Absorbed in normal operations |
| Negligible | 1 | Monitor only |

## Probability bands

| Band | Score | Meaning |
|---|---|---|
| Near certain | 5 | Already in motion, or contractually dated |
| Likely | 4 | More likely than not within 12 months |
| Possible | 3 | Credible but not established |
| Unlikely | 2 | Would need conditions to change |
| Remote | 1 | Theoretical |

## Scoring
`risk_score = severity x probability`, range 1 to 25.

| Score | Tier | Handling |
|---|---|---|
| 20 to 25 | Critical | Immediate action, escalate to human |
| 12 to 19 | High | Mitigation plan required this quarter |
| 6 to 11 | Medium | Plan and monitor |
| 1 to 5 | Low | Monitor only |

## Rules
- A dated obligation inside 12 months is Near certain by definition. A maturity date is not a probability judgement.
- A covenant breach is Critical severity regardless of the sum involved, because it transfers control to the lender.
- Any mitigation costing above $5M is held for human approval and marked pending in the register.
- Two risks driven by the same root cause are listed separately and the shared cause is named, because they will arrive together.
