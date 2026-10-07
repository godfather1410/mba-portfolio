"""Deterministic ratio calculations for the financial-audit skill.

The agent must call these rather than compute ratios in prose, so the same inputs always
produce the same numbers and the working can be audited.

Usage:
    python ratios.py --demo      # runs against the RetailCorp FY2025 figures
"""


def current_ratio(current_assets, current_liabilities):
    if not current_liabilities:
        return None
    return current_assets / current_liabilities


def working_capital(current_assets, current_liabilities):
    return current_assets - current_liabilities


def ebitda_margin(ebitda, revenue):
    if not revenue:
        return None
    return ebitda / revenue * 100


def gross_profit(revenue, gross_margin_pct):
    return revenue * gross_margin_pct / 100


def debt_to_ebitda(short_term_debt, long_term_debt, ebitda):
    if not ebitda:
        return None
    return (short_term_debt + long_term_debt) / ebitda


def cash_to_short_term_debt(cash, short_term_debt):
    if not short_term_debt:
        return None
    return cash / short_term_debt


def pp_change(new_pct, old_pct):
    """Movement in percentage points. Use for margins."""
    return new_pct - old_pct


def relative_change(new, old):
    """Relative change in percent. Use for absolute quantities."""
    if not old:
        return None
    return (new - old) / old * 100


def covenant_headroom(coverage_ratio, covenant_floor):
    return coverage_ratio - covenant_floor


def quick_ratio(current_assets, inventory, current_liabilities):
    """Returns None when inventory is not disclosed. The caller must report
    'Not derivable from source' rather than substituting an estimate."""
    if inventory is None or not current_liabilities:
        return None
    return (current_assets - inventory) / current_liabilities


if __name__ == "__main__":
    fy24 = dict(rev=450.0, gm=38.2, ebitda=42.5, cash=22.0, ca=65.0, cl=48.0)
    fy25 = dict(rev=412.0, gm=34.0, ebitda=28.0, cash=13.8, ca=58.0, cl=52.7)
    std, ltd, dscr, floor = 12.5, 85.0, 1.15, 1.10

    for label, f in (("FY2024", fy24), ("FY2025", fy25)):
        print(f"{label}: current ratio {current_ratio(f['ca'], f['cl']):.2f} | "
              f"working capital {working_capital(f['ca'], f['cl']):.1f} | "
              f"EBITDA margin {ebitda_margin(f['ebitda'], f['rev']):.2f}% | "
              f"gross profit {gross_profit(f['rev'], f['gm']):.2f}")

    print(f"Debt/EBITDA FY2025      {debt_to_ebitda(std, ltd, fy25['ebitda']):.2f}x")
    print(f"Cash/short-term debt    {cash_to_short_term_debt(fy25['cash'], std):.2f}x")
    print(f"Gross margin movement   {pp_change(fy25['gm'], fy24['gm']):+.1f} pp")
    print(f"Gross margin relative   {relative_change(fy25['gm'], fy24['gm']):+.1f}%")
    print(f"Covenant headroom       {covenant_headroom(dscr, floor):+.2f}x")
    print(f"Quick ratio             {quick_ratio(fy25['ca'], None, fy25['cl'])}  <- inventory not disclosed")
