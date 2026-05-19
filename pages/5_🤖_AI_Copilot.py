"""GreenCRDB AI Copilot — Sustainability Report Generator & Portfolio Q&A"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st

import web_data as wd
from auth import require_login, sidebar_user_card, require_module_access, can_access_module

st.set_page_config(page_title="AI Copilot | GreenCRDB", page_icon="🤖", layout="wide")

# ── Auth ──────────────────────────────────────────────────────────────────────
require_login()
sidebar_user_card()
require_module_access("ai_copilot")

st.markdown(
    '<div style="background:#7C3AED;padding:14px 24px;border-radius:8px;margin-bottom:12px;">'
    '<h2 style="color:white;margin:0;font-size:22px;">🤖 AI Copilot — Sustainability Intelligence Assistant</h2>'
    '<p style="color:#e9d5ff;margin:2px 0 0 0;font-size:13px;">'
    "Ask questions about your portfolio · Generate TCFD · PRB · SASB · SDG reports · "
    "Analyse climate scenarios · IFC PS guidance · BoT 2025 compliance"
    "</p></div>",
    unsafe_allow_html=True,
)

# ── Sidebar: API Key setup ─────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔑 API Key Setup")
    st.markdown(
        "**Get your FREE Gemini API key:**\n"
        "1. Go to [aistudio.google.com](https://aistudio.google.com/apikey)\n"
        "2. Sign in with your Google account\n"
        "3. Click **Get API Key** → Create API key\n"
        "4. Paste it below\n\n"
        "Free tier: 1,000,000 tokens/day — more than enough.",
    )
    api_key = st.text_input("Gemini API Key", type="password", placeholder="AIza...")
    model_choice = st.selectbox(
        "Model",
        ["gemini-1.5-flash (Fast, Free)", "gemini-1.5-pro (Best Quality, Free)"],
    )
    model_name = "gemini-1.5-flash" if "flash" in model_choice else "gemini-1.5-pro"

    st.markdown("---")
    st.markdown(
        "**Claude API (Optional — best for formal reports)**\n\n"
        "Alternatively, get $5 free credit at [console.anthropic.com](https://console.anthropic.com)\n\n"
        "Enter Claude API key:"
    )
    claude_key = st.text_input("Anthropic / Claude API Key", type="password", placeholder="sk-ant-...")

# Determine which AI to use
use_claude = bool(claude_key and claude_key.strip())
use_gemini = bool(api_key and api_key.strip()) and not use_claude

if use_claude:
    st.info("Using Claude AI (best quality for formal sustainability reports).")
elif use_gemini:
    st.info(f"Using Google Gemini ({model_name}). Free tier active.")
else:
    st.warning(
        "No API key entered. Enter your free Gemini API key in the sidebar to activate the AI Copilot. "
        "Get one free at aistudio.google.com/apikey — takes 2 minutes."
    )


# ── Build portfolio context (loaded once) ────────────────────────────────────
@st.cache_data
def get_context() -> str:
    return wd.build_portfolio_context()


SYSTEM_PROMPT = """You are TZ-CRIP Copilot, an expert AI assistant for CRDB Bank's Climate Risk and
Sustainability Unit in Tanzania. You have deep expertise in:
- TCFD (Task Force on Climate-related Financial Disclosures) framework
- IFC Performance Standards (PS1-PS7)
- GRI Sustainability Reporting Standards
- SASB (Sustainability Accounting Standards Board)
- Climate risk assessment for Sub-Saharan Africa banking
- Green finance, sustainability-linked loans (SLLs), and ESG-linked lending
- Tanzania and East Africa economic context

You have access to the complete TZ-CRIP portfolio data below. Always use specific numbers from this
data in your answers. When generating reports, follow the relevant framework structure precisely.
Write in professional, formal banking language suitable for a bank Managing Director.

{context}

