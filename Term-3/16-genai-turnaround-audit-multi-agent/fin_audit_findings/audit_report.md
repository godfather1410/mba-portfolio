# Financial Audit Findings

```
agent:        financial-audit
status:       COMPLETE
confidence:   0.92
source:       RetailCorp_Annual_Report.pdf, Section 1 (Executive Overview & Financial
              Performance) and the Debt Structure & Liabilities subsection
missing:      inventory value (blocks quick ratio); interest expense; net income; total
              assets and shareholders' equity (block ROA, ROE and interest cover)
escalate:     YES
```

**Company:** RetailCorp Inc.  **Fiscal year:** FY2025 (ended 31 December 2025)
**Comparative:** FY2024  **Currency:** USD millions, as reported

## Ratio summary

Computed by `skills/financial-audit/scripts/ratios.py`. Verdicts from
`references/audit-thresholds.md`.

| Metric | FY2024 | FY2025 | Movement | Verdict |
|---|---|---|---|---|
| Current ratio | 1.35 | 1.10 | -0.25 | **Breach** (< 1.20) |
| Working capital | $17.0M | $5.3M | -68.8% | Watch (positive but shrinking) |
| EBITDA margin | 9.44% | 6.80% | -2.65 pp | Watch (6.0-9.9%) |
| Gross margin | 38.2% | 34.0% | -4.2 pp (-11.0% relative) | **Breach** (worse than -3.0 pp) |
| Total debt / EBITDA | not derivable | 3.48x | n/a | Watch (2.51-3.50x) |
| Cash / short-term debt | $22.0M / n/d | 1.10x | n/a | Watch (1.00-1.99x) |
| Debt-service coverage | not disclosed | 1.15x | n/a | **Breach** (floor 1.10x + 0.05x) |
| Quick ratio | Not derivable from source | Not derivable from source | n/a | inventory not disclosed |

Supporting figures: revenue $450.0M to $412.0M (-8.44%); EBITDA $42.5M to $28.0M (-34.12%);
cash $22.0M to $13.8M (-37.27%); current assets $65.0M to $58.0M; current liabilities $48.0M to
$52.7M; gross profit $171.90M to $140.08M (-18.5%).

## Flags

- **Short-term debt above the $10.0M escalation line.** $12.5M senior revolving credit facility
  matures 30 June 2026, inside 12 months of the balance sheet date. Escalated on the maturity
  rule alone, independent of the ratio verdicts.
- **Covenant proximity.** Debt-service coverage stands at 1.15x against a stated covenant floor
  of 1.10x. Headroom is 0.05x, inside the 0.10x escalation band.
- **Three Breach rows.** The thresholds file escalates the whole audit at two or more.
- **Liquidity and leverage are moving together.** Cash covers the maturing revolver only 1.10x,
  while the current ratio has fallen through 1.20. The company can meet the June 2026 maturity
  from cash only by leaving almost nothing behind it.
- Long-term debt of $85.0M in senior notes at 5.8% falls due in 2029 and is not a near-term issue.

## Data quality notes

Two discrepancies in the source document. Neither changes a verdict, but both are reported
because the audit trail should show which figure was used.

1. The document states the liquidity ratio fell 18.5% year on year. Computed from the underlying
   current assets and liabilities, the fall is 18.73%. The document's figure comes from dividing
   the already-rounded ratios (1.10 against 1.35). The underlying figures are the ones used here.
2. The document reports the gross margin change as "-4.2%" in a column headed "YoY Change (%)".
   That is a movement of 4.2 percentage points. The relative decline is 11.0%. Both are stated
   above so the two are not confused in the summary.

## Risk statement

RetailCorp has moved from adequate to strained liquidity in a single year, with the current ratio
through its floor, working capital down more than two thirds, and $12.5M falling due in June 2026
against $13.8M of cash. The binding constraint is not profitability but the debt-service covenant,
where 0.05x of headroom on a coverage ratio that has to be tested before the revolver matures
leaves almost no room for a further earnings decline.
