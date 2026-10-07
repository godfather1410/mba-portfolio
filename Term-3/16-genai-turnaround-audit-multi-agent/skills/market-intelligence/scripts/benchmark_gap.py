"""Deterministic benchmark gap calculations for the market-intelligence skill.

Keeps the gap arithmetic out of prose so the same inputs always give the same gap,
and so the structural/tactical call is made by a rule rather than by impression.

Usage:
    python benchmark_gap.py --demo
"""

STRUCTURAL_PP = 15.0   # gaps wider than this are structural, per references/industry-benchmarks.md


def gap_pp(company_pct, industry_pct):
    """Gap in percentage points. Negative means the company is behind."""
    return company_pct - industry_pct


def classify_gap(gap):
    return "Structural" if abs(gap) > STRUCTURAL_PP else "Tactical"


def gap_vs_range(value, low, high):
    """For benchmarks expressed as a range. Returns distance outside the range, or 0.0 inside."""
    if value < low:
        return value - low
    if value > high:
        return value - high
    return 0.0


def relative_to_sector(company_rate, sector_rate):
    """How many times the sector rate the company is moving at."""
    if not sector_rate:
        return None
    return company_rate / sector_rate


if __name__ == "__main__":
    g = gap_pp(12.0, 34.0)
    print(f"E-commerce share gap       {g:+.0f} pp -> {classify_gap(g)}")
    print(f"Inventory turnover vs 4-5x {gap_vs_range(3.1, 4.0, 5.0):+.1f}x outside range")
    print(f"Foot traffic vs sector     {relative_to_sector(18.0, 6.0):.1f}x the sector decline rate")
