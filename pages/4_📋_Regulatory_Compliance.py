"""Module 4 — Regulatory Compliance, PCAF & Portfolio Temperature Alignment"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd

import web_data as wd
from auth import require_login, sidebar_user_card, require_module_access

st.set_page_config(page_title="Regulatory | GreenCRDB", page_icon="📋", layout="wide")

# ── Auth ──────────────────────────────────────────────────────────────────────
require_login()
sidebar_user_card()
require_module_access("regulatory")

st.markdown(
    '<div style="background:#D97706;padding:14px 24px;border-radius:8px;margin-bottom:12px;">'
    '<h2 style="color:white;margin:0;font-size:22px;">📋 Module 4 — Regulatory Compliance & PCAF Analytics</h2>'
    '<p style="color:#fef3c7;margin:2px 0 0 0;font-size:13px;">'
    "Bank of Tanzania 2025 Guidelines · PCAF Financed Emissions (Scope 3) · "
    "Portfolio Temperature Alignment · SASB FN-CB · PRB · UN SDG Mapping"
    "</p></div>",
    unsafe_allow_html=True,
)

@st.cache_data
def _load_data():
    return wd.financed_emissions_df(), wd.portfolio_itr(), wd.green_asset_ratio_current()

fe, itr, gar_current = _load_data()
fr = wd.FINANCIAL_RATIOS

# ── KPI row ───────────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)
total_fe = fe["financed_emissions_ktco2e"].sum() if not fe.empty else 0
c1.metric("Portfolio ITR", f"{itr:.2f} °C", f"{itr - 1.5:.2f}°C above 1.5°C target", delta_color="inverse")
c2.metric("Financed Emissions", f"{total_fe:,.0f} ktCO₂e", "PCAF Scope 3 Category 15")
c3.metric("Green Asset Ratio", f"{gar_current:.0f}%", f"Target: {wd.CRDB_TARGETS['green_asset_ratio_2030']:.0f}% by 2030 · 2024 Actual")
c4.metric("BoT 2025 Compliance", "12 / 13 items", "1 in progress", delta_color="off")
c5.metric("Moody's Rating", fr["moodys_rating"], f"Stable · prev {fr['moodys_prev_rating']} · first TZ bank B1")

st.markdown("---")

# ── BoT Regulatory Buffer Dashboard ───────────────────────────────────────────
st.markdown("#### 🏛️ BoT Prudential Ratios — 2024 Actual vs Regulatory Requirements")
st.caption("Source: CRDB Bank 2024 Integrated Annual Report (actual) · Bank of Tanzania Prudential Guidelines")

reg_cols = st.columns(5)
reg_metrics = [
    ("CAR (Total)", fr["car_total_pct"], fr["bot_min_car_total"], "Higher = better", "#1D9E75"),
    ("CAR (Tier 1)", fr["car_tier1_pct"], fr["bot_min_car_tier1"], "Higher = better", "#1D9E75"),
    ("Liquidity", fr["liquidity_ratio_pct"], fr["bot_min_liquidity"], "Higher = better", "#1D9E75"),
    ("NPL Ratio", fr["npl_ratio_pct"], fr["bot_max_npl"], "Lower = better", "#1D9E75"),
    ("CIR", fr["cir_pct"], fr["bot_max_cir"], "Lower = better", "#1D9E75"),
]
for col, (label, actual, limit, direction, colour) in zip(reg_cols, reg_metrics):
    if direction == "Higher = better":
        buffer = actual - limit
        delta_str = f"+{buffer:.1f}% above min {limit}%"
    else:
        buffer = limit - actual
        delta_str = f"{buffer:.1f}% below limit {limit}%"
    col.metric(f"{label}", f"{actual}%", delta_str)

st.markdown("---")

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_bot, tab_pcaf, tab_sasb, tab_prb, tab_sdg, tab_mat, tab_social, tab_tnfd = st.tabs([
    "🏛️ BoT 2025 Compliance",
    "🌡️ PCAF Emissions",
    "📊 SASB FN-CB",
    "🤝 PRB Principles",
    "🌐 UN SDGs",
    "⬡ Materiality Matrix",
    "🤝 Social Impact & iMBEJU",
    "🌿 TNFD Readiness",
])

# ── TAB 1: BoT 2025 Compliance ─────────────────────────────────────────────────
with tab_bot:
    st.markdown("#### Bank of Tanzania Guidelines on Climate-Related Financial Risks (2025)")
    st.markdown(
        "Climate risk reporting is now **mandatory** for all licensed banks in Tanzania under the "
        "Bank of Tanzania Guidelines 2025, aligned to TCFD / ISSB S2 framework."
    )

    bot_df = pd.DataFrame(wd.BOT_COMPLIANCE)
    status_colours = {"Compliant": "#1D9E75", "In Progress": "#F59E0B", "Planned": "#D85A30"}

    for pillar in bot_df["Pillar"].unique():
        st.markdown(f"**{pillar}**")
        pillar_df = bot_df[bot_df["Pillar"] == pillar]
        for _, row in pillar_df.iterrows():
            colour = status_colours.get(row["Status"], "#888")
            icon = "✅" if row["Status"] == "Compliant" else "🔄" if row["Status"] == "In Progress" else "📋"
            st.markdown(
                f'<div style="display:flex;align-items:flex-start;gap:10px;padding:8px 12px;'
                f'background:#f9fafb;border-left:4px solid {colour};border-radius:0 6px 6px 0;margin:4px 0;">'
                f'<span style="font-size:16px;min-width:20px;">{icon}</span>'
                f'<div style="flex:1;">'
                f'<div style="display:flex;justify-content:space-between;">'
                f'<span style="font-size:13px;font-weight:600;">{row["Requirement"]}</span>'
                f'<span style="background:{colour};color:white;padding:2px 8px;border-radius:10px;font-size:11px;">'
                f'{row["Status"]}</span>'
                f'</div>'
                f'<p style="font-size:12px;color:#555;margin:2px 0 0 0;">{row["Evidence"]}</p>'
                f'</div></div>',
                unsafe_allow_html=True,
            )

    compliant = len(bot_df[bot_df["Status"] == "Compliant"])
    total = len(bot_df)
    st.markdown(f"\n**Summary:** {compliant}/{total} requirements fully compliant · {total - compliant} in progress")

# ── TAB 2: PCAF Financed Emissions ────────────────────────────────────────────
with tab_pcaf:
    st.markdown("#### PCAF Scope 3 Category 15 — Simulated Financed Emissions")
    st.info(
        "**Methodology:** IPCC AR6 Africa sector emission intensity proxies. "
        "PCAF Data Quality Score: **4** (economic-activity-based estimates — standard for emerging markets). "
        "This is CRDB's acknowledged gap in its 2024 TCFD Report; this module provides a pathway to full PCAF compliance."
    )

    col_a, col_b = st.columns([1.4, 1])
    with col_a:
        if not fe.empty:
            fig_fe = px.bar(
                fe,
                x="financed_emissions_ktco2e",
                y="sector",
                color="risk_tier",
                color_discrete_map=wd.RISK_COLOURS,
                orientation="h",
                text="financed_emissions_ktco2e",
                labels={
                    "financed_emissions_ktco2e": "Financed Emissions (ktCO₂e)",
                    "sector": "",
                    "risk_tier": "Risk Tier",
                },
                title="Financed Emissions by Sector (ktCO₂e)",
            )
            fig_fe.update_traces(texttemplate="%{text:,.1f}", textposition="outside")
            fig_fe.update_layout(
                height=420,
                plot_bgcolor="white",
                paper_bgcolor="white",
                margin=dict(l=10, r=60, t=40, b=10),
                legend=dict(orientation="h", y=1.08),
            )
            st.plotly_chart(fig_fe, use_container_width=True)

    with col_b:
        st.markdown("##### PCAF Attribution Summary")
        if not fe.empty:
            total_fe_val = fe["financed_emissions_ktco2e"].sum()
            for _, row in fe.head(6).iterrows():
                pct = row["financed_emissions_ktco2e"] / total_fe_val * 100
                colour = wd.RISK_COLOURS.get(row["risk_tier"], "#888")
                st.markdown(
                    f'<div style="margin:6px 0;">'
                    f'<div style="display:flex;justify-content:space-between;font-size:12px;">'
                    f'<span>{row["sector"]}</span>'
                    f'<span style="color:{colour};font-weight:bold;">{row["financed_emissions_ktco2e"]:,.1f} ktCO₂e ({pct:.1f}%)</span>'
                    f'</div>'
                    f'<div style="background:#e5e7eb;border-radius:4px;height:8px;margin-top:2px;">'
                    f'<div style="background:{colour};height:8px;border-radius:4px;width:{pct:.1f}%;"></div>'
                    f'</div></div>',
                    unsafe_allow_html=True,
                )
            st.markdown(f"**Total Portfolio: {total_fe_val:,.0f} ktCO₂e**")

        st.markdown("---")
        st.markdown("##### PCAF Data Quality Framework")
        quality_items = [
            ("Score 1", "Verified GHG data from borrower", "Best"),
            ("Score 2", "Reported but unverified data", "Good"),
            ("Score 3", "Physical activity-based estimates", "Moderate"),
            ("Score 4", "Economic proxy — **current level**", "Acceptable"),
            ("Score 5", "Regional/national average factors", "Minimal"),
        ]
        for score, desc, level in quality_items:
            is_current = "current level" in desc
            bg = f"background:{wd.CRDB_GREEN};" if is_current else ""
            colour = "color:white;" if is_current else ""
            st.markdown(
                f'<div style="{bg}padding:4px 10px;border-radius:4px;margin:2px 0;font-size:12px;">'
                f'<span style="{colour}"><b>{score}</b> — {desc}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("---")
    st.markdown("#### Portfolio Temperature Alignment — Implied Temperature Rise (ITR)")
    col_itr1, col_itr2 = st.columns([1, 1.5])

    with col_itr1:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=itr,
            delta={"reference": 1.5, "suffix": "°C vs Paris", "increasing": {"color": "#D85A30"}},
            number={"suffix": " °C", "font": {"size": 42, "color": "#1a1a1a"}},
            title={"text": "Portfolio Implied Temperature Rise (ITR)<br><span style='font-size:13px;color:#888;'>Simulated · NGFS Pathways · PACTA Methodology</span>"},
            gauge={
                "axis": {"range": [1.5, 4.0], "ticksuffix": "°C", "tickfont": {"size": 11}},
                "bar": {"color": "#D85A30" if itr > 2.5 else "#EF9F27", "thickness": 0.3},
                "bgcolor": "white",
                "steps": [
                    {"range": [1.5, 2.0], "color": "#d4edda", "name": "1.5°C aligned"},
                    {"range": [2.0, 3.0], "color": "#fff3cd"},
                    {"range": [3.0, 4.0], "color": "#f8d7da"},
                ],
                "threshold": {
                    "line": {"color": wd.CRDB_GREEN, "width": 6},
                    "thickness": 0.8,
                    "value": 1.5,
                },
            },
        ))
        fig_gauge.update_layout(height=300, margin=dict(l=30, r=30, t=80, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col_itr2:
        st.markdown("##### Sector ITR Contribution")
        if not wd.sector_risk().empty:
            sr = wd.sector_risk()
            itr_rows = []
            for _, row in sr.iterrows():
                delta = wd.SECTOR_ITR_DELTA.get(row["sector"], 1.0)
                weight = row["loan_book_tzs_bn"] / sr["loan_book_tzs_bn"].sum()
                itr_rows.append({
                    "sector": row["sector"],
                    "ITR (°C)": round(1.5 + delta, 1),
                    "Portfolio Weight (%)": round(weight * 100, 1),
                    "Weighted Contribution (°C)": round(delta * weight, 3),
                    "risk_tier": row["risk_tier"],
                })
            itr_df = pd.DataFrame(itr_rows).sort_values("Weighted Contribution (°C)", ascending=False)

            fig_itr_bar = px.bar(
                itr_df,
                x="sector",
                y="ITR (°C)",
                color="risk_tier",
                color_discrete_map=wd.RISK_COLOURS,
                text="ITR (°C)",
                labels={"sector": "", "ITR (°C)": "Sector ITR (°C)"},
            )
            fig_itr_bar.add_hline(y=1.5, line_dash="dash", line_color=wd.CRDB_GREEN,
                                   annotation_text="Paris 1.5°C target", annotation_position="top right")
            fig_itr_bar.update_traces(texttemplate="%{text:.1f}°C", textposition="outside")
            fig_itr_bar.update_layout(
                height=300,
                showlegend=False,
                plot_bgcolor="white",
                paper_bgcolor="white",
                margin=dict(l=10, r=10, t=10, b=80),
                xaxis_tickangle=-45,
            )
            st.plotly_chart(fig_itr_bar, use_container_width=True)

# ── TAB 3: SASB FN-CB ─────────────────────────────────────────────────────────
with tab_sasb:
    st.markdown("#### SASB Commercial Banks Standard (FN-CB) — Five Disclosure Topics")
    st.markdown(
        "The SASB FN-CB standard identifies the five most material ESG topics for commercial banks. "
        "Maintained by the IFRS Foundation (acquired SASB 2022). Used by MSCI, Sustainalytics, and "
        "international investors as the benchmark for bank ESG disclosure quality."
    )

    status_c = {"Strong": "#1D9E75", "Adequate": "#378ADD", "Developing": "#EF9F27", "Insufficient": "#D85A30"}

    for topic, data in wd.SASB_METRICS.items():
        colour = status_c.get(data["status"], "#888")
        score_pct = data["score"] / 5.0 * 100
        st.markdown(
            f'<div style="background:#f9fafb;border:1px solid #e5e7eb;border-left:5px solid {colour};'
            f'padding:14px;border-radius:0 8px 8px 0;margin:8px 0;">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;">'
            f'<h4 style="margin:0;font-size:15px;">{topic}</h4>'
            f'<span style="background:{colour};color:white;padding:3px 12px;border-radius:12px;font-size:12px;">'
            f'{data["status"]}</span>'
            f'</div>'
            f'<p style="margin:6px 0 8px 0;font-size:13px;color:#555;">{data["note"]}</p>'
            f'<div style="background:#e5e7eb;border-radius:8px;height:10px;">'
            f'<div style="background:{colour};height:10px;border-radius:8px;width:{score_pct:.0f}%;"></div>'
            f'</div>'
            f'<div style="display:flex;justify-content:space-between;font-size:11px;color:#888;margin-top:2px;">'
            f'<span>0</span><span style="color:{colour};font-weight:bold;">Score: {data["score"]:.1f}/5.0</span><span>5.0</span>'
            f'</div></div>',
            unsafe_allow_html=True,
        )

    sasb_avg = sum(d["score"] for d in wd.SASB_METRICS.values()) / len(wd.SASB_METRICS)
    st.markdown(f"\n**Overall SASB FN-CB Score: {sasb_avg:.2f} / 5.0**  ·  Simulated · Framework: IFRS Foundation / SASB")

# ── TAB 4: PRB Principles ─────────────────────────────────────────────────────
with tab_prb:
    st.markdown("#### Principles for Responsible Banking (UNEP FI)")
    st.markdown(
        "The PRB framework (350+ signatory banks, ~50% of global banking assets) requires banks to "
        "align their strategy with the Paris Agreement and UN SDGs, set SMART targets, and report annually. "
        "CRDB Bank is positioned to become a PRB signatory — this assessment models the current readiness."
    )

    col_prb1, col_prb2 = st.columns([1, 1])
    with col_prb1:
        categories = list(wd.PRB_SCORES.keys())
        values = list(wd.PRB_SCORES.values())
        fig_r = go.Figure()
        fig_r.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill="toself",
            fillcolor="rgba(0, 107, 60, 0.2)",
            line=dict(color=wd.CRDB_GREEN, width=2),
            name="CRDB Score",
        ))
        fig_r.add_trace(go.Scatterpolar(
            r=[5.0] * (len(categories) + 1),
            theta=categories + [categories[0]],
            fill=None,
            line=dict(color="#ddd", width=1, dash="dot"),
            name="Maximum",
        ))
        fig_r.add_trace(go.Scatterpolar(
            r=[3.0] * (len(categories) + 1),
            theta=categories + [categories[0]],
            fill=None,
            line=dict(color="#f39c12", width=1, dash="dot"),
            name="PRB Minimum",
        ))
        fig_r.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 5], tickvals=[1, 2, 3, 4, 5])),
            showlegend=True,
            legend=dict(orientation="h", y=-0.2),
            height=400,
            margin=dict(l=60, r=60, t=40, b=60),
        )
        st.plotly_chart(fig_r, use_container_width=True)

    with col_prb2:
        st.markdown("##### Pillar-by-Pillar Assessment")
        prb_descs = {
            "Alignment": "Align business strategy to Paris Agreement and UN SDGs",
            "Impact & Targets": "Set and publish SMART sustainability performance targets",
            "Clients & Customers": "Work with clients to enable sustainable behaviours",
            "Stakeholders": "Engage stakeholders on sustainability themes",
            "Governance & Culture": "Embed sustainability in governance and culture",
            "Transparency": "Be accountable and transparent on progress",
        }
        for pillar, score in wd.PRB_SCORES.items():
            colour = "#1D9E75" if score >= 4.0 else "#EF9F27" if score >= 3.0 else "#D85A30"
            pct = score / 5.0 * 100
            st.markdown(
                f'<div style="margin:8px 0;">'
                f'<div style="display:flex;justify-content:space-between;font-size:13px;">'
                f'<b>{pillar}</b>'
                f'<span style="color:{colour};">{score:.1f} / 5.0</span>'
                f'</div>'
                f'<p style="font-size:11px;color:#777;margin:1px 0 3px 0;">{prb_descs[pillar]}</p>'
                f'<div style="background:#e5e7eb;border-radius:4px;height:8px;">'
                f'<div style="background:{colour};height:8px;border-radius:4px;width:{pct:.0f}%;"></div>'
                f'</div></div>',
                unsafe_allow_html=True,
            )
        prb_avg = sum(wd.PRB_SCORES.values()) / len(wd.PRB_SCORES)
        st.markdown(f"\n**Overall PRB Readiness Score: {prb_avg:.2f} / 5.0**")
        st.success("CRDB is above the 3.0/5.0 minimum threshold across all pillars. Recommended next step: formal PRB signatory application.")

# ── TAB 5: SDG Alignment ──────────────────────────────────────────────────────
with tab_sdg:
    st.markdown("#### UN Sustainable Development Goals — Portfolio Alignment")
    st.markdown(
        "Mapping CRDB Bank's lending portfolio to the UN SDGs most relevant to a Tanzanian commercial bank. "
        "SDG reporting is required by DFI partners (GCF, AfDB, Proparco) and increasingly by international investors."
    )

    sdg_df = pd.DataFrame([
        {"SDG": k, "Score": v["score"], "Activity": v["activity"]}
        for k, v in wd.SDG_ALIGNMENT.items()
    ])

    col_sdg1, col_sdg2 = st.columns([1.2, 1])
    with col_sdg1:
        sdg_colours = {row["SDG"]: (
            "#1D9E75" if row["Score"] >= 4.0 else
            "#378ADD" if row["Score"] >= 3.5 else
            "#EF9F27" if row["Score"] >= 3.0 else "#D85A30"
        ) for _, row in sdg_df.iterrows()}

        fig_sdg = px.bar(
            sdg_df.sort_values("Score"),
            x="Score",
            y="SDG",
            color="Score",
            color_continuous_scale=[[0, "#D85A30"], [0.4, "#EF9F27"], [0.65, "#378ADD"], [1, "#1D9E75"]],
            orientation="h",
            text="Score",
            labels={"Score": "Alignment Score (0–5)", "SDG": ""},
            range_color=[2.5, 5.0],
        )
        fig_sdg.update_traces(texttemplate="%{text:.1f}", textposition="outside")
        fig_sdg.update_layout(
            height=400,
            plot_bgcolor="white",
            paper_bgcolor="white",
            coloraxis_showscale=False,
            margin=dict(l=10, r=60, t=10, b=10),
        )
        fig_sdg.add_vline(x=3.0, line_dash="dot", line_color="#888", annotation_text="Baseline")
        st.plotly_chart(fig_sdg, use_container_width=True)

    with col_sdg2:
        for sdg, data in wd.SDG_ALIGNMENT.items():
            score = data["score"]
            colour = "#1D9E75" if score >= 4.0 else "#378ADD" if score >= 3.5 else "#EF9F27" if score >= 3.0 else "#D85A30"
            st.markdown(
                f'<div style="padding:6px 10px;border-left:3px solid {colour};background:#f9fafb;margin:4px 0;border-radius:0 4px 4px 0;">'
                f'<div style="display:flex;justify-content:space-between;font-size:12px;">'
                f'<b>{sdg}</b><span style="color:{colour};">{score:.1f}/5</span>'
                f'</div>'
                f'<p style="font-size:11px;color:#666;margin:1px 0 0 0;">{data["activity"]}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )

# ── TAB 6: Materiality Matrix ──────────────────────────────────────────────────
with tab_mat:
    st.markdown("#### Double Materiality Matrix")
    st.markdown(
        "Double materiality assesses both **financial materiality** (how ESG issues affect CRDB financially) "
        "and **impact materiality** (how CRDB's activities affect the environment and society). "
        "Required under ISSB S1/S2 and the EU CSRD framework."
    )

    materiality_data = [
        {"Issue": "Agricultural Climate Risk", "Financial Materiality": 4.8, "Impact Materiality": 4.5, "size": 40, "category": "Environmental"},
        {"Issue": "Financed GHG Emissions", "Financial Materiality": 3.9, "Impact Materiality": 4.7, "size": 35, "category": "Environmental"},
        {"Issue": "Biodiversity Loss", "Financial Materiality": 2.8, "Impact Materiality": 4.2, "size": 25, "category": "Environmental"},
        {"Issue": "Financial Inclusion", "Financial Materiality": 3.5, "Impact Materiality": 4.6, "size": 38, "category": "Social"},
        {"Issue": "Gender Equality", "Financial Materiality": 2.9, "Impact Materiality": 4.0, "size": 28, "category": "Social"},
        {"Issue": "Labour Practices", "Financial Materiality": 3.1, "Impact Materiality": 3.8, "size": 24, "category": "Social"},
        {"Issue": "Data Security", "Financial Materiality": 4.5, "Impact Materiality": 3.2, "size": 30, "category": "Governance"},
        {"Issue": "Business Ethics", "Financial Materiality": 4.6, "Impact Materiality": 3.9, "size": 32, "category": "Governance"},
        {"Issue": "Transition Risk (Energy)", "Financial Materiality": 4.1, "Impact Materiality": 3.7, "size": 33, "category": "Environmental"},
        {"Issue": "Physical Climate Risk", "Financial Materiality": 4.3, "Impact Materiality": 4.4, "size": 36, "category": "Environmental"},
        {"Issue": "Water Stress", "Financial Materiality": 3.6, "Impact Materiality": 4.1, "size": 27, "category": "Environmental"},
        {"Issue": "Community Relations", "Financial Materiality": 2.7, "Impact Materiality": 3.5, "size": 22, "category": "Social"},
    ]
    mat_df = pd.DataFrame(materiality_data)

    cat_colours = {
        "Environmental": "#1D9E75",
        "Social": "#378ADD",
        "Governance": "#7C3AED",
    }

    fig_mat = px.scatter(
        mat_df,
        x="Financial Materiality",
        y="Impact Materiality",
        size="size",
        color="category",
        color_discrete_map=cat_colours,
        text="Issue",
        labels={
            "Financial Materiality": "Financial Materiality → (Impact on CRDB Bank)",
            "Impact Materiality": "Impact Materiality → (CRDB's impact on society/environment)",
            "category": "ESG Category",
        },
        size_max=40,
    )
    fig_mat.update_traces(textposition="top center", textfont_size=10)
    fig_mat.add_vline(x=3.5, line_dash="dot", line_color="#ccc")
    fig_mat.add_hline(y=3.5, line_dash="dot", line_color="#ccc")
    fig_mat.add_annotation(x=4.6, y=4.6, text="Priority Action Zone", showarrow=False,
                            font=dict(color="#D85A30", size=11), bgcolor="#fff")
    fig_mat.update_layout(
        height=500,
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=10, r=10, t=20, b=10),
        xaxis=dict(range=[2.0, 5.5]),
        yaxis=dict(range=[2.5, 5.2]),
        legend=dict(orientation="h", y=-0.1),
    )
    st.plotly_chart(fig_mat, use_container_width=True)
    st.caption(
        "Priority Action Zone (top-right): Issues with high financial AND impact materiality require immediate management and disclosure. "
        "Simulated · ISSB S1/S2 · ESRS double materiality framework"
    )

# ── TAB 7: Social Impact & iMBEJU ────────────────────────────────────────────
with tab_social:
    si = wd.SOCIAL_IMPACT
    st.markdown("#### iMBEJU Community Investment Programme — 2024 Actual")
    st.markdown(
        "CRDB Bank's **iMBEJU** programme is the flagship corporate social investment initiative. "
        "In 2024, CRDB invested **TZS 7.76 Bn** across 153 community projects — "
        "directly reaching **218,471 beneficiaries** across Tanzania. "
        "iMBEJU directly advances SDG 1, 2, 3, 4, and 13."
    )

    ki1, ki2, ki3, ki4 = st.columns(4)
    ki1.metric("Total CSI Investment", f"TZS {si['imbeju_investment_tzs_bn']:.2f} Bn", "2024 Actual")
    ki2.metric("Beneficiaries", f"{si['imbeju_beneficiaries']:,}", "Direct community impact")
    ki3.metric("Projects Funded", si['imbeju_projects'], "153 community projects")
    ki4.metric("Focus Pillars", len(si['imbeju_focus_areas']), "Education, Health, Environment, Livelihoods")

    st.markdown("---")
    st.markdown("#### iMBEJU Investment by Pillar")
    imbeju_data = [
        {"Pillar": "Education", "TZS Bn": si["education_investment_tzs_bn"], "colour": "#2563EB"},
        {"Pillar": "Healthcare", "TZS Bn": si["healthcare_investment_tzs_bn"], "colour": "#D97706"},
        {"Pillar": "Community Livelihoods", "TZS Bn": si["livelihoods_investment_tzs_bn"], "colour": "#1D9E75"},
        {"Pillar": "Environmental Conservation", "TZS Bn": si["environment_investment_tzs_bn"], "colour": "#059669"},
    ]
    for item in imbeju_data:
        pct = item["TZS Bn"] / si["imbeju_investment_tzs_bn"] * 100
        st.markdown(
            f'<div style="margin:8px 0;">'
            f'<div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:3px;">'
            f'<b>{item["Pillar"]}</b>'
            f'<span style="color:{item["colour"]};font-weight:bold;">TZS {item["TZS Bn"]:.2f} Bn ({pct:.0f}%)</span>'
            f'</div>'
            f'<div style="background:#e5e7eb;border-radius:6px;height:14px;">'
            f'<div style="background:{item["colour"]};height:14px;border-radius:6px;width:{pct:.0f}%;"></div>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("#### Human Capital & Workforce Diversity (2024 Actual)")
    hc1, hc2, hc3, hc4, hc5, hc6 = st.columns(6)
    hc1.metric("Total Employees", f"{si['employees_total']:,}", "Group — TZ + Burundi + Congo")
    hc2.metric("Female Employees", f"{si['female_employees_pct']}%", "of total workforce")
    hc3.metric("Female in Senior Mgmt", f"{si['senior_management_female_pct']}%", "vs 30% global average")
    hc4.metric("Female Board Directors", f"{si['board_female_pct']}%", "Board-level diversity")
    hc5.metric("Training Hours/Employee", f"{si['training_hours_per_employee']}h", "per year — 2024")
    hc6.metric("PWDs Employed", si['pwds_employed'], "Persons with disabilities")

    st.markdown("---")
    st.markdown("#### Financial Inclusion & Rural Reach")
    fi_col1, fi_col2 = st.columns(2)
    with fi_col1:
        inclusion_items = [
            ("Rural Portfolio Share", f"{si['rural_lending_pct']}%", "of total lending book", "#1D9E75"),
            ("Women-owned SME share", f"{si['women_sme_portfolio_pct']}%", "of SME portfolio", "#7C3AED"),
            ("Youth Accounts", f"{si['youth_accounts_mn']}M", "SimBanking youth accounts", "#2563EB"),
            ("SACCO Partnerships", str(si['sacco_partnerships']), "cooperative partnerships", "#D97706"),
            ("Digital Channel Usage", f"{si['digital_channel_usage_pct']}%", "transactions via digital channels", "#059669"),
        ]
        for label, value, note, colour in inclusion_items:
            st.markdown(
                f'<div style="background:#f9fafb;border-left:4px solid {colour};padding:8px 12px;'
                f'border-radius:0 6px 6px 0;margin:5px 0;display:flex;justify-content:space-between;align-items:center;">'
                f'<div><b style="font-size:13px;">{label}</b><br>'
                f'<span style="font-size:11px;color:#666;">{note}</span></div>'
                f'<b style="font-size:18px;color:{colour};">{value}</b>'
                f'</div>',
                unsafe_allow_html=True,
            )
    with fi_col2:
        st.markdown(
            f'<div style="background:linear-gradient(135deg,{wd.CRDB_GREEN}22,{wd.CRDB_GREEN}08);'
            f'border:1px solid {wd.CRDB_GREEN}44;border-radius:10px;padding:16px;height:100%;">'
            f'<b>🎯 Social Impact Summary</b>'
            f'<ul style="font-size:12px;margin:8px 0;padding-left:16px;">'
            f'<li>iMBEJU: TZS 7.76 Bn invested across 153 projects · 218,471 beneficiaries</li>'
            f'<li>Rural reach: 48% of portfolio serves underserved communities</li>'
            f'<li>Women-owned SMEs: 34% of SME book — above East Africa average</li>'
            f'<li>41% female workforce · 36% female board representation</li>'
            f'<li>97% digital adoption — reduces carbon footprint of banking operations</li>'
            f'<li>6.4M customers · 4.1M digital accounts · 36,566 Wakala agents</li>'
            f'</ul>'
            f'<hr style="border-color:{wd.CRDB_GREEN}44;margin:8px 0;">'
            f'<b>SDG Links:</b> <span style="font-size:11px;">SDG 1 (No Poverty) · SDG 2 (Zero Hunger) · '
            f'SDG 5 (Gender Equality) · SDG 8 (Decent Work) · SDG 10 (Reduced Inequalities) · SDG 13 (Climate Action)</span>'
            f'</div>',
            unsafe_allow_html=True,
        )
    st.caption("Source: CRDB Bank 2024 Integrated Annual Report — actual figures. iMBEJU programme data p.87–92.")


# ── TAB 8: TNFD Readiness Tracker ────────────────────────────────────────────
with tab_tnfd:
    st.markdown("#### 🌿 TNFD Readiness Tracker — Nature-Related Financial Disclosures")
    st.markdown(
        "The **Taskforce on Nature-related Financial Disclosures (TNFD)** framework (v1.0, September 2023) "
        "follows TCFD's four-pillar structure. It is increasingly required by DFI partners (GCF, AfDB, IFC). "
        "CRDB's 2024 TCFD Report notes TNFD readiness as a 2025–2026 priority. "
        "The assessment below tracks current maturity against the TNFD LEAP approach."
    )

    tnfd_df = pd.DataFrame(wd.TNFD_READINESS)
    status_colours_tnfd = {"Compliant": "#1D9E75", "In Progress": "#F59E0B", "Partial": "#D97706", "Planned": "#9CA3AF"}

    compliant_count = len(tnfd_df[tnfd_df["status"] == "Compliant"])
    in_progress_count = len(tnfd_df[tnfd_df["status"].isin(["In Progress", "Partial"])])
    planned_count = len(tnfd_df[tnfd_df["status"] == "Planned"])

    tn1, tn2, tn3, tn4 = st.columns(4)
    tn1.metric("Compliant", compliant_count, f"of {len(tnfd_df)} requirements")
    tn2.metric("In Progress / Partial", in_progress_count, "active development")
    tn3.metric("Planned", planned_count, "on 2025–2026 roadmap")
    tn4.metric("Target Year — Full TNFD", "2026", "Pilot report 2025")

    st.markdown("---")

    for pillar in tnfd_df["pillar"].unique():
        st.markdown(f"**{pillar}**")
        pillar_df = tnfd_df[tnfd_df["pillar"] == pillar]
        for _, row in pillar_df.iterrows():
            colour = status_colours_tnfd.get(row["status"], "#888")
            icon = "✅" if row["status"] == "Compliant" else "🔄" if row["status"] == "In Progress" else "⚠️" if row["status"] == "Partial" else "📋"
            st.markdown(
                f'<div style="display:flex;align-items:flex-start;gap:10px;padding:8px 12px;'
                f'background:#f9fafb;border-left:4px solid {colour};border-radius:0 6px 6px 0;margin:4px 0;">'
                f'<span style="font-size:16px;min-width:20px;">{icon}</span>'
                f'<div style="flex:1;">'
                f'<div style="display:flex;justify-content:space-between;">'
                f'<span style="font-size:13px;font-weight:600;">{row["requirement"]}</span>'
                f'<span style="background:{colour};color:white;padding:2px 8px;border-radius:10px;font-size:11px;">'
                f'{row["status"]}</span>'
                f'</div>'
                f'<p style="font-size:12px;color:#555;margin:2px 0 0 0;">{row["evidence"]}</p>'
                f'</div></div>',
                unsafe_allow_html=True,
            )

    st.markdown("---")
    st.markdown("#### TNFD vs TCFD Coverage — Gap Analysis")
    gap_col1, gap_col2 = st.columns(2)
    with gap_col1:
        st.markdown(
            f'<div style="background:#d1fae5;border-left:4px solid {wd.CRDB_GREEN};padding:12px;border-radius:0 6px 6px 0;">'
            f'<b>✅ TCFD → TNFD Transfer (Already in place)</b>'
            f'<ul style="font-size:12px;margin:6px 0;padding-left:16px;">'
            f'<li>Board & management governance structures — fully transferable</li>'
            f'<li>Physical risk identification (climate) → maps to nature physical risk</li>'
            f'<li>IFC PS6 biodiversity screening — partial TNFD coverage</li>'
            f'<li>ESMS water stress assessment — water dependency disclosure</li>'
            f'</ul>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with gap_col2:
        st.markdown(
            f'<div style="background:#fef3c7;border-left:4px solid #F59E0B;padding:12px;border-radius:0 6px 6px 0;">'
            f'<b>⚠️ TNFD-Specific Gaps (2025–2026 actions)</b>'
            f'<ul style="font-size:12px;margin:6px 0;padding-left:16px;">'
            f'<li>LEAP approach: Location-specific analysis of agriculture portfolio</li>'
            f'<li>Nature-related dependency mapping across 12 sectors</li>'
            f'<li>Biodiversity metrics (species, hectares affected) — new data required</li>'
            f'<li>Deforestation-free agriculture policy (draft in progress)</li>'
            f'<li>GRI 304 biodiversity indicators in 2025 Sustainability Report</li>'
            f'</ul>'
            f'</div>',
            unsafe_allow_html=True,
        )
    st.caption("TNFD v1.0 (September 2023) · LEAP = Locate, Evaluate, Assess, Prepare. Source: CRDB 2024 TCFD Report + TNFD framework.")
