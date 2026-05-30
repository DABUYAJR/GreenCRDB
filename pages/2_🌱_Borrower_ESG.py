"""Module 2 — Borrower ESG Scoring Engine"""
from __future__ import annotations

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

import plotly.express as px
import streamlit as st

import web_data as wd
from auth import require_login, sidebar_user_card, can_access_module, can_enter_data, get_user, require_module_access, access_level_banner, can_export, user_sectors, user_regions, filter_by_user, mask_sensitive_data
from data_store import append_borrower, get_entered_borrowers, merge_with_processed

st.set_page_config(page_title="Borrower ESG | GreenCRDB", page_icon="🌱", layout="wide")

# ── Auth ──────────────────────────────────────────────────────────────────────
user = require_login()
sidebar_user_card()
require_module_access("borrower_esg")
access_level_banner("borrower_esg")

st.markdown(
    '<div style="background:#1D9E75;padding:14px 24px;border-radius:8px;margin-bottom:12px;">'
    '<h2 style="color:white;margin:0;font-size:22px;">🌱 Module 2 — Borrower ESG Scoring Engine</h2>'
    '<p style="color:#d4ede7;margin:2px 0 0 0;font-size:13px;">'
    "E · S · G pillar scoring blended with sector climate risk · 60 simulated borrowers · 12 sectors · 10 Tanzania regions"
    "</p></div>",
    unsafe_allow_html=True,
)
wd.render_crdb_finding(
    "Addresses CRDB 2024 Sustainability Report finding:",
    "Unmeasured Scope 3 Category 15 financed emissions at borrower level.",
)
wd.render_gap_demonstration(
    "CRDB's 2024 Sustainability Report discloses Group operational emissions (Scope 1 and 2) but does not measure financed emissions. PCAF Scope 3 Category 15 — the dominant emissions category for any bank — is not implemented at borrower level. Without it, CRDB cannot accurately report its climate footprint or set science-based targets.",
    [
        "Borrower-level scoring on Environmental (40%), Social (30%), and Governance (30%) pillars on a 0–10 scale.",
        "Four-tier classification: Green Eligible (≥7.5), Standard (5.5–7.4), Watch List (4.0–5.4), High Risk (<4.0).",
        "PCAF Scope 3 Category 15 financed emissions calculation per borrower, attributed to CRDB by outstanding loan amount.",
        "Sector-filtered views and exportable borrower profiles.",
    ],
    [
        "ESG-linked pricing for Green Eligible borrowers becomes operational rather than aspirational.",
        "Quarterly PCAF Category 15 disclosure ready out of the box.",
        "Watch List borrowers flagged for active engagement rather than discovered after a default.",
    ],
)

# Load data and apply user portfolio restrictions
@st.cache_data
def _load_data():
    return wd.borrowers(), wd.class_summary(), wd.sector_esg()

bw_base, cs, se = _load_data()
bw_base = filter_by_user(bw_base)
bw = merge_with_processed(bw_base, "borrowers", join_col="borrower_id") if not bw_base.empty else bw_base

if bw.empty:
    st.error("Module 2 data not found. Run scripts/02_TZCRIP_Module2_Borrower_ESG_Scoring_Engine.py first.")
    st.stop()

# ── Sidebar filters ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🌱 ESG Filters")
    sectors = ["All"] + sorted(bw["sector"].unique().tolist())
    sel_sector = st.selectbox("Sector", sectors)

    regions = ["All"] + sorted(bw["region"].unique().tolist())
    sel_region = st.selectbox("Region", regions)

    classes = ["All"] + sorted(bw["classification"].unique().tolist())
    sel_class = st.selectbox("ESG Classification", classes)

    show_table = st.checkbox("Show borrower table", value=True)

# Apply sidebar filters
filtered = bw.copy()
if sel_sector != "All":
    filtered = filtered[filtered["sector"] == sel_sector]
if sel_region != "All":
    filtered = filtered[filtered["region"] == sel_region]
if sel_class != "All":
    filtered = filtered[filtered["classification"] == sel_class]

