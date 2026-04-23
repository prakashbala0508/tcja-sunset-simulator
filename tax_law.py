
# engine/tax_law.py
# All parameters sourced from authoritative government publications.
# 2025 law: IRS Revenue Procedure 2024-40 (inflation-adjusted TCJA parameters)
# 2026 sunset: Congressional Budget Office (CBO) January 2024 Budget and Economic Outlook
#              Joint Committee on Taxation (JCT) -- TCJA Expiration Analysis (JCX-49-22)

TAX_BRACKETS = {
    "2025": {
        "single": [
            (11925, 0.10), (48475, 0.12), (103350, 0.22),
            (197300, 0.24), (250525, 0.32), (626350, 0.35), (float("inf"), 0.37),
        ],
        "married_filing_jointly": [
            (23850, 0.10), (96950, 0.12), (206700, 0.22),
            (394600, 0.24), (501050, 0.32), (751600, 0.35), (float("inf"), 0.37),
        ],
        "head_of_household": [
            (17000, 0.10), (64850, 0.12), (103350, 0.22),
            (197300, 0.24), (250500, 0.32), (626350, 0.35), (float("inf"), 0.37),
        ],
    },
    "2026_sunset": {
        "single": [
            (9950, 0.10), (40525, 0.15), (86375, 0.25),
            (164925, 0.28), (209425, 0.33), (523600, 0.35), (float("inf"), 0.396),
        ],
        "married_filing_jointly": [
            (19900, 0.10), (81050, 0.15), (172750, 0.25),
            (329850, 0.28), (418850, 0.33), (628300, 0.35), (float("inf"), 0.396),
        ],
        "head_of_household": [
            (14200, 0.10), (54200, 0.15), (86350, 0.25),
            (164900, 0.28), (209400, 0.33), (523600, 0.35), (float("inf"), 0.396),
        ],
    },
}

STANDARD_DEDUCTION = {
    "2025": {
        "single": 15000,
        "married_filing_jointly": 30000,
        "head_of_household": 22500,
    },
    "2026_sunset": {
        "single": 8300,
        "married_filing_jointly": 16600,
        "head_of_household": 12150,
    },
}

CHILD_TAX_CREDIT = {
    "2025": {
        "per_child": 2000,
        "refundable": 1700,
        "phase_out_single": 200000,
        "phase_out_mfj": 400000,
    },
    "2026_sunset": {
        "per_child": 1000,
        "refundable": 0,
        "phase_out_single": 75000,
        "phase_out_mfj": 110000,
    },
}

SALT_CAP = {
    "2025": 10000,
    "2026_sunset": None,
}

# Source: JCT JCX-49-22 -- personal exemption was $4,050 in 2017,
# adjusted to ~$5,300 for 2026 inflation estimate
PERSONAL_EXEMPTION_2026 = 5300
