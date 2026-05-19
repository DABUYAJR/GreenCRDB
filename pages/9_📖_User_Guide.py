"""GreenCRDB — User Guide"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import pandas as pd
import web_data as wd
from auth import require_login, sidebar_user_card, ROLES, DEMO_CREDENTIALS, USERS

st.set_page_config(page_title="User Guide | GreenCRDB", page_icon="📖", layout="wide")

require_login()
sidebar_user_card()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    f'<div style="background:linear-gradient(135deg,#1e3a5f 0%,#2563EB 60%,#1D9E75 100%);'
    f'padding:28px 36px;border-radius:12px;margin-bottom:20px;">'
    f'<h1 style="color:white;margin:0;font-size:28px;">📖 GreenCRDB User Guide</h1>'
    f'<p style="color:#bfdbfe;margin:6px 0 0 0;font-size:14px;">'
    f'Complete guide to every module, feature, workflow, and scoring logic in the platform'
    f'</p>'
    f'<div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:10px;">'
    f'<span style="background:rgba(255,255,255,0.2);color:white;padding:3px 10px;border-radius:12px;font-size:11px;">Getting Started</span>'
    f'<span style="background:rgba(255,255,255,0.2);color:white;padding:3px 10px;border-radius:12px;font-size:11px;">Module Walkthroughs</span>'
    f'<span style="background:rgba(255,255,255,0.2);color:white;padding:3px 10px;border-radius:12px;font-size:11px;">Scoring Logic</span>'
    f'<span style="background:rgba(255,255,255,0.2);color:white;padding:3px 10px;border-radius:12px;font-size:11px;">Role Permissions</span>'
    f'<span style="background:rgba(255,255,255,0.2);color:white;padding:3px 10px;border-radius:12px;font-size:11px;">Data Entry Workflows</span>'
    f'<span style="background:rgba(255,255,255,0.2);color:white;padding:3px 10px;border-radius:12px;font-size:11px;">FAQ</span>'
    f'</div>'
    f'</div>',
    unsafe_allow_html=True,
)

(
    tab_start, tab_nav, tab_roles,
    tab_m0, tab_m1, tab_m2, tab_m3, tab_m4,
    tab_ai, tab_workflow, tab_faq,
) = st.tabs([
    "🚀 Getting Started",
    "🗺️ Navigation",
    "🔑 Roles & Permissions",
    "🏦 Module 0 · MultiBank",
    "📊 Module 1 · Sector Risk",
    "🌱 Module 2 · Borrower ESG",
    "💡 Module 3 · Decisions",
    "📋 Module 4 · Regulatory",
    "🤖 AI Copilot",
    "📝 Data Entry Workflows",
    "❓ FAQ",
])


# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — GETTING STARTED
# ════════════════════════════════════════════════════════════════════════════
with tab_start:
    st.markdown("### Welcome to GreenCRDB")
    st.markdown(
        "GreenCRDB is CRDB Bank's **Tanzania Climate-Finance Risk Intelligence Platform**. "
        "It helps the Sustainable Finance Unit integrate climate risk into lending decisions, "
        "track green finance targets, and generate regulatory reports for Bank of Tanzania 2025 compliance."
    )

    gs_col1, gs_col2 = st.columns([1.2, 1])

    with gs_col1:
        st.markdown("#### Step 1 — Log In")
        st.markdown(
            f'<div style="background:#f0f9f4;border-left:4px solid {wd.CRDB_GREEN};'
            f'padding:14px;border-radius:0 8px 8px 0;">'
            f'<ol style="font-size:13px;margin:0;padding-left:18px;line-height:2;">'
            f'<li>Go to <b>app.py</b> home page (or follow the link your administrator provided)</li>'
            f'<li>Enter your <b>username</b> and <b>password</b> in the login form</li>'
            f'<li>Your role determines which modules you can access and what actions you can take</li>'
            f'<li>If you forget your password, contact the <b>Chief Sustainability Officer</b></li>'
            f'</ol>'
            f'<hr style="margin:10px 0;border-color:{wd.CRDB_GREEN}33;">'
            f'<b style="font-size:13px;">For demo / presentation:</b> Use the credentials in the expandable section on the login page'
            f'</div>',
            unsafe_allow_html=True,
        )

        st.markdown("#### Step 2 — Navigate the Platform")
        st.markdown(
            f'<div style="background:#f9fafb;border-left:4px solid #2563EB;'
            f'padding:14px;border-radius:0 8px 8px 0;">'
            f'<p style="font-size:13px;margin:0;">Use the <b>sidebar on the left</b> to navigate between modules. '
            f'Pages you cannot access will show a 🔒 <b>Access Restricted</b> screen. '
            f'Your user card at the top of the sidebar shows your name, role, and access level.</p>'
            f'</div>',
            unsafe_allow_html=True,
        )

        st.markdown("#### Step 3 — Load Platform Data")
        st.markdown(
            f'<div style="background:#fef3c7;border-left:4px solid #D97706;'
            f'padding:14px;border-radius:0 8px 8px 0;">'
            f'<p style="font-size:13px;margin:0;">Before using modules 1–4, ensure the data pipeline has been run. '
            f'If you see "data not found" errors, a <b>Climate Risk Manager or CSO</b> needs to run the scripts '
            f'or upload CSV files via the <b>Data Upload Studio (Module 6)</b>.</p>'
            f'<p style="font-size:12px;color:#92400e;margin:6px 0 0 0;">Scripts: python3 scripts/01... → 02... → 03...</p>'
            f'</div>',
            unsafe_allow_html=True,
        )

    with gs_col2:
        st.markdown("#### Demo Credentials")
        for uname, pw, title, colour in DEMO_CREDENTIALS:
            st.markdown(
                f'<div style="border:1px solid #e5e7eb;border-left:4px solid {colour};'
                f'padding:8px 12px;border-radius:0 6px 6px 0;margin:4px 0;">'
                f'<div style="display:flex;justify-content:space-between;">'
                f'<b style="font-size:12px;">{title}</b>'
                f'<span style="background:{colour};color:white;font-size:10px;padding:1px 7px;border-radius:8px;">{uname}</span>'
                f'</div>'
                f'<span style="font-family:monospace;font-size:11px;background:#f0f4f0;'
                f'padding:1px 6px;border-radius:3px;color:#444;">{pw}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown("---")
        st.markdown("#### What Each Role Can Do")
        role_summary = {
            "Chief Sustainability Officer (CSO)": ("Full access — all modules, data entry, reports, user management", "#7C3AED"),
            "Climate Risk Manager": ("Full Module 1 & Regulatory. Read-only 2 & 3. Can upload data.", "#D97706"),
            "ESG Assessment Officer": ("Full Module 2 (assigned sectors). Read-only 1, 3, 4.", "#1D9E75"),
            "Green Finance Officer": ("Full Module 3. Read-only 1 & 2.", "#2563EB"),
            "Compliance Officer": ("Full read all modules. Full Regulatory. Can generate reports.", "#0F766E"),
            "Data Analyst": ("Read-only Modules 1–3 only. No data entry, no AI, no export.", "#6B7280"),
        }
        for role, (desc, colour) in role_summary.items():
            st.markdown(
                f'<div style="background:{colour}11;border-left:3px solid {colour};'
                f'padding:5px 10px;border-radius:0 4px 4px 0;margin:3px 0;">'
                f'<b style="font-size:12px;color:{colour};">{role}</b>'
                f'<p style="font-size:11px;color:#555;margin:1px 0 0 0;">{desc}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )


# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — NAVIGATION GUIDE
# ════════════════════════════════════════════════════════════════════════════
with tab_nav:
    st.markdown("### Platform Navigation Map")
    st.markdown("Every page in GreenCRDB is accessible from the **left sidebar**. Here's what each page does:")

    pages = [
        ("🏠", "Home (app.py)", "—", "Portfolio KPIs, green ratio tracker, climate scenario chart, PRB radar, CRDB milestones, social impact, group intelligence. Best starting point for any user.", wd.CRDB_GREEN),
        ("🏦", "0 · MultiBank Intelligence", "All roles", "CRDB Group entities (TZ, BI, CD, Insurance) · DFI facilities + regulatory ratios · GCF TACATDP pipeline · Africa league table · East Africa benchmark · Global peers · Onboard new entity.", "#7C3AED"),
        ("📊", "1 · Sector Climate Risk Engine", "All roles", "12-sector climate risk scoring on 5 hazard dimensions. Risk tiers, financial impact scores, regional exposure, heatmaps. Climate Risk Managers can enter/update sector data.", wd.CRDB_GREEN),
        ("🌱", "2 · Borrower ESG Scoring Engine", "All (ESG Officer = assigned sectors)", "60+ borrower ESG scores across E, S, G pillars. Classification (Green/Standard/Watch/High Risk). Sector comparisons. ESG Officers enter assessments for assigned sectors.", "#1D9E75"),
        ("💡", "3 · Climate Finance Decision Engine", "All (GFO full, others read)", "Composite decision scores, lending decision distribution, green finance pipeline, IFC PS alignment, TCFD metrics, climate scenario credit loss. Green Finance Officers record decisions.", "#2563EB"),
        ("📋", "4 · Regulatory Compliance & PCAF", "All (Data Analyst: no access)", "BoT 2025 compliance (13 items) · PCAF financed emissions · SASB FN-CB · PRB radar · SDG alignment · Double materiality matrix · iMBEJU social impact · TNFD readiness tracker.", "#D97706"),
        ("🤖", "5 · AI Sustainability Copilot", "CSO, Climate RM, GFO, Compliance", "Ask questions about the portfolio in plain English. Generate 4 formal reports: TCFD Climate Report, ESG Summary, Green Finance Report, Board Brief. Requires Gemini API key.", "#7C3AED"),
        ("📂", "6 · Data Upload Studio", "CSO, Climate RM, ESG Officer, Compliance", "Upload borrower CSV files, sector data, and portfolio snapshots. Template provided. Validates columns before saving.", "#059669"),
        ("👥", "7 · User Management", "CSO only", "View all platform users, roles, sectors, and regions. Add or modify users (in production build).", "#D85A30"),
        ("ℹ️", "8 · About GreenCRDB", "All roles", "Platform overview, CRDB Bank background, module architecture, frameworks (TCFD, PRB, PCAF etc.), technology stack, data sources, roadmap, team.", "#555"),
        ("📖", "9 · User Guide (this page)", "All roles", "Complete user manual. Getting started, module walkthroughs, scoring formulas, role permissions, data entry workflows, FAQ.", "#2563EB"),
    ]

    for icon, page, access, desc, colour in pages:
        st.markdown(
            f'<div style="border:1px solid #e5e7eb;border-left:5px solid {colour};'
            f'padding:10px 16px;border-radius:0 8px 8px 0;margin:6px 0;">'
            f'<div style="display:flex;justify-content:space-between;align-items:flex-start;">'
            f'<div style="flex:1;">'
            f'<b style="font-size:14px;">{icon} {page}</b>'
            f'<p style="font-size:12px;color:#555;margin:4px 0 0 0;">{desc}</p>'
            f'</div>'
            f'<span style="background:{colour}18;color:{colour};font-size:10px;padding:2px 8px;'
            f'border-radius:8px;font-weight:bold;white-space:nowrap;margin-left:10px;">{access}</span>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True,
        )


# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — ROLES & PERMISSIONS
# ════════════════════════════════════════════════════════════════════════════
with tab_roles:
    st.markdown("### Role-Based Access Control (RBAC)")
    st.markdown(
        "GreenCRDB uses **6 user roles** with different permission levels. "
        "Permissions are enforced server-side — a role that is shown as read-only will not have any data entry forms rendered. "
        "ESG Officers have an additional layer: **sector and region filtering**, so they only see borrowers in their assigned scope."
    )

    # Permission matrix
    st.markdown("#### Full Permission Matrix")
    modules = ["sector_risk", "borrower_esg", "finance_decisions", "regulatory", "ai_copilot", "data_upload"]
    module_labels = ["Module 1\nSector Risk", "Module 2\nBorrower ESG", "Module 3\nDecisions", "Module 4\nRegulatory", "AI Copilot", "Data Upload"]

    matrix_rows = []
    for role_key, role_cfg in ROLES.items():
        row = {"Role": f'{role_cfg["label"]}'}
        for mod, label in zip(modules, module_labels):
            level = role_cfg["module_access"].get(mod, "none")
            row[label] = level
        row["Data Entry"] = ", ".join(role_cfg.get("can_enter_data", [])) or "None"
        row["Reports"] = "✅" if role_cfg.get("can_generate_reports") else "—"
        row["Export"] = "✅" if role_cfg.get("can_export") else "—"
        row["Manage Users"] = "✅" if role_cfg.get("can_manage_users") else "—"
        matrix_rows.append(row)

    matrix_df = pd.DataFrame(matrix_rows)

    level_colours = {"full": "#d1fae5", "read": "#dbeafe", "limited": "#fef3c7", "none": "#fee2e2", "": "white"}

    # Render as styled HTML table
    headers = list(matrix_df.columns)
    header_html = "".join(f'<th style="padding:6px 10px;text-align:center;font-size:11px;background:#f3f4f6;white-space:pre-line;">{h}</th>' for h in headers)
    rows_html = ""
    for i, (_, row) in enumerate(matrix_df.iterrows()):
        bg = "#fafafa" if i % 2 == 0 else "white"
        cells = f'<td style="padding:6px 10px;font-size:12px;font-weight:600;">{row["Role"]}</td>'
        for label in module_labels:
            val = row[label]
            cell_bg = level_colours.get(val, "white")
            cell_text = {"full": "Full ●", "read": "Read ○", "limited": "Limited △", "none": "None ✗"}.get(val, val)
            cell_colour = {"full": "#065f46", "read": "#1e40af", "limited": "#92400e", "none": "#991b1b"}.get(val, "#333")
            cells += f'<td style="padding:6px 10px;background:{cell_bg};text-align:center;font-size:11px;color:{cell_colour};">{cell_text}</td>'
        for col in ["Data Entry", "Reports", "Export", "Manage Users"]:
            cells += f'<td style="padding:6px 10px;text-align:center;font-size:12px;">{row[col]}</td>'
        rows_html += f'<tr style="background:{bg};">{cells}</tr>'

    st.markdown(
        f'<div style="overflow-x:auto;">'
        f'<table style="width:100%;border-collapse:collapse;font-size:12px;">'
        f'<thead><tr style="border-bottom:2px solid #e5e7eb;">{header_html}</tr></thead>'
        f'<tbody>{rows_html}</tbody>'
        f'</table>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("#### Sector & Region Filtering (ESG Officers)")
    st.markdown(
        f'<div style="background:#d1fae5;border-left:4px solid #1D9E75;padding:14px;border-radius:0 8px 8px 0;">'
        f'<b>ESG Assessment Officers</b> have an additional access restriction beyond module-level permissions:<br>'
        f'<ul style="font-size:13px;margin:6px 0;padding-left:18px;">'
        f'<li>They can only <b>view and enter data</b> for their <b>assigned sectors</b> (e.g., Agriculture, Energy, Mining)</li>'
        f'<li>They can only view borrowers in their <b>assigned regions</b> (e.g., Dar es Salaam, Arusha)</li>'
        f'<li>All tables and forms in Modules 2 & 3 automatically filter to their scope</li>'
        f'<li>Example: David Osei (dosei) can only see borrowers in Agriculture/Energy/Manufacturing/Mining in Dar/Arusha/Mwanza</li>'
        f'</ul>'
        f'The CSO can assign sectors and regions per user in the User Management page.'
        f'</div>',
        unsafe_allow_html=True,
    )


# ════════════════════════════════════════════════════════════════════════════
# TAB 4 — MODULE 0: MULTIBANK INTELLIGENCE
# ════════════════════════════════════════════════════════════════════════════
with tab_m0:
    st.markdown("### Module 0 — MultiBank Intelligence")
    st.markdown(
        "This module gives a **group-level view** of CRDB Bank's consolidated sustainability position "
        "and benchmarks the bank against African and global peers."
    )

    st.markdown("#### Six Tabs in This Module")
    m0_tabs = [
        ("🏦 CRDB Group Entities", "View each entity (TZ, Burundi, Congo, Insurance) individually. Click the radio buttons to switch entities. See portfolio size, ITR, green ratio, PAT, climate framework, key risks, and green milestones. Compare all entities on portfolio size and ITR bubble chart."),
        ("💰 DFI Facilities & Ratios", "Track all USD 600M+ DFI facilities (MUFG, GCF, FMO, Proparco, GCPF, IFC). View BoT regulatory compliance margins (how far above/below minimum ratios). See the GCF TACATDP USD 200M project pipeline with 6 components. Environmental operations (EDGE, recycling, green projects)."),
        ("🌍 Africa Sustainability Ranking", "CRDB Bank's position in the Africa Top 20 banks league table. Composite score based on TCFD (20%), PRB (15%), green ratio (25%), ITR (20%), DFI partnerships (10%), reporting quality (10%). See unique competitive advantages vs. areas to improve."),
        ("📊 East Africa Benchmark", "Detailed 10-bank East Africa peer comparison across ESG score, climate disclosure quality, DFI access score, green ratio, ESMS quality, BoT compliance equivalence. Includes radar chart comparing CRDB vs KCB vs Equity Bank on 6 dimensions."),
        ("🏆 Global Peer Comparison", "Benchmarks CRDB against IFC portfolio banks and GCF-accredited institutions in emerging markets globally (Bangladesh, Ecuador, Mongolia, Georgia, Sri Lanka, etc.). Shows where CRDB leads (DFI network, Kijani Bond) and gaps (green ratio, ITR)."),
        ("➕ Onboard New Entity", "6-step wizard to register a new bank entity (e.g. future CRDB partnerships). Collects entity info, portfolio data, climate profile, regulatory framework, users, and launches the entity on the platform."),
    ]
    for tab_name, desc in m0_tabs:
        st.markdown(
            f'<div style="border-left:4px solid {wd.CRDB_GREEN};background:#f0f9f4;'
            f'padding:10px 14px;border-radius:0 6px 6px 0;margin:6px 0;">'
            f'<b style="font-size:13px;">{tab_name}</b>'
            f'<p style="font-size:12px;color:#444;margin:4px 0 0 0;">{desc}</p>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("#### Key Metrics Explained")
    explain_items = [
        ("Group ITR (°C)", "Implied Temperature Rise — weighted average across all entities by portfolio size. CRDB Group: 2.73°C vs Paris 1.5°C target. Lower is better."),
        ("Green Asset Ratio (%)", "Proportion of total loan book classified as green finance (GCF-eligible, Kijani Bond projects, renewable energy, climate-smart agriculture). CRDB 2024 actual: 7%. Target: 15% by 2030."),
        ("Group Financed Emissions", "PCAF Scope 3 Category 15 — emissions from the bank's lending activities. 1,247 ktCO₂e (simulated proxy). Dominated by Agriculture and Mining sectors."),
        ("Africa Rank #8", "Composite sustainability score based on 6 dimensions. CRDB ranks #8 of Top 20 African banks and #3 in East Africa. CRDB leads in GCF access and DFI partnerships; trails on absolute green ratio."),
    ]
    for metric, explanation in explain_items:
        st.markdown(
            f'<div style="display:flex;gap:12px;padding:8px 0;border-bottom:1px solid #f3f4f6;">'
            f'<div style="min-width:180px;font-weight:600;font-size:13px;color:{wd.CRDB_GREEN};">{metric}</div>'
            f'<div style="font-size:13px;color:#444;">{explanation}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )


# ════════════════════════════════════════════════════════════════════════════
# TAB 5 — MODULE 1: SECTOR CLIMATE RISK ENGINE
# ════════════════════════════════════════════════════════════════════════════
with tab_m1:
    st.markdown("### Module 1 — Sector Climate Risk Engine")
    st.markdown(
        "Module 1 is the **foundation of the entire pipeline**. It scores all 12 sectors of CRDB's portfolio "
        "on physical and transition climate risk, producing a composite risk score that feeds into Modules 2 and 3."
    )

    m1_col1, m1_col2 = st.columns([1.2, 1])
    with m1_col1:
        st.markdown("#### The 5 Hazard Dimensions & Weights")
        hazards = [
            ("🌵", "Drought Risk", 25, "Probability and severity of drought events affecting sector output and borrower repayment capacity. Highest weight — Agriculture (28% of CRDB book) is Tanzania's most drought-exposed sector."),
            ("🌊", "Flood Risk", 20, "River flooding, flash floods, and coastal inundation risk. Agriculture, Real Estate, and Transport are most exposed. Lake Victoria and coastal zones are high-risk areas."),
            ("🌡️", "Extreme Temperature Risk", 20, "Heat stress on crops, livestock, and worker productivity. Also covers urban heat island effects on energy demand and infrastructure."),
            ("⚡", "Transition Risk", 20, "Risk from climate policy changes (carbon pricing, fossil fuel regulations), technology shifts (EVs, solar), and market shifts. Mining and Energy sectors are most exposed."),
            ("💧", "Water Stress Risk", 15, "Long-term water scarcity risk driven by population growth, irrigation demand, and reduced rainfall. Agriculture and Manufacturing are most exposed."),
        ]
        for icon, name, weight, desc in hazards:
            st.markdown(
                f'<div style="display:flex;gap:12px;align-items:flex-start;padding:8px 12px;'
                f'background:#f9fafb;border-left:4px solid {wd.CRDB_GREEN};border-radius:0 6px 6px 0;margin:4px 0;">'
                f'<span style="font-size:20px;">{icon}</span>'
                f'<div style="flex:1;">'
                f'<div style="display:flex;justify-content:space-between;">'
                f'<b style="font-size:13px;">{name}</b>'
                f'<span style="background:{wd.CRDB_GREEN};color:white;font-size:11px;padding:1px 7px;border-radius:8px;">{weight}%</span>'
                f'</div>'
                f'<p style="font-size:12px;color:#555;margin:3px 0 0 0;">{desc}</p>'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    with m1_col2:
        st.markdown("#### Scoring Formula & Risk Tiers")
        st.markdown(
            f'<div style="background:#1e3a5f;color:#e0f2fe;padding:16px;border-radius:10px;font-family:monospace;font-size:13px;">'
            f'<div style="color:#6ee7b7;font-weight:bold;margin-bottom:8px;">composite_climate_risk (0–10):</div>'
            f'= drought × 0.25<br>'
            f'+ flood × 0.20<br>'
            f'+ temperature × 0.20<br>'
            f'+ transition × 0.20<br>'
            f'+ water_stress × 0.15<br><br>'
            f'<div style="color:#6ee7b7;">financial_climate_risk:</div>'
            f'= composite × loan_book_share<br>'
            f'× normalised_exposure_factor'
            f'</div>',
            unsafe_allow_html=True,
        )

        st.markdown("**Risk Tier Thresholds:**")
        tiers = [
            ("Low", "< 4.5", "#2ecc71", "Manageable climate exposure — standard monitoring"),
            ("Medium", "4.5 – 6.0", "#f39c12", "Elevated risk — enhanced due diligence required"),
            ("High", "6.0 – 7.5", "#e74c3c", "Significant risk — conditional lending criteria"),
            ("Critical", "> 7.5", "#7b241c", "Severe risk — senior approval required; active mitigation plan"),
        ]
        for tier, range_str, colour, action in tiers:
            st.markdown(
                f'<div style="background:{colour}22;border-left:4px solid {colour};'
                f'padding:6px 12px;border-radius:0 4px 4px 0;margin:4px 0;">'
                f'<div style="display:flex;justify-content:space-between;">'
                f'<b style="color:{colour};">{tier}</b>'
                f'<span style="font-size:12px;font-family:monospace;">{range_str}</span>'
                f'</div>'
                f'<p style="font-size:11px;color:#555;margin:2px 0 0 0;">{action}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown("---")
        st.markdown("#### How to Read the Module")
        st.markdown(
            "<ul style='font-size:13px;'>"
            "<li><b>Financial Climate Risk chart</b> — horizontal bars showing sector exposure. Agriculture and Mining typically highest.</li>"
            "<li><b>Risk Tier table</b> — colour-coded. Filter by tier to focus on High/Critical sectors.</li>"
            "<li><b>Regional Heatmap</b> — which Tanzania regions are most exposed to each hazard.</li>"
            "<li><b>Sector Heatmap</b> — all 5 hazards across all 12 sectors simultaneously.</li>"
            "</ul>",
            unsafe_allow_html=True,
        )


# ════════════════════════════════════════════════════════════════════════════
# TAB 6 — MODULE 2: BORROWER ESG SCORING ENGINE
# ════════════════════════════════════════════════════════════════════════════
with tab_m2:
    st.markdown("### Module 2 — Borrower ESG Scoring Engine")
    st.markdown(
        "Module 2 takes each of CRDB's ~6.4M borrowers (simulated as ~60 per sector) and assigns "
        "an **E/S/G score** that is then blended with the sector climate risk score from Module 1 "
        "to generate a borrower classification."
    )

    m2_col1, m2_col2 = st.columns([1.2, 1])
    with m2_col1:
        st.markdown("#### The E / S / G Pillars & Weights")
        pillars = [
            ("E", "Environmental", 40, "#1D9E75",
             "Carbon footprint, energy efficiency, resource use, waste management, land use practices, "
             "water usage, pollution controls, deforestation exposure. "
             "Blended with sector climate risk score: high-risk sector = lower environmental baseline."),
            ("S", "Social", 30, "#2563EB",
             "Labour standards, health & safety, community relations, financial inclusion impact, "
             "gender equality, customer satisfaction, human rights in supply chain. "
             "CRDB's ESMS (IFC PS2 & PS5) provides the screening framework."),
            ("G", "Governance", 30, "#7C3AED",
             "Board independence, audit quality, transparency & disclosure quality, anti-corruption, "
             "executive compensation alignment, regulatory compliance record. "
             "Proxy: company size, listed vs private, reporting frequency."),
        ]
        for letter, name, weight, colour, desc in pillars:
            st.markdown(
                f'<div style="border:2px solid {colour};border-radius:10px;padding:12px 16px;margin:8px 0;">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;">'
                f'<div style="display:flex;align-items:center;gap:10px;">'
                f'<div style="background:{colour};color:white;width:32px;height:32px;border-radius:50%;'
                f'display:flex;align-items:center;justify-content:center;font-weight:900;font-size:16px;">{letter}</div>'
                f'<b style="font-size:15px;">{name}</b>'
                f'</div>'
                f'<span style="background:{colour};color:white;padding:2px 10px;border-radius:10px;font-size:13px;font-weight:bold;">{weight}%</span>'
                f'</div>'
                f'<p style="font-size:12px;color:#555;margin:8px 0 0 0;">{desc}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )

    with m2_col2:
        st.markdown("#### ESG Scoring Formula")
        st.markdown(
            f'<div style="background:#1e3a5f;color:#e0f2fe;padding:16px;border-radius:10px;font-family:monospace;font-size:13px;">'
            f'<div style="color:#6ee7b7;font-weight:bold;margin-bottom:8px;">ESG Composite Score (0–10):</div>'
            f'esg_composite<br>'
            f'= E_score × 0.40<br>'
            f'+ S_score × 0.30<br>'
            f'+ G_score × 0.30<br><br>'
            f'<div style="color:#fde68a;">Where each pillar is scored 0–10<br>'
            f'(generated from sector baselines<br>'
            f'+ noise simulation in Module 2)</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        st.markdown("**Borrower Classification Tiers:**")
        classes = [
            ("Green Eligible", "≥ 7.5 / 10", "#1D9E75", "Qualifies for green finance products (Kijani Bond, GCF facility, SLL)"),
            ("Standard", "5.5 – 7.4", "#378ADD", "Standard lending — some green potential with conditions"),
            ("Watch List", "4.0 – 5.4", "#EF9F27", "Enhanced monitoring — improvement plan required"),
            ("High Risk", "< 4.0", "#D85A30", "Restricted lending — senior credit committee review"),
        ]
        for cls, threshold, colour, desc in classes:
            st.markdown(
                f'<div style="background:{colour}22;border-left:4px solid {colour};'
                f'padding:8px 12px;border-radius:0 6px 6px 0;margin:4px 0;">'
                f'<div style="display:flex;justify-content:space-between;">'
                f'<b style="color:{colour};font-size:13px;">{cls}</b>'
                f'<span style="font-size:12px;font-family:monospace;">{threshold}</span>'
                f'</div>'
                f'<p style="font-size:11px;color:#555;margin:2px 0 0 0;">{desc}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown("---")
        st.markdown("#### How to Use Module 2")
        st.markdown(
            "<ul style='font-size:13px;'>"
            "<li><b>Sector selector</b> — filter to one sector to see all borrowers in it</li>"
            "<li><b>ESG heatmap</b> — compare E, S, G scores side by side across sectors</li>"
            "<li><b>Classification distribution chart</b> — see what % of portfolio is Green/Standard/Watch/High Risk</li>"
            "<li><b>Borrower table</b> — sort by ESG score, export as CSV (if role permits)</li>"
            "<li><b>Data entry tab</b> (ESG Officers only) — enter/update ESG assessments for assigned borrowers</li>"
            "</ul>",
            unsafe_allow_html=True,
        )


# ════════════════════════════════════════════════════════════════════════════
# TAB 7 — MODULE 3: FINANCE DECISION ENGINE
# ════════════════════════════════════════════════════════════════════════════
with tab_m3:
    st.markdown("### Module 3 — Climate Finance Decision Engine")
    st.markdown(
        "Module 3 is the **core decision-making engine**. It blends borrower ESG scores with sector climate risk "
        "to generate composite financing decisions, and tracks the green finance pipeline, TCFD metrics, "
        "IFC Performance Standards alignment, and climate scenario credit losses."
    )

    m3_col1, m3_col2 = st.columns([1.2, 1])
    with m3_col1:
        st.markdown("#### The Decision Scoring Formula")
        st.markdown(
            f'<div style="background:#1a2744;color:#bfdbfe;padding:18px;border-radius:10px;font-family:monospace;font-size:13px;line-height:1.9;">'
            f'<div style="color:#93c5fd;font-weight:bold;margin-bottom:8px;">STEP 1 — Convert scales to 0–100:</div>'
            f'esg_100 = esg_composite × 10<br>'
            f'&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#86efac;">(0–10 → 0–100)</span><br><br>'
            f'sector_readiness_100<br>'
            f'= (10 − composite_climate_risk) × 10<br>'
            f'&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#fde68a;">⚠ INVERSION: high risk → low readiness</span><br><br>'
            f'<div style="color:#93c5fd;font-weight:bold;margin-top:8px;margin-bottom:8px;">STEP 2 — Blend the scores:</div>'
            f'composite_decision_score<br>'
            f'= esg_100 × 0.55<br>'
            f'+ sector_readiness_100 × 0.45<br><br>'
            f'<div style="color:#93c5fd;font-weight:bold;margin-top:8px;margin-bottom:8px;">STEP 3 — Apply decision thresholds:</div>'
            f'≥ 65 → <span style="color:#86efac;">Approve</span><br>'
            f'52–64 → <span style="color:#93c5fd;">Conditional Approval</span><br>'
            f'40–51 → <span style="color:#fde68a;">Review Required</span><br>'
            f'&lt; 40 → <span style="color:#fca5a5;">Decline</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

        st.markdown("#### Why Sector Risk is Inverted")
        st.markdown(
            f'<div style="background:#fef3c7;border-left:4px solid #D97706;padding:12px;border-radius:0 6px 6px 0;">'
            f'<b>Critical concept:</b> The composite_climate_risk from Module 1 is on a 0–10 scale where '
            f'<b>higher = more risky</b>. In Module 3, we need a 0–100 score where <b>higher = more creditworthy</b>. '
            f'So we invert: <code>(10 − risk_score) × 10</code> — a sector with risk score 8.0 gets readiness 20/100, '
            f'while a sector with risk score 2.0 gets readiness 80/100. '
            f'<b>Do not pass climate risk directly — inversion is required.</b>'
            f'</div>',
            unsafe_allow_html=True,
        )

    with m3_col2:
        st.markdown("#### TCFD Metrics Dashboard")
        st.markdown(
            "<ul style='font-size:12px;'>"
            "<li><b>Weighted average ESG composite</b> — portfolio-wide ESG quality</li>"
            "<li><b>High/Critical risk sector exposure</b> — % of book in High/Critical risk sectors</li>"
            "<li><b>Green finance pipeline</b> — TZS amount in GCF-eligible pipeline</li>"
            "<li><b>Portfolio ITR</b> — Implied Temperature Rise (°C) vs 1.5°C Paris target</li>"
            "<li><b>Financed emissions</b> — PCAF Scope 3 Category 15 estimate</li>"
            "</ul>",
            unsafe_allow_html=True,
        )

        st.markdown("#### IFC Performance Standards (PS)")
        st.markdown(
            "<ul style='font-size:12px;'>"
            "<li><b>PS1</b> — Environmental & Social Assessment</li>"
            "<li><b>PS2</b> — Labour & Working Conditions</li>"
            "<li><b>PS3</b> — Resource Efficiency & Pollution Prevention</li>"
            "<li><b>PS4</b> — Community Health & Safety</li>"
            "<li><b>PS5</b> — Land Acquisition & Resettlement</li>"
            "<li><b>PS6</b> — Biodiversity Conservation</li>"
            "<li><b>PS7</b> — Indigenous Peoples</li>"
            "<li><b>PS8</b> — Cultural Heritage</li>"
            "</ul>"
            "<p style='font-size:12px;color:#555;'>Each PS is scored 0–10. The bar chart shows alignment tier "
            "(Full / Adequate / Partial / Insufficient) and key gaps to address.</p>",
            unsafe_allow_html=True,
        )

        st.markdown("#### Climate Scenario Analysis")
        scenarios = [
            ("Base Case", "Business as usual — moderate physical risk, no abrupt transition", "#3B82F6"),
            ("Accelerated Transition", "Rapid carbon pricing, fossil fuel phase-out — transition shock to Mining/Energy", "#F59E0B"),
            ("Severe Physical Shock", "Extreme weather events — drought + flood compound in Agriculture/Real Estate", "#D85A30"),
        ]
        for name, desc, colour in scenarios:
            st.markdown(
                f'<div style="background:{colour}22;border-left:4px solid {colour};'
                f'padding:8px 12px;border-radius:0 6px 6px 0;margin:4px 0;">'
                f'<b style="color:{colour};">{name}</b>'
                f'<p style="font-size:11px;color:#555;margin:2px 0 0 0;">{desc}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )


# ════════════════════════════════════════════════════════════════════════════
# TAB 8 — MODULE 4: REGULATORY COMPLIANCE
# ════════════════════════════════════════════════════════════════════════════
with tab_m4:
    st.markdown("### Module 4 — Regulatory Compliance & PCAF Analytics")
    st.markdown(
        "Module 4 is the **compliance and reporting hub**. It brings together all regulatory frameworks "
        "that CRDB Bank must meet — from the mandatory Bank of Tanzania 2025 Guidelines to voluntary "
        "frameworks like PRB, SASB, and TNFD — plus social impact and nature-related disclosure readiness."
    )

    m4_tabs_guide = [
        ("🏛️ BoT 2025 Compliance", "13-item compliance checklist across 4 pillars: Governance (3), Risk Management (4), Disclosure (4), Strategy (2). Shows status (Compliant / In Progress) with evidence for each item. 12/13 fully compliant; 1 in progress (financed emissions — PCAF adoption target Score 2 by 2026)."),
        ("🌡️ PCAF Emissions", "Simulated Scope 3 Category 15 financed emissions by sector using IPCC AR6 Africa emission intensity proxies. PCAF Data Quality Score 4 (economic-activity proxy — standard for emerging markets). Includes ITR gauge showing portfolio at 2.73°C vs Paris 1.5°C target. Sector ITR contribution breakdown."),
        ("📊 SASB FN-CB", "Five SASB FN-CB Commercial Banks disclosure topics scored 0–5: Data Security (3.8), Financial Inclusion (4.2), ESG in Credit Analysis (3.5), Business Ethics (4.6), Systematic Risk Management (3.9). Overall average 4.0/5.0."),
        ("🤝 PRB Principles", "Six PRB pillars scored 0–5 with radar chart and bar chart. CRDB above 3.0/5.0 threshold across all pillars. Recommended next step: formal PRB signatory application (already a signatory)."),
        ("🌐 UN SDGs", "Portfolio alignment to 9 SDGs most relevant to a Tanzanian commercial bank. SDG 17 (Partnerships) and SDG 1 (No Poverty) are CRDB's strongest. SDG 15 (Life on Land) is weakest — TNFD gap."),
        ("⬡ Materiality Matrix", "Double materiality scatter plot: x-axis = financial materiality (how ESG issues affect CRDB), y-axis = impact materiality (CRDB's impact on society/environment). Priority Action Zone = top-right quadrant. Agricultural Climate Risk and Physical Climate Risk are top priorities."),
        ("🤝 Social Impact & iMBEJU", "iMBEJU Community Investment Programme: TZS 7.76 Bn across 153 projects, 218,471 beneficiaries. Investment by pillar (Education, Healthcare, Livelihoods, Environment). Human capital metrics: 41% female workforce, 36% female board, 47 PWDs employed. Financial inclusion KPIs."),
        ("🌿 TNFD Readiness", "8-requirement TNFD readiness tracker across 4 pillars (Governance, Strategy, Risk Management, Metrics & Targets). Status: 2 Compliant, 3 In Progress/Partial, 3 Planned. Gap analysis: what TCFD work transfers to TNFD vs. what is TNFD-specific. Roadmap: pilot 2025, full report 2026."),
    ]
    for tab_name, desc in m4_tabs_guide:
        st.markdown(
            f'<div style="border-left:4px solid #D97706;background:#fffbeb;'
            f'padding:10px 14px;border-radius:0 6px 6px 0;margin:6px 0;">'
            f'<b style="font-size:13px;color:#92400e;">{tab_name}</b>'
            f'<p style="font-size:12px;color:#444;margin:4px 0 0 0;">{desc}</p>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("#### KPI Strip at Top of Module 4")
    st.markdown(
        "The 5 KPIs at the top of Module 4 give an at-a-glance regulatory summary:\n\n"
        "| KPI | Value | What it means |\n"
        "|-----|-------|---------------|\n"
        "| Portfolio ITR | 2.73°C | +1.23°C above Paris 1.5°C — action required |\n"
        "| Financed Emissions | ~1,247 ktCO₂e | PCAF Scope 3 proxy — agriculture dominates |\n"
        "| Green Asset Ratio | 7% | 2024 actual — 8% points gap to 15% by 2030 |\n"
        "| BoT 2025 | 12/13 items | 92% compliance — 1 in progress |\n"
        "| Moody's Rating | B1 | First Tanzanian bank — Stable outlook |"
    )


# ════════════════════════════════════════════════════════════════════════════
# TAB 9 — AI COPILOT
# ════════════════════════════════════════════════════════════════════════════
with tab_ai:
    st.markdown("### Module 5 — AI Sustainability Copilot")
    st.markdown(
        "The AI Copilot uses **Google Gemini** (free tier available) to answer questions about CRDB's "
        "sustainability portfolio and generate four types of formal sustainability reports."
    )

    ai_col1, ai_col2 = st.columns([1.2, 1])
    with ai_col1:
        st.markdown("#### Setting Up the API Key")
        st.markdown(
            f'<div style="background:#d1fae5;border-left:4px solid {wd.CRDB_GREEN};padding:14px;border-radius:0 8px 8px 0;">'
            f'<ol style="font-size:13px;margin:0;padding-left:18px;line-height:2.2;">'
            f'<li>Go to <b>aistudio.google.com/apikey</b> and create a free Google account</li>'
            f'<li>Click <b>"Create API Key"</b> — copy the key (starts with "AIza...")</li>'
            f'<li>In GreenCRDB, open <b>Module 5 — AI Copilot</b></li>'
            f'<li>Paste your API key in the sidebar field labelled "Google Gemini API Key"</li>'
            f'<li>Click "Confirm Key" — the copilot is now active</li>'
            f'</ol>'
            f'<p style="font-size:11px;color:#065f46;margin:6px 0 0 0;">Free tier: 15 requests/minute, 1M tokens/day — more than enough for demo and regular use.</p>'
            f'</div>',
            unsafe_allow_html=True,
        )

        st.markdown("#### What to Ask the Copilot")
        questions = [
            "What is CRDB's most climate-exposed sector and what should we do about it?",
            "Generate a 300-word summary of our TCFD compliance status",
            "Which borrowers should we prioritise for green finance restructuring?",
            "What is our portfolio ITR and how does it compare to the Paris target?",
            "Explain the Kijani Bond and how it helps us reach our 15% green ratio target",
            "What are the three biggest gaps in our IFC Performance Standards alignment?",
            "Summarise our BoT 2025 compliance position for the Board",
            "What climate scenario poses the highest credit loss risk to CRDB?",
        ]
        for q in questions:
            st.markdown(
                f'<div style="background:#f9fafb;border-left:3px solid #7C3AED;'
                f'padding:6px 12px;border-radius:0 4px 4px 0;margin:3px 0;font-size:12px;font-style:italic;">'
                f'"{q}"'
                f'</div>',
                unsafe_allow_html=True,
            )

    with ai_col2:
        st.markdown("#### 4 Formal Report Templates")
        reports = [
            ("📄", "TCFD Climate Risk Report", "Structured TCFD four-pillar report (Governance, Strategy, Risk Management, Metrics & Targets). ~800 words. Cites actual CRDB portfolio data.", wd.CRDB_GREEN),
            ("🌱", "ESG Portfolio Summary", "Sector-by-sector ESG assessment narrative. Highlights top green eligible borrowers. Recommends priority sectors for ESG improvement.", "#1D9E75"),
            ("💰", "Green Finance Opportunity Report", "Green finance pipeline analysis. Kijani Bond progress. GCF TACATDP deployment. Recommended green products per sector.", "#2563EB"),
            ("📊", "Board Climate Risk Brief", "Executive-level 1-page brief for CRDB Board. Key risks, green ratio progress, regulatory compliance status, recommended Board actions.", "#D97706"),
        ]
        for icon, name, desc, colour in reports:
            st.markdown(
                f'<div style="border:1px solid #e5e7eb;border-left:4px solid {colour};'
                f'padding:10px 14px;border-radius:0 8px 8px 0;margin:5px 0;">'
                f'<b style="font-size:13px;">{icon} {name}</b>'
                f'<p style="font-size:12px;color:#555;margin:4px 0 0 0;">{desc}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown("---")
        st.markdown("#### How Portfolio Context is Built")
        st.markdown(
            f'<div style="background:#EFF6FF;border-left:4px solid #2563EB;padding:12px;border-radius:0 6px 6px 0;">'
            f'<p style="font-size:12px;margin:0;">'
            f'Every AI query automatically includes a <b>full portfolio context string</b> built by '
            f'<code>web_data.build_portfolio_context()</code>. This includes: all sector risk scores, '
            f'borrower ESG classification summary, lending decisions, TCFD metrics, climate scenarios, '
            f'IFC PS alignment, financed emissions, PRB scores, SDG alignment, and all actual CRDB 2024 '
            f'financial figures. The AI always answers with real portfolio data — not generic responses.'
            f'</p>'
            f'</div>',
            unsafe_allow_html=True,
        )


# ════════════════════════════════════════════════════════════════════════════
# TAB 10 — DATA ENTRY WORKFLOWS
# ════════════════════════════════════════════════════════════════════════════
with tab_workflow:
    st.markdown("### Data Entry & Common Workflows")
    st.markdown("Step-by-step instructions for the most common tasks performed in GreenCRDB.")

    workflows = [
        {
            "title": "🌱 Record a New Lending Decision",
            "who": "Green Finance Officer · CSO",
            "module": "Module 3 → ✏️ Record Lending Decision tab",
            "steps": [
                "Navigate to Module 3 — Climate Finance Decision Engine",
                "Click the '✏️ Record Lending Decision' tab (only visible to Green Finance Officers and CSOs)",
                "Enter Borrower ID (e.g. BW-042) and Borrower Name",
                "Select Sector, Region, and Loan Amount (TZS Mn)",
                "Set the ESG Score (0–100) — use Module 2 output as reference",
                "Set the Sector Climate Risk Score (0–100, lower = more ready) — reference Module 1",
                "Review the auto-calculated Composite Decision Score and System Decision",
                "Override the decision if required and select the appropriate product",
                "Tick 'ESMS Cleared' if IFC PS1–PS8 screening is complete (required for GCF/DFI loans)",
                "Add officer notes (conditions, covenants, IFC PS gaps)",
                "Click '✅ Record Lending Decision' to save",
            ]
        },
        {
            "title": "📊 Update Sector Climate Risk Scores",
            "who": "Climate Risk Manager · CSO",
            "module": "Module 1 → Data Entry tab",
            "steps": [
                "Navigate to Module 1 — Sector Climate Risk Engine",
                "Click the data entry tab (visible to Climate Risk Managers and CSOs)",
                "Select the sector you want to update",
                "Adjust the 5 hazard sliders (Drought, Flood, Temperature, Transition, Water Stress)",
                "The composite score auto-calculates in real-time",
                "Save the updated scores — they will immediately flow through to Modules 2 and 3",
                "Alternatively: re-run scripts/01_TZCRIP_Module1_Sector_Climate_Risk.py with updated CSV data",
            ]
        },
        {
            "title": "📂 Upload Portfolio Data (CSV)",
            "who": "Climate Risk Manager · ESG Officer · CSO · Compliance Officer",
            "module": "Module 6 — Data Upload Studio",
            "steps": [
                "Navigate to Module 6 — Data Upload Studio",
                "Download the CRDB GreenCRDB template CSV by clicking 'Download Template'",
                "Fill in your borrower/sector data in the template (do not rename columns)",
                "Go back to Module 6 and select the file type you are uploading",
                "Click 'Browse files' and select your completed CSV",
                "Review the preview — check that columns have mapped correctly",
                "Click 'Upload and Validate' — the system checks for missing required columns",
                "If validation passes, click 'Save to Platform' — data is now live in all modules",
            ]
        },
        {
            "title": "🤖 Generate a Sustainability Report",
            "who": "CSO · Climate Risk Manager · Compliance Officer · Green Finance Officer",
            "module": "Module 5 — AI Sustainability Copilot",
            "steps": [
                "Ensure your Gemini API key is entered in the sidebar (see AI Copilot guide above)",
                "Navigate to Module 5 — AI Sustainability Copilot",
                "Click the report type you want: TCFD Report / ESG Summary / Green Finance / Board Brief",
                "The AI will use your live portfolio data to generate the report (takes ~10–20 seconds)",
                "Review the generated report text",
                "Click 'Copy to clipboard' or 'Download as .txt' to export",
                "Paste into your Word/Google Docs template for final formatting before submission",
            ]
        },
        {
            "title": "🏦 Onboard a New Bank Entity",
            "who": "CSO",
            "module": "Module 0 → ➕ Onboard New Entity tab",
            "steps": [
                "Navigate to Module 0 — MultiBank Intelligence",
                "Click the '➕ Onboard New Entity' tab",
                "Step 1: Enter entity name, country, currency, entity type, established year, regulator",
                "Step 2: Enter portfolio size, number of borrowers, primary sectors, data method",
                "Step 3: Set country climate risk profile (5 hazard sliders) — composite auto-calculates",
                "Step 4: Map regulatory frameworks (TCFD, PRB, GCF, ESMS, etc.)",
                "Step 5: Configure users — Sustainability Head, Risk Officer, Data Analyst",
                "Step 6: Review all data and click '🚀 Launch Entity'",
                "Entity appears in Group Intelligence view; data onboarding next steps are shown",
            ]
        },
    ]

    for wf in workflows:
        with st.expander(f'{wf["title"]} — {wf["who"]}', expanded=False):
            wf_c1, wf_c2 = st.columns([1.5, 1])
            with wf_c1:
                st.markdown(f'**Module:** `{wf["module"]}`')
                st.markdown("**Steps:**")
                for i, step in enumerate(wf["steps"], 1):
                    st.markdown(
                        f'<div style="display:flex;gap:10px;align-items:flex-start;margin:5px 0;">'
                        f'<div style="background:{wd.CRDB_GREEN};color:white;min-width:22px;height:22px;border-radius:50%;'
                        f'display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:bold;">{i}</div>'
                        f'<span style="font-size:13px;">{step}</span>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )
            with wf_c2:
                st.markdown(
                    f'<div style="background:#f0f9f4;border:1px solid {wd.CRDB_GREEN}44;'
                    f'border-radius:8px;padding:12px;">'
                    f'<b>Who can do this:</b><br>'
                    f'<span style="font-size:13px;color:{wd.CRDB_GREEN};">{wf["who"]}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )


# ════════════════════════════════════════════════════════════════════════════
# TAB 11 — FAQ
# ════════════════════════════════════════════════════════════════════════════
with tab_faq:
    st.markdown("### Frequently Asked Questions")

    faqs = [
        {
            "q": "Why does the platform say 'data not found' or show empty dashboards?",
            "a": "The platform pipeline scripts have not been run yet. Ask your Climate Risk Manager or CSO to run the 3 scripts in order (01 → 02 → 03) from the scripts/ directory, or upload the required CSV files via Module 6 — Data Upload Studio.",
            "cat": "Technical",
        },
        {
            "q": "The composite decision score is calculated automatically — can I override it?",
            "a": "Yes. In Module 3 → Record Lending Decision, the system auto-calculates the composite score and suggests a decision. You can override the final decision using the dropdown. The system decision is always shown so it is auditable. Your override and notes are saved with the record.",
            "cat": "Module 3",
        },
        {
            "q": "Why is sector climate risk inverted when calculating decision scores?",
            "a": "Module 1 produces composite_climate_risk on 0–10 where higher = more risky. Module 3 needs a score where higher = more creditworthy. So we convert: sector_readiness = (10 − risk_score) × 10. A sector with climate risk 8.0 has readiness 20/100. A low-risk sector (2.0) has readiness 80/100. This prevents high-risk sectors from getting artificially inflated decision scores.",
            "cat": "Scoring Logic",
        },
        {
            "q": "What is the green asset ratio and how is it calculated?",
            "a": "The green asset ratio = (green-eligible loans / total loan book) × 100. CRDB's 2024 actual ratio is 7% (from the 2024 Integrated Annual Report). In the platform, it is computed from the green finance pipeline output of Module 3 divided by the total sector portfolio. Target: 15% by 2030, 30% by 2050.",
            "cat": "Green Finance",
        },
        {
            "q": "I can see some borrowers are masked with asterisks — why?",
            "a": "If you have the Data Analyst role (read-only), individual borrower names are anonymised for data privacy: the first and last character are shown, the rest is masked. ESG Officers and above see full borrower names within their assigned sectors/regions.",
            "cat": "Access Control",
        },
        {
            "q": "How do I get a Gemini API key for the AI Copilot?",
            "a": "Go to aistudio.google.com/apikey, sign in with a Google account, and click 'Create API Key'. It's free and gives 15 requests/minute and 1 million tokens/day — more than enough for daily use. Paste the key into the sidebar field in Module 5. The key is stored in your session only (not saved to the server).",
            "cat": "AI Copilot",
        },
        {
            "q": "Can I export data from the platform?",
            "a": "Yes, if your role has export permission (CSO, Climate Risk Manager, ESG Officer, Green Finance Officer, Compliance Officer). Look for the '⬇ Download' buttons at the bottom of tables. Data Analysts cannot export.",
            "cat": "Data",
        },
        {
            "q": "What is the ESMS checkbox in the lending decision form?",
            "a": "ESMS = Environmental & Social Management System. Checking this confirms that the borrower/project has been screened against IFC Performance Standards PS1–PS8. This is mandatory for all GCF-funded, DFI co-financed, or Kijani Bond-eligible loans. The ESMS clearance is recorded alongside the lending decision for audit purposes.",
            "cat": "Module 3",
        },
        {
            "q": "What is PCAF Data Quality Score 4 — and should I be worried?",
            "a": "PCAF Data Quality ranges from Score 1 (best — verified GHG data from borrower) to Score 5 (worst — regional average). Score 4 (economic-activity proxy) is the standard for emerging market banks and what CRDB uses. CRDB acknowledged this in its 2024 TCFD Report. The GreenCRDB platform provides a pathway to improve to Score 2–3 over time as more borrower data is collected.",
            "cat": "Regulatory",
        },
        {
            "q": "The ITR shows 2.73°C — is that bad?",
            "a": "It means CRDB's loan portfolio is currently aligned to a global warming trajectory of 2.73°C — above the Paris Agreement 1.5°C target and above the 2°C ceiling. The primary drivers are Agriculture (highest exposure, highest ITR delta) and Mining. To reduce ITR, CRDB needs to: (1) grow green-eligible portfolio faster (Kijani Bond, GCF), (2) apply stricter climate conditions to high-risk sectors, (3) engage borrowers on decarbonisation plans.",
            "cat": "Climate",
        },
        {
            "q": "How does the Africa Sustainability Ranking work?",
            "a": "It is a composite score based on 6 dimensions: TCFD disclosure (20%), PRB commitment (15%), green finance ratio (25%), ITR alignment (20%), DFI partnerships (10%), reporting quality (10%). CRDB ranks #8 of 20 African banks and #3 in East Africa (after KCB Group and Equity Bank Kenya). The rankings are for illustrative benchmarking — not based on proprietary bank data.",
            "cat": "Module 0",
        },
        {
            "q": "Is all the portfolio data real?",
            "a": "No — the portfolio data (borrower names, loan sizes, sector exposures, ESG scores) is simulated and illustrative. The CRDB Bank financial figures (total assets, PAT, ROE, green ratio, Kijani Bond, etc.) ARE real and sourced from the 2024 Integrated Annual Report. Real deployment would require integration with Temenos T24 core banking.",
            "cat": "Data",
        },
    ]

    cat_colours = {
        "Technical": "#9CA3AF",
        "Module 3": "#2563EB",
        "Scoring Logic": "#D97706",
        "Green Finance": "#1D9E75",
        "Access Control": "#7C3AED",
        "AI Copilot": "#7C3AED",
        "Data": "#059669",
        "Regulatory": "#D97706",
        "Climate": "#D85A30",
        "Module 0": wd.CRDB_GREEN,
    }

    for faq in faqs:
        colour = cat_colours.get(faq["cat"], "#888")
        with st.expander(f'❓ {faq["q"]}', expanded=False):
            st.markdown(
                f'<div style="display:flex;gap:8px;align-items:center;margin-bottom:8px;">'
                f'<span style="background:{colour};color:white;font-size:10px;padding:2px 8px;border-radius:8px;">{faq["cat"]}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
            st.markdown(f'<p style="font-size:14px;line-height:1.7;color:#333;">{faq["a"]}</p>', unsafe_allow_html=True)

st.markdown("---")
st.caption(
    "GreenCRDB User Guide · Platform v1.0 · "
    "For support: contact the Chief Sustainability Officer or email the Sustainable Finance Unit."
)