# ── Tabs ──────────────────────────────────────────────────────────────────────
tabs = ["🌱 Dashboard", "✏️ Enter Borrower ESG Data"] if can_enter_data("borrower_esg") else ["🌱 Dashboard"]
active_tabs = st.tabs(tabs)
tab_dash = active_tabs[0]
tab_enter = active_tabs[1] if len(active_tabs) > 1 else None

# ════════════════════════════════════════════════════════════════════════════
# DASHBOARD TAB
# ════════════════════════════════════════════════════════════════════════════
with tab_dash:
    c1, c2, c3, c4, c5 = st.columns(5)
    green_elig = filtered[filtered["classification"] == "Green Eligible"]
    high_risk = filtered[filtered["classification"] == "High Risk"]
    c1.metric("Borrowers Shown", len(filtered))
    c2.metric("Green Eligible", len(green_elig), f"TZS {green_elig['loan_size_tzs_mn'].sum():,.0f}Mn")
    c3.metric("Avg ESG Score", f"{filtered['esg_composite'].mean():.2f} / 10" if not filtered.empty else "—")
    c4.metric("Avg E Score", f"{filtered['E_score'].mean():.2f} / 10" if not filtered.empty else "—")
    c5.metric("High Risk", len(high_risk), f"TZS {high_risk['loan_size_tzs_mn'].sum():,.0f}Mn")

    st.markdown("---")

    col_a, col_b = st.columns([1, 1.4])

    with col_a:
        st.markdown("#### Borrower Classification Distribution")
        if not cs.empty:
            class_order = ["Green Eligible", "Standard", "Watch List", "High Risk"]
            fig = px.pie(
                cs,
                names="classification",
                values="borrowers",
                color="classification",
                color_discrete_map=wd.ESG_COLOURS,
                hole=0.45,
                category_orders={"classification": class_order},
            )
            fig.update_traces(textposition="outside", textinfo="percent+label", textfont_size=12)
            fig.update_layout(height=360, showlegend=False, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig, use_container_width=True)

            for _, row in cs.iterrows():
                colour = wd.ESG_COLOURS.get(row["classification"], "#888")
                st.markdown(
                    f'<span style="background:{colour};color:white;padding:3px 10px;'
                    f'border-radius:4px;font-size:12px;margin:2px;">'
                    f'{row["classification"]}: {int(row["borrowers"])} borrowers · '
                    f'TZS {row["total_exposure_tzs_mn"]:,.0f}Mn</span>',
                    unsafe_allow_html=True,
                )

    with col_b:
        st.markdown("#### ESG Score vs Sector Climate Risk")
        fig2 = px.scatter(
            filtered,
            x="sector_climate_risk",
            y="esg_composite",
            size="loan_size_tzs_mn",
            color="classification",
            color_discrete_map=wd.ESG_COLOURS,
            hover_data={
                "borrower_name": True, "sector": True, "region": True,
                "loan_size_tzs_mn": ":.1f", "esg_composite": ":.2f", "sector_climate_risk": ":.2f",
            },
            labels={
                "sector_climate_risk": "Sector Climate Risk (0–10)",
                "esg_composite": "ESG Composite Score (0–10)",
                "classification": "Classification",
                "loan_size_tzs_mn": "Loan (TZS Mn)",
            },
            size_max=35,
        )
        fig2.add_hline(y=5.5, line_dash="dot", line_color="#1D9E75", annotation_text="Green Eligible threshold")
        fig2.update_layout(
            height=360, plot_bgcolor="white", paper_bgcolor="white",
            margin=dict(l=10, r=10, t=10, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.01),
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("#### ESG Pillar Scores by Sector (Portfolio Averages)")
    if not se.empty:
        heat_data = se.set_index("sector")[["avg_E", "avg_S", "avg_G"]].rename(
            columns={"avg_E": "Environmental (E)", "avg_S": "Social (S)", "avg_G": "Governance (G)"}
        )
        fig3 = px.imshow(
            heat_data,
            color_continuous_scale=[[0, "#D85A30"], [0.4, "#EF9F27"], [0.65, "#378ADD"], [1, "#1D9E75"]],
            zmin=0, zmax=10,
            text_auto=".2f",
            labels={"x": "ESG Pillar", "y": "Sector", "color": "Score"},
            aspect="auto",
        )
        fig3.update_layout(
            height=380, margin=dict(l=10, r=10, t=10, b=10),
            coloraxis_colorbar=dict(title="Score\n(0–10)"),
        )
        st.plotly_chart(fig3, use_container_width=True)

    if show_table:
        st.markdown("#### Borrower Detail Table")
        display_cols = [
            "rank", "borrower_name", "sector", "region", "classification",
            "esg_composite", "E_score", "S_score", "G_score",
            "sector_climate_risk", "final_score", "loan_size_tzs_mn", "green_loan_eligible",
        ]
        available = [c for c in display_cols if c in filtered.columns]
        # Mask individual client identifiers for read-only roles (data analyst)
        masked_df = mask_sensitive_data(filtered[available], name_col="borrower_name")
        display_df = masked_df.rename(columns={
            "rank": "#", "borrower_name": "Borrower", "sector": "Sector", "region": "Region",
            "classification": "Class", "esg_composite": "ESG Score", "E_score": "E",
            "S_score": "S", "G_score": "G", "sector_climate_risk": "Climate Risk",
            "final_score": "Final Score", "loan_size_tzs_mn": "Loan (TZS Mn)",
            "green_loan_eligible": "Green?",
        }).sort_values("Final Score", ascending=False) if "final_score" in filtered.columns else masked_df
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "ESG Score": st.column_config.ProgressColumn("ESG Score", min_value=0, max_value=10, format="%.2f"),
                "Final Score": st.column_config.ProgressColumn("Final Score", min_value=0, max_value=10, format="%.2f"),
                "Green?": st.column_config.CheckboxColumn("Green Eligible"),
            },
        )
        if can_export():
            st.download_button(
                "⬇ Download Borrower ESG Data (CSV)",
                filtered[available].to_csv(index=False),
                file_name="GreenCRDB_Borrower_ESG_Filtered.csv",
                mime="text/csv",
            )
        else:
            st.caption("🔒 Export is not available for your role.")

    entered = get_entered_borrowers()
    if not entered.empty:
        st.markdown("---")
        st.info(f"{len(entered)} borrower record(s) entered via web form are merged into the dashboard above.")
        st.dataframe(entered, use_container_width=True, hide_index=True)