Important: This is simulated/illustrative prototype data for an MSc Finance & Investment research project.
Always note this when generating official-style reports.
"""


def call_gemini(prompt: str, context: str, key: str, model: str, extra: str = "") -> str:
    try:
        import google.generativeai as genai  # type: ignore[import]
    except ImportError:
        return "google-generativeai package not installed. Run: pip install google-generativeai"

    genai.configure(api_key=key)
    system = SYSTEM_PROMPT.format(context=context) + extra
    try:
        m = genai.GenerativeModel(model_name=model, system_instruction=system)
        response = m.generate_content(prompt)
        return response.text
    except Exception as exc:
        return f"Error calling Gemini API: {exc}"


def call_claude(prompt: str, context: str, key: str) -> str:
    try:
        from anthropic import Anthropic  # type: ignore[import]
    except ImportError:
        return "anthropic package not installed. Run: pip install anthropic"

    client = Anthropic(api_key=key)
    system = SYSTEM_PROMPT.format(context=context)
    try:
        msg = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            system=system,
            messages=[{"role": "user", "content": prompt}],
        )
        return msg.content[0].text
    except Exception as exc:
        return f"Error calling Claude API: {exc}"


def ask_ai(prompt: str) -> str:
    context = get_context()
    extra = SYSTEM_CONTEXT_EXTRA
    if use_claude:
        return call_claude(prompt, context + "\n" + extra, claude_key)
    elif use_gemini:
        return call_gemini(prompt, context, api_key, model_name, extra)
    return "Please enter an API key in the sidebar to use the AI Copilot."


# ── Report prompts ────────────────────────────────────────────────────────────
SYSTEM_CONTEXT_EXTRA = """
IMPORTANT CRDB BANK REAL FACTS TO REFERENCE IN REPORTS:
- GreenCRDB is the platform name; TZ-CRIP is the internal code name
- CRDB Bank is Tanzania's largest commercial bank, listed on the Dar es Salaam Stock Exchange
- Kijani Bond: USD 68.3M raised in October 2023 (429% oversubscribed); listed on Luxembourg Stock Exchange (LuxSE)
- GCF Accreditation: CRDB is the FIRST commercial bank in East and Central Africa with GCF direct access; up to USD 100M concessional finance
- MUFG (Mitsubishi UFJ Financial Group, Japan): USD 225M green lending facility secured
- Proparco (French DFI): USD 50M + USD 75M co-finance for climate and gender lending
- Green loans disbursed 2024: TZS 86.9 billion
- Green asset ratio target: 15% of portfolio by 2030; 30% by 2050 (currently ~2.1%)
- Bank of Tanzania 2025 Guidelines: climate risk reporting is NOW MANDATORY for all licensed banks in Tanzania
- CRDB published its FIRST standalone TCFD Report in 2024
- CRDB's Sustainability Report 2024 theme: "Connect. Empower. Sustain."
- Governance: Risk and Sustainability Committee at board level; Sustainable Finance Unit (SFU) operational
- IFC investment: IFC invested in CRDB's Kijani Bond to finance climate-resilient lending
- Climate Agriculture Programme: USD 100M co-investment; climate-smart agriculture for 2 million Tanzanian farmers
- Clean energy target: transition 2 million Tanzanians from firewood/charcoal to clean energy

Always reference these real facts when generating reports to demonstrate credibility.
"""

REPORT_PROMPTS = {
    "TCFD Climate Disclosure Report": """
Generate a comprehensive TCFD Climate Disclosure Report for CRDB Bank using the portfolio data provided.
Structure the report exactly as follows:

# TCFD CLIMATE-RELATED FINANCIAL DISCLOSURE
## CRDB Bank — Tanzania Portfolio
### Reporting Period: 2024–2025

## 1. GOVERNANCE
- Board oversight of climate-related risks
- Management's role in assessing and managing climate risks

## 2. STRATEGY
- Climate risks and opportunities identified (use actual sector risk data)
- Portfolio impact under three scenarios (use the scenario data provided)
- Resilience of strategy under different climate scenarios

## 3. RISK MANAGEMENT
- Process for identifying climate risks (reference the 5 hazard dimensions)
- Integration of climate risk into overall risk management
- High-risk sectors and mitigation strategies (reference actual sectors)

## 4. METRICS AND TARGETS
- Use ALL the TCFD metrics provided in the data
- Green finance targets and current pipeline
- ESG pillar scores and targets
- Proposed targets for improvement

Write in formal banking language. Include specific numbers from the data throughout.
End with a brief Executive Summary (3 bullet points).
""",
    "ESG Portfolio Assessment Report": """
Generate a formal ESG Portfolio Assessment Report for CRDB Bank. Structure as:

# ESG PORTFOLIO ASSESSMENT REPORT
## CRDB Bank Tanzania — Borrower Portfolio Analysis

## EXECUTIVE SUMMARY
(3 bullet points highlighting key findings)

## 1. PORTFOLIO ESG OVERVIEW
- Overall ESG performance (use actual scores)
- Distribution across E, S, G pillars with commentary

## 2. ENVIRONMENTAL PILLAR (E — 40% weight)
- Portfolio average E score
- Best and worst performing sectors
- Climate adaptation performance

## 3. SOCIAL PILLAR (S — 30% weight)
- Portfolio average S score
- Labour practices, community impact, gender inclusion findings

## 4. GOVERNANCE PILLAR (G — 30% weight)
- Portfolio average G score
- Board oversight, transparency, compliance findings

## 5. BORROWER CLASSIFICATION ANALYSIS
- Green Eligible, Standard, Watch List, High Risk breakdown with numbers
- Sector concentration analysis

## 6. RECOMMENDATIONS
- 5 specific, actionable recommendations for improving ESG performance

Use all available data. Write in formal language suitable for a bank board presentation.
""",
    "Green Finance Strategy Brief": """
Generate a Green Finance Strategy Brief for CRDB Bank. Structure as:

# GREEN FINANCE STRATEGY BRIEF
## CRDB Bank Tanzania — 2025–2027 Roadmap

## EXECUTIVE SUMMARY
(2 paragraphs: current position and strategic opportunity)

## 1. CURRENT GREEN FINANCE PORTFOLIO
- Green-eligible borrowers and exposure (use actual data)
- Sectors with green potential
- Current product mix

