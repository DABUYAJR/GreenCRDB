"""Module 3 — Climate Finance Decision Engine"""
from __future__ import annotations

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

import web_data as wd
from auth import require_login, sidebar_user_card, can_access_module, can_enter_data, get_user, require_module_access, access_level_banner, can_export, filter_by_user, mask_sensitive_data
from data_store import append_decision, get_entered_decisions

st.set_page_config(page_title="Finance Decisions | GreenCRDB", page_icon="💡", layout="wide")

# ── Auth ──────────────────────────────────────────────────────────────────────
user = require_login()
sidebar_user_card()
require_module_access("finance_decisions")
access_level_banner("finance_decisions")

st.markdown(
    '<div style="background:#2563EB;padding:14px 24px;border-radius:8px;margin-bottom:12px;">'
    '<h2 style="color:white;margin:0;font-size:22px;">💡 Module 3 — Climate Finance Decision Engine</h2>'
    '<p style="color:#bfdbfe;margin:2px 0 0 0;font-size:13px;">'
    "TCFD framework · IFC Performance Standards · Green Finance Pipeline · Climate Scenario Analysis"
    "</p></div>",
    unsafe_allow_html=True,
)

dec_full = wd.decisions()
gp_full = wd.green_pipeline()
tc = wd.tcfd()
sc = wd.scenarios()
ic = wd.ifc()
_gar_actual = wd.CRDB_TARGETS["green_asset_ratio_2024_actual"]   # 7.0%
_gar_2030 = wd.CRDB_TARGETS["green_asset_ratio_2030"]            # 15.0%
_gar_2050 = wd.CRDB_TARGETS["green_asset_ratio_2050"]            # 30.0%

if dec_full.empty:
    st.error("Module 3 data not found. Run scripts/03_TZCRIP_Module3_Climate_Finance_Decision_Engine.py first.")
    st.stop()

# Apply portfolio restriction: ESG officers only see their assigned sectors/regions
dec = filter_by_user(dec_full)
gp = filter_by_user(gp_full)

# Mask individual borrower names for read-only roles (data analyst)
dec = mask_sensitive_data(dec, name_col="borrower_name", id_col="borrower_id")
gp = mask_sensitive_data(gp, name_col="borrower_name")

# ── Tabs ──────────────────────────────────────────────────────────────────────
tabs = ["💡 Dashboard", "✏️ Record Lending Decision"] if can_enter_data("finance_decisions") else ["💡 Dashboard"]
active_tabs = st.tabs(tabs)
tab_dash = active_tabs[0]
tab_enter = active_tabs[1] if len(active_tabs) > 1 else None

