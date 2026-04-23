# TCJA Sunset Simulator

**A federal tax planning tool projecting the precise impact of TCJA expiration on client liability.**

---

## What Is This?

The Tax Cuts and Jobs Act (TCJA), signed into law in December 2017, dramatically restructured
individual federal income taxes. Lower rates, a near-doubled standard deduction, an expanded
child tax credit, and a $10,000 SALT cap were its defining features. Unless Congress acts,
every one of these provisions expires after December 31, 2025.

This simulator computes exactly what that means for a specific client -- in dollars, not generalities.

---

## Why Does It Matter Right Now?

This is the single most consequential tax planning event of the decade. Every CPA firm, every
financial planner, and every corporate tax department is having this conversation with clients
and leadership in 2025. The question is not whether this affects your clients -- it is by how
much, and what you should do before year-end.

This tool answers both questions.

---

## The Three Views

### Client Analysis
Enter a client profile -- filing status, AGI, dependents, itemized deductions, and SALT paid --
and receive a full side-by-side computation of 2025 versus 2026 liability. Every line item is
broken out: deduction strategy, personal exemptions restored under sunset, CTC reduction,
effective rate shift, and net dollar impact. Sourced from IRS Rev. Proc. 2024-40 and CBO
January 2024 projections.

### Income Scenario Matrix
Fixes the client filing profile and runs the 2025 vs. 2026 comparison across ten income levels
from $30,000 to $1,000,000. Surfaces which client segments face the greatest dollar and
percentage exposure. Designed for portfolio-level advisory conversations with practice leadership.

### Planning Actions
Generates a prioritized set of specific, implementable planning recommendations -- income
acceleration, retirement contribution maximization, SALT strategy for 2026, CTC mitigation,
and estate planning thresholds -- ranked by estimated impact and calibrated to the client
specific profile. Every recommendation is grounded in current IRS guidance and CBO projections.

---

## What Does This Tell Us?

For most middle and upper-middle income filers, the TCJA sunset represents a meaningful and
largely invisible tax increase. The standard deduction nearly halves. The top rate climbs from
37% to 39.6%. The CTC drops from $2,000 to $1,000 per child. Personal exemptions return --
but they do not offset the other losses for most filers.

High-income clients in high-tax states with significant SALT payments may actually benefit from
sunset in 2026, as the SALT cap expires along with the TCJA. This nuance is something most
clients do not know and most advisors have not modeled at the individual level. This tool makes
it visible.

---

## Data Sources

All tax parameters are sourced from authoritative government publications:

- 2025 law: IRS Revenue Procedure 2024-40 (inflation-adjusted TCJA parameters)
- 2026 sunset projections: Congressional Budget Office, January 2024 Budget and Economic Outlook
- Bracket reversion: Joint Committee on Taxation -- TCJA Expiration Analysis (JCX-49-22)
- Contribution limits: IRS Notice 2024-80

No third-party tax software or commercial data is used.

---

## Technical Stack

- Python -- tax law engine and scenario computation
- Streamlit -- interactive three-tab dashboard
- Plotly -- bar charts, line charts, and comparative visualizations
- Pandas -- tabular output and scenario matrix

---

*Built by Prakash Balasubramanian -- Mathematics and Statistics, UMBC | IRS VITA Certified Tax Preparer*