## 2. MARKET OPPORTUNITY
- Green lending pipeline value
- Sectors with highest green potential
- Regional distribution of green opportunities

## 3. PRODUCT RECOMMENDATIONS
- Green Project Loans (target sectors, criteria)
- Sustainability-Linked Loans (SLL KPI structure, trigger events)
- Green SME Facilities (eligibility criteria)

## 4. IFC PERFORMANCE STANDARDS ALIGNMENT GAPS
- Current alignment scores by standard (use actual IFC data)
- Priority areas for improvement

## 5. 2025–2027 TARGETS AND MILESTONES
- Year 1: Foundational targets
- Year 2: Growth targets
- Year 3: Leadership targets

## 6. RISK CONSIDERATIONS
- Climate transition risks
- Greenwashing risk mitigation

Write as a strategic document for the Managing Director and Board.
""",
    "Executive Brief for Board": """
Generate a 1-page Executive Brief for the CRDB Bank Board of Directors. Structure as:

# EXECUTIVE BRIEF — CLIMATE & ESG RISK UPDATE
## CRDB Bank | Board of Directors | May 2025

## KEY FINDINGS (5 bullet points, each with a specific number from the data)

## CRITICAL RISK AREAS
(3 bullet points on highest risk areas requiring board attention)

## GREEN FINANCE OPPORTUNITY
(2 bullet points on immediate green lending opportunities — reference Kijani Bond, GCF, MUFG)

## CLIMATE SCENARIO IMPLICATIONS
(3 concise bullet points with credit loss figures for each scenario)

## RECOMMENDED BOARD ACTIONS
(3 clear action items for the board to approve)

---
*Note: Portfolio analysis figures are from the GreenCRDB prototype (illustrative). Key CRDB facts are from published 2024 reports.*

Keep this to maximum 400 words. Use bold text for key numbers. Board-level language.
""",
    "PRB Self-Assessment Report": """
Generate a formal PRB (Principles for Responsible Banking) Self-Assessment Report for CRDB Bank.
Reference the 2024 Third Biennial Progress Report structure (UNEP FI).

# PRB SELF-ASSESSMENT REPORT
## CRDB Bank Tanzania | Reporting Period: 2024–2025

## OVERVIEW OF CRDB BANK
(Brief description including Kijani Bond, GCF accreditation, BoT 2025 compliance)

## PRINCIPLE 1: ALIGNMENT
- How CRDB's strategy aligns with the Paris Agreement (1.5°C)
- How it aligns with Tanzania's NDC targets (30% emissions reduction by 2030)
- Strategic business area with greatest positive/negative climate impact

## PRINCIPLE 2: IMPACT & TARGETS
- Two SMART sustainability targets CRDB should set (based on the data: ESG improvement and green asset ratio)
- Baseline, trajectory, and 2030 targets
- KPI measurement methodology

## PRINCIPLE 3: CLIENTS & CUSTOMERS
- How CRDB engages clients on sustainability (ESMS, ESG scoring, green products)
- High-impact client segments (Agriculture, Energy, Mining)

## PRINCIPLE 4: STAKEHOLDERS
- Key stakeholders: BoT, GCF, IFC, MUFG, Proparco, smallholder farmers
- Engagement approach

## PRINCIPLE 5: GOVERNANCE & CULTURE
- Board committee structure (Risk & Sustainability Committee)
- Sustainable Finance Unit (SFU)
- Staff training programme

## PRINCIPLE 6: TRANSPARENCY & ACCOUNTABILITY
- Reporting: TCFD 2024, Sustainability Report 2024, GreenCRDB platform
- Assurance status and next steps

Write in formal UNEP FI signatory language. Include specific scores from the PRB assessment data.
""",
    "SASB FN-CB Disclosure": """
Generate a formal SASB FN-CB (Commercial Banks) Sustainability Accounting Standard disclosure
for CRDB Bank, following the IFRS Foundation SASB standard format.

# SASB COMMERCIAL BANKS SUSTAINABILITY DISCLOSURE
## CRDB Bank Tanzania | FY 2024–2025

## DISCLOSURE TOPIC 1: DATA SECURITY
- Risk management approach
- Any material data breaches
- Cybersecurity governance framework
- Metrics: [use SASB score data provided]

## DISCLOSURE TOPIC 2: FINANCIAL INCLUSION & CAPACITY BUILDING
- Rural and underserved community access programme
- Microfinance and SME lending volumes
- Financial literacy programme participants
- Metrics: [use portfolio data — TZS 420Bn microfinance; rural exposure %]

## DISCLOSURE TOPIC 3: ESG INTEGRATION IN CREDIT ANALYSIS
- ESMS integration in loan origination (GreenCRDB/TZ-CRIP scoring system)
- High-risk sector policies (Agriculture, Mining, Energy)
- Loan portfolio breakdown by climate risk tier
- Metrics: [use sector risk and borrower ESG data]

## DISCLOSURE TOPIC 4: BUSINESS ETHICS
- Anti-corruption and anti-bribery programme
- Training completion rates
- Legal proceedings (material/non-material)
- Whistleblower policy

