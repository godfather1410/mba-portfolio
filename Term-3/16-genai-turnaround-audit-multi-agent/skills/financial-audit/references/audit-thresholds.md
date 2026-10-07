# Audit thresholds

Policy file. Edit these values as the finance team's tolerances change; the skill instructions
do not need to change with them.

| Metric | Pass | Watch | Breach |
|---|---|---|---|
| Current ratio | >= 1.50 | 1.20 to 1.49 | < 1.20 |
| Debt-service coverage ratio | >= 1.40x | 1.11x to 1.39x | <= covenant floor + 0.05x |
| Total debt / EBITDA | <= 2.50x | 2.51x to 3.50x | > 3.50x |
| EBITDA margin | >= 10.0% | 6.0% to 9.9% | < 6.0% |
| Gross margin movement | >= 0.0 pp | -0.1 to -3.0 pp | worse than -3.0 pp |
| Cash / short-term debt | >= 2.00x | 1.00x to 1.99x | < 1.00x |
| Working capital | positive and growing | positive but shrinking | negative |

## Escalation rules
- Short-term debt above $10.0M maturing within 12 months is escalated regardless of other ratios.
- A coverage ratio within 0.10x of its covenant floor is escalated even when it technically passes.
- Two or more Breach rows in one audit means the whole report is escalated to human review.

## Reporting conventions
- Margins are stated in percentage points for movement and percent for relative change, both labelled.
- Currency is reported in the document's own unit. Do not convert.
- Ratios are reported to two decimal places, percentages to one.
