"""Module 1 — Sector Climate Risk Engine"""
from __future__ import annotations

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

import web_data as wd
from auth import require_login, sidebar_user_card, can_access_module, can_enter_data, get_user, require_module_access, access_level_banner, can_export
from data_store import append_sector, get_entered_sectors, merge_with_processed

st.set_page_config(page_title="Sector Risk | GreenCRDB", page_icon="📊", layout="wide")

# ── Auth ──────────────────────────────────────────────────────────────────────
user = require_login()
sidebar_user_card()
require_module_access("sector_risk")
access_level_banner("sector_risk")

st.markdown(
    f'<div style="background:{wd.CRDB_GREEN};padding:14px 24px;border-radius:8px;margin-bottom:12px;">'
    '<h2 style="color:white;margin:0;font-size:22px;">📊 Module 1 — Sector Climate Risk Engine</h2>'
    '<p style="color:#c8e6c9;margin:2px 0 0 0;font-size:13px;">'
    "Weighted composite scoring across 5 climate hazards · 12 Tanzania sectors · IPCC AR6 / INFORM Risk Index"
    "</p></div>",
    unsafe_allow_html=True,
)
wd.render_crdb_finding(
    "Addresses CRDB 2024 Sustainability Report finding:",
    "Physical climate risk not quantified at sector level.",
)

@st.cache_data
def _load_data():
    return wd.sector_risk(), wd.regional()

sr_base, reg = _load_data()
sr = merge_with_processed(sr_base, "sectors", join_col="sector") if not sr_base.empty else sr_base

if sr.empty:
    st.error("Module 1 data not found. Run scripts/01_TZCRIP_Module1_Sector_Climate_Risk.py first.")
    st.stop()

# ── Sidebar filters ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📊 Sector Risk Filters")
    tier_opts = ["All"] + sr["risk_tier"].dropna().unique().tolist()
    selected_tier = st.selectbox("Filter by Risk Tier", tier_opts)
    show_table = st.checkbox("Show raw data table", value=False)

filtered = sr if selected_tier == "All" else sr[sr["risk_tier"] == selected_tier]

# ── Tabs ──────────────────────────────────────────────────────────────────────
tabs = ["📊 Dashboard", "✏️ Enter Climate Risk Data"] if can_enter_data("sector_risk") else ["📊 Dashboard"]
active_tabs = st.tabs(tabs)
tab_dash = active_tabs[0]
tab_enter = active_tabs[1] if len(active_tabs) > 1 else None