## DISCLOSURE TOPIC 5: SYSTEMATIC RISK MANAGEMENT
- Climate stress testing programme (BoT 2025 compliance)
- Three-scenario credit loss analysis results
- Capital adequacy implications of climate risk
- Portfolio climate concentration index (use TCFD data)

## ACTIVITY METRICS
- Number and value of loans outstanding by segment
- Geographic distribution of lending (10 Tanzania regions)

Write in formal SASB disclosure language. Auditor-ready format.
""",
    "SDG Impact Report": """
Generate a formal UN SDG Impact Report for CRDB Bank Tanzania, suitable for DFI partners (GCF, AfDB, Proparco).

# SDG IMPACT REPORT
## CRDB Bank Tanzania | Financial Year 2024–2025

## EXECUTIVE SUMMARY
(CRDB's SDG commitment, headline impact figures, alignment with Tanzania's SDG priorities)

## METHODOLOGY
(How SDG alignment was measured; reference UNEP FI SDG Impact Standards for Banking)

## SDG-BY-SDG CONTRIBUTION
For each of the 9 mapped SDGs, write 2–3 sentences:
- What CRDB is doing (specific products/activities)
- Quantified impact (use numbers from portfolio data)
- Score against benchmark
Include: SDG 1, SDG 2, SDG 5, SDG 7, SDG 8, SDG 10, SDG 13, SDG 15, SDG 17

## PORTFOLIO-LEVEL IMPACT SUMMARY
- Total lending aligned to SDGs (TZS Bn and %)
- Highest-impact SDGs by portfolio weight
- Areas requiring improvement

## DFI PARTNER ALIGNMENT
- GCF: which SDGs does the climate agriculture programme address?
- Proparco: gender equality (SDG 5) progress
- MUFG green facility: SDG 7 and SDG 13 alignment

## 2025–2027 TARGETS
(3 specific SDG-linked targets CRDB should commit to)

Write in formal DFI reporting language. Suitable for submission to GCF, AfDB, and Proparco.
""",
    "BoT 2025 Compliance Report": """
Generate a formal Bank of Tanzania Climate-Related Financial Risks Compliance Report.

# CLIMATE-RELATED FINANCIAL RISKS — COMPLIANCE REPORT
## CRDB Bank Tanzania
## Bank of Tanzania Guidelines 2025

## 1. EXECUTIVE STATEMENT OF COMPLIANCE
(Senior management statement confirming compliance with BoT 2025 Guidelines)

## 2. GOVERNANCE PILLAR (BoT Requirement)
- Board-level climate oversight: Risk & Sustainability Committee
- Management-level function: Sustainable Finance Unit (SFU)
- Staff training and capacity building (36 senior managers trained 2024)
- Compliance status: [use BoT compliance tracker data]

## 3. RISK MANAGEMENT PILLAR
- Physical climate risk process: [reference Module 1 — 5 hazard dimensions, 12 sectors]
- Transition risk process: [reference sector transition risk scores]
- ESMS for financial intermediary activities: [IFC PS1–PS7 alignment]
- Compliance status: [use compliance tracker data]

## 4. SCENARIO ANALYSIS (BoT Minimum: 2 scenarios)
- Scenario 1: Base Case (2.5°C by 2100, current NDC trajectory)
- Scenario 2: Accelerated Transition (1.5°C pathway, carbon pricing)
- Scenario 3: Severe Physical Shock (1-in-20-year event)
- Credit loss range: [use actual scenario figures]
- Capital adequacy implications

## 5. DISCLOSURES PILLAR
- TCFD Report 2024: published [reference key metrics]
- Sustainability Report 2024: published
- Financed emissions: data quality Score 4 proxy; PCAF full adoption roadmap

## 6. STRATEGY PILLAR
- Green lending target: 15% green asset ratio by 2030
- GreenCRDB platform: climate risk integration in credit process
- Kijani Bond: green capital markets positioning

## 7. AREAS FOR IMPROVEMENT AND ROADMAP
(3 specific items — financed emissions, ITR measurement, TNFD readiness)

