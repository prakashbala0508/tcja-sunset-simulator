
# engine/calculator.py
# Core federal tax computation logic applying 2025 and 2026 sunset parameters.

from tax_law import (
    TAX_BRACKETS, STANDARD_DEDUCTION, CHILD_TAX_CREDIT,
    SALT_CAP, PERSONAL_EXEMPTION_2026
)


def compute_tax(taxable_income: float, year: str, filing_status: str) -> float:
    """
    Marginal rate federal income tax calculation.
    Applies bracket structure for the specified year and filing status.
    """
    brackets = TAX_BRACKETS[year][filing_status]
    tax = 0.0
    prev = 0.0
    for limit, rate in brackets:
        if taxable_income <= prev:
            break
        taxable_at_rate = min(taxable_income, limit) - prev
        tax += taxable_at_rate * rate
        prev = limit
    return round(tax, 2)


def compute_ctc(agi: float, year: str, filing_status: str, num_children: int) -> float:
    """
    Estimates Child Tax Credit based on AGI, filing status, and year.
    Source: IRC Section 24; TCJA sunset from CBO January 2024 projections.
    """
    ctc = CHILD_TAX_CREDIT[year]
    phase_out = ctc["phase_out_mfj"] if filing_status == "married_filing_jointly" else ctc["phase_out_single"]
    if agi > phase_out:
        reduction = ((agi - phase_out) // 2000) * 50
        credit = max(0, ctc["per_child"] * num_children - reduction)
    else:
        credit = ctc["per_child"] * num_children
    return round(credit, 2)


def run_scenario(
    agi: float,
    filing_status: str,
    num_children: int,
    itemized_deductions: float,
    salt_paid: float,
    year: str,
) -> dict:
    """
    Full tax scenario computation for a given year and client profile.
    Returns a detailed breakdown dict for display and comparison.
    """
    std_ded = STANDARD_DEDUCTION[year][filing_status]

    salt_cap = SALT_CAP[year]
    if salt_cap is not None:
        effective_salt = min(salt_paid, salt_cap)
        itemized_adjusted = itemized_deductions - salt_paid + effective_salt
    else:
        itemized_adjusted = itemized_deductions
        effective_salt = salt_paid

    personal_exemptions = 0.0
    if year == "2026_sunset":
        exemption_count = 1
        if filing_status == "married_filing_jointly":
            exemption_count = 2
        exemption_count += num_children
        personal_exemptions = PERSONAL_EXEMPTION_2026 * exemption_count

    deduction_used = max(itemized_adjusted, std_ded)
    deduction_type = "Itemized" if itemized_adjusted > std_ded else "Standard"

    taxable_income = max(0, agi - deduction_used - personal_exemptions)
    gross_tax = compute_tax(taxable_income, year, filing_status)
    ctc = compute_ctc(agi, year, filing_status, num_children)
    net_tax = max(0, gross_tax - ctc)
    effective_rate = net_tax / agi if agi > 0 else 0

    return {
        "year": year,
        "std_deduction": std_ded,
        "itemized_adjusted": itemized_adjusted,
        "deduction_used": deduction_used,
        "deduction_type": deduction_type,
        "personal_exemptions": personal_exemptions,
        "taxable_income": taxable_income,
        "gross_tax": gross_tax,
        "child_tax_credit": ctc,
        "net_tax": net_tax,
        "effective_rate": effective_rate,
        "salt_cap": salt_cap,
        "effective_salt": effective_salt,
    }
