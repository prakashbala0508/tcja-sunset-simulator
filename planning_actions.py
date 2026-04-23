
# views/planning_actions.py

import streamlit as st
from calculator import run_scenario


def run(client: dict):
    st.markdown("## Planning Action Recommendations")
    st.markdown(
        "Based on this client profile and projected TCJA sunset exposure, "
        "the following planning actions are ranked by estimated impact. "
        "All recommendations reflect standard year-end and multi-year tax planning "
        "strategies consistent with current IRS guidance."
    )

    r2025 = run_scenario(
        client["agi"], client["filing_status"], client["num_children"],
        client["itemized_deductions"], client["salt_paid"], "2025"
    )
    r2026 = run_scenario(
        client["agi"], client["filing_status"], client["num_children"],
        client["itemized_deductions"], client["salt_paid"], "2026_sunset"
    )

    delta = r2026["net_tax"] - r2025["net_tax"]
    agi = client["agi"]
    filing_status = client["filing_status"]
    salt_paid = client["salt_paid"]

    actions = []

    if delta > 500:
        actions.append({
            "priority": "High",
            "action": "Accelerate Taxable Income into 2025",
            "rationale": (
                f"Client faces a projected ${delta:,.2f} increase in 2026. "
                "Pulling bonuses, Roth conversions, or capital gains realizations "
                "into 2025 locks in the lower current-law rates."
            ),
            "impact": "Varies -- proportional to income accelerated",
        })

    if agi > 100000:
        actions.append({
            "priority": "High",
            "action": "Maximize Pre-Tax Retirement Contributions (2025)",
            "rationale": (
                "401(k), 403(b), and IRA contributions reduce 2025 AGI and defer "
                "income past the sunset cliff. Particularly valuable for clients "
                "in the 22-35% current brackets."
            ),
            "impact": "Up to $23,500 reduction in 2025 AGI (IRS Notice 2024-80)",
        })

    if salt_paid > 10000 and r2026["deduction_type"] == "Itemized":
        actions.append({
            "priority": "Moderate",
            "action": "Model SALT Deduction Strategy for 2026",
            "rationale": (
                "The $10,000 SALT cap expires under sunset law, restoring unlimited "
                "SALT deductions. Clients in high-tax states who currently itemize "
                "may benefit significantly in 2026."
            ),
            "impact": f"Potential deduction increase of ${salt_paid - 10000:,.0f} in 2026",
        })

    if client["num_children"] > 0:
        ctc_loss = r2025["child_tax_credit"] - r2026["child_tax_credit"]
        if ctc_loss > 0:
            actions.append({
                "priority": "Moderate",
                "action": "Plan Around Child Tax Credit Reduction",
                "rationale": (
                    f"CTC drops from $2,000 to $1,000 per child under sunset law, "
                    f"a ${ctc_loss:,.0f} reduction for this client. Review dependent "
                    "care FSA and other child-related benefit strategies."
                ),
                "impact": f"${ctc_loss:,.0f} additional liability from CTC reduction alone",
            })

    if agi > 400000:
        actions.append({
            "priority": "High",
            "action": "Review Estate and Gift Tax Exposure",
            "rationale": (
                "The TCJA doubled the estate and gift tax exemption. Under sunset, "
                "this reverts to approximately $7M per individual. High-net-worth "
                "clients should review gifting strategies before year-end 2025."
            ),
            "impact": "Significant for estates approaching the $7M threshold",
        })

    if not actions:
        st.success(
            "Based on this client profile, TCJA sunset exposure is limited. "
            "Standard year-end review is sufficient."
        )
        return

    for i, action in enumerate(actions, 1):
        color = "#e74c3c" if action["priority"] == "High" else "#f39c12"
        st.markdown(
            f"""
            <div style="border-left:4px solid {color};padding:12px 16px;
            margin-bottom:16px;background:#fafafa;border-radius:4px;">
                <strong style="color:{color};">
                [{action["priority"]} Priority] Action {i}: {action["action"]}
                </strong><br>
                <span style="font-size:13px;color:#333;">{action["rationale"]}</span><br>
                <span style="font-size:12px;color:#666;margin-top:4px;display:block;">
                <em>Estimated Impact: {action["impact"]}</em></span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div style="padding:12px;background:#eaf4fb;border-radius:6px;
        font-size:11px;color:#555;margin-top:16px;">
        These recommendations are for planning purposes only and should be reviewed
        by a licensed CPA before implementation. Tax law is subject to Congressional
        action prior to the scheduled sunset date.
        </div>
        """,
        unsafe_allow_html=True,
    )