Write in formal regulatory submission language for the Bank of Tanzania.
""",
}

# ── Tab layout: Chat + Report Generator ──────────────────────────────────────
# "limited" access (ESG Officer) = chat only; "full" = all report tabs
_ai_level = can_access_module("ai_copilot")
if _ai_level == "full":
    tab_chat, tab_full, tab_reports, tab_quick = st.tabs(
        ["💬 Portfolio Chat", "📰 Full Sustainability Report", "📄 Section Reports", "⚡ Quick Insights"]
    )
else:
    # limited: chat + quick insights only; no report generation (that's CSO/Compliance function)
    _limited_tabs = st.tabs(["💬 Portfolio Chat", "⚡ Quick Insights"])
    tab_chat = _limited_tabs[0]
    tab_quick = _limited_tabs[1]
    tab_full = None
    tab_reports = None
    st.markdown(
        '<div style="background:#FFFBEB;border-left:4px solid #F59E0B;padding:10px 16px;'
        'border-radius:0 6px 6px 0;font-size:13px;margin-bottom:8px;">'
        '⚠️ <b>Limited AI access</b> — Report generation is restricted to Climate Risk Manager, '
        'Compliance Officer, Green Finance Officer, and CSO roles. '
        'You have access to Portfolio Chat and Quick Insights.'
        '</div>',
        unsafe_allow_html=True,
    )

# ── TAB 1: Chat ────────────────────────────────────────────────────────────────
with tab_chat:
    st.markdown("#### Ask anything about your portfolio")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask about portfolio risk, ESG scores, scenarios, TCFD metrics...")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Analysing portfolio data..."):
                reply = ask_ai(user_input)
            st.markdown(reply)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})

    if st.session_state.chat_history:
        if st.button("Clear chat history"):
            st.session_state.chat_history = []
            st.rerun()

    st.markdown("---")
    st.markdown("**Suggested questions:**")
    suggestions = [
        "Which sectors have the highest climate risk and what should we do?",
        "How does our Agriculture sector exposure compare to our risk appetite?",
        "What is the total green finance opportunity in our portfolio?",
        "Explain what the severe physical shock scenario means for CRDB.",
        "Which borrowers should we prioritise for sustainability-linked loans?",
        "How does our ESG score compare to best practice benchmarks?",
    ]
    cols = st.columns(2)
    for i, suggestion in enumerate(suggestions):
        with cols[i % 2]:
            if st.button(suggestion, key=f"sug_{i}", use_container_width=True):
                st.session_state.chat_history.append({"role": "user", "content": suggestion})
                with st.spinner("Analysing..."):
                    reply = ask_ai(suggestion)
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
                st.rerun()

# ── TAB 2: Full Sustainability Report ─────────────────────────────────────────
if tab_full is not None:
 with tab_full:
    st.markdown("#### Full Sustainability Report Generator")
    st.markdown(
        "Generate a **complete professional Sustainability Report** in the style of "
        "CRDB Bank's 2024 'Connect. Empower. Sustain.' report — with all chapters, "
        "using your actual portfolio data. The AI generates 6 chapters in sequence "
        "and combines them into one downloadable document."
    )

    FULL_REPORT_CHAPTERS = {
        "about_and_messages": {
            "title": "About This Report & Leadership Messages",
            "prompt": """Write the opening sections of a formal sustainability report for CRDB Bank Tanzania.
Include:

1. ABOUT THIS REPORT
- Reporting period: Financial Year 2024–2025
- Reporting frameworks: TCFD/ISSB S2, GRI Standards, PRB, SASB FN-CB, IFC Performance Standards, BoT 2025 Guidelines
- Reporting boundary: CRDB Bank consolidated (Tanzania operations)
- Assurance: Management-reviewed; external assurance planned for 2025
- Note: GreenCRDB platform data (this report) uses simulated/illustrative portfolio data for prototype demonstration

2. BOARD CHAIRPERSON'S MESSAGE (~250 words)
- Tanzania's climate challenge and CRDB's leadership role
- Kijani Bond success and GCF accreditation significance
- Commitment to Paris Agreement through lending strategy
- Board oversight of climate risk and sustainability

3. MANAGING DIRECTOR & CEO'S MESSAGE (~250 words)
- Strategic vision for green finance
- GreenCRDB platform as the bank's climate intelligence backbone
- Key 2024 achievements (Kijani Bond, GCF, MUFG, Proparco)
- 2030 green asset ratio target and pathway
- Call to action for CRDB clients and partners

Write in formal, professional banking language. Use real CRDB facts from the context provided.""",
        },
        "governance": {
            "title": "Governance & Climate Risk Management",
            "prompt": """Write the Governance chapter of CRDB Bank's Sustainability Report.

# CHAPTER 1: GOVERNANCE & CLIMATE RISK MANAGEMENT

## 1.1 Sustainability Governance Structure
- Board-level: Risk and Sustainability Committee (composition, mandate, meeting frequency)
- Management-level: Sustainable Finance Unit (SFU) — structure, reporting lines, mandate
- ESG integration across all business units

## 1.2 Climate Risk Governance (BoT 2025 Compliance)
- How the bank identifies, assesses, and manages climate-related risks
- Physical risk vs. transition risk governance process
- Integration with existing Enterprise Risk Management (ERM) framework
- Staff capacity building: 36 senior managers trained in 2024

## 1.3 ESG-Linked Executive Remuneration
- Framework for linking executive pay to sustainability KPIs
- Proposed ESG KPIs for executive incentive scheme
- Green asset ratio target as a board KPI

## 1.4 Anti-Corruption & Business Ethics
- Anti-corruption programme and training
- Whistleblower mechanism
- Regulatory compliance record

## 1.5 TCFD Governance Pillar Disclosure
(Structured TCFD Governance pillar disclosure using all relevant data from context)

Use real CRDB governance facts from context. Write in formal annual report language.""",
        },
        "environmental": {
            "title": "Environmental — Climate Risk & Green Finance",
            "prompt": """Write the Environmental chapter of CRDB Bank's Sustainability Report.

