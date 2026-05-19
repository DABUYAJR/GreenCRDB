"""GreenCRDB — About the Platform"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import web_data as wd
from auth import require_login, sidebar_user_card

st.set_page_config(page_title="About GreenCRDB", page_icon="ℹ️", layout="wide")

require_login()
sidebar_user_card()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    f'<div style="background:linear-gradient(135deg,{wd.CRDB_GREEN} 0%,#004d2b 60%,#001f10 100%);'
    f'padding:36px 40px;border-radius:12px;margin-bottom:20px;">'
    f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px;">'
    f'<div>'
    f'<h1 style="color:white;margin:0;font-size:32px;letter-spacing:0.5px;">🌍 GreenCRDB</h1>'
    f'<p style="color:#a5d6a7;margin:6px 0 2px 0;font-size:16px;font-weight:500;">'
    f'Tanzania Climate-Finance Risk Intelligence Platform</p>'
    f'<p style="color:#6ee7b7;margin:0;font-size:13px;">'
    f'Built for CRDB Bank · Sustainable Finance Unit · MSc Finance & Investment Prototype</p>'
    f'</div>'
    f'<div style="text-align:right;">'
    f'<div style="background:rgba(255,255,255,0.15);padding:12px 20px;border-radius:10px;">'
    f'<div style="color:#a5d6a7;font-size:11px;">Platform Version</div>'
    f'<div style="color:white;font-size:22px;font-weight:900;">v1.0</div>'
    f'<div style="color:#6ee7b7;font-size:11px;">2024–2025</div>'
    f'</div>'
    f'</div>'
    f'</div>'
    f'</div>',
    unsafe_allow_html=True,
)

# ── Mission Statement ─────────────────────────────────────────────────────────
st.markdown(
    f'<div style="background:#f0f9f4;border-left:6px solid {wd.CRDB_GREEN};'
    f'padding:20px 24px;border-radius:0 10px 10px 0;margin-bottom:20px;">'
    f'<h3 style="color:{wd.CRDB_GREEN};margin:0 0 8px 0;font-size:18px;">Our Mission</h3>'
    f'<p style="font-size:15px;color:#1a1a1a;margin:0;line-height:1.7;">'
    f'GreenCRDB is a <b>climate-finance intelligence platform</b> that equips CRDB Bank\'s Sustainable Finance Unit '
    f'with the analytical tools to integrate climate risk into every lending decision — '
    f'meeting Bank of Tanzania 2025 regulatory requirements, advancing the Kijani (green) agenda, '
    f'and positioning CRDB Bank as East Africa\'s leading climate-aligned commercial bank.'
    f'</p>'
    f'</div>',
    unsafe_allow_html=True,
)

tab_overview, tab_crdb, tab_modules, tab_frameworks, tab_tech, tab_data, tab_roadmap, tab_team = st.tabs([
    "🌍 What is GreenCRDB?",
    "🏦 About CRDB Bank",
    "📦 Platform Modules",
    "📐 Frameworks & Standards",
    "⚙️ Technology Stack",
    "📊 Data Sources",
    "🗺️ Roadmap",
    "👥 Team & Acknowledgements",
])


# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — WHAT IS GREENCRDB?
# ════════════════════════════════════════════════════════════════════════════
with tab_overview:
    col_a, col_b = st.columns([1.3, 1])

    with col_a:
        st.markdown("### What Problem Does GreenCRDB Solve?")
        st.markdown(
            "Climate change poses a **material financial risk** to Sub-Saharan banks. "
            "Tanzania's economy is 65% agriculture-dependent — one of the sectors most exposed to drought, floods, and temperature shocks. "
            "Yet most commercial banks in East Africa lack the tools to:"
        )
        for item in [
            "Systematically score the **climate risk of each sector** in their lending portfolio",
            "Assess individual **borrower ESG performance** and flag climate-vulnerable clients",
            "Generate **TCFD-aligned disclosures** required by Bank of Tanzania 2025 Guidelines",
            "Track progress against **green finance targets** (e.g. 15% green asset ratio by 2030)",
            "Access **concessional climate finance** from GCF, DFIs, and green bond markets",
        ]:
            st.markdown(
                f'<div style="display:flex;gap:10px;align-items:flex-start;margin:6px 0;">'
                f'<span style="color:{wd.CRDB_GREEN};font-size:16px;min-width:20px;">✓</span>'
                f'<span style="font-size:14px;">{item}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown("---")
        st.markdown("### The GreenCRDB Solution")
        st.markdown(
            "GreenCRDB integrates **four analytical modules** into a single platform that takes CRDB Bank's "
            "portfolio data through a complete climate-finance intelligence pipeline:"
        )
        pipeline_steps = [
            ("1", "Sector Climate Risk", "Score all 12 sectors on 5 hazard dimensions → identify concentration risk", wd.CRDB_GREEN),
            ("2", "Borrower ESG Scoring", "Score ~6.4M customers on Environmental, Social & Governance factors", "#1D9E75"),
            ("3", "Finance Decision Engine", "Blend ESG + sector risk → generate lending decisions + green finance pipeline", "#2563EB"),
            ("4", "Regulatory Compliance", "TCFD, BoT 2025, PCAF, PRB, SASB — all in one compliance dashboard", "#D97706"),
        ]
        for num, title, desc, colour in pipeline_steps:
            st.markdown(
                f'<div style="display:flex;gap:12px;align-items:flex-start;margin:8px 0;">'
                f'<div style="background:{colour};color:white;min-width:32px;height:32px;border-radius:50%;'
                f'display:flex;align-items:center;justify-content:center;font-weight:900;font-size:14px;">{num}</div>'
                f'<div><b style="font-size:14px;">{title}</b>'
                f'<br><span style="font-size:12px;color:#666;">{desc}</span></div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    with col_b:
        st.markdown("### Platform Highlights")
        highlights = [
            ("🌡️", "Sector Climate Risk Scoring", "5 hazard dimensions · 12 sectors · 0–10 composite score"),
            ("🌱", "Borrower ESG Engine", "E/S/G pillar scoring · 4-tier classification · borrower-level decisions"),
            ("💡", "Climate Finance Decisions", "Composite decision score · TCFD metrics · IFC PS alignment"),
            ("📋", "Regulatory Compliance", "BoT 2025 · PCAF Scope 3 · PRB · SASB FN-CB · TNFD readiness"),
            ("🏦", "MultiBank Intelligence", "Group benchmarking · DFI facility tracker · Africa league table"),
            ("🤖", "AI Sustainability Copilot", "Gemini-powered · 4 formal reports · Q&A on portfolio data"),
            ("🔐", "Role-Based Access Control", "6 user roles · granular module permissions · audit trail"),
            ("📂", "Data Upload Studio", "CSV/Excel import · CRDB template · data validation layer"),
        ]
        for icon, title, desc in highlights:
            st.markdown(
                f'<div style="border:1px solid #e5e7eb;border-left:4px solid {wd.CRDB_GREEN};'
                f'padding:10px 14px;border-radius:0 8px 8px 0;margin:5px 0;">'
                f'<div style="font-size:18px;display:inline;">{icon}</div>'
                f'<b style="font-size:13px;margin-left:8px;">{title}</b>'
                f'<p style="font-size:12px;color:#666;margin:3px 0 0 0;">{desc}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown("---")
        st.markdown("### Academic Context")
        st.markdown(
            f'<div style="background:#EFF6FF;border-left:4px solid #2563EB;'
            f'padding:14px;border-radius:0 8px 8px 0;">'
            f'<b>MSc Finance & Investment Prototype</b><br>'
            f'<p style="font-size:12px;color:#555;margin:6px 0 0 0;">'
            f'GreenCRDB was developed as an academic prototype for an MSc Finance & Investment programme, '
            f'designed to demonstrate how CRDB Bank can operationalise its climate finance strategy. '
            f'All portfolio values and climate risk scores are <b>simulated and illustrative</b> — '
            f'based on publicly available data and CRDB\'s 2024 Integrated Annual Report.'
            f'</p>'
            f'</div>',
            unsafe_allow_html=True,
        )


# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — ABOUT CRDB BANK
# ════════════════════════════════════════════════════════════════════════════
with tab_crdb:
    fr = wd.FINANCIAL_RATIOS
    gc = wd.GROUP_CONSOLIDATED

    st.markdown("### CRDB Bank — Tanzania's Largest Commercial Bank")

    crdb_col1, crdb_col2 = st.columns([1.3, 1])
    with crdb_col1:
        st.markdown(
            "CRDB Bank Plc is **Tanzania's largest commercial bank** by assets and customer base. "
            "Listed on the Dar es Salaam Stock Exchange (DSE) since 2009, CRDB holds approximately "
            "**27% of Tanzania's deposit market share** and serves over **6.4 million customers** through "
            "259 branches, 684 ATMs, and 36,566 Wakala agents."
        )
        st.markdown("#### 2024 Financial Highlights (Actual — Annual Report)")
        fin_items = [
            ("Total Assets", f"TZS {fr['total_assets_tzs_bn']:,.1f} Bn", f"+25.3% YoY", wd.CRDB_GREEN),
            ("Loans & Advances", f"TZS {fr['loans_advances_tzs_bn']:,.1f} Bn", "+22.7% YoY", wd.CRDB_GREEN),
            ("Customer Deposits", f"TZS {fr['customer_deposits_tzs_bn']:,.1f} Bn", "Market-leading", wd.CRDB_GREEN),
            ("Profit After Tax", f"TZS {fr['pat_tzs_bn']} Bn", "+30.4% YoY", "#1D9E75"),
            ("Return on Equity", f"{fr['roe_pct']}%", "Above target", "#1D9E75"),
            ("Moody's Rating", fr['moodys_rating'], "First TZ bank B1 — Stable", "#7C3AED"),
            ("Share Price", f"TZS {fr['share_price_tzs']:,}", f"+{fr['price_appreciation_pct']}% in 2024", "#D97706"),
            ("Market Cap", f"TZS {fr['market_cap_tzs_bn']:,.0f} Bn", "DSE listed", "#D97706"),
        ]
        for label, value, note, colour in fin_items:
            st.markdown(
                f'<div style="display:flex;justify-content:space-between;align-items:center;'
                f'padding:5px 10px;border-left:3px solid {colour};background:#f9fafb;margin:3px 0;border-radius:0 4px 4px 0;">'
                f'<span style="font-size:13px;">{label}</span>'
                f'<div style="text-align:right;">'
                f'<b style="color:{colour};">{value}</b>'
                f'<span style="font-size:11px;color:#888;margin-left:8px;">{note}</span>'
                f'</div></div>',
                unsafe_allow_html=True,
            )

    with crdb_col2:
        st.markdown("#### Sustainability Achievements — Industry Firsts")
        milestones = [
            ("🌍", "FIRST GCF-accredited commercial bank in East & Central Africa", "Since 2019"),
            ("📄", "FIRST standalone TCFD Report published in Tanzania", "2024"),
            ("🏦", "FIRST Tanzanian bank with Moody's B1 local currency rating", "2024"),
            ("🟢", "FIRST East & Central Africa green bond (Kijani Bond)", "USD 65.7M · 2024"),
            ("🏢", "FIRST EDGE-certified building in Tanzania", "CRDB HQ · 2024"),
            ("🤖", "FIRST AI chatbot in East, Sub-Saharan & West Africa", "Elle Chatbot · 2024"),
        ]
        for icon, title, detail in milestones:
            st.markdown(
                f'<div style="border-left:4px solid {wd.CRDB_GREEN};background:#d1fae5;'
                f'padding:8px 12px;border-radius:0 6px 6px 0;margin:5px 0;">'
                f'<div style="font-size:16px;display:inline;">{icon}</div>'
                f'<b style="font-size:12px;margin-left:6px;">{title}</b>'
                f'<p style="font-size:11px;color:#065f46;margin:2px 0 0 0;">{detail}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown("#### Group Structure")
        for e in wd.GROUP_ENTITIES:
            st.markdown(
                f'<div style="display:flex;gap:8px;align-items:center;padding:5px 10px;'
                f'background:#f9fafb;border-left:3px solid {e["colour"]};margin:3px 0;border-radius:0 4px 4px 0;">'
                f'<span style="font-size:16px;">{e["flag"]}</span>'
                f'<div><b style="font-size:12px;">{e["name"]}</b>'
                f'<span style="font-size:11px;color:#888;margin-left:6px;">{e["status"]}</span></div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("---")
    st.markdown("#### Green Finance Strategy — Key Targets")
    targets_col1, targets_col2, targets_col3 = st.columns(3)
    t = wd.CRDB_TARGETS
    with targets_col1:
        st.markdown(
            f'<div style="background:{wd.CRDB_GREEN};color:white;padding:16px;border-radius:10px;text-align:center;">'
            f'<div style="font-size:28px;font-weight:900;">{t["green_asset_ratio_2030"]:.0f}%</div>'
            f'<div style="font-size:12px;opacity:0.85;">Green Asset Ratio Target by 2030</div>'
            f'<div style="font-size:11px;margin-top:4px;opacity:0.7;">(From {t["green_asset_ratio_2024_actual"]:.0f}% in 2024)</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with targets_col2:
        st.markdown(
            f'<div style="background:#D97706;color:white;padding:16px;border-radius:10px;text-align:center;">'
            f'<div style="font-size:28px;font-weight:900;">{t["net_zero_target_year"]}</div>'
            f'<div style="font-size:12px;opacity:0.85;">Net-Zero Emissions Target</div>'
            f'<div style="font-size:11px;margin-top:4px;opacity:0.7;">Own operations · EDGE Advance by {t["edge_advance_target_year"]}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with targets_col3:
        st.markdown(
            f'<div style="background:#2563EB;color:white;padding:16px;border-radius:10px;text-align:center;">'
            f'<div style="font-size:28px;font-weight:900;">USD {t["total_dfi_facilities_usd_m"]:,.0f}M+</div>'
            f'<div style="font-size:12px;opacity:0.85;">DFI Facilities Secured (2024)</div>'
            f'<div style="font-size:11px;margin-top:4px;opacity:0.7;">MUFG · GCF · FMO · Proparco · GCPF · IFC</div>'
            f'</div>',
            unsafe_allow_html=True,
        )


# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — PLATFORM MODULES
# ════════════════════════════════════════════════════════════════════════════
with tab_modules:
    st.markdown("### Platform Module Architecture")
    st.markdown(
        "GreenCRDB is structured as a **sequential pipeline** — each module produces outputs that feed into the next. "
        "The pipeline flows from macro-level sector risk all the way to individual lending decisions and regulatory reporting."
    )

    # Pipeline diagram
    pipeline_viz = [
        {"num": "0", "icon": "🏦", "name": "MultiBank Intelligence", "subtitle": "Group · Africa · Global", "colour": "#7C3AED",
         "inputs": "GROUP_ENTITIES, DFI_FACILITIES, Africa benchmarks",
         "outputs": "Group consolidated view · DFI tracker · ESG league tables",
         "key_logic": "Consolidates Tanzania (flagship) + Burundi + Congo + Insurance into group metrics. Benchmarks against 20 African banks and 10 global EM peers.",
         "users": "CSO, Climate Risk Manager, Compliance Officer"},
        {"num": "1", "icon": "📊", "name": "Sector Climate Risk Engine", "subtitle": "5 Hazards · 12 Sectors", "colour": wd.CRDB_GREEN,
         "inputs": "crdb_sector_data.csv · climate_risk_scores.csv · regional_exposure_data.csv",
         "outputs": "composite_climate_risk (0–10 scale) · risk_tier · Sector_Risk_Ranking.csv",
         "key_logic": "Weighted composite score: Drought (25%) + Flood (20%) + Temperature (20%) + Transition (20%) + Water Stress (15%). Thresholds: Low <4.5, Medium 4.5–6.0, High 6.0–7.5, Critical >7.5.",
         "users": "Climate Risk Manager (data entry) · All roles (read)"},
        {"num": "2", "icon": "🌱", "name": "Borrower ESG Scoring Engine", "subtitle": "E/S/G Pillars · 60 Borrowers", "colour": "#1D9E75",
         "inputs": "Module 1 Sector_Risk_Ranking.csv",
         "outputs": "module2_borrower_esg_scores.csv · classification_summary · sector_esg_summary",
         "key_logic": "ESG Score = E×0.40 + S×0.30 + G×0.30 (all on 0–10 scale). Classification: Green Eligible (≥7.5) · Standard (5.5–7.4) · Watch List (4.0–5.4) · High Risk (<4.0).",
         "users": "ESG Officer (data entry + assigned sectors) · CSO (full)"},
        {"num": "3", "icon": "💡", "name": "Climate Finance Decision Engine", "subtitle": "TCFD · IFC PS · Scenarios", "colour": "#2563EB",
         "inputs": "Module 1 rankings + Module 2 ESG scores",
         "outputs": "Climate_Finance_Decisions.csv · green_loan_pipeline · tcfd_metrics · scenarios",
         "key_logic": "Decision Score = ESG_100×55% + Sector_Readiness_100×45% where Sector_Readiness = (10 − sector_risk)×10. Thresholds: Approve ≥65 · Conditional ≥52 · Review ≥40 · Decline <40.",
         "users": "Green Finance Officer (data entry) · CSO (full)"},
        {"num": "4", "icon": "📋", "name": "Regulatory Compliance & PCAF", "subtitle": "BoT 2025 · SASB · PRB · TNFD", "colour": "#D97706",
         "inputs": "All module outputs + FINANCIAL_RATIOS + SOCIAL_IMPACT constants",
         "outputs": "BoT compliance tracker · PCAF financed emissions · PRB readiness · SDG map · TNFD tracker",
         "key_logic": "BoT 2025 compliance: 13 requirements across Governance, Risk Management, Disclosure, Strategy. PCAF: IPCC AR6 Africa emission intensity proxies (Data Quality Score 4). TNFD: 8 requirements across 4 pillars.",
         "users": "Compliance Officer (full) · CSO (full) · Others (read)"},
        {"num": "5", "icon": "🤖", "name": "AI Sustainability Copilot", "subtitle": "Gemini · Reports · Q&A", "colour": "#7C3AED",
         "inputs": "Full portfolio context (all module outputs) + user question",
         "outputs": "Chat answers · TCFD Report · ESG Summary · Green Finance Report · Board Brief",
         "key_logic": "Sends full portfolio context (built by build_portfolio_context()) to Google Gemini API. 4 formal report templates with structured prompts. Context includes all sector, borrower, decision, emissions, and targets data.",
         "users": "CSO · Climate Risk Manager · Green Finance Officer · Compliance Officer"},
    ]

    for mod in pipeline_viz:
        with st.expander(f'{mod["icon"]} Module {mod["num"]} — {mod["name"]} · {mod["subtitle"]}', expanded=False):
            mc1, mc2, mc3 = st.columns([1.2, 1.2, 1])
            with mc1:
                st.markdown(f'**Inputs:**')
                st.markdown(f'<div style="background:#f9fafb;border-left:3px solid #e5e7eb;padding:8px 12px;border-radius:0 4px 4px 0;font-size:12px;">{mod["inputs"]}</div>', unsafe_allow_html=True)
                st.markdown(f'**Outputs:**')
                st.markdown(f'<div style="background:#f0f9f4;border-left:3px solid {mod["colour"]};padding:8px 12px;border-radius:0 4px 4px 0;font-size:12px;">{mod["outputs"]}</div>', unsafe_allow_html=True)
            with mc2:
                st.markdown(f'**Scoring Logic & Thresholds:**')
                st.markdown(f'<div style="background:#fffbeb;border-left:3px solid #F59E0B;padding:8px 12px;border-radius:0 4px 4px 0;font-size:12px;line-height:1.6;">{mod["key_logic"]}</div>', unsafe_allow_html=True)
            with mc3:
                st.markdown(f'**Who Uses This Module:**')
                st.markdown(f'<div style="background:#EFF6FF;border-left:3px solid #2563EB;padding:8px 12px;border-radius:0 4px 4px 0;font-size:12px;">{mod["users"]}</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 4 — FRAMEWORKS & STANDARDS
# ════════════════════════════════════════════════════════════════════════════
with tab_frameworks:
    st.markdown("### Regulatory & Sustainability Frameworks")
    st.markdown(
        "GreenCRDB is built on — and demonstrates compliance with — **eight major international and local frameworks**. "
        "Each framework influences one or more modules of the platform."
    )

    frameworks = [
        {
            "name": "TCFD — Task Force on Climate-related Financial Disclosures",
            "icon": "📄", "colour": wd.CRDB_GREEN,
            "owner": "Financial Stability Board (FSB)",
            "module": "Modules 3 & 4 · AI Copilot",
            "desc": "Four-pillar framework (Governance, Strategy, Risk Management, Metrics & Targets) for climate-related financial disclosure. CRDB Bank published its FIRST standalone TCFD Report in Tanzania in 2024.",
            "crdb_status": "Compliant — First TCFD Report published 2024",
        },
        {
            "name": "ISSB S2 — Climate-related Disclosures Standard",
            "icon": "📐", "colour": "#2563EB",
            "owner": "IFRS Foundation / International Sustainability Standards Board",
            "module": "Modules 4 · Regulatory Compliance",
            "desc": "Successor to TCFD; mandatory for ISSB-adopting jurisdictions. Tanzania BoT 2025 Guidelines align to ISSB S2. GreenCRDB's compliance tracker maps BoT requirements to ISSB S2 pillars.",
            "crdb_status": "In Progress — BoT Guidelines 2025 aligned",
        },
        {
            "name": "PRB — Principles for Responsible Banking",
            "icon": "🤝", "colour": "#1D9E75",
            "owner": "UNEP Finance Initiative (UNEP FI)",
            "module": "Modules 3 & 4 · AI Copilot",
            "desc": "Six-principle framework requiring banks to align strategy with Paris Agreement and UN SDGs, set SMART targets, and report annually. 350+ signatory banks globally (~50% of global banking assets). CRDB Bank is a PRB signatory.",
            "crdb_status": "Compliant — Active PRB Signatory",
        },
        {
            "name": "SASB FN-CB — Commercial Banks Standard",
            "icon": "📊", "colour": "#D97706",
            "owner": "IFRS Foundation (acquired SASB 2022)",
            "module": "Module 4 · Regulatory Compliance",
            "desc": "Five material ESG disclosure topics for commercial banks: Data Security, Financial Inclusion & Capacity Building, ESG Integration in Credit Analysis, Business Ethics, Systematic Risk Management. Used by MSCI, Sustainalytics, and institutional investors.",
            "crdb_status": "Adequate — Average score 3.9/5.0",
        },
        {
            "name": "IFC Performance Standards (PS1–PS8)",
            "icon": "🌐", "colour": "#7C3AED",
            "owner": "International Finance Corporation (IFC)",
            "module": "Modules 2, 3 · ESMS",
            "desc": "Eight standards covering environmental and social risk management, labour, resource efficiency, community health, land acquisition, biodiversity, indigenous peoples, and cultural heritage. Required for all GCF and DFI-funded transactions. CRDB's ESMS is IFC PS-aligned.",
            "crdb_status": "Operational — ESMS covers PS1–PS7",
        },
        {
            "name": "PCAF — Partnership for Carbon Accounting Financials",
            "icon": "🌡️", "colour": "#059669",
            "owner": "PCAF Global",
            "module": "Module 4 · PCAF Emissions tab",
            "desc": "Methodology for calculating and disclosing financed emissions (Scope 3 Category 15). CRDB acknowledged in its 2024 TCFD Report that it is in the process of adopting PCAF. GreenCRDB provides proxy calculations at PCAF Data Quality Score 4 (economic-activity proxies).",
            "crdb_status": "In Progress — Data Quality Score 4 proxy",
        },
        {
            "name": "BoT 2025 — Bank of Tanzania Climate Risk Guidelines",
            "icon": "🏛️", "colour": "#D97706",
            "owner": "Bank of Tanzania (BoT)",
            "module": "Module 4 · BoT Compliance tab",
            "desc": "Tanzania's mandatory climate risk reporting framework for all licensed commercial banks. Effective 2025. Requires: board climate governance, physical & transition risk identification, climate scenario analysis (≥2 scenarios), ESMS, and annual TCFD-aligned disclosure.",
            "crdb_status": "Compliant — 10/13 items · 3 in progress",
        },
        {
            "name": "TNFD — Taskforce on Nature-related Financial Disclosures",
            "icon": "🌿", "colour": "#065f46",
            "owner": "TNFD / UNDP / UNEP FI / WWF",
            "module": "Module 4 · TNFD Readiness tab",
            "desc": "Nature-equivalent of TCFD. Four-pillar framework (Governance, Strategy, Risk Management, Metrics & Targets) for biodiversity and nature-related financial disclosure. Uses the LEAP approach (Locate, Evaluate, Assess, Prepare). CRDB is targeting a pilot report in 2025 and full TNFD disclosure in 2026.",
            "crdb_status": "Readiness Phase — Pilot 2025 · Full 2026",
        },
    ]

    for fw in frameworks:
        with st.expander(f'{fw["icon"]} {fw["name"]}', expanded=False):
            fw_c1, fw_c2 = st.columns([2, 1])
            with fw_c1:
                st.markdown(f'**Owner:** {fw["owner"]}')
                st.markdown(f'**Relevant Modules:** {fw["module"]}')
                st.markdown(f'<p style="font-size:13px;color:#444;line-height:1.7;">{fw["desc"]}</p>', unsafe_allow_html=True)
            with fw_c2:
                colour = "#1D9E75" if "Compliant" in fw["crdb_status"] or "Operational" in fw["crdb_status"] else "#F59E0B"
                st.markdown(
                    f'<div style="background:{colour}22;border:2px solid {colour};border-radius:8px;padding:12px;text-align:center;">'
                    f'<div style="font-size:12px;color:{colour};font-weight:bold;">CRDB Status</div>'
                    f'<div style="font-size:13px;color:{colour};margin-top:4px;">{fw["crdb_status"]}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )


# ════════════════════════════════════════════════════════════════════════════
# TAB 5 — TECHNOLOGY STACK
# ════════════════════════════════════════════════════════════════════════════
with tab_tech:
    st.markdown("### Technology Stack")

    tech_col1, tech_col2 = st.columns(2)

    with tech_col1:
        st.markdown("#### Frontend & Visualisation")
        tech_items = [
            ("🖥️", "Streamlit", "Python web framework for multi-page dashboards. Runs in browser. No frontend code required.", "v1.35+"),
            ("📊", "Plotly", "Interactive charts — bar, scatter, radar, gauge, pie, choropleth.", "v5.x"),
            ("🐼", "Pandas", "Data manipulation, CSV reading, DataFrame operations.", "v2.x"),
            ("🎨", "CRDB Brand Theme", "Custom .streamlit/config.toml with CRDB green (#006B3C) and gold (#C8A84B).", "Custom"),
        ]
        for icon, name, desc, version in tech_items:
            st.markdown(
                f'<div style="border:1px solid #e5e7eb;padding:10px 14px;border-radius:8px;margin:5px 0;">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;">'
                f'<span><span style="font-size:18px;">{icon}</span> <b style="font-size:14px;margin-left:6px;">{name}</b></span>'
                f'<span style="background:#f0f4f0;color:#555;font-size:10px;padding:2px 8px;border-radius:4px;">{version}</span>'
                f'</div>'
                f'<p style="font-size:12px;color:#666;margin:4px 0 0 0;">{desc}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown("#### Backend & Data Pipeline")
        backend_items = [
            ("🐍", "Python 3.11+", "Core language for all scripts, data processing, and scoring logic."),
            ("📁", "CSV / YAML", "Data storage format. Config files in config/. Processed data in data/processed/."),
            ("🔧", "Custom YAML Parser", "load_yaml_config() — no PyYAML dependency; handles simple key-value + nested maps."),
            ("🔐", "SHA-256 Auth", "Password hashing in auth.py. Production would use bcrypt + database."),
        ]
        for icon, name, desc in backend_items:
            st.markdown(
                f'<div style="background:#f9fafb;border-left:3px solid {wd.CRDB_GREEN};'
                f'padding:8px 12px;border-radius:0 4px 4px 0;margin:5px 0;">'
                f'<span style="font-size:16px;">{icon}</span>'
                f'<b style="font-size:13px;margin-left:8px;">{name}</b>'
                f'<p style="font-size:12px;color:#666;margin:2px 0 0 0;">{desc}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )

    with tech_col2:
        st.markdown("#### AI & Analytics")
        ai_items = [
            ("🤖", "Google Gemini API", "Powers the AI Copilot. Free tier available at aistudio.google.com. Model: gemini-1.5-flash.", "Free / Paid"),
            ("📈", "NGFS Pathways", "Climate scenario analysis based on Network for Greening the Financial System 2023 pathways.", "v3.0"),
            ("🌡️", "PACTA Methodology", "Portfolio Alignment Climate Testing — used for Implied Temperature Rise (ITR) calculations.", "Proxy"),
            ("💨", "PCAF Methodology", "Partnership for Carbon Accounting Financials — financed emissions (Scope 3 Cat.15).", "Score 4"),
        ]
        for icon, name, desc, version in ai_items:
            st.markdown(
                f'<div style="border:1px solid #e5e7eb;padding:10px 14px;border-radius:8px;margin:5px 0;">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;">'
                f'<span><span style="font-size:18px;">{icon}</span> <b style="font-size:14px;margin-left:6px;">{name}</b></span>'
                f'<span style="background:#EFF6FF;color:#2563EB;font-size:10px;padding:2px 8px;border-radius:4px;">{version}</span>'
                f'</div>'
                f'<p style="font-size:12px;color:#666;margin:4px 0 0 0;">{desc}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown("#### Deployment Options")
        deploy_items = [
            ("☁️", "Streamlit Community Cloud", "share.streamlit.io — FREE · Public or private · GitHub push-to-deploy", "Recommended"),
            ("🐳", "Docker + Cloud Run", "Containerised deployment on Google Cloud Run or AWS ECS", "Enterprise"),
            ("💻", "Local / On-Premise", "Run locally with streamlit run app.py — no internet required after setup", "Dev/Demo"),
        ]
        for icon, name, desc, tier in deploy_items:
            colour = wd.CRDB_GREEN if tier == "Recommended" else "#D97706" if tier == "Enterprise" else "#9CA3AF"
            st.markdown(
                f'<div style="border:1px solid #e5e7eb;border-left:4px solid {colour};'
                f'padding:10px 14px;border-radius:0 8px 8px 0;margin:5px 0;">'
                f'<div style="display:flex;justify-content:space-between;">'
                f'<span><span style="font-size:18px;">{icon}</span> <b style="font-size:13px;margin-left:6px;">{name}</b></span>'
                f'<span style="background:{colour};color:white;font-size:10px;padding:2px 8px;border-radius:8px;">{tier}</span>'
                f'</div>'
                f'<p style="font-size:12px;color:#666;margin:4px 0 0 0;">{desc}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )


# ════════════════════════════════════════════════════════════════════════════
# TAB 6 — DATA SOURCES
# ════════════════════════════════════════════════════════════════════════════
with tab_data:
    st.markdown("### Data Sources & Methodology")
    st.warning(
        "⚠️ **Important Disclaimer:** All portfolio values, borrower names, sector loan book sizes, "
        "and climate risk scores are **simulated and illustrative**. They do not represent CRDB Bank's actual "
        "proprietary portfolio data. This platform is an academic prototype. "
        "Real deployment would require integration with CRDB's core banking system (Temenos T24)."
    )

    sources = [
        {
            "category": "📋 CRDB Annual Report Data (ACTUAL — not simulated)",
            "colour": wd.CRDB_GREEN,
            "items": [
                "CRDB Bank 2024 Integrated Annual Report — total assets, loans, deposits, PAT, ROE, CAR, NPL, share price",
                "Green asset ratio: 7% (2024 actual, Annual Report p.119)",
                "Kijani Bond: USD 65.7M raised, 429% oversubscribed, Luxembourg-listed, 10.25% yield",
                "GCF TACATDP: USD 200M (USD 100M GCF), 6.1M+ beneficiaries",
                "DFI facilities: MUFG USD 225M, FMO USD 75M, Proparco USD 50M, GCPF USD 25M",
                "IFC EDGE certification: CRDB HQ — 21% energy, 27% water, 28% embodied carbon",
                "Moody's B1 (Stable) — first Tanzanian bank with B1 local currency deposit rating",
                "iMBEJU: TZS 7.76 Bn CSI investment, 218,471 beneficiaries, 153 projects",
                "BoT prudential ratios: CAR 17.2%, Tier 1 16.3%, Liquidity 28.2%, NPL 2.9%, CIR 45.7%",
                "Group entities: Tanzania, Burundi, DR Congo, CRDB Insurance (all from 2024 Annual Report)",
            ]
        },
        {
            "category": "🌍 Climate Risk Data (Simulated/Proxy)",
            "colour": "#D97706",
            "items": [
                "Sector climate risk scores — simulated from IPCC AR6 Africa regional data and World Bank Climate Portal",
                "Hazard weights: Drought 25% · Flood 20% · Temperature 20% · Transition 20% · Water Stress 15%",
                "Implied Temperature Rise (ITR) — NGFS 2023 sectoral pathways; PACTA methodology proxy",
                "Financed emissions — PCAF Scope 3 Cat.15; IPCC AR6 Africa sector intensity proxies; Data Quality Score 4",
                "Regional exposure data — World Bank climate risk data for Tanzania regions",
            ]
        },
        {
            "category": "👤 Borrower/Portfolio Data (Simulated)",
            "colour": "#2563EB",
            "items": [
                "~60 simulated borrowers generated per sector from SECTOR_ESG_BASELINE constants in Module 2 script",
                "ESG scores blended with sector climate risk using E×0.40 + S×0.30 + G×0.30",
                "Loan sizes simulated from sector proportions (Agriculture 28%, Transport 12%, Mining 10%, etc.)",
                "Borrower names and IDs are fictional — no real customer data is used",
            ]
        },
        {
            "category": "🏦 Benchmarking Data (Estimated/Public Sources)",
            "colour": "#7C3AED",
            "items": [
                "Africa Sustainability Ranking — composite scores based on published sustainability reports, PRB database, GCF registry",
                "East Africa benchmark — bank sustainability reports, World Bank CCSA database, PRB signatory list",
                "Global peer comparison — IFC portfolio banks and GCF-accredited institutions in emerging markets",
                "All benchmark scores are illustrative and not based on proprietary bank data",
            ]
        },
    ]

    for source in sources:
        st.markdown(
            f'<div style="border-left:4px solid {source["colour"]};padding:12px 16px;'
            f'background:#f9fafb;border-radius:0 8px 8px 0;margin:10px 0;">'
            f'<b style="font-size:14px;color:{source["colour"]};">{source["category"]}</b>'
            f'<ul style="font-size:12px;margin:8px 0;padding-left:16px;">'
            + "".join(f"<li>{item}</li>" for item in source["items"])
            + f'</ul></div>',
            unsafe_allow_html=True,
        )


# ════════════════════════════════════════════════════════════════════════════
# TAB 7 — ROADMAP
# ════════════════════════════════════════════════════════════════════════════
with tab_roadmap:
    st.markdown("### Platform Roadmap — From Prototype to Production")

    phases = [
        {
            "phase": "Phase 1 · Current",
            "period": "2024–2025",
            "status": "Live",
            "colour": wd.CRDB_GREEN,
            "entity": "CRDB Bank Tanzania",
            "items": [
                "✅ All 7 platform modules live for Tanzania operations",
                "✅ Full CRDB 2024 Annual Report data integrated",
                "✅ AI Copilot with 4 formal sustainability report templates",
                "✅ Role-based access control (6 roles)",
                "✅ BoT 2025 compliance tracker — 10/13 items",
                "✅ TCFD, PRB, SASB, PCAF, IFC PS, TNFD dashboards",
                "✅ iMBEJU social impact · GCF TACATDP pipeline tracker",
                "✅ Africa league table · East Africa benchmark · Global peers",
            ]
        },
        {
            "phase": "Phase 2 · Planned",
            "period": "Q3 2025 – Q2 2026",
            "status": "In Development",
            "colour": "#D97706",
            "entity": "CRDB Burundi + Insurance",
            "items": [
                "🔄 CRDB Burundi module integration (BIF portfolio data)",
                "🔄 CRDB Insurance Intelligence dedicated dashboard",
                "🔄 Full PCAF adoption (Data Quality Score 2 target)",
                "🔄 TNFD pilot report — LEAP approach implementation",
                "🔄 Live data connection to Temenos T24 core banking (API)",
                "🔄 Al-Barakah Islamic finance climate screening module",
                "🔄 Enhanced satellite-based agricultural climate monitoring",
                "🔄 ISSB S2 full adoption — CRDB disclosure framework",
            ]
        },
        {
            "phase": "Phase 3 · Vision",
            "period": "2026–2027",
            "status": "Planned",
            "colour": "#9CA3AF",
            "entity": "CRDB Congo + Group Consolidation",
            "items": [
                "📋 CRDB Congo module (start-up phase operations)",
                "📋 Full group sustainability consolidation reporting",
                "📋 GCF TACATDP impact monitoring integration",
                "📋 TNFD full disclosure report (2026 target)",
                "📋 Automated TCFD annual report generation",
                "📋 Scope 3 financed emissions Score 1–2 data pipeline",
                "📋 External ESG rating integration (Sustainalytics, MSCI)",
                "📋 Climate stress testing aligned to NGFS Orderly/Disorderly scenarios",
            ]
        },
    ]

    for phase in phases:
        colour = phase["colour"]
        status_bg = "#d1fae5" if phase["status"] == "Live" else "#fef3c7" if phase["status"] == "In Development" else "#f3f4f6"
        st.markdown(
            f'<div style="border:2px solid {colour};border-radius:10px;margin:12px 0;overflow:hidden;">'
            f'<div style="background:{colour};padding:12px 18px;display:flex;justify-content:space-between;align-items:center;">'
            f'<div>'
            f'<span style="color:white;font-size:16px;font-weight:900;">{phase["phase"]}</span>'
            f'<span style="color:rgba(255,255,255,0.75);font-size:12px;margin-left:12px;">{phase["period"]}</span>'
            f'</div>'
            f'<div style="text-align:right;">'
            f'<span style="background:rgba(255,255,255,0.25);color:white;padding:3px 10px;border-radius:10px;font-size:12px;">{phase["status"]}</span>'
            f'<div style="color:rgba(255,255,255,0.75);font-size:11px;margin-top:2px;">{phase["entity"]}</div>'
            f'</div>'
            f'</div>'
            f'<div style="padding:12px 18px;">'
            + "".join(f'<div style="font-size:13px;padding:3px 0;">{item}</div>' for item in phase["items"])
            + f'</div></div>',
            unsafe_allow_html=True,
        )


# ════════════════════════════════════════════════════════════════════════════
# TAB 8 — TEAM & ACKNOWLEDGEMENTS
# ════════════════════════════════════════════════════════════════════════════
with tab_team:
    st.markdown("### Team & Acknowledgements")

    team_col1, team_col2 = st.columns([1.2, 1])

    with team_col1:
        st.markdown("#### Platform Development")
        st.markdown(
            f'<div style="background:{wd.CRDB_GREEN};color:white;padding:20px;border-radius:10px;margin-bottom:12px;">'
            f'<h3 style="margin:0 0 4px 0;font-size:18px;">GreenCRDB Research & Development Team</h3>'
            f'<p style="margin:0;font-size:13px;opacity:0.85;">MSc Finance & Investment · Academic Prototype</p>'
            f'<hr style="border-color:rgba(255,255,255,0.3);margin:12px 0;">'
            f'<p style="font-size:13px;margin:0;line-height:1.7;">'
            f'This platform was developed as part of an MSc Finance & Investment academic programme, '
            f'focusing on the practical application of climate finance risk management in emerging market banking. '
            f'The research was conducted in the context of CRDB Bank\'s 2024 sustainability strategy and '
            f'the Bank of Tanzania\'s 2025 Climate Risk Guidelines.'
            f'</p>'
            f'</div>',
            unsafe_allow_html=True,
        )

        st.markdown("#### Acknowledgements")
        acks = [
            ("🏦", "CRDB Bank Plc", "For the 2024 Integrated Annual Report, TCFD Report, and Sustainability Report which form the data foundation of this platform."),
            ("🌍", "Green Climate Fund (GCF)", "For CRDB Bank's GCF accreditation and the TACATDP programme framework that underpins Module 3."),
            ("📐", "IFC / World Bank Group", "IFC Performance Standards framework and EDGE certification methodology used in ESMS and building metrics."),
            ("🌡️", "PCAF Global", "Partnership for Carbon Accounting Financials methodology for Scope 3 Category 15 financed emissions."),
            ("📄", "TCFD / FSB", "Task Force on Climate-related Financial Disclosures — the four-pillar framework at the core of the platform."),
            ("🏛️", "Bank of Tanzania (BoT)", "2025 Climate Risk Guidelines that define CRDB's mandatory disclosure and risk management requirements."),
        ]
        for icon, org, desc in acks:
            st.markdown(
                f'<div style="display:flex;gap:12px;align-items:flex-start;margin:8px 0;">'
                f'<span style="font-size:20px;min-width:24px;">{icon}</span>'
                f'<div><b style="font-size:13px;">{org}</b>'
                f'<p style="font-size:12px;color:#666;margin:2px 0 0 0;">{desc}</p>'
                f'</div></div>',
                unsafe_allow_html=True,
            )

    with team_col2:
        st.markdown("#### Demo Users for Presentation")
        from auth import DEMO_CREDENTIALS, ROLES
        for uname, pw, title, colour in DEMO_CREDENTIALS:
            role_key = [k for k, v in ROLES.items() if v["label"].startswith(title.split()[0])]
            role_desc = ROLES.get(role_key[0] if role_key else "data_analyst", {}).get("description", "")
            st.markdown(
                f'<div style="border:1px solid #e5e7eb;border-left:4px solid {colour};'
                f'padding:10px 14px;border-radius:0 8px 8px 0;margin:4px 0;">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;">'
                f'<b style="font-size:13px;color:{colour};">{title}</b>'
                f'<span style="background:{colour};color:white;font-size:10px;padding:2px 7px;border-radius:8px;">{uname}</span>'
                f'</div>'
                f'<div style="font-size:11px;color:#666;margin-top:3px;">'
                f'<span style="font-family:monospace;background:#f0f4f0;padding:1px 5px;border-radius:3px;">{pw}</span>'
                f'<span style="margin-left:6px;">{role_desc[:80]}...</span>'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown("---")
        st.markdown("#### Contact & Feedback")
        st.markdown(
            f'<div style="background:#f0f9f4;border:1px solid {wd.CRDB_GREEN}44;'
            f'border-radius:8px;padding:14px;">'
            f'<p style="font-size:13px;margin:0;"><b>Platform enquiries:</b><br>'
            f'📧 Sustainable Finance Unit — CRDB Bank Plc<br>'
            f'📍 Azikiwe Street, Dar es Salaam, Tanzania<br>'
            f'🌐 <a href="https://www.crdbbank.co.tz" style="color:{wd.CRDB_GREEN};">www.crdbbank.co.tz</a>'
            f'</p>'
            f'<hr style="border-color:{wd.CRDB_GREEN}22;margin:10px 0;">'
            f'<p style="font-size:11px;color:#888;margin:0;">'
            f'GreenCRDB v1.0 · Academic Prototype · All portfolio data is simulated/illustrative. '
            f'CRDB Bank financial data sourced from the 2024 Integrated Annual Report (actual figures).'
            f'</p>'
            f'</div>',
            unsafe_allow_html=True,
        )

st.markdown("---")
st.caption(
    "GreenCRDB About Page · Platform v1.0 · MSc Finance & Investment Academic Prototype · "
    "Frameworks: TCFD · ISSB S2 · PRB · SASB FN-CB · IFC PS · PCAF · BoT 2025 · TNFD · UN SDGs"
)