# ════════════════════════════════════════════════════════════════════════════
# DATA ENTRY TAB
# ════════════════════════════════════════════════════════════════════════════
if tab_enter is not None:
    with tab_enter:
        st.markdown("### Enter Borrower ESG Assessment")

        # Restrict sectors to user's portfolio
        user_sec = user_sectors()
        SECTORS = [
            "Agriculture", "Energy", "Manufacturing", "Mining",
            "Financial Services", "Tourism", "Real Estate", "Transport",
            "Healthcare", "Education", "Retail", "Construction",
        ]
        if user_sec != "all":
            SECTORS = [s for s in SECTORS if s in user_sec]

        REGIONS = [
            "Dar es Salaam", "Arusha", "Mwanza", "Dodoma", "Mbeya",
            "Zanzibar", "Tanga", "Morogoro", "Iringa", "Kigoma",
        ]
        user_reg = user_regions()
        if user_reg != "all":
            REGIONS = [r for r in REGIONS if r in user_reg]

        CLASSIFICATIONS = ["Green Eligible", "Standard", "Watch List", "High Risk"]

        import uuid
        with st.form("borrower_entry_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                borrower_name = st.text_input("Borrower Name *", placeholder="e.g. Kilimo Salama Ltd")
                sector = st.selectbox("Sector *", SECTORS)
                region = st.selectbox("Region *", REGIONS)
                loan_amount = st.number_input("Loan Amount (TZS Mn) *", min_value=1.0, max_value=50000.0, value=100.0, step=10.0)
            with col2:
                st.markdown("**Environmental (E) Sub-Scores**")
                env_emissions = st.slider("Emissions Management (0–10)", 0.0, 10.0, 5.0, 0.1)
                env_waste = st.slider("Waste & Pollution Control (0–10)", 0.0, 10.0, 5.0, 0.1)
                env_biodiversity = st.slider("Biodiversity & Land Use (0–10)", 0.0, 10.0, 5.0, 0.1)
                env_score = round((env_emissions + env_waste + env_biodiversity) / 3, 2)
                st.caption(f"Environmental Score: **{env_score:.2f} / 10**")

            col3, col4 = st.columns(2)
            with col3:
                st.markdown("**Social (S) Sub-Scores**")
                soc_labor = st.slider("Labor Standards (0–10)", 0.0, 10.0, 5.0, 0.1)
                soc_community = st.slider("Community Engagement (0–10)", 0.0, 10.0, 5.0, 0.1)
                soc_gender = st.slider("Gender Inclusion (0–10)", 0.0, 10.0, 5.0, 0.1)
                social_score = round((soc_labor + soc_community + soc_gender) / 3, 2)
                st.caption(f"Social Score: **{social_score:.2f} / 10**")
            with col4:
                st.markdown("**Governance (G) Sub-Scores**")
                gov_board = st.slider("Board Independence (0–10)", 0.0, 10.0, 5.0, 0.1)
                gov_transparency = st.slider("Reporting Transparency (0–10)", 0.0, 10.0, 5.0, 0.1)
                gov_anticorr = st.slider("Anti-Corruption Policies (0–10)", 0.0, 10.0, 5.0, 0.1)
                gov_score = round((gov_board + gov_transparency + gov_anticorr) / 3, 2)
                st.caption(f"Governance Score: **{gov_score:.2f} / 10**")

            # Live ESG composite
            esg_composite = round(env_score * 0.40 + social_score * 0.30 + gov_score * 0.30, 2)
            if esg_composite >= 6.5:
                auto_class = "Green Eligible"
                class_colour = "#1D9E75"
            elif esg_composite >= 5.0:
                auto_class = "Standard"
                class_colour = "#2563EB"
            elif esg_composite >= 3.5:
                auto_class = "Watch List"
                class_colour = "#D97706"
            else:
                auto_class = "High Risk"
                class_colour = "#D85A30"

            st.markdown(
                f'<div style="background:#f0f4f0;padding:14px;border-radius:8px;margin:8px 0;">'
                f'<b>ESG Composite Score: <span style="font-size:22px;color:{class_colour};">{esg_composite:.2f}</span> / 10 &nbsp;|&nbsp; '
                f'Classification: <span style="color:{class_colour};font-weight:bold;">{auto_class}</span></b>'
                f'<br><small style="color:#666;">E×40% + S×30% + G×30% · Override classification below if required.</small>'
                f'</div>',
                unsafe_allow_html=True,
            )

            override_class = st.selectbox(
                "Classification (override auto-classification if needed)",
                CLASSIFICATIONS,
                index=CLASSIFICATIONS.index(auto_class),
            )
            notes = st.text_area("Officer Notes", placeholder="Add any relevant observations or IFC PS compliance notes...")

            submitted = st.form_submit_button("✅ Submit Borrower ESG Assessment", type="primary", use_container_width=True)

        if submitted and borrower_name.strip():
            record = {
                "borrower_id": str(uuid.uuid4())[:8].upper(),
                "borrower_name": borrower_name.strip(),
                "sector": sector,
                "region": region,
                "loan_amount_tzs_mn": loan_amount,
                "env_score": env_score,
                "social_score": social_score,
                "governance_score": gov_score,
                "esg_composite": esg_composite,
                "classification": override_class,
                "officer_notes": notes,
                "entered_by": user["name"],
                "entered_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            }
            append_borrower(record)
            st.success(f"Borrower **{borrower_name}** saved. ESG: {esg_composite:.2f}/10 · {override_class}")
            st.rerun()
        elif submitted:
            st.warning("Borrower name is required.")

        existing = get_entered_borrowers()
        if not existing.empty:
            st.markdown("---")
            st.markdown("#### Previously Entered Borrowers")
            st.dataframe(existing, use_container_width=True, hide_index=True)
            st.download_button(
                "⬇ Download Entered Borrower Data",
                existing.to_csv(index=False),
                file_name="entered_borrower_esg.csv",
                mime="text/csv",
            )