# CHAPTER 2: ENVIRONMENTAL PERFORMANCE & CLIMATE ACTION

## 2.1 Climate Risk Assessment Framework
- GreenCRDB platform description: 3-module approach
- Module 1: Sector Climate Risk Engine — 5 hazard dimensions (drought, flood, temperature, transition, water stress)
- Risk tier results: which sectors are Critical/High/Medium/Low (use actual data)
- Portfolio climate concentration index

## 2.2 Financed Emissions (PCAF Scope 3 Category 15)
- Methodology: IPCC AR6 Africa sector emission intensity proxies; PCAF data quality Score 4
- Total portfolio financed emissions: [use the 12,889 ktCO2e figure]
- Top 3 emitting sectors with specific numbers
- Roadmap to PCAF Score 1 data quality
- Portfolio Implied Temperature Rise: [use 2.73°C figure] vs. 1.5°C Paris target

## 2.3 Green Finance Portfolio
- Green loan disbursements 2024: TZS 86.9 billion
- Kijani Bond: USD 68.3M (detailed use of proceeds)
- GCF accreditation: first in East & Central Africa; USD 100M window
- MUFG green facility: USD 225M
- Green Finance Pipeline: [use Module 3 pipeline data — borrower count and exposure]
- Green Asset Ratio: current vs. 15% target by 2030

## 2.4 Climate Scenario Analysis
- Three pathways: Base Case, Accelerated Transition, Severe Physical Shock
- Credit loss estimates: [use actual scenario figures]
- Agricultural sector as key vulnerability
- Board response and mitigation strategy

## 2.5 TCFD Strategy & Metrics Disclosure
- Full TCFD Metrics table [use all 11 TCFD metrics from context]
- Forward-looking: decarbonisation pathway

## 2.6 Own Operations Environmental Footprint
- Scope 1 & 2 emissions (branch network, vehicle fleet) — note data gap; pledge to measure in 2025
- Paper, water, energy intensity initiatives

Write with specific numbers from context. Formal sustainability report language.""",
        },
        "social": {
            "title": "Social — People, Inclusion & Community",
            "prompt": """Write the Social chapter of CRDB Bank's Sustainability Report.

# CHAPTER 3: SOCIAL PERFORMANCE

## 3.1 Financial Inclusion
- Microfinance lending: TZS 420Bn; rural SACCOs supported
- Rural branch penetration: 22% of branches in underserved areas
- Women-owned MSMEs: ~34% of SME portfolio
- 10 Tanzania regions covered (list all 10 from context)
- Smallholder farmer finance under climate agriculture programme

## 3.2 Borrower ESG Assessment — Social Pillar (Module 2)
- Social pillar (S) average score across portfolio: [use actual S_score data]
- Labour practices, community impact, gender inclusion scores by sector
- Sector with highest social score; sector with lowest
- ESG classification results relevant to social performance

## 3.3 Employee Wellbeing & Development
- Training and capacity building (36 senior managers ESG-trained 2024)
- Diversity and inclusion commitment
- Health and safety practices

## 3.4 Community Investment & Development Impact
- Clean energy transition programme: target 2 million Tanzanians off firewood/charcoal
- Climate-smart agriculture programme: USD 100M; 2 million farmers
- Financial literacy initiatives

## 3.5 IFC Performance Standards — Social Compliance
- PS2 (Labour and Working Conditions): score and gaps [use actual IFC data]
- PS4 (Community Health, Safety and Security): score [use data]
- PS7 (Indigenous Peoples): assessment
- Client-level ESMS screening volumes

## 3.6 PRB Principle 3 (Clients & Customers) and Principle 4 (Stakeholders)
[Reference PRB scores and describe client engagement programme]

Write with all specific numbers from context. Formal tone.""",
        },
        "frameworks_appendix": {
            "title": "Framework Alignment & Data Appendix",
            "prompt": """Write the frameworks alignment section and data appendix of CRDB Bank's Sustainability Report.

# CHAPTER 4: FRAMEWORK ALIGNMENT & GOVERNANCE STANDARDS

## 4.1 IFC Performance Standards Alignment Summary
For each IFC PS (PS1–PS7, excluding PS5/PS8 not in data):
- Standard name
- Portfolio score [use actual scores from context]
- Alignment tier
- Key gap and sectors at risk
- Planned improvement action

## 4.2 PRB Six Principles Self-Assessment
For each of the 6 PRB principles:
- Score [use PRB scores from context]
- Key activities undertaken
- 2025 target

## 4.3 SASB FN-CB Alignment
For each of the 5 SASB FN-CB topics:
- Status (Strong/Adequate/Developing)
- Key metrics disclosed [use SASB data from context]

## 4.4 UN SDG Contribution Summary
- SDG alignment scores [use all 9 SDGs from context]
- Highest contribution SDGs
- Areas for improvement

