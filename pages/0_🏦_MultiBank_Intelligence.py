"""
GreenCRDB — MultiBank Intelligence Module
CRDB Group Entities · Africa Sustainability Ranking · East Africa Benchmark · Entity Onboarding
"""
from __future__ import annotations

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd

import web_data as wd
from auth import require_login, sidebar_user_card

st.set_page_config(page_title="MultiBank Intelligence | GreenCRDB", page_icon="🏦", layout="wide")

# ── Auth ──────────────────────────────────────────────────────────────────────
user = require_login()
sidebar_user_card()

entities = wd.GROUP_ENTITIES
gc = wd.GROUP_CONSOLIDATED

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    f'<div style="background:linear-gradient(135deg,{wd.CRDB_GREEN} 0%,#003d20 100%);'
    f'padding:20px 28px;border-radius:10px;margin-bottom:16px;">'
    f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;">'
    f'<div>'
    f'<h1 style="color:white;margin:0;font-size:24px;">🏦 MultiBank Intelligence</h1>'
    f'<p style="color:#a5d6a7;margin:4px 0 0 0;font-size:13px;">'
    f'CRDB Group · DFI Facilities · Africa Sustainability Ranking · East Africa Benchmark · Entity Onboarding'
    f'</p>'
    f'</div>'
    f'<div style="display:flex;gap:8px;flex-wrap:wrap;">'
    f'<span style="background:rgba(255,255,255,0.2);color:white;padding:4px 12px;border-radius:20px;font-size:11px;font-weight:bold;">🇹🇿 Tanzania</span>'
    f'<span style="background:rgba(255,255,255,0.15);color:#FCD34D;padding:4px 12px;border-radius:20px;font-size:11px;">🇧🇮 Burundi</span>'
    f'<span style="background:rgba(255,255,255,0.1);color:#D1D5DB;padding:4px 12px;border-radius:20px;font-size:11px;">🇨🇩 DRC</span>'
    f'<span style="background:rgba(255,255,255,0.15);color:#a7f3d0;padding:4px 12px;border-radius:20px;font-size:11px;">🛡️ Insurance</span>'
    f'</div>'
    f'</div>'
    f'</div>',
    unsafe_allow_html=True,
)

# ── Group consolidated KPI strip ──────────────────────────────────────────────
c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Group Total Assets", f"TZS {gc['total_assets_tzs_bn']:,.0f} Bn", "+25.3% YoY · 2024 Actual")
c2.metric("Group ITR", f"{gc['group_itr']:.2f}°C", "vs 1.5°C target", delta_color="inverse")
c3.metric("Green Asset Ratio", f"{gc['group_green_ratio']:.0f}%", f"Target 15% by 2030 · Actual 2024")
c4.metric("Moody's Rating", gc.get("moody_rating","B1"), "First TZ bank B1 · Stable")
c5.metric("Group Emissions", f"{gc['group_emissions_ktco2e']:,} ktCO₂e", "PCAF Scope 3")
c6.metric("Africa ESG Rank", "#8 / 20", "East Africa: #3")

st.markdown("---")

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_group, tab_dfi, tab_africa, tab_ea, tab_global, tab_onboard = st.tabs([
    "🏦 CRDB Group Entities",
    "💰 DFI Facilities & Ratios",
    "🌍 Africa Sustainability Ranking",
    "📊 East Africa Benchmark",
    "🏆 Global Peer Comparison",
    "➕ Onboard New Entity",
])


# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — CRDB GROUP ENTITIES
# ════════════════════════════════════════════════════════════════════════════
with tab_group:
    st.markdown("### CRDB Group — All Entities Deep Dive")
    st.markdown(
        "CRDB Bank Group comprises **5 entities** across 3 countries in Sub-Saharan Africa. "
        "Tanzania is the flagship entity (TZS 16,699 Bn total assets, 27% market share). "
        "Burundi is the most profitable subsidiary (ROE 31.1%). Congo is in its 2nd year of operations. "
        "CRDB Insurance achieved break-even in 2024 and is scaling climate-linked products."
    )

    # Entity selector
    entity_names = [f'{e["flag"]} {e["country"]}' for e in entities]
    sel = st.radio("Select entity for detail view:", entity_names, horizontal=True, index=0)
    sel_entity = next(e for e in entities if f'{e["flag"]} {e["country"]}' == sel)

    # Entity detail card
    col_card, col_metrics = st.columns([1, 2])
    with col_card:
        itr_col = "#D85A30" if sel_entity["itr_c"] >= 2.8 else "#F59E0B" if sel_entity["itr_c"] >= 2.3 else "#1D9E75"
        st.markdown(
            f'<div style="background:{sel_entity["colour"]};color:white;padding:20px;border-radius:12px;">'
            f'<div style="font-size:48px;text-align:center;">{sel_entity["flag"]}</div>'
            f'<h3 style="text-align:center;margin:8px 0 4px 0;">{sel_entity["name"]}</h3>'
            f'<p style="text-align:center;font-size:12px;opacity:0.85;margin:0;">{sel_entity["status"]}</p>'
            f'<hr style="border-color:rgba(255,255,255,0.3);margin:12px 0;">'
            f'<table style="width:100%;font-size:12px;color:white;">'
            f'<tr><td>Est.</td><td style="text-align:right;font-weight:bold;">{sel_entity["established"]}</td></tr>'
            f'<tr><td>Regulator</td><td style="text-align:right;font-weight:bold;font-size:10px;">{sel_entity["regulator"].split("(")[0]}</td></tr>'
            f'<tr><td>Currency</td><td style="text-align:right;font-weight:bold;">{sel_entity["currency"]}</td></tr>'
            f'<tr><td>Branches</td><td style="text-align:right;font-weight:bold;">{sel_entity["branches"]}</td></tr>'
            f'<tr><td>Est. Clients</td><td style="text-align:right;font-weight:bold;">{sel_entity["borrowers_est"]:,}</td></tr>'
            f'</table>'
            f'<div style="margin-top:12px;background:rgba(255,255,255,0.2);padding:8px;border-radius:6px;text-align:center;">'
            f'<span style="font-size:11px;">{sel_entity["platform_status"]}</span>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    with col_metrics:
        m1, m2, m3 = st.columns(3)
        m1.metric("Portfolio / Assets", sel_entity["portfolio_display"])
        m2.metric("ITR", f'{sel_entity["itr_c"]:.2f}°C', delta=f'{sel_entity["itr_c"]-1.5:.2f}°C above Paris', delta_color="inverse")
        m3.metric("Green Ratio", f'{sel_entity["green_ratio_pct"]:.1f}%')

        m4, m5, m6 = st.columns(3)
        pat_display = f'TZS {sel_entity["pat_tzs_bn"]:.1f} Bn' if sel_entity["pat_tzs_bn"] and sel_entity["pat_tzs_bn"] > 0 else (f'Loss TZS {abs(sel_entity["pat_tzs_bn"]):.1f} Bn' if sel_entity["pat_tzs_bn"] else "Break-even")
        m4.metric("PAT 2024", pat_display)
        m5.metric("Branches / Outlets", sel_entity["branches"])
        m6.metric("High Risk %", f'{sel_entity["high_risk_pct"]}%')

        st.markdown("**Climate Framework**")
        st.markdown(
            f'<div style="background:#f0f4f0;padding:10px 14px;border-left:4px solid {sel_entity["colour"]};'
            f'border-radius:0 6px 6px 0;font-size:12px;">{sel_entity["climate_framework"]}</div>',
            unsafe_allow_html=True,
        )
        st.markdown("**Key Climate Risks**")
        st.markdown(
            f'<div style="background:#fef3c7;padding:10px 14px;border-left:4px solid #F59E0B;'
            f'border-radius:0 6px 6px 0;font-size:12px;">{sel_entity["key_risk"]}</div>',
            unsafe_allow_html=True,
        )
        st.markdown("**Green Finance Milestones**")
        st.markdown(
            f'<div style="background:#d1fae5;padding:10px 14px;border-left:4px solid #1D9E75;'
            f'border-radius:0 6px 6px 0;font-size:12px;">{sel_entity["green_milestone"]}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # All entities comparison charts
    st.markdown("#### Group Portfolio & Climate Metrics Comparison")
    df_e = pd.DataFrame(entities)
    col_ch1, col_ch2 = st.columns(2)

    with col_ch1:
        fig = px.bar(df_e, x="country", y="portfolio_tzs_bn",
            color="country",
            color_discrete_map={e["country"]: e["colour"] for e in entities},
            text="portfolio_tzs_bn",
            labels={"portfolio_tzs_bn": "Portfolio (TZS Bn equiv.)", "country": ""},
            title="Portfolio Size by Entity (TZS Bn equivalent)")
        fig.update_traces(texttemplate="TZS %{text:,}Bn", textposition="outside")
        fig.update_layout(showlegend=False, plot_bgcolor="white", paper_bgcolor="white",
                          margin=dict(l=10,r=10,t=30,b=10), height=300)
        st.plotly_chart(fig, use_container_width=True)

    with col_ch2:
        fig2 = go.Figure()
        for e in entities:
            fig2.add_trace(go.Scatter(
                x=[e["portfolio_tzs_bn"]], y=[e["itr_c"]],
                mode="markers+text",
                text=[f'{e["flag"]} {e["country"]}'],
                textposition="top center",
                marker=dict(size=max(e["green_ratio_pct"]*3, 12), color=e["colour"], opacity=0.85,
                            line=dict(width=2, color="white")),
                name=e["country"],
            ))
        fig2.add_hline(y=1.5, line_dash="dot", line_color=wd.CRDB_GREEN, annotation_text="Paris 1.5°C")
        fig2.add_hline(y=2.0, line_dash="dot", line_color="#F59E0B", annotation_text="2°C ceiling")
        fig2.update_layout(
            title="Portfolio Size vs ITR (bubble = green ratio size)",
            xaxis_title="Portfolio (TZS Bn)", yaxis_title="ITR (°C)",
            showlegend=False, plot_bgcolor="white", paper_bgcolor="white",
            margin=dict(l=10,r=10,t=30,b=10), height=300,
            yaxis=dict(range=[1.2, 3.5]),
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Group Green Ratio progress bars
    st.markdown("#### Green Asset Ratio Progress — All Entities vs 2030 Group Target (15%)")
    for e in entities:
        pct = min(e["green_ratio_pct"] / gc["group_target_green_2030"], 1.0) * 100
        gap = gc["group_target_green_2030"] - e["green_ratio_pct"]
        st.markdown(
            f'<div style="margin:6px 0;display:flex;align-items:center;gap:12px;">'
            f'<div style="width:180px;font-size:12px;font-weight:bold;">{e["flag"]} {e["country"]}</div>'
            f'<div style="flex:1;background:#e5e7eb;border-radius:6px;height:18px;overflow:hidden;">'
            f'<div style="background:{e["colour"]};height:18px;width:{pct:.1f}%;border-radius:6px;'
            f'display:flex;align-items:center;padding-left:6px;">'
            f'<span style="color:white;font-size:10px;font-weight:bold;">{e["green_ratio_pct"]:.1f}%</span>'
            f'</div></div>'
            f'<div style="width:130px;font-size:11px;color:#D85A30;">Gap: {gap:.1f}% pts to target</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        f'<div style="background:#f0f4f0;padding:10px 14px;border-left:3px solid {wd.CRDB_GREEN};'
        f'border-radius:0 6px 6px 0;font-size:12px;margin-top:10px;">'
        f'<b>Group Green Asset Ratio: {gc["group_green_ratio"]:.0f}% (2024 Actual)</b> — '
        f'{gc["group_target_green_2030"] - gc["group_green_ratio"]:.0f}% points to close by 2030. '
        f'Tanzania flagship (7%) drives the ratio. Insurance entity leads proportionally with climate-linked Kijani Bima products. '
        f'GCF USD 200M + Kijani Bond USD 65.7M are primary vehicles to reach 15% target.'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.caption("Tanzania figures from 2024 Integrated Annual Report (actual). Burundi/Congo/Insurance figures from 2024 Annual Report. Subsidiary sustainability estimates illustrative.")

    # ── Milestone badges ──────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("#### 🏆 CRDB Group — Industry Firsts & Key Milestones (2024)")
    milestones = [
        ("🌍", "FIRST GCF Accredited Bank in East & Central Africa", "Since 2019 — enables direct access to Green Climate Fund concessional finance", "#1D9E75"),
        ("📄", "FIRST TCFD Report in Tanzania", "Published 2024 — first commercial bank in Tanzania to publish standalone TCFD climate disclosure", "#1D9E75"),
        ("🏦", "FIRST Tanzanian Bank with Moody's B1", "Upgraded 2024 — first local currency B1 rating for any Tanzanian bank; drove USD 567M lender commitments", "#1D9E75"),
        ("🟢", "FIRST East & Central Africa Green Bond", "Kijani Bond USD 65.7M — 429% oversubscribed; 10.25% yield; listed Luxembourg Stock Exchange June 2025", "#D97706"),
        ("🏢", "FIRST EDGE Certified Building in Tanzania", "CRDB HQ — 21% energy saving, 27% water saving, 28% embodied carbon reduction vs baseline", "#2563EB"),
        ("🤖", "FIRST AI Chatbot in East, Sub-Saharan & West Africa", "Elle Chatbot on website + WhatsApp — deployed 2024 across CRDB Bank platforms", "#7C3AED"),
    ]
    for i in range(0, len(milestones), 2):
        cols_m = st.columns(2)
        for j, col in enumerate(cols_m):
            if i + j < len(milestones):
                icon, title, desc, colour = milestones[i + j]
                with col:
                    st.markdown(
                        f'<div style="border-left:4px solid {colour};background:{colour}11;'
                        f'padding:10px 14px;border-radius:0 8px 8px 0;margin:4px 0;">'
                        f'<div style="font-size:20px;">{icon}</div>'
                        f'<b style="font-size:13px;color:{colour};">{title}</b>'
                        f'<p style="font-size:11px;color:#555;margin:4px 0 0 0;">{desc}</p>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )


# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — DFI FACILITIES & FINANCIAL RATIOS
# ════════════════════════════════════════════════════════════════════════════
with tab_dfi:
    fr = wd.FINANCIAL_RATIOS
    facilities = wd.DFI_FACILITIES
    env = wd.ENVIRONMENTAL_METRICS

    st.markdown("### 💰 DFI Facility Tracker & Financial Performance Dashboard")
    st.markdown(
        "CRDB Bank has secured **over USD 600 million** in medium-to-long-term development finance facilities. "
        "These commitments are a direct result of the Moody's B1 upgrade and GCF accreditation — "
        "a virtuous cycle of sustainability credibility unlocking cheaper capital."
    )

    # ── Financial KPI strip ───────────────────────────────────────────────────
    st.markdown("#### 📊 CRDB Bank 2024 Financial Performance (Actual — Annual Report)")
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    k1.metric("Total Assets", f"TZS {fr['total_assets_tzs_bn']:,.0f} Bn", "+25.3% YoY")
    k2.metric("Loans & Advances", f"TZS {fr['loans_advances_tzs_bn']:,.0f} Bn", "+22.7% YoY")
    k3.metric("PAT", f"TZS {fr['pat_tzs_bn']} Bn", "+30.4% YoY")
    k4.metric("ROE", f"{fr['roe_pct']}%", "Target >28%")
    k5.metric("Share Price", f"TZS {fr['share_price_tzs']:,.0f}", f"+{fr['price_appreciation_pct']}% 2024")
    k6.metric("Market Cap", f"TZS {fr['market_cap_tzs_bn']:,.0f} Bn", "DSE listed")

    st.markdown("---")

    # ── BoT Regulatory Compliance Margins ────────────────────────────────────
    st.markdown("#### 🏛️ BoT Regulatory Ratios — Actual vs Minimum Requirements")
    reg_items = [
        ("Total Capital Adequacy Ratio (CAR)", fr["car_total_pct"], fr["bot_min_car_total"], "%", "Higher = better"),
        ("Tier 1 Capital Ratio", fr["car_tier1_pct"], fr["bot_min_car_tier1"], "%", "Higher = better"),
        ("Liquidity Ratio", fr["liquidity_ratio_pct"], fr["bot_min_liquidity"], "%", "Higher = better"),
        ("NPL Ratio", fr["npl_ratio_pct"], fr["bot_max_npl"], "%", "Lower = better"),
        ("Cost-to-Income Ratio", fr["cir_pct"], fr["bot_max_cir"], "%", "Lower = better"),
    ]
    for label, actual, threshold, unit, direction in reg_items:
        if direction == "Higher = better":
            buffer = actual - threshold
            compliant = actual >= threshold
            colour = "#1D9E75" if compliant else "#D85A30"
            buffer_text = f"+{buffer:.1f}% above minimum"
        else:
            buffer = threshold - actual
            compliant = actual <= threshold
            colour = "#1D9E75" if compliant else "#D85A30"
            buffer_text = f"{buffer:.1f}% below limit"

        bar_pct = min(actual / (threshold * 2) * 100, 100) if direction == "Higher = better" else min((threshold - actual) / threshold * 100 + 50, 100)
        st.markdown(
            f'<div style="background:#f9fafb;border-left:4px solid {colour};padding:8px 14px;'
            f'border-radius:0 6px 6px 0;margin:4px 0;">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;">'
            f'<span style="font-size:13px;font-weight:600;">{label}</span>'
            f'<div style="text-align:right;">'
            f'<span style="font-size:18px;font-weight:bold;color:{colour};">{actual}{unit}</span>'
            f'<span style="font-size:11px;color:#888;margin-left:8px;">vs BoT: {threshold}{unit}</span>'
            f'</div></div>'
            f'<div style="font-size:11px;color:{colour};margin-top:2px;">✅ {buffer_text}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ── DFI Facilities ────────────────────────────────────────────────────────
    st.markdown("#### 💼 Development Finance Facility Tracker")
    total_usd = sum(f["amount_usd_m"] for f in facilities)
    st.markdown(
        f'<div style="background:linear-gradient(90deg,{wd.CRDB_GREEN}22,{wd.CRDB_GREEN}11);'
        f'border:2px solid {wd.CRDB_GREEN};border-radius:10px;padding:12px 18px;margin-bottom:14px;">'
        f'<span style="font-size:22px;font-weight:900;color:{wd.CRDB_GREEN};">USD {total_usd:,.0f}M</span>'
        f'<span style="font-size:13px;color:#555;margin-left:12px;">Total DFI facilities secured · Driven by Moody\'s B1 upgrade and GCF accreditation</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    fac_col1, fac_col2 = st.columns([1.6, 1])
    with fac_col1:
        for fac in facilities:
            bar_w = min(fac["amount_usd_m"] / total_usd * 100 * 3.5, 100)
            st.markdown(
                f'<div style="border:1px solid #e5e7eb;border-left:5px solid {fac["colour"]};'
                f'border-radius:0 8px 8px 0;padding:10px 14px;margin:6px 0;">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;">'
                f'<div>'
                f'<span style="font-size:18px;">{fac["flag"]}</span>'
                f'<b style="font-size:14px;margin-left:8px;">{fac["institution"]}</b>'
                f'<span style="background:#f0f4f0;color:#555;font-size:10px;padding:2px 6px;border-radius:4px;margin-left:8px;">{fac["type"]}</span>'
                f'</div>'
                f'<span style="font-size:18px;font-weight:bold;color:{fac["colour"]};">USD {fac["amount_usd_m"]}M</span>'
                f'</div>'
                f'<p style="font-size:12px;color:#666;margin:4px 0 6px 0;">{fac["purpose"]}</p>'
                f'<div style="background:#e5e7eb;border-radius:4px;height:6px;">'
                f'<div style="background:{fac["colour"]};height:6px;border-radius:4px;width:{bar_w:.0f}%;"></div>'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    with fac_col2:
        fac_df = pd.DataFrame(facilities)
        fig_fac = px.pie(
            fac_df, names="institution", values="amount_usd_m",
            color="institution",
            color_discrete_sequence=[f["colour"] for f in facilities],
            hole=0.4,
            title="DFI Facility Mix",
        )
        fig_fac.update_traces(textposition="outside", textinfo="percent+label", textfont_size=10)
        fig_fac.update_layout(
            height=360, showlegend=False,
            margin=dict(l=10, r=10, t=40, b=10),
        )
        st.plotly_chart(fig_fac, use_container_width=True)

        st.markdown(
            f'<div style="background:#d1fae5;border-left:3px solid {wd.CRDB_GREEN};'
            f'padding:10px;border-radius:0 6px 6px 0;font-size:12px;">'
            f'<b>Moody\'s B1 Impact:</b> In 2025, the rating upgrade drove <b>USD 567M</b> in lender commitments for a USD 200M syndicated facility — '
            f'demonstrating how sustainability credibility directly reduces cost of capital.'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ── Environmental Operations ──────────────────────────────────────────────
    st.markdown("#### 🌿 Environmental Operations Metrics (2024 Actual)")
    env_col1, env_col2, env_col3 = st.columns(3)

    with env_col1:
        st.markdown(
            f'<div style="background:#d1fae5;border-radius:10px;padding:14px;">'
            f'<b>🏢 IFC EDGE Certified HQ</b><br>'
            f'<div style="margin-top:8px;">'
            f'<div style="display:flex;justify-content:space-between;font-size:13px;"><span>Energy savings</span><b style="color:{wd.CRDB_GREEN};">{env["edge_energy_savings_pct"]}%</b></div>'
            f'<div style="display:flex;justify-content:space-between;font-size:13px;"><span>Water savings</span><b style="color:{wd.CRDB_GREEN};">{env["edge_water_savings_pct"]}%</b></div>'
            f'<div style="display:flex;justify-content:space-between;font-size:13px;"><span>Embodied carbon ↓</span><b style="color:{wd.CRDB_GREEN};">{env["edge_embodied_carbon_reduction_pct"]}%</b></div>'
            f'</div>'
            f'<hr style="margin:8px 0;border-color:#a7f3d0;">'
            f'<span style="font-size:11px;">🎯 EDGE Advance target: {env["target_edge_advance_year"]} | Net-zero: {env["target_net_zero_year"]}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

    with env_col2:
        total_recycled = (env["recycled_paper_cardboard_kg"] + env["recycled_plastic_kg"]
                          + env["recycled_glass_kg"])
        paper_saved = env["paper_reams_2023"] - env["paper_reams_2024"]
        st.markdown(
            f'<div style="background:#eff6ff;border-radius:10px;padding:14px;">'
            f'<b>♻️ Waste & Paper Reduction</b><br>'
            f'<div style="margin-top:8px;">'
            f'<div style="display:flex;justify-content:space-between;font-size:13px;"><span>Paper/cardboard recycled</span><b style="color:#2563EB;">{env["recycled_paper_cardboard_kg"]:,} kg</b></div>'
            f'<div style="display:flex;justify-content:space-between;font-size:13px;"><span>Plastic recycled</span><b style="color:#2563EB;">{env["recycled_plastic_kg"]:,} kg</b></div>'
            f'<div style="display:flex;justify-content:space-between;font-size:13px;"><span>Food waste processed</span><b style="color:#2563EB;">{env["food_waste_processed_kg"]:,} kg</b></div>'
            f'<div style="display:flex;justify-content:space-between;font-size:13px;"><span>Paper use reduction</span><b style="color:#2563EB;">{env["paper_reduction_pct"]}%</b></div>'
            f'</div>'
            f'<hr style="margin:8px 0;border-color:#bfdbfe;">'
            f'<span style="font-size:11px;">From {env["paper_reams_2023"]:,} → {env["paper_reams_2024"]:,} reams</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

    with env_col3:
        t = wd.CRDB_TARGETS
        st.markdown(
            f'<div style="background:#fef3c7;border-radius:10px;padding:14px;">'
            f'<b>⚡ Green Projects Impact</b><br>'
            f'<div style="margin-top:8px;">'
            f'<div style="display:flex;justify-content:space-between;font-size:13px;"><span>CO₂ reduction/year</span><b style="color:#D97706;">{t["co2_reduction_from_green_projects_kg"]/1e6:.1f}M kg</b></div>'
            f'<div style="display:flex;justify-content:space-between;font-size:13px;"><span>Clean energy generated</span><b style="color:#D97706;">{t["clean_energy_from_projects_gwh"]} GWh</b></div>'
            f'<div style="display:flex;justify-content:space-between;font-size:13px;"><span>Trees planted</span><b style="color:#D97706;">{env["trees_planted_2024"]:,}</b></div>'
            f'<div style="display:flex;justify-content:space-between;font-size:13px;"><span>Water reduction target</span><b style="color:#D97706;">{env["target_water_reduction_pct_2030"]}% by 2030</b></div>'
            f'</div>'
            f'<hr style="margin:8px 0;border-color:#fde68a;">'
            f'<span style="font-size:11px;">From Kijani Bond projects — TZS 86.9 Bn green loans</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ── GCF TACATDP Project Pipeline ──────────────────────────────────────────
    st.markdown("#### 🌍 GCF TACATDP Programme — USD 200M Project Pipeline")
    st.markdown(
        "CRDB Bank is the implementing entity for the **Tanzania Agriculture Climate Adaptation Technology Deployment Programme (TACATDP)** — "
        "a USD 200M programme (USD 100M GCF grant/concessional + USD 100M CRDB co-investment) targeting **6.1M+ beneficiaries** across Tanzania. "
        "This is the largest GCF programme managed by a commercial bank in Sub-Saharan Africa."
    )

    gcf_pipeline = wd.GCF_PIPELINE
    total_gcf = sum(p["allocation_usd_m"] for p in gcf_pipeline)
    total_bens = sum(p["beneficiaries"] for p in gcf_pipeline)

    gcf_k1, gcf_k2, gcf_k3, gcf_k4 = st.columns(4)
    gcf_k1.metric("Total Programme Value", f"USD {total_gcf}M", "GCF + CRDB co-finance")
    gcf_k2.metric("Target Beneficiaries", f"{total_bens/1e6:.1f}M+", "Smallholders & communities")
    gcf_k3.metric("Components", len(gcf_pipeline), "6 project components")
    gcf_k4.metric("GCF Accreditation", "Since 2019", "First E&C Africa commercial bank")

    gcf_col1, gcf_col2 = st.columns([1.6, 1])
    with gcf_col1:
        for proj in gcf_pipeline:
            bar_w = proj["allocation_usd_m"] / total_gcf * 100
            status_col = "#1D9E75" if proj["status"] == "Active" else "#F59E0B" if proj["status"] == "Deploying" else "#9CA3AF"
            st.markdown(
                f'<div style="border:1px solid #e5e7eb;border-left:5px solid {status_col};'
                f'border-radius:0 8px 8px 0;padding:8px 12px;margin:5px 0;">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;">'
                f'<div>'
                f'<b style="font-size:13px;">{proj["component"]}</b>'
                f'<span style="background:{status_col}22;color:{status_col};font-size:10px;padding:1px 6px;border-radius:4px;margin-left:6px;">{proj["status"]}</span>'
                f'</div>'
                f'<span style="font-size:15px;font-weight:bold;color:{status_col};">USD {proj["allocation_usd_m"]}M</span>'
                f'</div>'
                f'<div style="font-size:11px;color:#666;margin:2px 0;">{proj["region"]} · {proj["sector"]} · {proj["beneficiaries"]:,} beneficiaries</div>'
                f'<div style="background:#e5e7eb;border-radius:4px;height:5px;margin-top:5px;">'
                f'<div style="background:{status_col};height:5px;border-radius:4px;width:{bar_w:.0f}%;"></div>'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    with gcf_col2:
        gcf_df = pd.DataFrame(gcf_pipeline)
        fig_gcf = px.pie(
            gcf_df, names="component", values="allocation_usd_m",
            hole=0.4,
            color_discrete_sequence=["#1D9E75", "#2563EB", "#D97706", "#7C3AED", "#059669", "#0284C7"],
            title="GCF Fund Allocation",
        )
        fig_gcf.update_traces(textposition="outside", textinfo="percent", textfont_size=10)
        fig_gcf.update_layout(
            height=350, showlegend=False,
            margin=dict(l=10, r=10, t=40, b=10),
        )
        st.plotly_chart(fig_gcf, use_container_width=True)
        st.markdown(
            f'<div style="background:#d1fae5;border-left:3px solid {wd.CRDB_GREEN};'
            f'padding:8px 12px;border-radius:0 6px 6px 0;font-size:12px;margin-top:6px;">'
            f'<b>Largest GCF programme</b> managed by a Sub-Saharan commercial bank. '
            f'Funded by Green Climate Fund (USD 100M) + CRDB co-investment (USD 100M). '
            f'Agriculture sector: 28% of CRDB loan book.'
            f'</div>',
            unsafe_allow_html=True,
        )


# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — AFRICA SUSTAINABILITY RANKING
# ════════════════════════════════════════════════════════════════════════════
with tab_africa:
    st.markdown("### 🌍 Africa Bank Sustainability League Table")
    st.markdown(
        "How CRDB Bank compares against the **Top 20 African banks** on sustainability, "
        "green finance, climate disclosure, and ESG integration. "
        "Rankings are based on published sustainability reports, TCFD disclosures, PRB commitments, and green finance volumes."
    )

    AFRICA_BANKS = [
        {"rank": 1,  "bank": "Nedbank",                "country": "South Africa", "flag": "🇿🇦", "esg": 87, "green_ratio": 28.0, "itr": 2.10, "tcfd": True,  "prb": True,  "gcf": False, "bond": True,  "score": 91, "highlight": False, "tier": "Tier 1 Leader"},
        {"rank": 2,  "bank": "Standard Bank Group",    "country": "South Africa", "flag": "🇿🇦", "esg": 84, "green_ratio": 22.0, "itr": 2.20, "tcfd": True,  "prb": True,  "gcf": False, "bond": True,  "score": 87, "highlight": False, "tier": "Tier 1 Leader"},
        {"rank": 3,  "bank": "Absa Group",             "country": "South Africa", "flag": "🇿🇦", "esg": 79, "green_ratio": 19.0, "itr": 2.30, "tcfd": True,  "prb": True,  "gcf": False, "bond": True,  "score": 82, "highlight": False, "tier": "Tier 1 Leader"},
        {"rank": 4,  "bank": "Access Bank",            "country": "Nigeria",      "flag": "🇳🇬", "esg": 74, "green_ratio": 15.0, "itr": 2.50, "tcfd": True,  "prb": True,  "gcf": False, "bond": True,  "score": 76, "highlight": False, "tier": "Tier 1 Leader"},
        {"rank": 5,  "bank": "KCB Group",              "country": "Kenya",        "flag": "🇰🇪", "esg": 72, "green_ratio": 12.0, "itr": 2.60, "tcfd": True,  "prb": True,  "gcf": False, "bond": True,  "score": 74, "highlight": False, "tier": "Tier 2 Strong"},
        {"rank": 6,  "bank": "Equity Bank Group",      "country": "Kenya",        "flag": "🇰🇪", "esg": 70, "green_ratio": 10.0, "itr": 2.65, "tcfd": True,  "prb": True,  "gcf": False, "bond": False, "score": 71, "highlight": False, "tier": "Tier 2 Strong"},
        {"rank": 7,  "bank": "FirstRand",              "country": "South Africa", "flag": "🇿🇦", "esg": 68, "green_ratio": 18.0, "itr": 2.40, "tcfd": True,  "prb": False, "gcf": False, "bond": True,  "score": 69, "highlight": False, "tier": "Tier 2 Strong"},
        {"rank": 8,  "bank": "CRDB Bank",              "country": "Tanzania",     "flag": "🇹🇿", "esg": 65, "green_ratio":  7.0, "itr": 2.73, "tcfd": True,  "prb": True,  "gcf": True,  "bond": True,  "score": 68, "highlight": True,  "tier": "Tier 2 Strong"},
        {"rank": 9,  "bank": "Ecobank Transnational",  "country": "Pan-Africa",   "flag": "🌍", "esg": 62, "green_ratio":  8.0, "itr": 2.80, "tcfd": True,  "prb": True,  "gcf": False, "bond": False, "score": 64, "highlight": False, "tier": "Tier 2 Strong"},
        {"rank": 10, "bank": "Co-operative Bank",      "country": "Kenya",        "flag": "🇰🇪", "esg": 60, "green_ratio":  9.0, "itr": 2.80, "tcfd": True,  "prb": False, "gcf": False, "bond": False, "score": 61, "highlight": False, "tier": "Tier 3 Developing"},
        {"rank": 11, "bank": "Zenith Bank",            "country": "Nigeria",      "flag": "🇳🇬", "esg": 55, "green_ratio":  5.0, "itr": 3.00, "tcfd": False, "prb": False, "gcf": False, "bond": False, "score": 55, "highlight": False, "tier": "Tier 3 Developing"},
        {"rank": 12, "bank": "NMB Bank",               "country": "Tanzania",     "flag": "🇹🇿", "esg": 52, "green_ratio":  3.0, "itr": 2.90, "tcfd": True,  "prb": False, "gcf": False, "bond": False, "score": 52, "highlight": False, "tier": "Tier 3 Developing"},
        {"rank": 13, "bank": "Diamond Trust Bank",     "country": "Kenya/EA",     "flag": "🇰🇪", "esg": 51, "green_ratio":  4.0, "itr": 3.10, "tcfd": False, "prb": False, "gcf": False, "bond": False, "score": 50, "highlight": False, "tier": "Tier 3 Developing"},
        {"rank": 14, "bank": "Bank of Kigali",         "country": "Rwanda",       "flag": "🇷🇼", "esg": 49, "green_ratio":  6.0, "itr": 2.90, "tcfd": False, "prb": True,  "gcf": False, "bond": False, "score": 49, "highlight": False, "tier": "Tier 3 Developing"},
        {"rank": 15, "bank": "Stanbic Uganda",         "country": "Uganda",       "flag": "🇺🇬", "esg": 48, "green_ratio":  5.0, "itr": 3.10, "tcfd": True,  "prb": False, "gcf": False, "bond": False, "score": 48, "highlight": False, "tier": "Tier 3 Developing"},
        {"rank": 16, "bank": "Absa Kenya",             "country": "Kenya",        "flag": "🇰🇪", "esg": 46, "green_ratio":  7.0, "itr": 2.95, "tcfd": True,  "prb": False, "gcf": False, "bond": False, "score": 46, "highlight": False, "tier": "Tier 3 Developing"},
        {"rank": 17, "bank": "Centenary Bank",         "country": "Uganda",       "flag": "🇺🇬", "esg": 43, "green_ratio":  2.5, "itr": 3.20, "tcfd": False, "prb": False, "gcf": False, "bond": False, "score": 43, "highlight": False, "tier": "Tier 4 Emerging"},
        {"rank": 18, "bank": "BPR Bank Rwanda",        "country": "Rwanda",       "flag": "🇷🇼", "esg": 40, "green_ratio":  3.5, "itr": 3.10, "tcfd": False, "prb": False, "gcf": False, "bond": False, "score": 40, "highlight": False, "tier": "Tier 4 Emerging"},
        {"rank": 19, "bank": "KSHS Commercial Bank",   "country": "Tanzania",     "flag": "🇹🇿", "esg": 35, "green_ratio":  1.0, "itr": 3.40, "tcfd": False, "prb": False, "gcf": False, "bond": False, "score": 35, "highlight": False, "tier": "Tier 4 Emerging"},
        {"rank": 20, "bank": "First Allied Savings",   "country": "Ghana",        "flag": "🇬🇭", "esg": 30, "green_ratio":  0.8, "itr": 3.50, "tcfd": False, "prb": False, "gcf": False, "bond": False, "score": 30, "highlight": False, "tier": "Tier 4 Emerging"},
    ]
    df_africa = pd.DataFrame(AFRICA_BANKS)

    # CRDB position callout
    crdb_row = df_africa[df_africa["highlight"]].iloc[0]
    st.markdown(
        f'<div style="background:linear-gradient(90deg,{wd.CRDB_GREEN}22,{wd.CRDB_GREEN}11);'
        f'border:2px solid {wd.CRDB_GREEN};border-radius:10px;padding:14px 20px;margin-bottom:16px;">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;">'
        f'<div>'
        f'<span style="font-size:28px;font-weight:900;color:{wd.CRDB_GREEN};">#8 in Africa</span>'
        f'<span style="font-size:14px;color:#555;margin-left:10px;">out of 20 ranked banks · Tier 2 Strong</span><br>'
        f'<span style="font-size:13px;color:{wd.CRDB_GREEN};">🇹🇿 CRDB Bank Tanzania — Composite Sustainability Score: <b>68/100</b></span>'
        f'</div>'
        f'<div style="display:flex;gap:8px;flex-wrap:wrap;">'
        f'<span style="background:{wd.CRDB_GREEN};color:white;padding:4px 10px;border-radius:8px;font-size:11px;font-weight:bold;">✓ TCFD Published 2024</span>'
        f'<span style="background:{wd.CRDB_GREEN};color:white;padding:4px 10px;border-radius:8px;font-size:11px;font-weight:bold;">✓ PRB Signatory</span>'
        f'<span style="background:{wd.CRDB_GREEN};color:white;padding:4px 10px;border-radius:8px;font-size:11px;font-weight:bold;">✓ GCF Accredited — FIRST in E&C Africa</span>'
        f'<span style="background:{wd.CRDB_GOLD};color:#1a1a1a;padding:4px 10px;border-radius:8px;font-size:11px;font-weight:bold;">✓ Kijani Bond USD 65.7M (Luxembourg-listed)</span>'
        f'</div>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # League table
    tier_colours = {
        "Tier 1 Leader": "#1D9E75",
        "Tier 2 Strong": "#2563EB",
        "Tier 3 Developing": "#F59E0B",
        "Tier 4 Emerging": "#9CA3AF",
    }

    for _, row in df_africa.iterrows():
        bg = f"{wd.CRDB_GREEN}18" if row["highlight"] else "#fafafa"
        border = f"3px solid {wd.CRDB_GREEN}" if row["highlight"] else "1px solid #e5e7eb"
        tcfd_badge = f'<span style="background:#1D9E75;color:white;font-size:9px;padding:1px 5px;border-radius:3px;">TCFD</span>' if row["tcfd"] else '<span style="background:#e5e7eb;color:#888;font-size:9px;padding:1px 5px;border-radius:3px;">No TCFD</span>'
        prb_badge = f'<span style="background:#2563EB;color:white;font-size:9px;padding:1px 5px;border-radius:3px;">PRB</span>' if row["prb"] else ""
        gcf_badge = f'<span style="background:{wd.CRDB_GOLD};color:#1a1a1a;font-size:9px;padding:1px 5px;border-radius:3px;">GCF</span>' if row["gcf"] else ""
        bond_badge = f'<span style="background:#7C3AED;color:white;font-size:9px;padding:1px 5px;border-radius:3px;">Green Bond</span>' if row["bond"] else ""
        tier_col = tier_colours.get(row["tier"], "#888")
        score_width = row["score"]
        itr_col = "#D85A30" if row["itr"] >= 2.8 else "#F59E0B" if row["itr"] >= 2.3 else "#1D9E75"

        st.markdown(
            f'<div style="background:{bg};border:{border};border-radius:8px;padding:10px 14px;margin:4px 0;">'
            f'<div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">'
            f'<div style="width:30px;font-size:16px;font-weight:900;color:{tier_col};text-align:center;">#{row["rank"]}</div>'
            f'<div style="font-size:16px;">{row["flag"]}</div>'
            f'<div style="flex:1;min-width:200px;">'
            f'<b style="font-size:14px;{"color:" + wd.CRDB_GREEN + ";" if row["highlight"] else ""}">{row["bank"]}</b>'
            f'<span style="font-size:11px;color:#888;margin-left:6px;">{row["country"]}</span>'
            f'<div style="margin-top:3px;display:flex;gap:3px;">{tcfd_badge}{prb_badge}{gcf_badge}{bond_badge}</div>'
            f'</div>'
            f'<div style="width:160px;">'
            f'<div style="font-size:10px;color:#888;margin-bottom:2px;">Sustainability Score</div>'
            f'<div style="background:#e5e7eb;border-radius:4px;height:12px;overflow:hidden;">'
            f'<div style="background:{tier_col};height:12px;width:{score_width}%;"></div>'
            f'</div>'
            f'<div style="font-size:11px;font-weight:bold;color:{tier_col};">{row["score"]}/100</div>'
            f'</div>'
            f'<div style="width:80px;text-align:center;">'
            f'<div style="font-size:10px;color:#888;">Green %</div>'
            f'<div style="font-size:14px;font-weight:bold;color:{wd.CRDB_GREEN};">{row["green_ratio"]:.1f}%</div>'
            f'</div>'
            f'<div style="width:70px;text-align:center;">'
            f'<div style="font-size:10px;color:#888;">ITR</div>'
            f'<div style="font-size:14px;font-weight:bold;color:{itr_col};">{row["itr"]:.2f}°C</div>'
            f'</div>'
            f'<div style="width:90px;text-align:right;">'
            f'<span style="background:{tier_col}22;color:{tier_col};font-size:9px;padding:2px 6px;border-radius:8px;font-weight:bold;">{row["tier"]}</span>'
            f'</div>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("#### What Gives CRDB a Competitive Edge vs. Africa Peers")
    col_adv1, col_adv2, col_adv3 = st.columns(3)
    with col_adv1:
        st.markdown(
            f'<div style="background:#d1fae5;border-left:4px solid {wd.CRDB_GREEN};padding:12px;border-radius:0 6px 6px 0;">'
            f'<b>🏆 Unique Advantages</b><br>'
            f'<ul style="font-size:12px;margin:6px 0;padding-left:16px;">'
            f'<li>FIRST commercial bank in E&C Africa with GCF direct access</li>'
            f'<li>Kijani Bond 429% oversubscribed — highest demand of any EA green bond</li>'
            f'<li>MUFG Japan USD 225M — largest bilateral green facility in Tanzania</li>'
            f'<li>BoT 2025 compliant — ahead of regulatory peers</li>'
            f'</ul>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with col_adv2:
        st.markdown(
            f'<div style="background:#fef3c7;border-left:4px solid #F59E0B;padding:12px;border-radius:0 6px 6px 0;">'
            f'<b>⚠️ Areas to Improve</b><br>'
            f'<ul style="font-size:12px;margin:6px 0;padding-left:16px;">'
            f'<li>Green ratio 7% — Nedbank at 28%, KCB at 12% (gap remains significant)</li>'
            f'<li>Portfolio ITR 2.73°C — industry leaders below 2.2°C</li>'
            f'<li>Financed emissions disclosure (data quality Score 4 → target Score 2)</li>'
            f'<li>TNFD readiness still in scoping phase; PCAF full adoption pending</li>'
            f'</ul>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with col_adv3:
        st.markdown(
            f'<div style="background:#EFF6FF;border-left:4px solid #2563EB;padding:12px;border-radius:0 6px 6px 0;">'
            f'<b>🎯 2025–2027 Targets to Move Up</b><br>'
            f'<ul style="font-size:12px;margin:6px 0;padding-left:16px;">'
            f'<li>Reach #5 Africa by growing green ratio to 8% (2027)</li>'
            f'<li>Reduce portfolio ITR to 2.3°C via sector rebalancing</li>'
            f'<li>PCAF full adoption → Score 2 data quality</li>'
            f'<li>TNFD pilot report 2025 → full disclosure 2026</li>'
            f'</ul>'
            f'</div>',
            unsafe_allow_html=True,
        )
    st.caption("Rankings are composite scores based on: TCFD disclosure (20%), PRB commitment (15%), green finance ratio (25%), ITR alignment (20%), DFI partnerships (10%), reporting quality (10%). All simulated/illustrative.")


# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — EAST AFRICA BENCHMARK
# ════════════════════════════════════════════════════════════════════════════
with tab_ea:
    st.markdown("### 📊 East Africa Banking Sustainability Benchmark")
    st.markdown("Detailed peer comparison of CRDB Bank against the top **10 East African banks** across 8 sustainability dimensions.")

    EA_BANKS = [
        {"rank": 1, "bank": "KCB Group",             "country": "Kenya",     "flag": "🇰🇪", "esg": 72, "climate_risk": 6.8, "green_ratio": 12.0, "disclosure": 4.5, "esms": 4.2, "dfi_access": 4.8, "bot_equiv": "Compliant",    "prb": True,  "score": 74, "highlight": False},
        {"rank": 2, "bank": "Equity Bank Group",      "country": "Kenya",     "flag": "🇰🇪", "esg": 70, "climate_risk": 6.5, "green_ratio": 10.0, "disclosure": 4.3, "esms": 4.0, "dfi_access": 4.5, "bot_equiv": "Compliant",    "prb": True,  "score": 71, "highlight": False},
        {"rank": 3, "bank": "CRDB Bank",              "country": "Tanzania",  "flag": "🇹🇿", "esg": 65, "climate_risk": 7.2, "green_ratio":  7.0, "disclosure": 4.8, "esms": 4.3, "dfi_access": 5.0, "bot_equiv": "Compliant",    "prb": True,  "score": 68, "highlight": True},
        {"rank": 4, "bank": "Co-operative Bank",      "country": "Kenya",     "flag": "🇰🇪", "esg": 60, "climate_risk": 6.2, "green_ratio":  9.0, "disclosure": 3.8, "esms": 3.5, "dfi_access": 3.2, "bot_equiv": "Partial",      "prb": False, "score": 61, "highlight": False},
        {"rank": 5, "bank": "NMB Bank",               "country": "Tanzania",  "flag": "🇹🇿", "esg": 52, "climate_risk": 6.8, "green_ratio":  3.0, "disclosure": 3.5, "esms": 3.2, "dfi_access": 2.8, "bot_equiv": "Partial",      "prb": False, "score": 52, "highlight": False},
        {"rank": 6, "bank": "Diamond Trust Bank",     "country": "Kenya/EA",  "flag": "🇰🇪", "esg": 51, "climate_risk": 6.1, "green_ratio":  4.0, "disclosure": 3.2, "esms": 3.0, "dfi_access": 2.5, "bot_equiv": "Developing",   "prb": False, "score": 50, "highlight": False},
        {"rank": 7, "bank": "Bank of Kigali",         "country": "Rwanda",    "flag": "🇷🇼", "esg": 49, "climate_risk": 5.5, "green_ratio":  6.0, "disclosure": 3.0, "esms": 3.3, "dfi_access": 2.9, "bot_equiv": "Developing",   "prb": True,  "score": 49, "highlight": False},
        {"rank": 8, "bank": "Stanbic Tanzania",       "country": "Tanzania",  "flag": "🇹🇿", "esg": 48, "climate_risk": 6.9, "green_ratio":  5.0, "disclosure": 3.6, "esms": 3.4, "dfi_access": 3.5, "bot_equiv": "Compliant",    "prb": False, "score": 48, "highlight": False},
        {"rank": 9, "bank": "Standard Chartered TZ",  "country": "Tanzania",  "flag": "🇹🇿", "esg": 55, "climate_risk": 7.0, "green_ratio":  6.5, "disclosure": 4.0, "esms": 3.8, "dfi_access": 3.6, "bot_equiv": "Compliant",    "prb": False, "score": 53, "highlight": False},
        {"rank": 10,"bank": "Centenary Bank",         "country": "Uganda",    "flag": "🇺🇬", "esg": 43, "climate_risk": 5.8, "green_ratio":  2.5, "disclosure": 2.5, "esms": 2.8, "dfi_access": 1.8, "bot_equiv": "Developing",   "prb": False, "score": 43, "highlight": False},
    ]
    df_ea = pd.DataFrame(EA_BANKS)

    col_rank, col_radar = st.columns([1.3, 1])

    with col_rank:
        st.markdown("#### East Africa Sustainability League Table")
        st.markdown(
            f'<div style="background:{wd.CRDB_GREEN}18;border:2px solid {wd.CRDB_GREEN};border-radius:8px;'
            f'padding:8px 14px;margin-bottom:8px;font-size:13px;">'
            f'🇹🇿 <b>CRDB Bank ranks #3 in East Africa</b> — behind only KCB and Equity Bank Group. '
            f'CRDB leads all East African banks on DFI Access (5.0/5) and Climate Disclosure (4.8/5). '
            f'2024 green ratio: 7% (actual). Gap to #1: improving to 12% would challenge KCB by 2027.'
            f'</div>',
            unsafe_allow_html=True,
        )

        # Compact league table
        headers = ["#", "Bank", "Country", "ESG", "Disclosure", "DFI", "Green%", "PRB", "BoT Status", "Score"]
        header_html = "".join(f'<th style="padding:4px 8px;text-align:left;font-size:11px;color:#666;">{h}</th>' for h in headers)
        rows_html = ""
        for _, row in df_ea.iterrows():
            bg = f"{wd.CRDB_GREEN}22" if row["highlight"] else ("white" if row["rank"] % 2 == 0 else "#fafafa")
            fw = "bold" if row["highlight"] else "normal"
            prb_icon = "✅" if row["prb"] else "—"
            status_col = "#1D9E75" if row["bot_equiv"] == "Compliant" else "#F59E0B" if row["bot_equiv"] == "Partial" else "#9CA3AF"
            rows_html += (
                f'<tr style="background:{bg};">'
                f'<td style="padding:5px 8px;font-weight:bold;color:{wd.CRDB_GREEN if row["highlight"] else "#555"};">#{row["rank"]}</td>'
                f'<td style="padding:5px 8px;font-weight:{fw};">{row["flag"]} {row["bank"]}</td>'
                f'<td style="padding:5px 8px;font-size:11px;color:#888;">{row["country"]}</td>'
                f'<td style="padding:5px 8px;font-weight:bold;">{row["esg"]}</td>'
                f'<td style="padding:5px 8px;">{row["disclosure"]:.1f}</td>'
                f'<td style="padding:5px 8px;color:{wd.CRDB_GREEN};font-weight:bold;">{row["dfi_access"]:.1f}</td>'
                f'<td style="padding:5px 8px;color:{wd.CRDB_GREEN};font-weight:bold;">{row["green_ratio"]:.1f}%</td>'
                f'<td style="padding:5px 8px;">{prb_icon}</td>'
                f'<td style="padding:5px 8px;color:{status_col};font-size:10px;font-weight:bold;">{row["bot_equiv"]}</td>'
                f'<td style="padding:5px 8px;font-weight:bold;">{row["score"]}</td>'
                f'</tr>'
            )
        st.markdown(
            f'<table style="width:100%;border-collapse:collapse;font-size:12px;">'
            f'<thead><tr style="border-bottom:2px solid #e5e7eb;">{header_html}</tr></thead>'
            f'<tbody>{rows_html}</tbody>'
            f'</table>',
            unsafe_allow_html=True,
        )

    with col_radar:
        st.markdown("#### CRDB vs Peer Radar — 6 Dimensions")
        # Radar: CRDB vs KCB (top East Africa)
        dims = ["ESG Score", "Climate Disclosure", "DFI Access", "Green Ratio", "ESMS Quality", "Sector Risk Mgmt"]
        crdb_vals = [6.5, 4.8, 5.0, 2.1/3, 4.3, 4.2]  # normalised to 0-7
        kcb_vals  = [7.2, 4.5, 4.8, 4.0,   4.2, 4.5]
        equity_vals=[7.0, 4.3, 4.5, 3.3,   4.0, 4.3]

        fig_r = go.Figure()
        fig_r.add_trace(go.Scatterpolar(
            r=crdb_vals + [crdb_vals[0]],
            theta=dims + [dims[0]],
            fill="toself",
            fillcolor=f"rgba(0,107,60,0.25)",
            line=dict(color=wd.CRDB_GREEN, width=2),
            name="CRDB Bank",
        ))
        fig_r.add_trace(go.Scatterpolar(
            r=kcb_vals + [kcb_vals[0]],
            theta=dims + [dims[0]],
            fill="toself",
            fillcolor="rgba(59,130,246,0.15)",
            line=dict(color="#3B82F6", width=2, dash="dot"),
            name="KCB Group (#1 EA)",
        ))
        fig_r.add_trace(go.Scatterpolar(
            r=equity_vals + [equity_vals[0]],
            theta=dims + [dims[0]],
            fill="toself",
            fillcolor="rgba(245,158,11,0.12)",
            line=dict(color="#F59E0B", width=1.5, dash="dash"),
            name="Equity Bank (#2 EA)",
        ))
        fig_r.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 8], tickvals=[2,4,6,8])),
            showlegend=True,
            legend=dict(orientation="h", y=-0.15, x=0),
            height=360,
            margin=dict(l=40, r=40, t=20, b=60),
        )
        st.plotly_chart(fig_r, use_container_width=True)
        st.caption("CRDB leads on DFI Access and Climate Disclosure. KCB leads on Green Ratio and ESG Score.")

    st.markdown("---")

    # Green ratio comparison bar chart
    st.markdown("#### Green Finance Ratio — East Africa Peers vs CRDB")
    df_ea_sorted = df_ea.sort_values("green_ratio", ascending=True)
    colours_ea = [wd.CRDB_GREEN if h else "#D1D5DB" for h in df_ea_sorted["highlight"]]
    fig_ea = px.bar(
        df_ea_sorted,
        x="green_ratio", y="bank",
        orientation="h",
        text="green_ratio",
        color="highlight",
        color_discrete_map={True: wd.CRDB_GREEN, False: "#9CA3AF"},
        labels={"green_ratio": "Green Finance Ratio (%)", "bank": ""},
    )
    fig_ea.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig_ea.update_layout(
        height=320, showlegend=False,
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=10, r=50, t=10, b=10),
    )
    fig_ea.add_vline(x=15, line_dash="dot", line_color="#1D9E75",
                     annotation_text="Group 2030 Target: 15%")
    st.plotly_chart(fig_ea, use_container_width=True)

    st.caption("East Africa benchmark data is simulated/illustrative. Sources: Bank sustainability reports, PRB database, GCF accreditation list, World Bank CCSA database.")


# ════════════════════════════════════════════════════════════════════════════
# TAB 4 — GLOBAL PEER COMPARISON
# ════════════════════════════════════════════════════════════════════════════
with tab_global:
    st.markdown("### 🏆 Global Peer Comparison — IFC / GCF Client Banks")
    st.markdown(
        "CRDB Bank is benchmarked against other **IFC portfolio banks and GCF-accredited institutions** "
        "in emerging markets — its true global peer group as a development finance client."
    )

    GLOBAL_PEERS = [
        {"bank": "BRAC Bank", "country": "Bangladesh", "flag": "🇧🇩", "esg": 78, "green_ratio": 18.0, "itr": 2.30, "gcf": True,  "score": 79, "category": "DFI Client Leader"},
        {"bank": "Banco Pichincha", "country": "Ecuador", "flag": "🇪🇨", "esg": 74, "green_ratio": 14.0, "itr": 2.45, "gcf": True,  "score": 74, "category": "DFI Client Leader"},
        {"bank": "Access Bank Nigeria", "country": "Nigeria", "flag": "🇳🇬", "esg": 74, "green_ratio": 15.0, "itr": 2.50, "gcf": False, "score": 76, "category": "DFI Client Leader"},
        {"bank": "XacBank", "country": "Mongolia", "flag": "🇲🇳", "esg": 72, "green_ratio": 22.0, "itr": 2.20, "gcf": True,  "score": 73, "category": "DFI Client Leader"},
        {"bank": "CRDB Bank", "country": "Tanzania", "flag": "🇹🇿", "esg": 65, "green_ratio":  7.0, "itr": 2.73, "gcf": True,  "score": 68, "category": "DFI Client Strong", "highlight": True},
        {"bank": "Bank of Georgia", "country": "Georgia", "flag": "🇬🇪", "esg": 63, "green_ratio": 11.0, "itr": 2.55, "gcf": False, "score": 64, "category": "DFI Client Strong"},
        {"bank": "TBC Bank", "country": "Georgia", "flag": "🇬🇪", "esg": 62, "green_ratio":  9.5, "itr": 2.60, "gcf": False, "score": 62, "category": "DFI Client Strong"},
        {"bank": "Hatton National Bank", "country": "Sri Lanka", "flag": "🇱🇰", "esg": 60, "green_ratio":  8.0, "itr": 2.70, "gcf": True,  "score": 61, "category": "DFI Client Strong"},
        {"bank": "DFCC Bank", "country": "Sri Lanka", "flag": "🇱🇰", "esg": 55, "green_ratio":  6.5, "itr": 2.85, "gcf": False, "score": 55, "category": "DFI Client Developing"},
        {"bank": "Ecobank", "country": "Pan-Africa", "flag": "🌍", "esg": 62, "green_ratio":  8.0, "itr": 2.80, "gcf": False, "score": 64, "category": "DFI Client Strong"},
    ]
    df_g = pd.DataFrame([{**r, "highlight": r.get("highlight", False)} for r in GLOBAL_PEERS])

    # Scatter: ESG vs Green Ratio, size = score, color = GCF
    fig_g = px.scatter(
        df_g,
        x="esg", y="green_ratio",
        size="score",
        color="gcf",
        color_discrete_map={True: wd.CRDB_GREEN, False: "#9CA3AF"},
        text="bank",
        hover_data={"country": True, "itr": True, "score": True},
        labels={"esg": "ESG Score (0–100)", "green_ratio": "Green Finance Ratio (%)",
                "gcf": "GCF Accredited", "score": "Composite Score"},
        title="Global EM Bank Peers — ESG Score vs Green Finance Ratio (bubble = composite score)",
        size_max=30,
    )
    fig_g.update_traces(textposition="top center", textfont_size=10)
    fig_g.update_layout(
        height=420, plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=10, r=10, t=40, b=10),
    )
    st.plotly_chart(fig_g, use_container_width=True)

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown("#### CRDB's Position vs Global EM Peers")
        st.markdown(
            f'<div style="background:{wd.CRDB_GREEN}18;border-left:4px solid {wd.CRDB_GREEN};'
            f'padding:14px;border-radius:0 8px 8px 0;">'
            f'<b>Where CRDB leads globally:</b>'
            f'<ul style="font-size:12px;margin:6px 0;padding-left:16px;">'
            f'<li>GCF direct access — one of very few commercial banks with GCF accreditation</li>'
            f'<li>Kijani Bond — among the largest green bonds by an EA commercial bank</li>'
            f'<li>TCFD published report (2024) — ahead of most Sub-Saharan peers</li>'
            f'<li>IFC, MUFG, Proparco, GCF partnership — strongest DFI network in the peer group</li>'
            f'</ul>'
            f'<b>Gap to close:</b>'
            f'<ul style="font-size:12px;margin:6px 0;padding-left:16px;">'
            f'<li>Green ratio 7% vs peer leader XacBank at 22% — closing but gap remains</li>'
            f'<li>ITR 2.73°C vs leader XacBank at 2.20°C</li>'
            f'<li>PCAF adoption still proxy-based (Score 4)</li>'
            f'</ul>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with col_g2:
        df_g_sorted = df_g.sort_values("score", ascending=True)
        fig_bar = px.bar(
            df_g_sorted, x="score", y="bank", orientation="h",
            color="gcf",
            color_discrete_map={True: wd.CRDB_GREEN, False: "#9CA3AF"},
            text="score",
            labels={"score": "Composite Score", "bank": "", "gcf": "GCF Accredited"},
        )
        fig_bar.update_traces(texttemplate="%{text}", textposition="outside")
        fig_bar.update_layout(
            height=360, showlegend=True, plot_bgcolor="white", paper_bgcolor="white",
            margin=dict(l=10, r=40, t=10, b=10),
            legend=dict(orientation="h", y=1.1),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    st.caption("Global peer data is simulated/illustrative. Peer group = IFC portfolio banks and GCF-accredited commercial banks in emerging markets.")


# ════════════════════════════════════════════════════════════════════════════
# TAB 5 — ONBOARD NEW ENTITY
# ════════════════════════════════════════════════════════════════════════════
with tab_onboard:
    st.markdown("### ➕ Onboard New Bank Entity to GreenCRDB")
    st.markdown(
        "Use this wizard to register and configure a new CRDB subsidiary or partner bank on the platform. "
        "Once onboarded, the entity will appear in the Group Intelligence view and its data will flow into "
        "consolidated reporting."
    )

    # Progress tracker
    STEPS = [
        "1. Entity Info",
        "2. Portfolio Data",
        "3. Climate Profile",
        "4. Regulatory Map",
        "5. Users & Roles",
        "6. Review & Launch",
    ]
    if "onboard_step" not in st.session_state:
        st.session_state.onboard_step = 0
    if "onboard_data" not in st.session_state:
        st.session_state.onboard_data = {}

    step = st.session_state.onboard_step

    # Step progress bar
    step_cols = st.columns(len(STEPS))
    for i, (col, label) in enumerate(zip(step_cols, STEPS)):
        with col:
            done = i < step
            active = i == step
            bg = wd.CRDB_GREEN if done else (f"{wd.CRDB_GREEN}44" if active else "#e5e7eb")
            fg = "white" if done else (wd.CRDB_GREEN if active else "#9CA3AF")
            border = f"2px solid {wd.CRDB_GREEN}" if active else ("none" if done else "1px solid #e5e7eb")
            st.markdown(
                f'<div style="background:{bg};border:{border};border-radius:8px;padding:6px 8px;'
                f'text-align:center;font-size:10px;font-weight:{"bold" if active else "normal"};color:{fg};">'
                f'{"✓ " if done else ""}{label}</div>',
                unsafe_allow_html=True,
            )

    st.markdown("")

    # ── Step 0: Entity Information ────────────────────────────────────────
    if step == 0:
        st.markdown("#### Step 1: Entity Information")
        with st.form("onboard_step1"):
            c1, c2 = st.columns(2)
            with c1:
                entity_name = st.text_input("Legal Entity Name *", placeholder="e.g. CRDB Bank DRC SARL")
                country = st.selectbox("Country *", ["Tanzania", "Burundi", "DR Congo", "Kenya", "Uganda",
                                                      "Rwanda", "Dubai (UAE)", "South Africa", "Nigeria", "Other"])
                currency = st.selectbox("Reporting Currency", ["TZS", "BIF", "CDF", "KES", "UGX", "RWF", "USD", "Other"])
                entity_type = st.selectbox("Entity Type", ["Full Subsidiary", "Representative Office",
                                                            "Associate / Partner Bank", "Branch"])
            with c2:
                established = st.number_input("Year Established", min_value=1900, max_value=2025, value=2020)
                regulator = st.text_input("Primary Regulator", placeholder="e.g. Banque Centrale du Congo (BCC)")
                branches = st.number_input("Number of Branches", min_value=1, value=5)
                contact = st.text_input("Sustainability Contact (name & email)", placeholder="e.g. Jane Doe / j.doe@crdb.bi")

            submitted1 = st.form_submit_button("Next: Portfolio Data →", type="primary", use_container_width=True)

        if submitted1 and entity_name.strip():
            st.session_state.onboard_data.update({
                "entity_name": entity_name, "country": country, "currency": currency,
                "entity_type": entity_type, "established": established, "regulator": regulator,
                "branches": branches, "contact": contact,
            })
            st.session_state.onboard_step = 1
            st.rerun()

    # ── Step 1: Portfolio Data ─────────────────────────────────────────────
    elif step == 1:
        st.markdown("#### Step 2: Portfolio Data Configuration")
        with st.form("onboard_step2"):
            c1, c2 = st.columns(2)
            with c1:
                portfolio_size = st.number_input("Total Portfolio Size (local currency, Mn)", min_value=0.0, value=1000.0)
                num_borrowers = st.number_input("Estimated Number of Borrowers", min_value=1, value=10000)
                primary_sectors = st.multiselect("Primary Sectors", [
                    "Agriculture", "Energy", "Manufacturing", "Mining", "Financial Services",
                    "Tourism", "Real Estate", "Transport", "Healthcare", "Education",
                    "Retail", "Construction", "Trade Finance",
                ], default=["Agriculture", "Energy"])
            with c2:
                data_method = st.selectbox("Data Ingestion Method", [
                    "Manual CSV Upload (GreenCRDB template)",
                    "Excel Portfolio Export (auto-mapped)",
                    "API Connection (core banking)",
                    "Manual Web Form Entry",
                ])
                reporting_freq = st.selectbox("Reporting Frequency", ["Quarterly", "Semi-Annual", "Annual"])
                green_ratio = st.slider("Current Green Asset Ratio (%)", 0.0, 30.0, 1.0, 0.1)

            submitted2 = st.form_submit_button("Next: Climate Profile →", type="primary", use_container_width=True)

        if submitted2:
            st.session_state.onboard_data.update({
                "portfolio_size": portfolio_size, "num_borrowers": num_borrowers,
                "primary_sectors": primary_sectors, "data_method": data_method,
                "reporting_freq": reporting_freq, "green_ratio": green_ratio,
            })
            st.session_state.onboard_step = 2
            st.rerun()
        if st.button("← Back"):
            st.session_state.onboard_step = 0
            st.rerun()

    # ── Step 2: Climate Profile ────────────────────────────────────────────
    elif step == 2:
        st.markdown("#### Step 3: Country Climate Risk Profile")
        with st.form("onboard_step3"):
            st.info("Set the primary climate hazard scores for this entity's country context. These will feed into Module 1 for the entity.")
            c1, c2, c3 = st.columns(3)
            with c1:
                drought = st.slider("Drought Risk (0–10)", 0.0, 10.0, 5.0, 0.1)
                flood = st.slider("Flood Risk (0–10)", 0.0, 10.0, 5.0, 0.1)
            with c2:
                temperature = st.slider("Extreme Temperature Risk (0–10)", 0.0, 10.0, 5.0, 0.1)
                transition = st.slider("Transition Risk (0–10)", 0.0, 10.0, 4.0, 0.1)
            with c3:
                water_stress = st.slider("Water Stress Risk (0–10)", 0.0, 10.0, 5.0, 0.1)
                political_risk = st.slider("Political/Regulatory Risk (0–10)", 0.0, 10.0, 4.0, 0.1)

            composite = round((drought*0.25 + flood*0.20 + temperature*0.20 + transition*0.20 + water_stress*0.15), 2)
            st.markdown(f'**Composite Country Climate Risk Score: {composite:.2f} / 10**')

            climate_framework = st.selectbox("Central Bank Climate Framework", [
                "Full TCFD/ISSB S2 adoption",
                "Central bank climate risk guidelines (pilot)",
                "General prudential norms only",
                "No formal climate framework yet",
            ])
            submitted3 = st.form_submit_button("Next: Regulatory Map →", type="primary", use_container_width=True)

        if submitted3:
            st.session_state.onboard_data.update({
                "drought": drought, "flood": flood, "temperature": temperature,
                "transition": transition, "water_stress": water_stress,
                "political_risk": political_risk, "composite_risk": composite,
                "climate_framework": climate_framework,
            })
            st.session_state.onboard_step = 3
            st.rerun()
        if st.button("← Back"):
            st.session_state.onboard_step = 1
            st.rerun()

    # ── Step 3: Regulatory Mapping ─────────────────────────────────────────
    elif step == 3:
        st.markdown("#### Step 4: Regulatory Compliance Framework Mapping")
        with st.form("onboard_step4"):
            c1, c2 = st.columns(2)
            with c1:
                tcfd = st.checkbox("TCFD Report Published", value=False)
                prb = st.checkbox("PRB Signatory", value=False)
                gcf = st.checkbox("GCF Accredited", value=False)
                green_bond = st.checkbox("Green Bond Issued", value=False)
            with c2:
                ifrs_s2 = st.checkbox("ISSB S2 Adoption", value=False)
                tnfd = st.checkbox("TNFD Reporting", value=False)
                pcaf = st.checkbox("PCAF Member", value=False)
                esms = st.checkbox("IFC ESMS Operational", value=True)

            local_regs = st.text_area(
                "Local Regulatory Requirements (describe key climate/ESG requirements)",
                placeholder="e.g. BCC requires annual climate stress test for banks >USD 100M. Mandatory ESG disclosure from 2026.",
            )
            submitted4 = st.form_submit_button("Next: Users & Roles →", type="primary", use_container_width=True)

        if submitted4:
            st.session_state.onboard_data.update({
                "tcfd": tcfd, "prb": prb, "gcf": gcf, "green_bond": green_bond,
                "ifrs_s2": ifrs_s2, "tnfd": tnfd, "pcaf": pcaf, "esms": esms,
                "local_regs": local_regs,
            })
            st.session_state.onboard_step = 4
            st.rerun()
        if st.button("← Back"):
            st.session_state.onboard_step = 2
            st.rerun()

    # ── Step 4: Users & Roles ──────────────────────────────────────────────
    elif step == 4:
        st.markdown("#### Step 5: Configure Users & Access Roles")
        with st.form("onboard_step5"):
            st.markdown("Add the key users who will access GreenCRDB for this entity:")
            c1, c2, c3 = st.columns(3)
            with c1:
                cso_name = st.text_input("Sustainability Head (CSO equivalent)", placeholder="Full name")
                cso_email = st.text_input("CSO Email", placeholder="name@bank.xx")
            with c2:
                rm_name = st.text_input("Climate Risk Officer", placeholder="Full name")
                rm_email = st.text_input("Risk Officer Email", placeholder="name@bank.xx")
            with c3:
                analyst_name = st.text_input("Data Analyst", placeholder="Full name")
                analyst_email = st.text_input("Analyst Email", placeholder="name@bank.xx")

            access_model = st.selectbox("Access Model", [
                "Full GreenCRDB (all 7 modules)",
                "Core only (Modules 1–3 + Regulatory)",
                "Read-only (dashboard viewer)",
                "Custom (configure after onboarding)",
            ])
            submitted5 = st.form_submit_button("Next: Review & Launch →", type="primary", use_container_width=True)

        if submitted5:
            st.session_state.onboard_data.update({
                "cso_name": cso_name, "cso_email": cso_email,
                "rm_name": rm_name, "rm_email": rm_email,
                "analyst_name": analyst_name, "analyst_email": analyst_email,
                "access_model": access_model,
            })
            st.session_state.onboard_step = 5
            st.rerun()
        if st.button("← Back"):
            st.session_state.onboard_step = 3
            st.rerun()

    # ── Step 5: Review & Launch ────────────────────────────────────────────
    elif step == 5:
        d = st.session_state.onboard_data
        st.markdown("#### Step 6: Review Configuration & Launch Entity")

        st.markdown(
            f'<div style="background:{wd.CRDB_GREEN};color:white;padding:16px 20px;border-radius:10px;margin-bottom:12px;">'
            f'<h3 style="margin:0;">{d.get("entity_name","—")} — Ready to Launch</h3>'
            f'<p style="margin:4px 0 0 0;opacity:0.85;font-size:13px;">'
            f'{d.get("country","—")} · {d.get("entity_type","—")} · Est. {d.get("established","—")} · {d.get("branches","—")} branches'
            f'</p>'
            f'</div>',
            unsafe_allow_html=True,
        )

        r1, r2, r3 = st.columns(3)
        with r1:
            st.markdown("**Entity Details**")
            st.markdown(f"- Country: {d.get('country','—')}")
            st.markdown(f"- Regulator: {d.get('regulator','—')}")
            st.markdown(f"- Currency: {d.get('currency','—')}")
            st.markdown(f"- Portfolio: {d.get('currency','')}{d.get('portfolio_size',0):,.0f}M")
            st.markdown(f"- Borrowers: {d.get('num_borrowers',0):,}")
        with r2:
            st.markdown("**Climate Profile**")
            st.markdown(f"- Composite Risk: {d.get('composite_risk',0):.2f} / 10")
            st.markdown(f"- Primary Sectors: {', '.join(d.get('primary_sectors',[])[:3])}")
            st.markdown(f"- Climate Framework: {d.get('climate_framework','—')[:40]}")
            st.markdown(f"- Current Green Ratio: {d.get('green_ratio',0):.1f}%")
        with r3:
            st.markdown("**Frameworks & Users**")
            badges = []
            if d.get("tcfd"): badges.append("TCFD")
            if d.get("prb"): badges.append("PRB")
            if d.get("gcf"): badges.append("GCF")
            if d.get("esms"): badges.append("IFC ESMS")
            st.markdown(f"- Frameworks: {', '.join(badges) or 'None selected'}")
            st.markdown(f"- CSO: {d.get('cso_name','—')} ({d.get('cso_email','—')})")
            st.markdown(f"- Risk Officer: {d.get('rm_name','—')}")
            st.markdown(f"- Access Model: {d.get('access_model','—')}")

        st.markdown("---")

        col_l, col_r = st.columns([1, 1])
        with col_l:
            if st.button("← Back to Users"):
                st.session_state.onboard_step = 4
                st.rerun()
        with col_r:
            if st.button("🚀 Launch Entity on GreenCRDB Platform", type="primary", use_container_width=True):
                st.session_state.onboard_step = 6
                st.rerun()

    # ── Step 6: Success ────────────────────────────────────────────────────
    elif step == 6:
        d = st.session_state.onboard_data
        st.markdown(
            f'<div style="text-align:center;padding:40px;background:#d1fae5;border-radius:12px;">'
            f'<div style="font-size:56px;">🎉</div>'
            f'<h2 style="color:{wd.CRDB_GREEN};margin:12px 0 8px 0;">{d.get("entity_name","Entity")} Successfully Onboarded!</h2>'
            f'<p style="color:#065f46;font-size:15px;">'
            f'The entity has been registered on GreenCRDB. Credentials have been sent to {d.get("cso_email","the CSO")}.<br>'
            f'The entity will appear in the Group Intelligence view within 24 hours once initial data is uploaded.'
            f'</p>'
            f'</div>',
            unsafe_allow_html=True,
        )

        st.markdown("#### Next Steps for the New Entity")
        steps_next = [
            ("📂", "Upload Portfolio Data", "Use the Data Upload Studio to upload the entity's borrower and sector CSVs.", "Immediate"),
            ("⚙️", "Configure Module 1", "The Climate Risk Manager should enter country-specific sector hazard scores.", "Week 1"),
            ("🌱", "ESG Baseline Assessment", "ESG officers to complete initial borrower ESG assessments for top 20 borrowers.", "Month 1"),
            ("📋", "Regulatory Compliance Scan", "Compliance officer to complete the BoT equivalent checklist for the new jurisdiction.", "Month 1"),
            ("🤖", "AI Copilot Calibration", "Update the AI system prompt with entity-specific regulatory and market context.", "Month 2"),
            ("🌍", "Group Consolidation", "Entity data will auto-consolidate into Group Intelligence dashboard and GreenCRDB reports.", "Ongoing"),
        ]
        for i in range(0, len(steps_next), 2):
            cols_ns = st.columns(2)
            for j, col in enumerate(cols_ns):
                if i+j < len(steps_next):
                    icon, title, desc, timing = steps_next[i+j]
                    with col:
                        st.markdown(
                            f'<div style="border:1px solid #e5e7eb;border-left:4px solid {wd.CRDB_GREEN};'
                            f'padding:12px;border-radius:0 6px 6px 0;margin:4px 0;">'
                            f'<div style="display:flex;justify-content:space-between;">'
                            f'<b>{icon} {title}</b>'
                            f'<span style="background:#f0f4f0;color:#666;font-size:10px;padding:2px 6px;border-radius:4px;">{timing}</span>'
                            f'</div>'
                            f'<p style="font-size:12px;color:#666;margin:4px 0 0 0;">{desc}</p>'
                            f'</div>',
                            unsafe_allow_html=True,
                        )

        if st.button("Onboard Another Entity", use_container_width=True):
            st.session_state.onboard_step = 0
            st.session_state.onboard_data = {}
            st.rerun()

st.markdown("---")
st.caption(
    "GreenCRDB MultiBank Intelligence · All non-Tanzania entity data is simulated/illustrative. "
    "Africa and East Africa rankings are composite scores based on published sustainability reports, PRB database, GCF registry, and public disclosures. "
    "Rankings are for illustrative/benchmarking purposes only."
)
