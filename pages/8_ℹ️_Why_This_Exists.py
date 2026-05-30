"""GreenCRDB — Why this exists."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st

import web_data as wd
from auth import require_login, sidebar_user_card

st.set_page_config(page_title="Why This Exists | GreenCRDB", page_icon="ℹ️", layout="wide")

require_login()
sidebar_user_card()

st.markdown(
    f"""
    <div style="background:{wd.CRDB_GREEN};padding:24px 30px;border-radius:10px;margin-bottom:22px;">
        <h1 style="color:white;margin:0;font-size:30px;">Why this exists</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("## Who built this")
st.markdown(
    "I am **Dishon Abuya**, an MSc Finance and Investment student with a Financial Machine Learning specialisation at the University of Dundee, graduating with Distinction. "
    "I am from Tanzania and currently work at Branston Ltd in Scotland in a sustainability and data analytics capacity."
)

st.markdown("---")
st.markdown("## Why CRDB specifically")
st.markdown(
    "I read CRDB's 2024 Sustainability Report end to end because CRDB is one of Tanzania's most important financial institutions and already has serious climate-finance commitments. "
    "While reading it, I identified six concrete disclosure and operational gaps around financed emissions, climate risk, green asset deployment, framework reporting, borrower-level ESG data, and group-level sustainability visibility. "
    "I built GreenCRDB to show one possible path to closing those gaps using a working Streamlit demonstrator rather than a static write-up."
)

st.markdown("---")
st.markdown("## What this demonstrates")
for item in [
    "PCAF Scope 3 Category 15 financed emissions estimation for a lending portfolio.",
    "A multi-framework reporting crosswalk across GRI, IFRS S1/S2, GCF PPMS, IFC, and Bank of Tanzania 2025 requirements.",
    "Pan-African GCF peer benchmarking against other accredited African banks.",
    "Sector-level physical climate risk scoring for Tanzanian lending exposure.",
    "Borrower ESG scoring and a climate-finance decision engine for simulated loan applications.",
]:
    st.markdown(f"- {item}")

st.markdown("---")
st.markdown("## What I'm looking for")
st.markdown(
    "I am looking for a 30-minute conversation with CRDB's sustainability or risk team to walk through the demo, test whether the gaps I identified are useful in practice, and hear what would need to change for this kind of tool to support real internal work. "
    "You can reach me at **dishonabuyajr@gmail.com**."
)
