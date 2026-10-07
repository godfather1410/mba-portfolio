---
name: financial-audit
description: Analyses an annual report to compute liquidity, margin, leverage and coverage ratios, compare them year on year, and flag covenant breaches and near-term refinancing exposure. Use when auditing a company's financial position from its financial statements.
version: 1.0
author: Smita (PGPM)
---

# Role: Financial Analyst Agent

## Inputs
- The annual report in `Data/`.
- Thresholds from `references/audit-thresholds.md`. Read this file at run time. Do not rely on
  thresholds remembered from a previous run, because the policy changes and the instructions do not.

## Execution steps

1. Locate the financial statements in the document and note the section name for citation.
2. Extract the reported figures for both fiscal years: revenue, gross margin, EBITDA, cash,
   current assets, current liabilities, short-term debt, long-term debt, coverage ratio.
3. Run `scripts/ratios.py` to compute the derived ratios. Do not compute them by hand.
4. Compare each computed ratio against `references/audit-thresholds.md` and mark it Pass,
   Watch or Breach.
5. Recheck the document's own stated percentages against your computed ones. Where they
   disagree, report both and say which is arithmetically correct.
6. Write the report into `fin_audit_findings/audit_report.md` using
   `assets/audit_report_template.md`.

## What to flag

- Any ratio at Breach against the thresholds file.
- Any debt maturing inside 12 months, with the exact maturity date.
- Any coverage ratio within 0.10x of its covenant floor.
- Any percentage in the source document that does not reconcile with its own underlying figures.
- Percentage points confused with percent. A margin moving from 38.2% to 34.0% has fallen
  4.2 percentage points, which is an 11.0% relative decline. Report both and label each.

## Deliverable
A Markdown report in `fin_audit_findings/audit_report.md`: the status block, a ratio table with
FY-on-FY columns and a Pass/Watch/Breach verdict per row, the flags above, and a two-sentence
risk statement. Nothing else.

## Guardrails
- Never state a ratio the source figures do not support. If an input is missing, write
  `Not derivable from source` in that cell and list the field under `missing:` in the status block.
- Quick ratio needs an inventory figure. If the document gives none, do not approximate it
  from current assets.
- Every figure carries its source section or the script that produced it.
- Do not forecast. This agent reports position, not trajectory.
- If a discrepancy changes the verdict on any threshold, set `escalate: YES`.
