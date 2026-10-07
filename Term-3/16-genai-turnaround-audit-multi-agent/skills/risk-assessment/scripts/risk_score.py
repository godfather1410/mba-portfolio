"""Deterministic risk scoring for the risk-assessment skill.

Bands come from references/risk-scoring-policy.md. Keep the two in step: if the policy
changes, change the tables here, not the agent's instructions.

Usage:
    python risk_score.py --demo
"""

SEVERITY = {"critical": 5, "high": 4, "medium": 3, "low": 2, "negligible": 1}
PROBABILITY = {"near certain": 5, "likely": 4, "possible": 3, "unlikely": 2, "remote": 1}


def score(severity_band, probability_band):
    s = SEVERITY[severity_band.strip().lower()]
    p = PROBABILITY[probability_band.strip().lower()]
    return s * p


def tier(value):
    if value >= 20:
        return "Critical"
    if value >= 12:
        return "High"
    if value >= 6:
        return "Medium"
    return "Low"


def needs_human_approval(mitigation_cost_musd, threshold=5.0):
    """The orchestrator's group-level guardrail, applied at the point of recommendation."""
    return mitigation_cost_musd is not None and mitigation_cost_musd > threshold


def build_register(risks):
    """risks: list of dicts with category, threat, severity, probability, mitigation, cost_musd."""
    out = []
    for r in risks:
        v = score(r["severity"], r["probability"])
        out.append({**r, "score": v, "tier": tier(v),
                    "approval": "Pending human approval" if needs_human_approval(r.get("cost_musd")) else "Within delegated authority"})
    return sorted(out, key=lambda x: x["score"], reverse=True)


if __name__ == "__main__":
    demo = [
        dict(category="Financial", threat="$12.5M revolver matures 30 Jun 2026",
             severity="critical", probability="near certain", mitigation="Refinance or extend the facility", cost_musd=None),
        dict(category="Financial", threat="DSCR 1.15x against a 1.10x covenant floor",
             severity="critical", probability="likely", mitigation="Negotiate covenant waiver ahead of test date", cost_musd=None),
        dict(category="Strategic", threat="E-commerce at 12% against a 34% industry norm",
             severity="high", probability="near certain", mitigation="Digital platform pivot", cost_musd=3.0),
        dict(category="Operational", threat="Inventory turnover fell 4.2x to 3.1x",
             severity="high", probability="near certain", mitigation="Clear aged seasonal stock", cost_musd=None),
        dict(category="Supply chain", threat="42% single-source vendor dependency",
             severity="high", probability="possible", mitigation="Dual-source the top categories", cost_musd=None),
        dict(category="Market", threat="18% YoY enclosed-mall foot traffic decline",
             severity="high", probability="near certain", mitigation="Shift footprint toward strip formats", cost_musd=None),
    ]
    for r in build_register(demo):
        print(f"{r['score']:>3}  {r['tier']:<8}  {r['category']:<13}  {r['threat'][:52]:<52}  {r['approval']}")
