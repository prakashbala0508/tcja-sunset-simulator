
# app.py -- TCJA Sunset Simulator

import streamlit as st
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "engine"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "views"))

import single_client
import scenario_matrix
import planning_actions

st.set_page_config(
    page_title="TCJA Sunset Simulator",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <div style="background-color:#7b1a1a;padding:24px 32px 16px 32px;border-radius:8px;margin-bottom:24px;">
        <h1 style="color:white;margin:0;font-family:Arial;font-size:28px;">TCJA Sunset Simulator</h1>
        <p style="color:#f0b0b0;margin:6px 0 0 0;font-size:14px;">
        2025 vs. 2026 Federal Tax Liability &middot; TCJA Expiration Planning Tool
        &middot; Powered by CBO and JCT Projections
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "The Tax Cuts and Jobs Act provisions expire after December 31, 2025. "
    "This tool projects the precise dollar impact on your client under current 2025 law "
    "versus post-sunset 2026 law, identifies which clients face the greatest exposure, "
    "and generates specific planning actions ranked by impact."
)

with st.sidebar:
    st.markdown("## Client Profile")
    filing_status = st.selectbox(
        "Filing Status",
        ["single", "married_filing_jointly", "head_of_household"],
        format_func=lambda x: x.replace("_", " ").title(),
    )
    agi = st.number_input(
        "Adjusted Gross Income (AGI)",
        min_value=0, max_value=10000000, value=150000, step=5000
    )
    num_children = st.number_input(
        "Number of Qualifying Children",
        min_value=0, max_value=10, value=2, step=1
    )
    itemized_deductions = st.number_input(
        "Total Itemized Deductions (pre-SALT cap)",
        min_value=0, value=18000, step=1000
    )
    salt_paid = st.number_input(
        "State and Local Taxes (SALT) Paid",
        min_value=0, value=12000, step=500
    )

client = {
    "filing_status": filing_status,
    "agi": agi,
    "num_children": num_children,
    "itemized_deductions": itemized_deductions,
    "salt_paid": salt_paid,
}

tab1, tab2, tab3 = st.tabs(["Client Analysis", "Income Scenario Matrix", "Planning Actions"])

with tab1:
    single_client.run(client)
with tab2:
    scenario_matrix.run(client)
with tab3:
    planning_actions.run(client)

st.markdown(
    """
    <div style="margin-top:40px;padding:12px;background:#f4f6f9;border-radius:6px;font-size:11px;color:#888;">
    Data sources: IRS Revenue Procedure 2024-40 &middot; CBO January 2024 Budget and Economic Outlook
    &middot; Joint Committee on Taxation JCX-49-22 &middot; IRS Notice 2024-80.
    All projections assume no Congressional action prior to the scheduled sunset.
    Estimates are for planning purposes only and do not constitute tax advice.
    </div>
    """,
    unsafe_allow_html=True,
)
