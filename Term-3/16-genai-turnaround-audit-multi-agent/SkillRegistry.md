# Skill Registry

Three specialists are available to the orchestrator. Paths are relative to the folder holding
this file.

---

## financial-audit

**Location:** `skills/financial-audit/SKILL.md`
**Specialisation:** Financial statement analysis. Computes liquidity, margin, leverage and
coverage ratios from the annual report, compares them year on year, and flags covenant and
refinancing exposure.
**Reads:** `Data/`
**Writes:** `fin_audit_findings/audit_report.md`
**Runs in:** Phase 1 (parallel with market-intelligence)

---

## market-intelligence

**Location:** `skills/market-intelligence/SKILL.md`
**Specialisation:** Competitive and channel positioning. Benchmarks the company against
industry norms and named competitors, and identifies where share is being lost.
**Reads:** `Data/`
**Writes:** `market_intelligence/market_report.md`
**Runs in:** Phase 1 (parallel with financial-audit)

---

## risk-assessment

**Location:** `skills/risk-assessment/SKILL.md`
**Specialisation:** Risk modelling. Scores each identified threat on severity and probability,
builds the risk register, and names the single largest threat to continuity.
**Reads:** `Data/`, `fin_audit_findings/`, `market_intelligence/`
**Writes:** `risk_assessment/risk_report.md`
**Runs in:** Phase 2 (needs both Phase 1 outputs)

---

## Not in scope

No specialist here has authority to execute a transaction, contact a supplier or lender, or
write outside its own output folder.
