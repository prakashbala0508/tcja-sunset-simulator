
# views/single_client.py

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from calculator import run_scenario


def run(client: dict):
    st.markdown("## Single Client Analysis")
    st.markdown(
        "Side-by-side federal tax liability comparison under 2025 current law "
        "versus projected 2026 post-TCJA sunset law. "
        "Sources: IRS Rev. Proc. 2024-40; CBO January 2024 Outlook; JCT JCX-49-22."
    )

    r2025 = run_scenario(
        client["agi"], client["filing_status"], client["num_children"],
        client["itemized_deductions"], client["salt_paid"], "2025"
    )
    r2026 = run_scenario(
        client["agi"], client["filing_status"], client["num_children"],
        client["itemized_deductions"], client["salt_paid"], "2026_sunset"
    )

    net_2025 = r2025.get("net_tax", 0)
    net_2026 = r2026.get("net_tax", 0)
    std_2025 = r2025.get("std_deduction", 0)
    std_2026 = r2026.get("std_deduction", 0)
    delta = net_2026 - net_2025
    pct = (delta / net_2025 * 100) if net_2025 > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("2025 Net Federal Tax", f"${net_2025:,.2f}", "Current Law")
    col2.metric("2026 Net Federal Tax (Sunset)", f"${net_2026:,.2f}", f"+${delta:,.2f} ({pct:.1f}%)")
    col3.metric(
        "Standard Deduction Change",
        f"${std_2025:,.0f} -> ${std_2026:,.0f}",
        f"-${std_2025 - std_2026:,.0f}"
    )

    fig = go.Figure()
    labels = [
        "AGI", "Deduction", "Personal Exemptions",
        "Taxable Income", "Gross Tax", "Child Tax Credit", "Net Tax"
    ]

    for result, name, color in [
        (r2025, "2025 Law", "#1f3a5f"),
        (r2026, "2026 Sunset", "#c0392b")
    ]:
        fig.add_trace(go.Bar(
            name=name,
            x=labels,
            y=[
                result.get("agi", client["agi"]),
                -result.get("deduction_used", 0),
                -result.get("personal_exemptions", 0),
                result.get("taxable_income", 0),
                result.get("gross_tax", 0),
                -result.get("child_tax_credit", 0),
                result.get("net_tax", 0),
            ],
            marker_color=color,
        ))

    fig.update_layout(
        barmode="group",
        title="Full Tax Computation: 2025 Law vs. 2026 Sunset",
        yaxis_title="Amount ($)",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial", size=13),
        height=450,
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Detailed Breakdown")
    rows = [
        ("Standard Deduction", f"${r2025.get('std_deduction', 0):,.0f}", f"${r2026.get('std_deduction', 0):,.0f}"),
        ("Deduction Used", f"${r2025.get('deduction_used', 0):,.0f} ({r2025.get('deduction_type', '')})", f"${r2026.get('deduction_used', 0):,.0f} ({r2026.get('deduction_type', '')})"),
        ("Personal Exemptions", "$0 (suspended under TCJA)", f"${r2026.get('personal_exemptions', 0):,.0f} (restored)"),
        ("SALT Cap", "$10,000", "Unlimited (cap expires)"),
        ("Taxable Income", f"${r2025.get('taxable_income', 0):,.0f}", f"${r2026.get('taxable_income', 0):,.0f}"),
        ("Gross Federal Tax", f"${r2025.get('gross_tax', 0):,.2f}", f"${r2026.get('gross_tax', 0):,.2f}"),
        ("Child Tax Credit", f"-${r2025.get('child_tax_credit', 0):,.2f}", f"-${r2026.get('child_tax_credit', 0):,.2f}"),
        ("Net Federal Tax Liability", f"${r2025.get('net_tax', 0):,.2f}", f"${r2026.get('net_tax', 0):,.2f}"),
        ("Effective Tax Rate", f"{r2025.get('effective_rate', 0):.2%}", f"{r2026.get('effective_rate', 0):.2%}"),
    ]

    df = pd.DataFrame(rows, columns=["Component", "2025 (Current Law)", "2026 (Sunset Law)"])
    st.dataframe(df, use_container_width=True, hide_index=True)
