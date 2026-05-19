"""GreenCRDB — Tanzania Climate-Finance Risk Intelligence Platform
Home dashboard for CRDB Bank.
"""
from __future__ import annotations

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

import web_data as wd
from auth import require_login, sidebar_user_card

st.set_page_config(
    page_title="GreenCRDB | CRDB Climate Risk Platform",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Authentication gate ────────────────────────────────────────────────────────
user = require_login()
sidebar_user_card()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    f"""
    <div style="background:{wd.CRDB_GREEN};padding:20px 28px;border-radius:10px;margin-bottom:8px;">
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;">
            <div>
                <h1 style="color:white;margin:0;font-size:26px;letter-spacing:0.5px;">
                    🌍 GreenCRDB
                </h1>
                <p style="color:#c8e6c9;margin:4px 0 0 0;font-size:13px;">
                    Tanzania Climate-Finance Risk Intelligence Platform &nbsp;·&nbsp; CRDB Bank
                </p>
            </div>
            <div style="display:flex;gap:8px;flex-wrap:wrap;">
                <span style="background:{wd.CRDB_GOLD};color:#1a1a1a;padding:4px 12px;border-radius:20px;font-size:11px;font-weight:bold;">
                    BoT 2025 Compliant
                </span>
                <span style="background:#1D9E75;color:white;padding:4px 12px;border-radius:20px;font-size:11px;font-weight:bold;">
                    GCF Accredited
                </span>
                <span style="background:#2563EB;color:white;padding:4px 12px;border-radius:20px;font-size:11px;font-weight:bold;">
                    Kijani Bond Issuer
                </span>
                <span style="background:#7C3AED;color:white;padding:4px 12px;border-radius:20px;font-size:11px;">
                    Illustrative Prototype
                </span>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Load data ─────────────────────────────────────────────────────────────────
sr = wd.sector_risk()
gp = wd.green_pipeline()
tc = wd.tcfd()
sc = wd.scenarios()
fe = wd.financed_emissions_df()
itr = wd.portfolio_itr()
gar_current = wd.green_asset_ratio_current()
gar_target = wd.CRDB_TARGETS["green_asset_ratio_2030"]


def _tcfd(metric: str) -> str:
    if tc.empty:
        return "—"
    row = tc[tc["TCFD Metric"] == metric]
    return row["Portfolio Value"].iloc[0] if not row.empty else "—"


total_portfolio = sr["loan_book_tzs_bn"].sum() if not sr.empty else 0
green_exposure_bn = gp["loan_size_tzs_mn"].sum() / 1000 if not gp.empty else 0
avg_esg_raw = _tcfd("Weighted average ESG composite")
avg_esg = avg_esg_raw.split(" / ")[0] if " / " in avg_esg_raw else avg_esg_raw
high_critical_raw = _tcfd("High/Critical risk sector exposure")
stress_loss = (
    sc[sc["Scenario"] == "Severe physical shock"]["Est. credit loss TZS Bn"].iloc[0]
    if not sc.empty else 0
)
total_fe = fe["financed_emissions_ktco2e"].sum() if not fe.empty else 0

# ── KPI row ───────────────────────────────────────────────────────────────────
st.markdown("### Portfolio at a Glance")
c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Total Portfolio", f"TZS {total_portfolio:,.0f} Bn", "12 sectors")
c2.metric("High / Critical Risk", high_critical_raw, "requires action")
c3.metric("Green Finance Pipeline", f"TZS {green_exposure_bn:.1f} Bn", f"{len(gp)} eligible borrowers")
c4.metric("Avg ESG Score", f"{avg_esg} / 10", "60 borrowers")
c5.metric("Portfolio ITR", f"{itr:.2f} °C", "vs. 1.5°C target", delta_color="inverse")
c6.metric("Financed Emissions", f"{total_fe:,.0f} ktCO₂e", "PCAF Scope 3 Cat.15")

# ── Green Asset Ratio progress bar ───────────────────────────────────────────
st.markdown("---")
st.markdown("### 🌱 Green Asset Ratio — Progress to 2030 Target")
col_left, col_right = st.columns([2, 1])
with col_left:
    progress_pct = min(gar_current / gar_target, 1.0)
    st.markdown(
        f"""
        <div style="background:#f0f4f0;border-radius:8px;padding:14px;">
            <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
                <span style="font-size:14px;font-weight:600;">Current: <span style="color:{wd.CRDB_GREEN};">{gar_current:.1f}%</span></span>
                <span style="font-size:14px;">Target: <b>{gar_target:.0f}% by 2030</b></span>
            </div>
            <div style="background:#ddd;border-radius:10px;height:22px;overflow:hidden;">
                <div style="background:{wd.CRDB_GREEN};height:22px;width:{progress_pct*100:.1f}%;border-radius:10px;
                    display:flex;align-items:center;justify-content:flex-end;padding-right:8px;">
                    <span style="color:white;font-size:12px;font-weight:bold;">{gar_current:.1f}%</span>
                </div>
            </div>
            <div style="display:flex;justify-content:space-between;margin-top:4px;font-size:11px;color:#666;">
                <span>0%</span><span>5%</span><span>10%</span><span style="color:{wd.CRDB_GREEN};font-weight:bold;">15% (2030)</span>
                <span>20%</span><span>25%</span><span>30% (2050)</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col_right:
    st.markdown(
        f"""
        <div style="background:{wd.CRDB_GREEN};color:white;padding:14px;border-radius:8px;text-align:center;">
            <p style="margin:0;font-size:12px;color:#c8e6c9;">Gap to 2030 Target</p>
            <h2 style="margin:4px 0;font-size:32px;">{gar_target - gar_current:.1f}%</h2>
            <p style="margin:0;font-size:12px;color:#c8e6c9;">percentage points to close</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# ── Main charts ───────────────────────────────────────────────────────────────
left, right = st.columns([1.6, 1])

with left:
    st.markdown("### Sector Financial Climate Risk")
    if not sr.empty:
        sr_sorted = sr.sort_values("financial_climate_risk", ascending=True)
        fig = px.bar(
            sr_sorted,
            x="financial_climate_risk",
            y="sector",
            color="risk_tier",
            color_discrete_map=wd.RISK_COLOURS,
            category_orders={"risk_tier": ["Critical", "High", "Medium", "Low"]},
            orientation="h",
            text="financial_climate_risk",
            labels={"financial_climate_risk": "Score (0–10)", "sector": "", "risk_tier": "Tier"},
        )
        fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        fig.update_layout(
            height=400,
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(l=10, r=50, t=10, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="right", x=1),
        )
        fig.add_vline(x=4.5, line_dash="dot", line_color="#f39c12", annotation_text="Medium")
        fig.add_vline(x=6.0, line_dash="dot", line_color="#e74c3c", annotation_text="High")
        fig.add_vline(x=7.5, line_dash="dot", line_color="#7b241c", annotation_text="Critical")
        st.plotly_chart(fig, use_container_width=True)

with right:
    st.markdown("### Portfolio ITR — Temperature Alignment")
    fig_itr = go.Figure(go.Indicator(
        mode="gauge+number",
        value=itr,
        number={"suffix": " °C", "font": {"size": 36}},
        title={"text": "Implied Temperature Rise<br><span style='font-size:12px;color:#888;'>vs. Paris 1.5°C target</span>"},
        gauge={
            "axis": {"range": [1.5, 4.0], "ticksuffix": "°C"},
            "bar": {"color": "#D85A30" if itr > 2.5 else "#EF9F27"},
            "steps": [
                {"range": [1.5, 2.0], "color": "#d4edda"},
                {"range": [2.0, 2.5], "color": "#fff3cd"},
                {"range": [2.5, 4.0], "color": "#f8d7da"},
            ],
            "threshold": {
                "line": {"color": wd.CRDB_GREEN, "width": 4},
                "thickness": 0.75,
                "value": 1.5,
            },
        },
    ))
    fig_itr.update_layout(height=220, margin=dict(l=30, r=30, t=60, b=10))
    st.plotly_chart(fig_itr, use_container_width=True)

    st.markdown(
        f'<div style="background:#fff3cd;border-left:4px solid #f39c12;padding:10px 14px;border-radius:0 6px 6px 0;font-size:13px;">'
        f'Portfolio is aligned to <b>{itr:.2f}°C</b> — above the Paris Agreement 1.5°C target. '
        f'Reducing Agriculture and Mining sector exposure is the highest-priority lever.'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.caption("Simulated · NGFS pathways · PACTA methodology · PCAF data quality Score 4")

st.markdown("---")

# ── PRB Six Principles radar + Scenario chart ─────────────────────────────────
col_prb, col_sc = st.columns([1, 1.3])

with col_prb:
    st.markdown("### PRB Six Principles Assessment")
    categories = list(wd.PRB_SCORES.keys())
    values = list(wd.PRB_SCORES.values())
    categories_loop = categories + [categories[0]]
    values_loop = values + [values[0]]

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=values_loop,
        theta=categories_loop,
        fill="toself",
        fillcolor=f"rgba(0, 107, 60, 0.2)",
        line=dict(color=wd.CRDB_GREEN, width=2),
        name="CRDB Score",
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=[5.0] * (len(categories) + 1),
        theta=categories_loop,
        fill=None,
        line=dict(color="#ddd", width=1, dash="dot"),
        name="Maximum (5.0)",
    ))
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 5], tickvals=[1, 2, 3, 4, 5]),
        ),
        showlegend=True,
        legend=dict(orientation="h", y=-0.15),
        height=340,
        margin=dict(l=50, r=50, t=30, b=40),
    )
    st.plotly_chart(fig_radar, use_container_width=True)
    st.caption("Principles for Responsible Banking (UNEP FI) · Simulated self-assessment scores")

with col_sc:
    st.markdown("### Climate Scenario Credit Loss")
    if not sc.empty:
        colours = {"Base case": "#3B82F6", "Accelerated transition": "#F59E0B", "Severe physical shock": "#D85A30"}
        fig3 = px.bar(
            sc,
            x="Scenario",
            y="Est. credit loss TZS Bn",
            color="Scenario",
            color_discrete_map=colours,
            text="Est. credit loss TZS Bn",
            labels={"Est. credit loss TZS Bn": "Credit Loss (TZS Bn)"},
        )
        fig3.update_traces(texttemplate="TZS %{text:,.1f}Bn", textposition="outside")
        fig3.update_layout(
            height=340,
            showlegend=False,
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(l=10, r=10, t=10, b=10),
        )
        st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# ── CRDB Milestones ───────────────────────────────────────────────────────────
st.markdown("### CRDB Bank Sustainability Milestones")
m1, m2, m3, m4, m5 = st.columns(5)

milestones = [
    ("🌿", "Kijani Bond", "USD 65.7M raised\n429% oversubscribed\nLuxembourg-listed 2025"),
    ("🌍", "GCF Accreditation", "First commercial bank\nin East & Central Africa\nUSD 200M TACATDP"),
    ("🏦", "MUFG Facility", "USD 225M secured\nfrom MUFG Japan\nfor green lending"),
    ("🤝", "Proparco Facility", "USD 125M\nclimate + gender\nlending programme"),
    ("📋", "BoT 2025", "First TCFD Report\npublished 2024\nCompliant"),
]
for col, (icon, title, detail) in zip([m1, m2, m3, m4, m5], milestones):
    with col:
        st.markdown(
            f'<div style="background:#f8f9fa;border:1px solid #e5e7eb;border-top:4px solid {wd.CRDB_GREEN};'
            f'padding:14px;border-radius:0 0 8px 8px;text-align:center;height:130px;">'
            f'<div style="font-size:22px;">{icon}</div>'
            f'<b style="font-size:13px;">{title}</b>'
            f'<p style="font-size:11px;color:#555;margin:4px 0 0 0;white-space:pre-line;">{detail}</p>'
            f'</div>',
            unsafe_allow_html=True,
        )

st.markdown("---")

# ── CRDB Group Multi-Entity Intelligence ─────────────────────────────────────
gc = wd.GROUP_CONSOLIDATED
entities = wd.GROUP_ENTITIES

st.markdown("### 🌍 CRDB Group Intelligence — Multi-Entity Overview")
st.markdown(
    f'<div style="background:linear-gradient(135deg,{wd.CRDB_GREEN} 0%,#004d2b 100%);'
    f'padding:18px 24px;border-radius:10px;margin-bottom:14px;">'
    f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;">'
    f'<div>'
    f'<h3 style="color:white;margin:0;font-size:18px;">CRDB Bank Group — Consolidated Sustainability Position</h3>'
    f'<p style="color:#a5d6a7;margin:4px 0 0 0;font-size:12px;">'
    f'{gc["countries"]} countries · {gc["total_entities"]} entities · {gc["total_branches"]} branches · '
    f'Est. {gc["total_borrowers_est"]:,} clients · All data simulated/illustrative'
    f'</p>'
    f'</div>'
    f'<div style="display:flex;gap:10px;flex-wrap:wrap;">'
    f'<div style="background:rgba(255,255,255,0.15);padding:8px 14px;border-radius:8px;text-align:center;">'
    f'<div style="color:#a5d6a7;font-size:10px;font-weight:bold;">GROUP TOTAL ASSETS</div>'
    f'<div style="color:white;font-size:16px;font-weight:bold;">TZS {gc["total_assets_tzs_bn"]:,.0f} Bn</div>'
    f'</div>'
    f'<div style="background:rgba(255,255,255,0.15);padding:8px 14px;border-radius:8px;text-align:center;">'
    f'<div style="color:#a5d6a7;font-size:10px;font-weight:bold;">GROUP ITR</div>'
    f'<div style="color:#FCD34D;font-size:16px;font-weight:bold;">{gc["group_itr"]:.2f}°C</div>'
    f'</div>'
    f'<div style="background:rgba(255,255,255,0.15);padding:8px 14px;border-radius:8px;text-align:center;">'
    f'<div style="color:#a5d6a7;font-size:10px;font-weight:bold;">GROUP GREEN RATIO</div>'
    f'<div style="color:#6EE7B7;font-size:16px;font-weight:bold;">{gc["group_green_ratio"]:.1f}%</div>'
    f'</div>'
    f'<div style="background:rgba(255,255,255,0.15);padding:8px 14px;border-radius:8px;text-align:center;">'
    f'<div style="color:#a5d6a7;font-size:10px;font-weight:bold;">FINANCED EMISSIONS</div>'
    f'<div style="color:white;font-size:16px;font-weight:bold;">{gc["group_emissions_ktco2e"]:,} ktCO₂e</div>'
    f'</div>'
    f'</div>'
    f'</div>'
    f'</div>',
    unsafe_allow_html=True,
)

# Entity cards
e_cols = st.columns(4)
for col, entity in zip(e_cols, entities):
    with col:
        itr_colour = "#D85A30" if entity["itr_c"] >= 2.8 else "#F59E0B" if entity["itr_c"] >= 2.3 else "#1D9E75"
        st.markdown(
            f'<div style="border:2px solid {entity["colour"]};border-radius:10px;overflow:hidden;height:100%;">'
            f'<div style="background:{entity["colour"]};padding:10px 12px;">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;">'
            f'<span style="font-size:22px;">{entity["flag"]}</span>'
            f'<span style="background:rgba(255,255,255,0.25);color:white;font-size:9px;'
            f'padding:2px 7px;border-radius:10px;">{entity["code"]}</span>'
            f'</div>'
            f'<div style="color:white;font-weight:bold;font-size:13px;margin-top:4px;">{entity["name"]}</div>'
            f'<div style="color:rgba(255,255,255,0.8);font-size:10px;">{entity["status"]}</div>'
            f'</div>'
            f'<div style="padding:10px 12px;background:#fafafa;">'
            f'<table style="width:100%;font-size:11px;border-collapse:collapse;">'
            f'<tr><td style="color:#666;padding:2px 0;">Portfolio</td>'
            f'<td style="font-weight:bold;text-align:right;">{entity["portfolio_display"]}</td></tr>'
            f'<tr><td style="color:#666;padding:2px 0;">Sectors</td>'
            f'<td style="font-weight:bold;text-align:right;">{entity["sectors"]}</td></tr>'
            f'<tr><td style="color:#666;padding:2px 0;">Branches</td>'
            f'<td style="font-weight:bold;text-align:right;">{entity["branches"]}</td></tr>'
            f'<tr><td style="color:#666;padding:2px 0;">Portfolio ITR</td>'
            f'<td style="font-weight:bold;color:{itr_colour};text-align:right;">{entity["itr_c"]:.2f}°C</td></tr>'
            f'<tr><td style="color:#666;padding:2px 0;">Green Ratio</td>'
            f'<td style="font-weight:bold;color:{wd.CRDB_GREEN};text-align:right;">{entity["green_ratio_pct"]:.1f}%</td></tr>'
            f'<tr><td style="color:#666;padding:2px 0;">High Risk</td>'
            f'<td style="font-weight:bold;color:#D85A30;text-align:right;">{entity["high_risk_pct"]}%</td></tr>'
            f'</table>'
            f'<div style="margin-top:8px;padding:5px 8px;background:{entity["platform_colour"]}22;'
            f'border-left:3px solid {entity["platform_colour"]};border-radius:0 4px 4px 0;'
            f'font-size:10px;color:{entity["platform_colour"]};font-weight:bold;">'
            f'{entity["platform_status"]}</div>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

# Expandable detail per entity
st.markdown("")
with st.expander("📋 View Group Entity Detail — Climate Risk Profiles & Regulatory Frameworks"):
    for entity in entities:
        st.markdown(
            f'<div style="border-left:4px solid {entity["colour"]};padding:10px 16px;'
            f'margin:8px 0;background:#fafafa;border-radius:0 6px 6px 0;">'
            f'<b style="font-size:14px;">{entity["flag"]} {entity["name"]} ({entity["country"]})</b>'
            f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-top:8px;font-size:12px;">'
            f'<div><span style="color:#666;">Regulator:</span> {entity["regulator"]}</div>'
            f'<div><span style="color:#666;">Climate Framework:</span> {entity["climate_framework"]}</div>'
            f'<div><span style="color:#666;">Key Climate Risks:</span> {entity["key_risk"]}</div>'
            f'<div><span style="color:#666;">Green Milestones:</span> {entity["green_milestone"]}</div>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

st.markdown(
    f'<div style="background:#EFF6FF;border-left:4px solid #3B82F6;padding:10px 16px;'
    f'border-radius:0 6px 6px 0;font-size:12px;margin-top:8px;">'
    f'🔵 <b>Currently active:</b> GreenCRDB platform covers <b>Tanzania operations in full detail</b>. '
    f'Burundi integration is in Phase 2 (Q3 2025). DRC module planned Phase 3 (2026). CRDB Insurance dashboard planned Phase 2. '
    f'Group consolidated sustainability reporting uses Tanzania data as the primary entity.'
    f'</div>',
    unsafe_allow_html=True,
)

st.markdown("---")

# ── Social Impact & Awards ────────────────────────────────────────────────────
st.markdown("### 🤝 Social Impact & Recognition")
soc_col, aw_col = st.columns([1.1, 1])

with soc_col:
    si = wd.SOCIAL_IMPACT
    st.markdown("#### iMBEJU Community Investment Programme (2024)")
    st.markdown(
        f'<div style="background:linear-gradient(90deg,{wd.CRDB_GREEN}22,{wd.CRDB_GREEN}08);'
        f'border:1px solid {wd.CRDB_GREEN}44;border-radius:10px;padding:14px 18px;">'
        f'<div style="display:flex;justify-content:space-around;flex-wrap:wrap;gap:12px;text-align:center;">'
        f'<div><div style="font-size:22px;font-weight:900;color:{wd.CRDB_GREEN};">TZS {si["imbeju_investment_tzs_bn"]:.2f} Bn</div><div style="font-size:11px;color:#555;">CSI Investment</div></div>'
        f'<div><div style="font-size:22px;font-weight:900;color:{wd.CRDB_GREEN};">{si["imbeju_beneficiaries"]:,}</div><div style="font-size:11px;color:#555;">Beneficiaries</div></div>'
        f'<div><div style="font-size:22px;font-weight:900;color:{wd.CRDB_GREEN};">{si["imbeju_projects"]}</div><div style="font-size:11px;color:#555;">Projects</div></div>'
        f'<div><div style="font-size:22px;font-weight:900;color:{wd.CRDB_GREEN};">{si["female_employees_pct"]}%</div><div style="font-size:11px;color:#555;">Female Workforce</div></div>'
        f'</div>'
        f'<hr style="border-color:{wd.CRDB_GREEN}33;margin:10px 0;">'
        f'<div style="display:flex;gap:6px;flex-wrap:wrap;">'
        + "".join([f'<span style="background:{wd.CRDB_GREEN}22;color:{wd.CRDB_GREEN};padding:2px 8px;border-radius:8px;font-size:11px;">{a}</span>' for a in si["imbeju_focus_areas"]])
        + f'</div></div>',
        unsafe_allow_html=True,
    )

with aw_col:
    st.markdown("#### 🏆 Awards & Recognition 2024 (45+)")
    awards_top = wd.AWARDS_2024[:6]
    award_cat_colours = {
        "Banking Excellence": wd.CRDB_GREEN,
        "SME Finance": "#2563EB",
        "Retail Banking": "#7C3AED",
        "Governance": "#D97706",
        "Sustainability": "#059669",
        "Digital": "#0284C7",
        "Green Finance": wd.CRDB_GREEN,
    }
    for award in awards_top:
        colour = award_cat_colours.get(award["category"], "#888")
        st.markdown(
            f'<div style="border-left:3px solid {colour};background:#f9fafb;padding:5px 10px;'
            f'margin:4px 0;border-radius:0 5px 5px 0;display:flex;justify-content:space-between;align-items:center;">'
            f'<div><b style="font-size:12px;">{award["award"]}</b><br>'
            f'<span style="font-size:11px;color:#666;">{award["institution"]}</span></div>'
            f'<span style="background:{colour}22;color:{colour};padding:2px 7px;border-radius:6px;font-size:10px;font-weight:bold;">{award["category"]}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )
    st.caption(f"Showing 6 of {len(wd.AWARDS_2024)}+ awards. Full list in Regulatory Compliance module.")

st.markdown("---")

# ── Module navigation ─────────────────────────────────────────────────────────
st.markdown("### Platform Modules")
n1, n2, n3, n4, n5 = st.columns(5)
nav_items = [
    (n1, "📊", "Module 1", "Sector Climate\nRisk Engine", wd.CRDB_GREEN),
    (n2, "🌱", "Module 2", "Borrower ESG\nScoring Engine", "#1D9E75"),
    (n3, "💡", "Module 3", "Climate Finance\nDecision Engine", "#2563EB"),
    (n4, "📋", "Module 4", "Regulatory &\nPCAF Compliance", "#D97706"),
    (n5, "🤖", "AI Copilot", "Sustainability\nReport Generator", "#7C3AED"),
]
for col, icon, mod, desc, colour in nav_items:
    with col:
        st.markdown(
            f'<div style="background:{colour};color:white;padding:16px;border-radius:8px;text-align:center;">'
            f'<h4 style="margin:0;">{icon} {mod}</h4>'
            f'<p style="margin:6px 0 0 0;font-size:12px;white-space:pre-line;">{desc}</p>'
            f'</div>',
            unsafe_allow_html=True,
        )

st.markdown(
    "<p style='color:#888;font-size:11px;margin-top:20px;text-align:center;'>"
    "All portfolio values and climate risk scores are simulated / illustrative. "
    "Developed as an MSc Finance & Investment academic prototype. "
    "Framework references: TCFD · ISSB S1/S2 · PRB · SASB FN-CB · PCAF · IFC PS · Bank of Tanzania 2025 Guidelines"
    "</p>",
    unsafe_allow_html=True,
)
