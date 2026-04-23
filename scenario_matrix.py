
# views/scenario_matrix.py

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from calculator import run_scenario


def run(client: dict):
    st.markdown("## Income Scenario Matrix")
    st.markdown(
        "How does the TCJA sunset impact clients across different income levels with "
        "a similar profile? This matrix helps advisors identify which client segments "
        "face the greatest exposure."
    )

    income_levels = [
        30000, 50000, 75000, 100000, 150000,
        200000, 300000, 500000, 750000, 1000000
    ]
    results = []

    for income in income_levels:
        r2025 = run_scenario(
            income, client["filing_status"], client["num_children"],
            client["itemized_deductions"], client["salt_paid"], "2025"
        )
        r2026 = run_scenario(
            income, client["filing_status"], client["num_children"],
            client["itemized_deductions"], client["salt_paid"], "2026_sunset"
        )
        delta = r2026["net_tax"] - r2025["net_tax"]
        pct = (delta / r2025["net_tax"] * 100) if r2025["net_tax"] > 0 else 0
        results.append({
            "Income": f"${income:,.0f}",
            "2025 Net Tax": r2025["net_tax"],
            "2026 Net Tax": r2026["net_tax"],
            "Dollar Increase": delta,
            "Pct Change": pct,
            "2025 Eff Rate": r2025["effective_rate"],
            "2026 Eff Rate": r2026["effective_rate"],
        })

    df = pd.DataFrame(results)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Income"], y=df["2025 Net Tax"],
        mode="lines+markers", name="2025 Law",
        line=dict(color="#1f3a5f", width=2),
    ))
    fig.add_trace(go.Scatter(
        x=df["Income"], y=df["2026 Net Tax"],
        mode="lines+markers", name="2026 Sunset",
        line=dict(color="#c0392b", width=2, dash="dash"),
    ))
    fig.update_layout(
        title="Net Federal Tax: 2025 vs. 2026 Across Income Levels",
        xaxis_title="Income Level",
        yaxis_title="Net Federal Tax ($)",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial", size=13),
        height=420,
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    st.plotly_chart(fig, use_container_width=True)

    fig2 = go.Figure(go.Bar(
        x=df["Income"],
        y=df["Dollar Increase"],
        marker_color=["#e74c3c" if v > 0 else "#2ecc71" for v in df["Dollar Increase"]],
        text=[f"${v:,.0f}" for v in df["Dollar Increase"]],
        textposition="outside",
    ))
    fig2.update_layout(
        title="Dollar Impact of TCJA Sunset by Income Level",
        xaxis_title="Income",
        yaxis_title="Additional Tax ($)",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial", size=13),
        height=400,
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### Full Scenario Table")
    display_df = df.copy()
    display_df["2025 Net Tax"] = display_df["2025 Net Tax"].apply(lambda x: f"${x:,.2f}")
    display_df["2026 Net Tax"] = display_df["2026 Net Tax"].apply(lambda x: f"${x:,.2f}")
    display_df["Dollar Increase"] = display_df["Dollar Increase"].apply(lambda x: f"${x:,.2f}")
    display_df["Pct Change"] = display_df["Pct Change"].apply(lambda x: f"{x:.1f}%")
    display_df["2025 Eff Rate"] = display_df["2025 Eff Rate"].apply(lambda x: f"{x:.2%}")
    display_df["2026 Eff Rate"] = display_df["2026 Eff Rate"].apply(lambda x: f"{x:.2%}")
    st.dataframe(display_df, use_container_width=True, hide_index=True)