# ════════════════════════════════════════════════════════════════════════════
# DASHBOARD TAB
# ════════════════════════════════════════════════════════════════════════════
with tab_dash:
    approve = dec[dec["decision"] == "Approve"]
    conditional = dec[dec["decision"] == "Conditional Approval"]
    decline = dec[dec["decision"] == "Decline"]

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Applications", len(dec))
    c2.metric("Approve", len(approve), f"{len(approve)/len(dec)*100:.0f}% approval rate")
    c3.metric("Conditional Approval", len(conditional))
    c4.metric("Decline", len(decline))
    c5.metric(
        "Green Pipeline",
        f"TZS {gp['loan_size_tzs_mn'].sum():,.0f}Mn" if not gp.empty else "—",
        f"{len(gp)} borrowers" if not gp.empty else "",
    )

    # ── Green Asset Ratio progress tracker ───────────────────────────────────
    st.markdown(
        f'<div style="background:linear-gradient(90deg,{wd.CRDB_GREEN}18,{wd.CRDB_GREEN}08);'
        f'border:1px solid {wd.CRDB_GREEN}44;border-radius:10px;padding:12px 18px;margin:8px 0;">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">'
        f'<b style="font-size:13px;">🌿 Green Asset Ratio Journey (2024 → 2030 → 2050)</b>'
        f'<span style="font-size:11px;color:#555;">Source: CRDB 2024 Integrated Annual Report</span>'
        f'</div>'
        f'<div style="display:flex;align-items:center;gap:12px;">'
        f'<span style="font-size:11px;color:#888;width:60px;">0%</span>'
        f'<div style="flex:1;background:#e5e7eb;border-radius:8px;height:22px;position:relative;">'
        f'<div style="background:{wd.CRDB_GREEN};height:22px;width:{_gar_actual/_gar_2050*100:.0f}%;border-radius:8px;'
        f'display:flex;align-items:center;padding-left:8px;">'
        f'<span style="color:white;font-size:11px;font-weight:bold;">{_gar_actual:.0f}% (2024 Actual)</span>'
        f'</div>'
        f'<div style="position:absolute;top:0;left:{_gar_2030/_gar_2050*100:.0f}%;height:22px;border-left:3px dashed #D97706;"></div>'
        f'</div>'
        f'<span style="font-size:11px;color:#888;width:40px;">30%</span>'
        f'</div>'
        f'<div style="display:flex;justify-content:space-between;font-size:11px;color:#555;margin-top:4px;">'
        f'<span></span>'
        f'<span style="color:#D97706;">🎯 15% by 2030</span>'
        f'<span>30% by 2050</span>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")

    col_a, col_b = st.columns([1, 1.4])

    with col_a:
        st.markdown("#### Lending Decision Distribution")
        decision_counts = dec["decision"].value_counts().reset_index()
        decision_counts.columns = ["Decision", "Count"]
        order = ["Approve", "Conditional Approval", "Review Required", "Decline"]
        decision_counts["_order"] = decision_counts["Decision"].map({d: i for i, d in enumerate(order)})
        decision_counts = decision_counts.sort_values("_order")
        fig = px.bar(
            decision_counts, x="Decision", y="Count",
            color="Decision", color_discrete_map=wd.DECISION_COLOURS, text="Count",
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(
            height=360, showlegend=False, plot_bgcolor="white", paper_bgcolor="white",
            margin=dict(l=10, r=10, t=10, b=10), xaxis_tickangle=-15,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown("#### Decision Drivers: ESG vs Climate Risk")
        fig2 = px.scatter(
            dec, x="sector_risk_score", y="esg_score", color="decision",
            color_discrete_map=wd.DECISION_COLOURS,
            hover_data={"borrower_id": True, "composite_decision_score": ":.1f"},
            labels={
                "sector_risk_score": "Sector Risk Score (0–100, lower=better)",
                "esg_score": "ESG Score (0–100)", "decision": "Decision",
            },
            opacity=0.75,
        )
        fig2.update_layout(
            height=360, plot_bgcolor="white", paper_bgcolor="white",
            margin=dict(l=10, r=10, t=10, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.01),
        )
        fig2.add_hline(y=55, line_dash="dot", line_color="#1D9E75", annotation_text="Approve threshold (ESG axis)")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    col_c, col_d = st.columns([1.6, 1])

    with col_c:
        st.markdown("#### Green Finance Pipeline")
        if not gp.empty:
            st.dataframe(
                gp.sort_values("loan_size_tzs_mn", ascending=False),
                use_container_width=True, hide_index=True,
                column_config={
                    "esg_composite": st.column_config.ProgressColumn("ESG Score", min_value=0, max_value=10, format="%.2f"),
                    "final_score": st.column_config.ProgressColumn("Final Score", min_value=0, max_value=10, format="%.2f"),
                    "loan_size_tzs_mn": st.column_config.NumberColumn("Loan (TZS Mn)", format="%.1f"),
                },
            )
            if can_export():
                st.download_button(
                    "⬇ Download Green Pipeline (CSV)",
                    gp.to_csv(index=False),
                    file_name="GreenCRDB_Green_Pipeline.csv",
                    mime="text/csv",
                )
            else:
                st.caption("🔒 Export is not available for your role.")

    with col_d:
        st.markdown("#### Recommended Product Mix")
        if not gp.empty:
            prod_counts = gp["product_recommendation"].value_counts().reset_index()
            prod_counts.columns = ["Product", "Count"]
            fig3 = px.pie(
                prod_counts, names="Product", values="Count",
                color_discrete_sequence=["#1D9E75", "#3B82F6", "#F59E0B", "#8B5CF6"],
                hole=0.4,
            )
            fig3.update_traces(textposition="outside", textinfo="percent+label", textfont_size=11)
            fig3.update_layout(height=360, showlegend=False, margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")
    st.markdown("#### Climate Scenario Analysis — Three Pathways")
    if not sc.empty:
        col_e, col_f = st.columns([1.4, 1])
        colours = {"Base case": "#3B82F6", "Accelerated transition": "#F59E0B", "Severe physical shock": "#D85A30"}
        with col_e:
            fig4 = px.bar(
                sc, x="Scenario", y="Est. credit loss TZS Bn", color="Scenario",
                color_discrete_map=colours, text="Est. credit loss TZS Bn",
                labels={"Est. credit loss TZS Bn": "Credit Loss (TZS Bn)"},
            )
            fig4.update_traces(texttemplate="TZS %{text:,.1f}Bn", textposition="outside")
            fig4.update_layout(
                height=320, showlegend=False, plot_bgcolor="white", paper_bgcolor="white",
                margin=dict(l=10, r=10, t=10, b=10),
            )
            st.plotly_chart(fig4, use_container_width=True)

        with col_f:
            for _, row in sc.iterrows():
                colour = colours.get(row["Scenario"], "#888")
                st.markdown(
                    f'<div style="background:{colour};color:white;padding:12px;border-radius:8px;margin:6px 0;">'
                    f'<b>{row["Scenario"]}</b><br>'
                    f'<span style="font-size:12px;">{row["Description"]}</span><br><br>'
                    f'Portfolio Impact: <b>{row["Est. portfolio impact (%)"]:.1f}%</b><br>'
                    f'Credit Loss: <b>TZS {row["Est. credit loss TZS Bn"]:,.1f} Bn</b>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

    st.markdown("---")
    col_g, col_h = st.columns([1, 1])

    with col_g:
        st.markdown("#### TCFD Key Metrics")
        if not tc.empty:
            for _, row in tc.iterrows():
                st.markdown(
                    f'<div style="display:flex;justify-content:space-between;padding:6px 12px;'
                    f'border-left:4px solid {wd.CRDB_GREEN};background:#f9fafb;margin:3px 0;border-radius:0 4px 4px 0;">'
                    f'<span style="font-size:13px;">{row["TCFD Metric"]}</span>'
                    f'<b style="color:{wd.CRDB_GREEN};font-size:13px;">{row["Portfolio Value"]}</b>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

    with col_h:
        st.markdown("#### IFC Performance Standards Alignment")
        if not ic.empty:
            align_colour = {"Full": "#1D9E75", "Adequate": "#378ADD", "Partial": "#EF9F27", "Insufficient": "#D85A30"}
            fig5 = px.bar(
                ic, x="portfolio_score", y="title", color="alignment_tier",
                color_discrete_map=align_colour, orientation="h", text="portfolio_score",
                labels={"portfolio_score": "Portfolio Score (0–10)", "title": "", "alignment_tier": "Alignment"},
                hover_data={"key_gap": True, "sectors_at_risk": True},
            )
            fig5.update_traces(texttemplate="%{text:.2f}", textposition="outside")
            fig5.update_layout(
                height=320, plot_bgcolor="white", paper_bgcolor="white",
                margin=dict(l=10, r=50, t=10, b=10),
                legend=dict(orientation="h", yanchor="bottom", y=1.01),
            )
            fig5.add_vline(x=5.0, line_dash="dot", line_color="#888", annotation_text="Minimum threshold")
            st.plotly_chart(fig5, use_container_width=True)

    entered = get_entered_decisions()
    if not entered.empty:
        st.markdown("---")
        st.info(f"{len(entered)} lending decision(s) recorded via web form.")
        st.dataframe(entered, use_container_width=True, hide_index=True)

# ════════════════════════════════════════════════════════════════════════════
# DATA ENTRY TAB
# ════════════════════════════════════════════════════════════════════════════
if tab_enter is not None:
    with tab_enter:
        st.markdown("### Record Green Finance Lending Decision")
        st.info("Use this form to confirm, modify, or override system-generated lending decisions.")

        SECTORS = [
            "Agriculture", "Energy", "Manufacturing", "Mining",
            "Financial Services", "Tourism", "Real Estate", "Transport",
            "Healthcare", "Education", "Retail", "Construction",
        ]
        REGIONS = [
            "Dar es Salaam", "Arusha", "Mwanza", "Dodoma", "Mbeya",
            "Zanzibar", "Tanga", "Morogoro", "Iringa", "Kigoma",
        ]
        DECISIONS = ["Approve", "Conditional Approval", "Review Required", "Decline"]
        PRODUCTS = [
            "Green Bond (GCF-Aligned)",
            "Sustainability-Linked Loan (SLL)",
            "Climate Resilience Facility",
            "Angaza Loan (Solar Energy Financing)",
            "Nishati Safi Loan (LPG/Biogas — Clean Cooking)",
            "Recycle Loan (Waste-to-Materials)",
            "Renewable Energy Project Finance",
            "Al-Barakah Islamic Finance (Sharia-Compliant)",
            "Standard Commercial Loan",
            "Microfinance (Climate Adaptation)",
            "GCF TACATDP Concessional Facility",
        ]

        with st.form("decision_entry_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                borrower_id = st.text_input("Borrower ID *", placeholder="e.g. BW-042")
                borrower_name = st.text_input("Borrower Name *", placeholder="e.g. TanzaSolar Ltd")
                sector = st.selectbox("Sector *", SECTORS)
                region = st.selectbox("Region *", REGIONS)
                loan_amount = st.number_input("Loan Amount (TZS Mn) *", min_value=1.0, value=500.0, step=50.0)
            with col2:
                esg_score = st.slider("Borrower ESG Score (0–100)", 0, 100, 60)
                sector_risk = st.slider("Sector Climate Risk Score (0–100, lower=better readiness)", 0, 100, 45)
                composite = round(0.55 * esg_score + 0.45 * (100 - sector_risk), 1)
                auto_decision = (
                    "Approve" if composite >= 65
                    else "Conditional Approval" if composite >= 52
                    else "Review Required" if composite >= 40
                    else "Decline"
                )
                decision_colour = wd.DECISION_COLOURS.get(auto_decision, "#888")
                st.markdown(
                    f'<div style="background:#f0f4f0;padding:12px;border-radius:8px;margin:8px 0;">'
                    f'<b>Composite Decision Score: <span style="font-size:20px;">{composite:.1f}</span> / 100</b><br>'
                    f'<b>System Decision: <span style="color:{decision_colour};font-size:16px;">{auto_decision}</span></b>'
                    f'<br><small style="color:#666;">ESG×55% + Sector Readiness×45%</small>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
                final_decision = st.selectbox(
                    "Final Decision (override if required)",
                    DECISIONS,
                    index=DECISIONS.index(auto_decision),
                )
                green_eligible = st.checkbox("Mark as Green Finance Eligible", value=composite >= 65)
                esms_cleared = st.checkbox("ESMS Cleared (IFC Environmental & Social Management System)", value=True,
                                           help="IFC Performance Standards PS1–PS8 screened. Required for GCF/DFI co-financed loans.")
                product_type = st.selectbox("Recommended Product", PRODUCTS)

            notes = st.text_area("Officer Notes / Conditions", placeholder="Add approval conditions, IFC PS gaps, or required covenants...")
            submitted = st.form_submit_button("✅ Record Lending Decision", type="primary", use_container_width=True)

        if submitted and borrower_name.strip() and borrower_id.strip():
            record = {
                "borrower_id": borrower_id.strip().upper(),
                "borrower_name": borrower_name.strip(),
                "sector": sector,
                "region": region,
                "loan_amount_tzs_mn": loan_amount,
                "esg_composite": esg_score / 10,
                "composite_decision_score": composite,
                "decision": final_decision,
                "green_eligible": green_eligible,
                "esms_cleared": esms_cleared,
                "product_type": product_type,
                "officer_notes": notes,
                "entered_by": user["name"],
                "entered_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            }
            append_decision(record)
            st.success(f"Decision recorded: **{borrower_name}** → **{final_decision}** (score: {composite:.1f})")
            st.rerun()
        elif submitted:
            st.warning("Borrower ID and Borrower Name are required.")

        existing = get_entered_decisions()
        if not existing.empty:
            st.markdown("---")
            st.markdown("#### Recorded Decisions")
            st.dataframe(existing, use_container_width=True, hide_index=True)
            st.download_button(
                "⬇ Download Recorded Decisions",
                existing.to_csv(index=False),
                file_name="entered_lending_decisions.csv",
                mime="text/csv",
            )
