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

st.header("Who built this")
st.markdown(
    "I am **Dishon Abuya**, an MSc Finance and Investment student with a Financial Machine Learning specialisation at the University of Dundee. "
    "I built GreenCRDB independently, without instruction from CRDB Bank, after reading CRDB's 2024 Sustainability Report and TCFD Report end to end. "
    "Researching the intersection of climate finance and credit risk in East African banking."
)

st.markdown("---")
st.header("The thesis")
st.markdown(
    "The biggest gap in CRDB's 2024 disclosure — Scope 3 Category 15 financed emissions — is also the biggest unmeasured credit-risk exposure on the loan book. "
    "High-emission borrowers face the steepest climate shocks. Those shocks become loan distress. Loan distress becomes credit risk. "
    "This is not a sustainability problem with credit-risk implications. It is a credit-risk problem with sustainability data. "
    "GreenCRDB demonstrates what closing that gap looks like operationally today."
)

st.markdown("---")
st.header("Why CRDB")
st.markdown(
    "CRDB is a useful case because the 2024 Sustainability Report gives enough concrete detail to build a serious demonstrator. "
    "The Group operates three banking subsidiaries: **CRDB Bank Plc in Tanzania**, **CRDB Bank Burundi S.A.**, and **CRDB Bank DR Congo S.A.** "
    "It has a **USD 300M five-year Medium-Term Note Programme**, with the **Kijani Bond** as the first tranche and the **Samia Infrastructure Bond** as the second."
)
st.markdown(
    "The same report says CRDB considers **8 of 15 Scope 3 categories** relevant, but only **Category 6 Business Travel** and **Category 7 Employee Commuting** are currently measured. "
    "Category 15 financed emissions are named as a future reporting priority. That is the disclosure gap GreenCRDB turns into an operational credit-risk workflow."
)
for item in [
    "**TACATDP:** USD 200M, split between USD 100M GCF funding and USD 100M co-financing.",
    "**Project GAIA:** USD 1.5B blended finance structure with MUFG Bank.",
    "**Financing partners:** 10 partners with TZS 1.47 trillion outstanding.",
    "**Green Asset Ratio:** 7% in 2024, targeting 15% by 2030 and 30% by 2050.",
]:
    st.markdown(f"- {item}")

st.markdown("---")
st.header("What I'm looking for")
st.markdown(
    "A 30-minute conversation with someone in the Sustainable Finance Unit or the Risk function. "
    "I share the screen and walk through the live demo. You tell me what works, what doesn't, and what would make this useful in real internal work. "
    "After the meeting, I send a one-page summary tailored to the priorities you raise."
)
st.markdown(
    "- **Email:** dishonabuyajr@gmail.com\n"
    "- **LinkedIn:** linkedin.com/in/dishon-abuya\n"
    "- **App:** greencrdb.streamlit.app"
)