# ════════════════════════════════════════════════════════════════════════════
# DASHBOARD TAB
# ════════════════════════════════════════════════════════════════════════════
with tab_dash:
    c1, c2, c3, c4 = st.columns(4)
    high_crit = sr[sr["risk_tier"].isin(["High", "Critical"])]
    c1.metric("Sectors Analysed", len(sr))
    c2.metric("High / Critical Sectors", len(high_crit), f"{len(high_crit)/len(sr)*100:.0f}% of sectors")
    c3.metric("High/Critical Exposure", f"TZS {high_crit['loan_book_tzs_bn'].sum():,.0f} Bn")
    c4.metric("Avg Climate Risk Score", f"{sr['composite_climate_risk'].mean():.2f} / 10")

    st.markdown("---")

    col_a, col_b = st.columns([1, 1])

    with col_a:
        st.markdown("#### Financial Climate Risk by Sector")
        df_sorted = filtered.sort_values("financial_climate_risk", ascending=True)
        fig = px.bar(
            df_sorted,
            x="financial_climate_risk",
            y="sector",
            color="risk_tier",
            color_discrete_map=wd.RISK_COLOURS,
            category_orders={"risk_tier": ["Critical", "High", "Medium", "Low"]},
            orientation="h",
            text="financial_climate_risk",
            hover_data={"loan_book_tzs_bn": ":.0f", "num_borrowers": True},
            labels={
                "financial_climate_risk": "Risk Score (0–10)",
                "sector": "",
                "risk_tier": "Tier",
                "loan_book_tzs_bn": "Exposure (TZS Bn)",
                "num_borrowers": "Borrowers",
            },
        )
        fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        fig.update_layout(
            height=400,
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(l=10, r=50, t=10, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="right", x=1),
        )
        fig.add_vline(x=6.0, line_dash="dot", line_color="#e74c3c", annotation_text="High threshold")
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown("#### Climate Hazard Heatmap (5 Dimensions)")
        hazards = ["drought_risk", "flood_risk", "temperature_risk", "transition_risk", "water_stress_risk"]
        hazard_labels = ["Drought", "Flood", "Temperature", "Transition", "Water Stress"]
        heat_df = filtered.set_index("sector")[hazards].rename(columns=dict(zip(hazards, hazard_labels)))
        fig2 = px.imshow(
            heat_df,
            color_continuous_scale=[[0, "#2ecc71"], [0.45, "#f39c12"], [0.7, "#e74c3c"], [1, "#7b241c"]],
            zmin=0, zmax=10,
            text_auto=".1f",
            labels={"x": "Climate Hazard", "y": "Sector", "color": "Score"},
        )
        fig2.update_layout(
            height=400,
            margin=dict(l=10, r=10, t=10, b=10),
            coloraxis_colorbar=dict(title="Risk\nScore"),
        )
        st.plotly_chart(fig2, use_container_width=True)

    col_c, col_d = st.columns([1, 1])

    with col_c:
        st.markdown("#### Risk vs Exposure (Bubble = No. of Borrowers)")
        fig3 = px.scatter(
            filtered,
            x="composite_climate_risk",
            y="loan_book_tzs_bn",
            size="num_borrowers",
            color="risk_tier",
            color_discrete_map=wd.RISK_COLOURS,
            text="sector",
            hover_data={"composite_climate_risk": ":.2f", "loan_book_tzs_bn": ":.0f"},
            labels={
                "composite_climate_risk": "Composite Climate Risk (0–10)",
                "loan_book_tzs_bn": "Loan Book Exposure (TZS Bn)",
                "risk_tier": "Tier",
            },
        )
        fig3.update_traces(textposition="top center", textfont_size=10)
        fig3.update_layout(
            height=380,
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(l=10, r=10, t=10, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.01),
        )
        fig3.add_vline(x=6.0, line_dash="dot", line_color="#e74c3c", opacity=0.6)
        st.plotly_chart(fig3, use_container_width=True)

    with col_d:
        st.markdown("#### Regional Portfolio Climate Risk")
        if not reg.empty:
            reg_sorted = reg.sort_values("overall_climate_risk", ascending=True)
            fig4 = px.bar(
                reg_sorted,
                x="overall_climate_risk",
                y="region",
                color="overall_climate_risk",
                color_continuous_scale=[[0, "#2ecc71"], [0.5, "#f39c12"], [1, "#e74c3c"]],
                orientation="h",
                text="overall_climate_risk",
                hover_data={"exposure_tzs_bn": ":.0f", "portfolio_pct": ":.1f"},
                labels={
                    "overall_climate_risk": "Climate Risk Score (0–10)",
                    "region": "",
                    "exposure_tzs_bn": "Exposure (TZS Bn)",
                    "portfolio_pct": "Portfolio %",
                },
            )
            fig4.update_traces(texttemplate="%{text:.1f}", textposition="outside")
            fig4.update_layout(
                height=380,
                plot_bgcolor="white",
                paper_bgcolor="white",
                coloraxis_showscale=False,
                margin=dict(l=10, r=40, t=10, b=10),
            )
            st.plotly_chart(fig4, use_container_width=True)

    if show_table:
        st.markdown("#### Sector Risk Data Table")
        display_cols = [
            "sector", "risk_tier", "composite_climate_risk", "financial_climate_risk",
            "loan_book_tzs_bn", "loan_book_pct", "num_borrowers",
            "drought_risk", "flood_risk", "temperature_risk", "transition_risk", "water_stress_risk",
        ]
        available = [c for c in display_cols if c in filtered.columns]
        st.dataframe(
            filtered[available].sort_values("financial_climate_risk", ascending=False),
            use_container_width=True,
            hide_index=True,
        )

    # Entered records preview
    entered = get_entered_sectors()
    if not entered.empty:
        st.markdown("---")
        st.markdown(f"**{len(entered)} sector record(s) entered via web form** (merged into charts above)")
        st.dataframe(entered, use_container_width=True, hide_index=True)