## 4.5 GRI Content Index (Selected Disclosures)
Create a GRI-style content index table with columns: GRI Standard | Disclosure | Location | Omission
Include: GRI 2-1 (Organizational Details), GRI 2-22 (Statement on Sustainable Development Strategy),
GRI 2-23 (Policy Commitments), GRI 201-2 (Financial Implications of Climate Change),
GRI 302 (Energy), GRI 305 (Emissions), GRI 413 (Local Communities), GRI 418 (Customer Privacy)

# DATA APPENDIX
## Key Performance Indicators Table
Create a comprehensive table of all quantitative ESG metrics from the portfolio data with:
Metric | Value | Unit | Framework | Notes

Include ALL metrics: climate risk scores, ESG scores, financed emissions, scenario figures,
green asset ratio, IFC PS scores, PRB scores, SASB scores, SDG scores, scenario impacts.

Write in formal report language. Tables should be in Markdown table format.""",
        },
        "executive_summary": {
            "title": "Executive Summary & Recommendations",
            "prompt": """Write the Executive Summary for CRDB Bank's Sustainability Report.
This should be the FIRST thing readers see — written LAST so it captures all chapter highlights.

# EXECUTIVE SUMMARY

## About CRDB Bank (2–3 sentences on who CRDB is)

## 2024 Headline Achievements (5 bullet points, each with a specific number)

## Our Sustainability Commitments
A table with three columns:
| Commitment | 2024 Status | 2030 Target |
(Cover: green asset ratio, green loans, GCF facility, financed emissions, climate training, ESMS screening)

## Key Risks Identified (3 priority risks from the portfolio data)

## Material Opportunities (3 green finance opportunities from the pipeline)

## 2025–2027 Strategic Priorities (5 numbered priorities)

## How to Read This Report
(Brief guide to the 4 chapters and GreenCRDB platform)

Keep this under 600 words. Executive-level language. The MD should be able to read this in 3 minutes and understand everything.""",
        },
    }

    if not (use_claude or use_gemini):
        st.warning("Enter your Gemini API key in the sidebar to generate the full report.")
    else:
        col_info, col_btn = st.columns([2, 1])
        with col_info:
            st.markdown("""
**Report structure (6 chapters, generated in sequence):**

| # | Chapter | Content |
|---|---|---|
| 0 | Executive Summary | Headline achievements, commitments table, strategic priorities |
| 1 | Leadership Messages | Chairperson + MD/CEO statements |
| 2 | Governance | Board structure, BoT 2025 compliance, TCFD Governance pillar |
| 3 | Environmental | Climate risk scores, financed emissions, green finance, scenarios |
| 4 | Social | Financial inclusion, ESG social pillar, IFC PS, community |
| 5 | Frameworks & Appendix | IFC PS, PRB, SASB, GRI Content Index, KPI data table |