# ════════════════════════════════════════════════════════════════════════════
# DATA ENTRY TAB
# ════════════════════════════════════════════════════════════════════════════
if tab_enter is not None:
    with tab_enter:
        st.markdown("### Enter Sector Climate Risk Scores")
        st.info("Scores you submit here are immediately merged into the dashboard charts above.")

        SECTORS = [
            "Agriculture", "Energy", "Manufacturing", "Mining",
            "Financial Services", "Tourism", "Real Estate", "Transport",
            "Healthcare", "Education", "Retail", "Construction",
        ]

        with st.form("sector_entry_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                sector = st.selectbox("Sector *", SECTORS)
                drought = st.slider("Drought Risk Score (0–10)", 0.0, 10.0, 5.0, 0.1)
                flood = st.slider("Flood Risk Score (0–10)", 0.0, 10.0, 5.0, 0.1)
                temperature = st.slider("Temperature Risk Score (0–10)", 0.0, 10.0, 5.0, 0.1)
            with col2:
                transition = st.slider("Transition Risk Score (0–10)", 0.0, 10.0, 5.0, 0.1)
                water_stress = st.slider("Water Stress Risk Score (0–10)", 0.0, 10.0, 5.0, 0.1)

                # Live composite preview
                weights = {"drought": 0.25, "flood": 0.20, "temperature": 0.20,
                           "transition": 0.20, "water_stress": 0.15}
                composite = (
                    drought * weights["drought"] + flood * weights["flood"] +
                    temperature * weights["temperature"] + transition * weights["transition"] +
                    water_stress * weights["water_stress"]
                )
                if composite >= 7.5:
                    tier = "Critical"
                elif composite >= 6.0:
                    tier = "High"
                elif composite >= 4.5:
                    tier = "Medium"
                else:
                    tier = "Low"

                st.markdown(
                    f'<div style="background:#f0f4f0;padding:14px;border-radius:8px;margin-top:8px;">'
                    f'<p style="margin:0;font-size:13px;"><b>Composite Climate Risk:</b> '
                    f'<span style="color:{wd.RISK_COLOURS.get(tier, "#888")};font-size:20px;font-weight:bold;">'
                    f'{composite:.2f}</span> / 10</p>'
                    f'<p style="margin:4px 0 0 0;font-size:13px;"><b>Risk Tier:</b> '
                    f'<span style="color:{wd.RISK_COLOURS.get(tier, "#888")};font-weight:bold;">{tier}</span></p>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

            submitted = st.form_submit_button("✅ Submit Sector Risk Data", type="primary", use_container_width=True)

        if submitted:
            record = {
                "sector": sector,
                "drought_risk": drought,
                "flood_risk": flood,
                "temperature_risk": temperature,
                "transition_risk": transition,
                "water_stress_risk": water_stress,
                "composite_climate_risk": round(composite, 2),
                "risk_tier": tier,
                "entered_by": user["name"],
                "entered_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            }
            append_sector(record)
            st.success(f"Sector risk data for **{sector}** saved. Risk tier: **{tier}** ({composite:.2f}/10)")
            st.rerun()

        existing = get_entered_sectors()
        if not existing.empty:
            st.markdown("---")
            st.markdown("#### Previously Entered Records")
            st.dataframe(existing, use_container_width=True, hide_index=True)
            st.download_button(
                "⬇ Download Entered Sector Data",
                existing.to_csv(index=False),
                file_name="entered_sector_risk.csv",
                mime="text/csv",
            )