**Estimated time:** 3–6 minutes · **Output:** ~8,000–12,000 words · **Download:** .txt file
            """)
        with col_btn:
            st.markdown("<br>", unsafe_allow_html=True)
            generate_full = st.button(
                "📰 Generate Full Report",
                type="primary",
                use_container_width=True,
                help="Generates all 6 chapters using your portfolio data",
            )

        if generate_full or "full_report_sections" in st.session_state:
            if generate_full:
                st.session_state.full_report_sections = {}
                context = get_context()
                extra = SYSTEM_CONTEXT_EXTRA
                progress = st.progress(0, text="Starting report generation...")
                status = st.empty()

                chapters = list(FULL_REPORT_CHAPTERS.items())
                for i, (key, chapter) in enumerate(chapters):
                    status.markdown(
                        f'<div style="background:#f0f4f0;padding:10px;border-radius:6px;">'
                        f'Generating chapter {i+1}/{len(chapters)}: <b>{chapter["title"]}</b>...'
                        f'</div>',
                        unsafe_allow_html=True,
                    )
                    progress.progress((i) / len(chapters), text=f"Chapter {i+1} of {len(chapters)}")
                    text = ask_ai(chapter["prompt"])
                    st.session_state.full_report_sections[key] = {
                        "title": chapter["title"],
                        "text": text,
                    }
                progress.progress(1.0, text="Report complete!")
                status.success(f"All {len(chapters)} chapters generated successfully!")

            # Display the full report
            sections = st.session_state.get("full_report_sections", {})
            if sections:
                full_text_parts = [
                    "=" * 70,
                    "CRDB BANK TANZANIA — SUSTAINABILITY REPORT 2024–2025",
                    "GreenCRDB Platform | Climate-Finance Risk Intelligence",
                    "Frameworks: TCFD · ISSB S1/S2 · PRB · SASB FN-CB · IFC PS · BoT 2025",
                    "=" * 70,
                    "",
                    "IMPORTANT: This report is generated by the GreenCRDB prototype platform.",
                    "Portfolio figures are simulated/illustrative. Real CRDB facts are sourced",
                    "from published 2024 Annual Report and Sustainability Report.",
                    "",
                    "=" * 70,
                    "",
                ]

                # Correct display order: exec summary first, then messages, then chapters
                display_order = ["executive_summary", "about_and_messages", "governance",
                                  "environmental", "social", "frameworks_appendix"]

                for key in display_order:
                    if key in sections:
                        sec = sections[key]
                        full_text_parts.append(f"\n{'=' * 70}")
                        full_text_parts.append(sec["text"])

                full_text = "\n".join(full_text_parts)

                st.markdown("---")
                st.markdown("### Generated Report")
                st.download_button(
                    "⬇ Download Full Sustainability Report (.txt)",
                    full_text,
                    file_name="GreenCRDB_CRDB_Sustainability_Report_2024_25.txt",
                    mime="text/plain",
                    type="primary",
                )
                st.caption(f"Report size: {len(full_text):,} characters · {len(full_text.split()):,} words")

                for key in display_order:
                    if key in sections:
                        sec = sections[key]
                        with st.expander(f"📄 {sec['title']}", expanded=False):
                            st.markdown(sec["text"])
                            st.download_button(
                                f"⬇ Download this chapter",
                                sec["text"],
                                file_name=f"GreenCRDB_{key}.txt",
                                mime="text/plain",
                                key=f"dl_chapter_{key}",
                            )

# ── TAB 3: Report Generator ────────────────────────────────────────────────────
if tab_reports is not None:
 with tab_reports:
    st.markdown("#### Generate Formal Sustainability Reports")
    st.markdown(
        "Select a report type below. The AI will use your actual portfolio data to generate "
        "a structured, framework-aligned report you can download."
    )

    report_col1, report_col2 = st.columns(2)

    report_items = list(REPORT_PROMPTS.items())

    for idx, (report_name, report_prompt) in enumerate(report_items):
        col = report_col1 if idx % 2 == 0 else report_col2
        icons = ["📋", "🌍", "💚", "📊", "🤝", "📈", "🌐", "🏛️"]
        with col:
            st.markdown(
                f'<div style="background:#f9fafb;border:1px solid #e5e7eb;padding:14px;'
                f'border-radius:8px;margin-bottom:12px;">'
                f'<h4 style="margin:0 0 6px 0;color:#1a1a1a;">{icons[idx]} {report_name}</h4>'
                f"</div>",
                unsafe_allow_html=True,
            )
            if st.button(f"Generate {report_name}", key=f"report_{idx}", use_container_width=True):
                if not (use_claude or use_gemini):
                    st.error("Please enter an API key in the sidebar first.")
                else:
                    with st.spinner(f"Generating {report_name}... (this may take 30–60 seconds)"):
                        report_text = ask_ai(report_prompt)
                    st.session_state[f"report_result_{idx}"] = report_text
                    st.success("Report generated!")

            if f"report_result_{idx}" in st.session_state:
                with st.expander("View Report", expanded=True):
                    st.markdown(st.session_state[f"report_result_{idx}"])
                st.download_button(
                    f"⬇ Download {report_name} (.txt)",
                    st.session_state[f"report_result_{idx}"],
                    file_name=f"TZCRIP_{report_name.replace(' ', '_')}.txt",
                    mime="text/plain",
                    key=f"dl_{idx}",
                )

# ── TAB 3: Quick Insights ──────────────────────────────────────────────────────
with tab_quick:
    st.markdown("#### Pre-built Portfolio Insights")
    st.markdown("Click any insight to generate it instantly using your portfolio data.")

    quick_prompts = {
        "🔴 Critical Risk Summary": (
            "In 3 concise bullet points, summarise the critical climate risks in the CRDB portfolio. "
            "Include specific sector names, risk scores, and exposure amounts."
        ),
        "🟢 Green Finance Opportunity": (
            "In 3 bullet points, summarise the immediate green finance lending opportunity. "
            "Include specific borrower counts, exposure amounts, and top sectors."
        ),
        "📊 TCFD Snapshot": (
            "Provide a brief TCFD snapshot: one sentence each for Governance, Strategy, "
            "Risk Management, and Metrics & Targets, using the actual portfolio data."
        ),
        "⚠️ IFC Gaps Analysis": (
            "Which IFC Performance Standards does CRDB most urgently need to address? "
            "List the top 3 gaps with specific scores and affected sectors."
        ),
        "🌡️ Scenario Comparison": (
            "Compare the three climate scenarios in a clear table format showing: "
            "scenario name, portfolio impact %, and credit loss in TZS Bn. "
            "Then give one sentence of strategic implication for each."
        ),
        "📈 ESG Improvement Plan": (
            "What are the top 3 ESG improvement actions CRDB should take this year? "
            "Base your answer on the lowest-scoring pillars and sectors in the portfolio data."
        ),
    }

    q_cols = st.columns(2)
    for i, (q_name, q_prompt) in enumerate(quick_prompts.items()):
        with q_cols[i % 2]:
            if st.button(q_name, key=f"quick_{i}", use_container_width=True):
                if not (use_claude or use_gemini):
                    st.error("Please enter an API key in the sidebar first.")
                else:
                    with st.spinner("Generating insight..."):
                        result = ask_ai(q_prompt)
                    st.session_state[f"quick_result_{i}"] = result

            if f"quick_result_{i}" in st.session_state:
                st.markdown(st.session_state[f"quick_result_{i}"])
                st.markdown("---")
