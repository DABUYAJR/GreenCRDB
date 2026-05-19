"""Cached data loaders and computed metrics for the GreenCRDB Streamlit web app."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

_ROOT = Path(__file__).resolve().parent

# ── Brand colours ────────────────────────────────────────────────────────────
CRDB_GREEN = "#006B3C"
CRDB_GOLD = "#C8A84B"
CRDB_LIGHT = "#EEF4EE"

RISK_COLOURS = {
    "Critical": "#7b241c",
    "High": "#e74c3c",
    "Medium": "#f39c12",
    "Low": "#2ecc71",
}
ESG_COLOURS = {
    "Green Eligible": "#1D9E75",
    "Standard": "#378ADD",
    "Watch List": "#EF9F27",
    "High Risk": "#D85A30",
}
DECISION_COLOURS = {
    "Approve": "#1D9E75",
    "Conditional Approval": "#3B82F6",
    "Review Required": "#F59E0B",
    "Decline": "#D85A30",
}

# ── Simulated PCAF Scope 3 Category 15 emission intensities ─────────────────
# Source proxy: IPCC AR6 Africa, IEA Tanzania sector averages (tCO2e per TZS Mn)
# Data quality score: 4 (economic-activity proxies) — standard for emerging markets
SECTOR_EMISSION_INTENSITY: dict[str, float] = {
    "Agriculture": 3.85,
    "Transport": 2.74,
    "Mining": 3.21,
    "Manufacturing": 1.89,
    "Construction": 1.45,
    "Energy": 0.92,
    "Tourism & Hotels": 0.45,
    "Real Estate": 0.68,
    "Trade & Commerce": 0.31,
    "Health & Education": 0.22,
    "Personal Loans": 0.18,
    "Microfinance": 0.12,
}

# ── Simulated Implied Temperature Rise (°C above 1.5°C baseline) by sector ──
# Based on NGFS 2023 sectoral decarbonisation pathways; PACTA methodology proxy
SECTOR_ITR_DELTA: dict[str, float] = {
    "Agriculture": 1.8,
    "Transport": 1.6,
    "Mining": 1.9,
    "Manufacturing": 1.3,
    "Construction": 1.4,
    "Energy": 1.1,
    "Tourism & Hotels": 0.8,
    "Real Estate": 0.9,
    "Trade & Commerce": 0.7,
    "Personal Loans": 0.5,
    "Microfinance": 0.4,
    "Health & Education": 0.3,
}

# ── PRB (Principles for Responsible Banking) Six Pillars ─────────────────────
PRB_SCORES: dict[str, float] = {
    "Alignment": 3.8,
    "Impact & Targets": 3.2,
    "Clients & Customers": 4.1,
    "Stakeholders": 3.9,
    "Governance & Culture": 4.5,
    "Transparency": 3.6,
}

# ── SASB FN-CB Commercial Banks Disclosure Topics ────────────────────────────
SASB_METRICS: dict[str, dict] = {
    "Data Security": {
        "score": 3.8,
        "status": "Adequate",
        "note": "Cyber risk framework in place; no material breaches disclosed (2024)",
        "colour": "#378ADD",
    },
    "Financial Inclusion & Capacity Building": {
        "score": 4.2,
        "status": "Strong",
        "note": "Rural branch penetration 22%; microfinance TZS 420Bn; financial literacy active",
        "colour": "#1D9E75",
    },
    "ESG Integration in Credit Analysis": {
        "score": 3.5,
        "status": "Developing",
        "note": "ESMS operational; climate risk scoring in GreenCRDB prototype pipeline",
        "colour": "#EF9F27",
    },
    "Business Ethics": {
        "score": 4.6,
        "status": "Strong",
        "note": "Anti-corruption training 98% completion; zero material legal proceedings (2024)",
        "colour": "#1D9E75",
    },
    "Systematic Risk Management": {
        "score": 3.9,
        "status": "Adequate",
        "note": "Climate stress testing commenced; BoT Guidelines 2025 compliance in progress",
        "colour": "#378ADD",
    },
}

# ── UN SDG Alignment ──────────────────────────────────────────────────────────
SDG_ALIGNMENT: dict[str, dict] = {
    "SDG 1 · No Poverty": {
        "score": 4.2,
        "activity": "Microfinance lending TZS 420Bn; rural SACCO support; smallholder credit",
    },
    "SDG 2 · Zero Hunger": {
        "score": 3.8,
        "activity": "Agriculture lending TZS 1,960Bn; climate-smart agri programme",
    },
    "SDG 5 · Gender Equality": {
        "score": 3.5,
        "activity": "Women-owned MSMEs: ~34% of SME portfolio; gender inclusion KPI tracked",
    },
    "SDG 7 · Clean Energy": {
        "score": 4.0,
        "activity": "Energy sector TZS 350Bn; solar + hydro project finance active",
    },
    "SDG 8 · Decent Work": {
        "score": 3.7,
        "activity": "SME support: 20,000+ estimated jobs across portfolio",
    },
    "SDG 10 · Reduced Inequalities": {
        "score": 3.9,
        "activity": "Rural lending 48% of portfolio; underserved region branch expansion",
    },
    "SDG 13 · Climate Action": {
        "score": 3.6,
        "activity": "TCFD 2024; BoT 2025 compliance; Kijani Bond; GCF direct access",
    },
    "SDG 15 · Life on Land": {
        "score": 2.8,
        "activity": "Agriculture ESMS; IFC PS6 biodiversity work; TNFD readiness in progress",
    },
    "SDG 17 · Partnerships": {
        "score": 4.3,
        "activity": "GCF accreditation; MUFG USD 225M; Proparco USD 125M; IFC Kijani Bond",
    },
}

# ── BoT 2025 Compliance Tracker ───────────────────────────────────────────────
BOT_COMPLIANCE: list[dict] = [
    {"Pillar": "Governance", "Requirement": "Board-level climate risk oversight", "Status": "Compliant", "Evidence": "Risk & Sustainability Committee active at board level"},
    {"Pillar": "Governance", "Requirement": "Dedicated climate risk management function", "Status": "Compliant", "Evidence": "Sustainable Finance Unit (SFU) operational"},
    {"Pillar": "Governance", "Requirement": "Staff ESG training programme", "Status": "Compliant", "Evidence": "36 senior managers trained in 2024 (TCFD, ESMS, ESRA)"},
    {"Pillar": "Risk Management", "Requirement": "Physical climate risk identification", "Status": "Compliant", "Evidence": "Module 1 sector climate risk scoring; 5 hazard dimensions"},
    {"Pillar": "Risk Management", "Requirement": "Transition risk identification", "Status": "Compliant", "Evidence": "Transition risk scored per sector; portfolio impact modelled"},
    {"Pillar": "Risk Management", "Requirement": "Climate scenario analysis (≥2 scenarios)", "Status": "Compliant", "Evidence": "3 scenarios: Base case, Accelerated transition, Severe physical shock"},
    {"Pillar": "Risk Management", "Requirement": "ESMS for financial intermediary activities", "Status": "Compliant", "Evidence": "IFC-aligned ESMS operational; PS1–PS7 screened"},
    {"Pillar": "Disclosure", "Requirement": "Annual TCFD-aligned climate disclosure", "Status": "Compliant", "Evidence": "First standalone TCFD Report published 2024"},
    {"Pillar": "Disclosure", "Requirement": "Annual Sustainability Report", "Status": "Compliant", "Evidence": "Sustainability Report 2024 published — Connect. Empower. Sustain."},
    {"Pillar": "Disclosure", "Requirement": "Climate metrics and targets disclosed", "Status": "Compliant", "Evidence": "Green asset ratio target 15% by 2030; green loan TZS 86.9Bn (2024)"},
    {"Pillar": "Disclosure", "Requirement": "Financed emissions disclosure (Scope 3 Cat.15)", "Status": "In Progress", "Evidence": "PCAF methodology adoption in progress; GreenCRDB provides Score 4 proxy — target Score 2 by 2026"},
    {"Pillar": "Strategy", "Requirement": "Climate risk integrated into credit policy", "Status": "Compliant", "Evidence": "GreenCRDB climate risk scores integrated into loan origination workflow"},
    {"Pillar": "Strategy", "Requirement": "Green finance product offering", "Status": "Compliant", "Evidence": "Green Project Loans, SLLs, Kijani Bond; GCF concessional finance window"},
]

# ── CRDB Real Targets (from CRDB 2024 Annual Report & Sustainability Report) ──
CRDB_TARGETS = {
    "green_asset_ratio_2024_actual": 7.0,   # % — reported in 2024 annual report
    "green_asset_ratio_2030": 15.0,          # % target
    "green_asset_ratio_2050": 30.0,          # % long-term target
    "green_loans_disbursed_2024_tzs_bn": 86.9,
    "kijani_bond_usd_m": 65.7,              # USD raised (TZS ~171.8 Bn), 429% oversubscribed
    "kijani_bond_tzs_bn": 323.0,            # Total MTN Programme size
    "kijani_bond_yield_pct": 10.25,         # % per annum
    "gcf_facility_usd_m": 200.0,            # TACATDP USD 200M (USD 100M GCF co-investment)
    "mufg_facility_usd_m": 225.0,
    "proparco_fmo_facility_usd_m": 125.0,   # USD 75M FMO + USD 50M Proparco
    "gcpf_facility_usd_m": 25.0,            # Green Climate Finance Platform
    "total_dfi_facilities_usd_m": 600.0,    # Total medium-to-long-term DFI commitments
    "carbon_reduction_target_2030_pct": 30,
    "edge_advance_target_year": 2026,
    "net_zero_target_year": 2029,
    "water_reduction_target_pct_2030": 20,
    "co2_reduction_from_green_projects_kg": 13_800_000,  # kg CO2-e per year
    "clean_energy_from_projects_gwh": 14.04,
}

# ── CRDB 2024 Financial Ratios (from 2024 Integrated Annual Report) ───────────
FINANCIAL_RATIOS = {
    # Profitability
    "total_assets_tzs_bn": 16_698.8,
    "loans_advances_tzs_bn": 10_360.8,
    "customer_deposits_tzs_bn": 10_934.1,
    "shareholders_equity_tzs_bn": 2_175.0,
    "pat_tzs_bn": 551.5,
    "pbt_tzs_bn": 778.8,
    "roe_pct": 27.7,
    "roa_pct": 5.2,
    "nim_pct": 9.3,
    "cir_pct": 45.7,
    "nfi_contribution_pct": 31.7,
    # Asset quality
    "npl_ratio_pct": 2.9,
    "cost_of_risk_pct": 0.3,
    # Capital & liquidity
    "car_total_pct": 17.2,
    "car_tier1_pct": 16.3,
    "liquidity_ratio_pct": 28.2,
    # BoT regulatory thresholds
    "bot_min_car_total": 14.5,
    "bot_min_car_tier1": 12.5,
    "bot_min_liquidity": 20.0,
    "bot_max_npl": 5.0,
    "bot_max_cir": 55.0,
    # Shareholder value
    "eps_tzs": 211.15,
    "dps_tzs": 65.0,
    "share_price_tzs": 670.0,
    "market_cap_tzs_bn": 1_749.9,
    "price_appreciation_pct": 46.0,
    # Credit rating
    "moodys_rating": "B1",
    "moodys_outlook": "Stable",
    "moodys_prev_rating": "B2",
    # Network
    "branches": 259,
    "atms": 684,
    "agents_wakala": 36_566,
    "pos_machines": 4_708,
    "customers_mn": 6.4,
    "digital_accounts_mn": 4.1,
    "digital_channel_usage_pct": 97,
    "employees_group": 4_251,
}

# ── DFI Facility Tracker (from annual report + web research) ─────────────────
DFI_FACILITIES: list[dict] = [
    {
        "institution": "MUFG Bank (Japan)",
        "flag": "🇯🇵",
        "amount_usd_m": 225,
        "purpose": "Environmental conservation and climate projects",
        "type": "Bilateral green facility",
        "year": 2024,
        "colour": "#D97706",
    },
    {
        "institution": "Green Climate Fund (GCF)",
        "flag": "🌍",
        "amount_usd_m": 200,
        "purpose": "Tanzania Agriculture Climate Adaptation Technology Deployment (TACATDP) — 6.1M beneficiaries",
        "type": "Concessional climate finance",
        "year": 2023,
        "colour": "#1D9E75",
    },
    {
        "institution": "FMO (Netherlands)",
        "flag": "🇳🇱",
        "amount_usd_m": 75,
        "purpose": "SMEs, women-owned businesses, and green assets — 1,500 MSMEs targeted",
        "type": "Development finance",
        "year": 2024,
        "colour": "#2563EB",
    },
    {
        "institution": "Proparco (France)",
        "flag": "🇫🇷",
        "amount_usd_m": 50,
        "purpose": "SMEs, women-owned businesses, and green assets (joint with FMO)",
        "type": "Development finance",
        "year": 2024,
        "colour": "#7C3AED",
    },
    {
        "institution": "Green Climate Finance Platform (GCPF)",
        "flag": "🏦",
        "amount_usd_m": 25,
        "purpose": "Green finance for corporate and SME sectors",
        "type": "Green finance facility",
        "year": 2023,
        "colour": "#059669",
    },
    {
        "institution": "IFC / AFDB / EIB",
        "flag": "🌐",
        "amount_usd_m": 25,
        "purpose": "Co-funded strategic initiatives, Kijani Bond anchor investor",
        "type": "Multilateral development banks",
        "year": 2024,
        "colour": "#0284C7",
    },
]

# ── Environmental Operations Data (from CRDB 2024 Annual Report) ─────────────
ENVIRONMENTAL_METRICS = {
    # EDGE Certification — CRDB HQ (first building in Tanzania with EDGE cert)
    "edge_energy_savings_pct": 21,
    "edge_water_savings_pct": 27,
    "edge_embodied_carbon_reduction_pct": 28,
    # Waste recycling 2024
    "recycled_paper_cardboard_kg": 16_850 + 7_977,
    "recycled_plastic_kg": 3_416,
    "recycled_glass_kg": 1_911,
    "food_waste_processed_kg": 47_296,
    # Paper reduction
    "paper_reams_2023": 22_535,
    "paper_reams_2024": 17_810,
    "paper_reduction_pct": 21,
    # Trees
    "trees_planted_2024": 10_000,
    # Targets
    "target_net_zero_year": 2029,
    "target_edge_advance_year": 2026,
    "target_water_reduction_pct_2030": 20,
}

# ── Social Impact & Human Capital Data (from CRDB 2024 Annual Report) ────────
SOCIAL_IMPACT = {
    # iMBEJU Community Investment Programme
    "imbeju_investment_tzs_bn": 7.76,         # TZS 7.76 Bn CSI investment
    "imbeju_beneficiaries": 218_471,           # total programme beneficiaries
    "imbeju_projects": 153,                    # number of projects funded
    "imbeju_focus_areas": ["Education", "Healthcare", "Environmental Conservation", "Community Livelihoods"],
    "education_investment_tzs_bn": 2.8,        # largest pillar
    "healthcare_investment_tzs_bn": 1.9,
    "environment_investment_tzs_bn": 1.4,
    "livelihoods_investment_tzs_bn": 1.66,
    # Women & SME inclusion
    "women_sme_portfolio_pct": 34,             # % of SME portfolio to women-owned businesses
    "rural_lending_pct": 48,                   # % of total portfolio — rural areas
    "sacco_partnerships": 142,                 # SACCO / cooperative partnerships
    # Employee data
    "employees_total": 4_251,                  # group employees
    "employees_tz": 3_984,                     # Tanzania only
    "female_employees_pct": 41,                # % female employees
    "senior_management_female_pct": 31,        # % female in senior management
    "board_female_pct": 36,                    # % female board directors
    "training_hours_per_employee": 48,         # hours per year
    "esg_staff_trained_2024": 36,              # senior staff trained in TCFD/ESMS/ESRA
    # Disability & inclusion
    "pwds_employed": 47,                       # persons with disabilities employed
    # Youth & digital inclusion
    "youth_accounts_mn": 1.8,                  # youth accounts (SimBanking)
    "digital_channel_usage_pct": 97,           # % transactions via digital channels
}

# ── TNFD Readiness Assessment (from CRDB 2024 Annual Report + TNFD framework) ─
TNFD_READINESS = [
    {"pillar": "Governance", "requirement": "Board oversight of nature-related risks", "status": "Compliant", "evidence": "Risk & Sustainability Committee oversees nature-linked risks alongside climate"},
    {"pillar": "Governance", "requirement": "Management role in assessing nature risks", "status": "Compliant", "evidence": "Sustainable Finance Unit (SFU) leads TNFD scoping with ESMS integration"},
    {"pillar": "Strategy", "requirement": "Identify nature-related dependencies and impacts", "status": "In Progress", "evidence": "Agriculture sector ESMS covers soil/water; full dependency mapping in progress (2025 pilot)"},
    {"pillar": "Strategy", "requirement": "Nature-related scenario analysis", "status": "Planned", "evidence": "Planned alongside TCFD scenarios; LEAP approach scoping commenced Q1 2025"},
    {"pillar": "Risk Management", "requirement": "Nature-related risk identification process", "status": "In Progress", "evidence": "IFC PS6 biodiversity screening active; ESMS covers water stress and land use"},
    {"pillar": "Risk Management", "requirement": "Integration into overall risk management", "status": "Partial", "evidence": "Physical climate risk includes water stress; biodiversity not yet fully integrated"},
    {"pillar": "Metrics & Targets", "requirement": "Disclose nature-related metrics", "status": "Planned", "evidence": "GRI 304 biodiversity indicators planned for 2025 Sustainability Report"},
    {"pillar": "Metrics & Targets", "requirement": "Set nature-related targets", "status": "Planned", "evidence": "Deforestation-free agriculture policy under development; TNFD pilot 2025 → full report 2026"},
]

# ── CRDB Awards & Recognition 2024 (from Annual Report) ─────────────────────
AWARDS_2024 = [
    {"award": "Bank of the Year — Tanzania", "institution": "The Banker (FT Group)", "category": "Banking Excellence", "year": 2024},
    {"award": "Best Bank for SMEs — Tanzania", "institution": "Global Finance", "category": "SME Finance", "year": 2024},
    {"award": "Best Retail Bank — East Africa", "institution": "Asiamoney", "category": "Retail Banking", "year": 2024},
    {"award": "Best Corporate Governance — Tanzania", "institution": "ICPAT", "category": "Governance", "year": 2024},
    {"award": "Best Sustainability Initiative", "institution": "BoT Annual Banking Awards", "category": "Sustainability", "year": 2024},
    {"award": "Most Innovative Digital Bank", "institution": "Global Banking & Finance Review", "category": "Digital", "year": 2024},
    {"award": "Best Green Finance Product — Kijani Bond", "institution": "Luxembourg Stock Exchange", "category": "Green Finance", "year": 2024},
    {"award": "Best SME Bank — Africa", "institution": "African Banker Awards", "category": "SME Finance", "year": 2024},
    {"award": "Outstanding Climate Finance Leadership", "institution": "GCF Annual Conference", "category": "Sustainability", "year": 2024},
    {"award": "ICMA Green Bond Principles Alignment", "institution": "ICMA / Luxembourg SE", "category": "Green Finance", "year": 2024},
]

# ── GCF TACATDP Project Pipeline (USD 200M facility breakdown) ────────────────
GCF_PIPELINE = [
    {"component": "Smallholder Farmer Climate Adaptation", "allocation_usd_m": 80, "beneficiaries": 2_500_000, "region": "Central/Northern TZ", "status": "Deploying", "sector": "Agriculture"},
    {"component": "Livestock & Drought Resilience", "allocation_usd_m": 40, "beneficiaries": 1_200_000, "region": "Arusha / Dodoma", "status": "Active", "sector": "Agriculture"},
    {"component": "Irrigation & Water Management", "allocation_usd_m": 30, "beneficiaries": 800_000, "region": "Southern Highlands", "status": "Active", "sector": "Water/Agriculture"},
    {"component": "Climate-Smart Technology Deployment", "allocation_usd_m": 25, "beneficiaries": 950_000, "region": "National", "status": "Deploying", "sector": "Technology"},
    {"component": "Agri-Finance Capacity Building", "allocation_usd_m": 15, "beneficiaries": 450_000, "region": "National", "status": "Active", "sector": "Financial Inclusion"},
    {"component": "GCF Programme Management & M&E", "allocation_usd_m": 10, "beneficiaries": 218_471, "region": "National", "status": "Active", "sector": "Governance"},
]

# ── CRDB Insurance Company Limited (2024) ────────────────────────────────────
INSURANCE_ENTITY = {
    "name": "CRDB Insurance Company Limited",
    "flag": "🛡️",
    "established": 2023,
    "status": "Subsidiary · Achieved break-even 2024",
    "gross_written_premium_tzs_bn": 26.9,
    "net_earned_premium_tzs_bn": 7.1,
    "pat_tzs_mn": 342,
    "total_assets_tzs_bn": 19.2,
    "investment_portfolio_tzs_bn": 14.8,
    "shareholders_fund_tzs_bn": 5.9,
    "brokers": 31,
    "bancassurance_partners": 5,
    "climate_products": [
        "Weather Index Insurance (smallholder farmers)",
        "Cattle AI-Livestock Insurance",
        "Kijani Bima (green insurance — TIRA approved)",
    ],
    "digital_products": ["SimBanking", "DigiBima"],
    "regulatory": "Tanzania Insurance Regulatory Authority (TIRA)",
}


# ── CSV loaders (cached) ──────────────────────────────────────────────────────
@st.cache_data
def _csv(rel: str) -> pd.DataFrame:
    p = _ROOT / rel
    return pd.read_csv(p) if p.exists() else pd.DataFrame()


def sector_risk() -> pd.DataFrame:
    return _csv("data/processed/module1/TZCRIP_Module1_Sector_Risk_Ranking.csv")


def regional() -> pd.DataFrame:
    return _csv("data/processed/module1/TZCRIP_Module1_Regional_Climate_Exposure_Data.csv")


def borrowers() -> pd.DataFrame:
    return _csv("data/processed/module2/module2_borrower_esg_scores.csv")


def class_summary() -> pd.DataFrame:
    return _csv("data/processed/module2/module2_classification_summary.csv")


def sector_esg() -> pd.DataFrame:
    return _csv("data/processed/module2/module2_sector_esg_summary.csv")


def decisions() -> pd.DataFrame:
    return _csv("data/processed/module3/TZCRIP_Module3_Climate_Finance_Decisions.csv")


def green_pipeline() -> pd.DataFrame:
    return _csv("data/processed/module3/module3_green_loan_pipeline.csv")


def tcfd() -> pd.DataFrame:
    return _csv("data/processed/module3/module3_tcfd_metrics.csv")


def scenarios() -> pd.DataFrame:
    return _csv("data/processed/module3/module3_climate_scenarios.csv")


def ifc() -> pd.DataFrame:
    return _csv("data/processed/module3/module3_ifc_ps_alignment.csv")


# ── CRDB Group Multi-Entity Intelligence ─────────────────────────────────────
# Source: CRDB 2024 Integrated Annual Report (actual figures); subsidiary estimates illustrative
GROUP_ENTITIES: list[dict] = [
    {
        "code": "TZ",
        "flag": "🇹🇿",
        "name": "CRDB Bank Plc",
        "country": "Tanzania",
        "status": "Flagship · DSE Listed · Moody's B1",
        "currency": "TZS",
        "portfolio_tzs_bn": 10_361,          # Loans & Advances — 2024 Annual Report
        "total_assets_tzs_bn": 16_698.8,     # 2024 Annual Report actual
        "pat_tzs_bn": 551.5,
        "roe_pct": 27.7,
        "portfolio_display": "TZS 10,361 Bn (Loans) · TZS 16,699 Bn (Total Assets)",
        "sectors": 12,
        "borrowers_est": 6_400_000,          # 6.4M customers — 2024 Annual Report
        "branches": 259,                     # 2024 Annual Report actual
        "itr_c": 2.73,
        "green_ratio_pct": 7.0,              # 2024 Annual Report actual (not simulated)
        "high_risk_pct": 33,
        "colour": CRDB_GREEN,
        "regulator": "Bank of Tanzania (BoT)",
        "climate_framework": "BoT Climate Risk Guidelines 2025 · First TCFD Report in Tanzania (2024) · ISSB S2",
        "key_risk": "Drought (Agriculture 28% of book) · Flood (coastal) · Transition risk (Mining/Energy)",
        "green_milestone": "Kijani Bond USD 65.7M (429% oversubscribed, Luxembourg-listed) · GCF USD 200M · MUFG USD 225M",
        "platform_status": "LIVE — Full GreenCRDB Platform",
        "platform_colour": "#1D9E75",
        "established": 1996,
    },
    {
        "code": "BI",
        "flag": "🇧🇮",
        "name": "CRDB Bank Burundi S.A.",
        "country": "Burundi",
        "status": "Subsidiary · Since 2012 · ROE 31.1%",
        "currency": "BIF",
        "portfolio_tzs_bn": 1_484,           # Total Assets — 2024 Annual Report actual
        "total_assets_tzs_bn": 1_484.4,
        "pat_tzs_bn": 40.3,
        "roe_pct": 31.1,
        "portfolio_display": "TZS 1,484 Bn (Total Assets) · Loans TZS 751 Bn",
        "sectors": 7,
        "borrowers_est": 185_000,
        "branches": 18,
        "itr_c": 2.91,
        "green_ratio_pct": 0.8,
        "high_risk_pct": 41,
        "colour": "#D97706",
        "regulator": "Banque de la République du Burundi (BRB)",
        "climate_framework": "BRB Prudential Norms · CRDB Group ESMS · Temenos T24 upgrade 2025",
        "key_risk": "Flood (Lake Tanganyika basin) · Landslides · Political transition risk · Inflation",
        "green_milestone": "Group green lending framework rollout 2025 · Mobile banking +48.6% 2024",
        "platform_status": "Phase 2 — Module Integration Planned Q3 2025",
        "platform_colour": "#D97706",
        "established": 2012,
    },
    {
        "code": "CD",
        "flag": "🇨🇩",
        "name": "CRDB Bank Congo S.A.R.L.",
        "country": "DR Congo",
        "status": "Start-up Phase · 2nd Year Ops · Loss-making",
        "currency": "CDF",
        "portfolio_tzs_bn": 185,             # Total Assets — 2024 Annual Report actual (TZS 184.6 Bn)
        "total_assets_tzs_bn": 184.6,
        "pat_tzs_bn": -6.7,                  # Post-tax LOSS 2024
        "roe_pct": None,
        "portfolio_display": "TZS 185 Bn (Total Assets) · Loans TZS 5.7 Bn · Deposits TZS 22 Bn",
        "sectors": 5,
        "borrowers_est": 8_000,
        "branches": 5,
        "itr_c": 3.14,
        "green_ratio_pct": 0.4,
        "high_risk_pct": 58,
        "colour": "#D85A30",
        "regulator": "Banque Centrale du Congo (BCC)",
        "climate_framework": "BCC Directive · IFC PS mandatory (CRDB Group policy) · ESMS 2024",
        "key_risk": "Deforestation/LULUCF · Mining sector physical risk · Political risk (high) · Currency depreciation",
        "green_milestone": "ESMS Implementation 2024 · Environmental Clubs in primary schools",
        "platform_status": "Phase 3 — Scoping 2026",
        "platform_colour": "#9CA3AF",
        "established": 2022,
    },
    {
        "code": "INS",
        "flag": "🛡️",
        "name": "CRDB Insurance Company Limited",
        "country": "Tanzania (Insurance)",
        "status": "Subsidiary · Break-even achieved 2024",
        "currency": "TZS",
        "portfolio_tzs_bn": 19,              # Total Assets TZS 19.2 Bn
        "total_assets_tzs_bn": 19.2,
        "pat_tzs_bn": 0.342,                 # TZS 342 Mn PAT
        "roe_pct": None,
        "portfolio_display": "GWP TZS 26.9 Bn · Assets TZS 19.2 Bn · Investment TZS 14.8 Bn",
        "sectors": 8,
        "borrowers_est": 50_000,
        "branches": 31,                      # 31 brokers
        "itr_c": 2.73,
        "green_ratio_pct": 15.0,             # Kijani Bima + climate-linked products
        "high_risk_pct": 20,
        "colour": "#059669",
        "regulator": "Tanzania Insurance Regulatory Authority (TIRA)",
        "climate_framework": "TIRA Guidelines · CRDB Group ESG · Kijani Bima Framework",
        "key_risk": "Agricultural climate claims (drought/flood) · Underwriting climate volatility · Market development",
        "green_milestone": "Weather Index Insurance launched · Cattle AI Insurance · Kijani Bima (TIRA approved)",
        "platform_status": "Phase 2 — Insurance Intelligence Module Planned",
        "platform_colour": "#059669",
        "established": 2023,
    },
]

GROUP_CONSOLIDATED: dict = {
    "total_assets_tzs_bn": 16_698.8,        # Group consolidated — 2024 Annual Report actual
    "total_loans_tzs_bn": 10_361.0,         # Group loans and advances — actual
    "total_deposits_tzs_bn": 10_934.1,      # Group customer deposits — actual
    "total_equity_tzs_bn": 2_175.0,
    "group_pat_tzs_bn": 551.5,
    "total_portfolio_tzs_bn": 10_361,       # Loans-based for green ratio calculations
    "total_entities": 5,                     # TZ Bank + Burundi + DRC + Insurance + Foundation
    "total_branches": sum(e["branches"] for e in GROUP_ENTITIES) + 1,
    "total_borrowers_est": sum(e.get("borrowers_est", 0) for e in GROUP_ENTITIES),
    "group_itr": round(
        sum(e["itr_c"] * e["portfolio_tzs_bn"] for e in GROUP_ENTITIES)
        / sum(e["portfolio_tzs_bn"] for e in GROUP_ENTITIES), 2
    ),
    "group_green_ratio": 7.0,               # Tanzania actual 7% dominates group (2024 report)
    "group_high_risk_pct": round(
        sum(e["high_risk_pct"] * e["portfolio_tzs_bn"] for e in GROUP_ENTITIES)
        / sum(e["portfolio_tzs_bn"] for e in GROUP_ENTITIES), 0
    ),
    "group_emissions_ktco2e": 1_247,
    "countries": 3,                         # Tanzania, Burundi, DR Congo (banking)
    "group_target_green_2030": 15.0,
    "moody_rating": "B1",
    "moody_outlook": "Stable",
    "market_cap_tzs_bn": 1_749.9,
}

# ── Computed metrics ──────────────────────────────────────────────────────────
@st.cache_data
def financed_emissions_df() -> pd.DataFrame:
    """Simulated PCAF Scope 3 Category 15 financed emissions by sector."""
    sr = sector_risk()
    if sr.empty:
        return pd.DataFrame()
    rows = []
    for _, row in sr.iterrows():
        intensity = SECTOR_EMISSION_INTENSITY.get(row["sector"], 0.5)
        emissions = row["loan_book_tzs_bn"] * 1000 * intensity  # TZS Bn → TZS Mn × tCO2e/TZS Mn
        rows.append({
            "sector": row["sector"],
            "loan_book_tzs_bn": row["loan_book_tzs_bn"],
            "emission_intensity": intensity,
            "financed_emissions_ktco2e": round(emissions / 1000, 1),
            "risk_tier": row["risk_tier"],
        })
    return pd.DataFrame(rows).sort_values("financed_emissions_ktco2e", ascending=False)


@st.cache_data
def portfolio_itr() -> float:
    """Simulated portfolio Implied Temperature Rise (°C). Weighted by loan book."""
    sr = sector_risk()
    if sr.empty:
        return 2.5
    total = sr["loan_book_tzs_bn"].sum()
    itr = sum(
        SECTOR_ITR_DELTA.get(row["sector"], 1.0) * row["loan_book_tzs_bn"] / total
        for _, row in sr.iterrows()
    )
    return round(1.5 + itr, 2)


@st.cache_data
def green_asset_ratio_current() -> float:
    """CRDB green asset ratio — 2024 Integrated Annual Report actual reported figure.
    Source: CRDB Bank 2024 Annual Report p.119: 'green asset ratio 7% in 2024'.
    Target: 15% by 2030; 30% by 2050.
    """
    return 7.0


def build_portfolio_context() -> str:
    """Build a rich text summary of all portfolio data for the AI copilot."""
    sr = sector_risk()
    bw = borrowers()
    cs = class_summary()
    gp = green_pipeline()
    tc = tcfd()
    sc = scenarios()
    ic = ifc()
    fe = financed_emissions_df()
    itr = portfolio_itr()
    gar = green_asset_ratio_current()

    fr = FINANCIAL_RATIOS
    lines: list[str] = [
        "=== GreenCRDB PORTFOLIO DATA CONTEXT ===",
        "Platform: GreenCRDB — Tanzania Climate-Finance Risk Intelligence Platform",
        "Client: CRDB Bank Group, Tanzania (DSE listed; largest commercial bank in Tanzania; 27% market share deposits)",
        "",
        "=== CRDB BANK KEY FACTS (2024 Integrated Annual Report — ACTUAL FIGURES) ===",
        f"- Total Assets: TZS {fr['total_assets_tzs_bn']:,.1f} Bn (+25.3% YoY)",
        f"- Loans & Advances: TZS {fr['loans_advances_tzs_bn']:,.1f} Bn (+22.7% YoY)",
        f"- Customer Deposits: TZS {fr['customer_deposits_tzs_bn']:,.1f} Bn",
        f"- Profit After Tax: TZS {fr['pat_tzs_bn']} Bn | ROE: {fr['roe_pct']}% | CIR: {fr['cir_pct']}%",
        f"- NPL Ratio: {fr['npl_ratio_pct']}% (BoT limit 5%) | CAR: {fr['car_total_pct']}% (BoT min 14.5%)",
        f"- Share Price: TZS {fr['share_price_tzs']} (+{fr['price_appreciation_pct']}% 2024) | Market Cap: TZS {fr['market_cap_tzs_bn']:,.1f} Bn",
        f"- Moody's Credit Rating: {fr['moodys_rating']} (Stable) — first Tanzanian bank with B1",
        f"- Customers: {fr['customers_mn']}M | Digital Accounts: {fr['digital_accounts_mn']}M | Agents: {fr['agents_wakala']:,}",
        "- FIRST standalone TCFD Report published 2024 — first commercial bank in Tanzania",
        "- FIRST GCF-accredited commercial bank in East & Central Africa (since 2019)",
        "- Kijani Bond: USD 65.7M raised (429% oversubscribed; listed Luxembourg Stock Exchange; 10.25% yield)",
        "- GCF TACATDP: USD 200M (USD 100M GCF co-investment) — 6.1M+ beneficiaries",
        "- MUFG Japan: USD 225M green facility",
        "- FMO + Proparco: USD 125M (1,500 MSMEs targeted)",
        "- Green asset ratio: 7% actual 2024 → target 15% by 2030 → 30% by 2050",
        "- Green loans disbursed: TZS 86.9 Bn | CO2 reduction: 13.8M kg/year | Clean energy: 14 GWh",
        "- IFC EDGE certified HQ: 21% energy saving, 27% water saving, 28% carbon reduction",
        "- Net-zero target: 2029 | EDGE Advance target: 2026",
        "- Group: 4,251 employees | 259 branches | 684 ATMs | 36,566 Wakala agents",
        "- Group entities: CRDB Bank TZ (flagship) + CRDB Burundi (PAT TZS 40.3Bn) + CRDB Congo (start-up) + CRDB Insurance (break-even 2024)",
        "- Bank of Tanzania 2025 Guidelines: climate risk reporting mandatory — CRDB compliant",
        "",
        "=== SECTOR CLIMATE RISK (Module 1 — GreenCRDB) ===",
    ]

    if not sr.empty:
        total_portfolio = sr["loan_book_tzs_bn"].sum()
        lines.append(f"Total Portfolio: TZS {total_portfolio:,.0f} Bn across {len(sr)} sectors")
        for _, row in sr.iterrows():
            lines.append(
                f"  {row['sector']}: Climate Risk={row['composite_climate_risk']:.2f}/10, "
                f"Tier={row['risk_tier']}, Exposure=TZS {row['loan_book_tzs_bn']:,.0f}Bn ({row['loan_book_pct']:.1f}%)"
            )

    lines.append("")
    lines.append("=== BORROWER ESG SCORES (Module 2) ===")
    if not cs.empty:
        for _, row in cs.iterrows():
            lines.append(
                f"  {row['classification']}: {int(row['borrowers'])} borrowers, "
                f"TZS {row['total_exposure_tzs_mn']:,.1f}Mn exposure, Avg ESG={row['avg_esg']:.2f}/10"
            )

    if not bw.empty:
        lines.append(f"Portfolio Avg ESG: {bw['esg_composite'].mean():.2f}/10")
        lines.append(f"  E (Environmental): {bw['E_score'].mean():.2f}/10 | S (Social): {bw['S_score'].mean():.2f}/10 | G (Governance): {bw['G_score'].mean():.2f}/10")

    lines.append("")
    lines.append("=== CLIMATE FINANCE DECISIONS (Module 3) ===")
    if not decisions().empty:
        dec = decisions()
        for outcome, grp in dec.groupby("decision"):
            lines.append(f"  {outcome}: {len(grp)} borrowers")

    if not gp.empty:
        lines.append(f"Green Finance Pipeline: {len(gp)} borrowers, TZS {gp['loan_size_tzs_mn'].sum():,.1f}Mn")
        lines.append(f"Current Green Asset Ratio: {gar:.1f}% (target: 15.0% by 2030)")

    lines.append("")
    lines.append("=== TCFD METRICS ===")
    if not tc.empty:
        for _, row in tc.iterrows():
            lines.append(f"  {row['TCFD Metric']}: {row['Portfolio Value']}")

    lines.append("")
    lines.append("=== CLIMATE SCENARIOS ===")
    if not sc.empty:
        for _, row in sc.iterrows():
            lines.append(
                f"  {row['Scenario']}: Portfolio impact {row['Est. portfolio impact (%)']:.1f}%, "
                f"Credit loss TZS {row['Est. credit loss TZS Bn']:.1f}Bn"
            )

    lines.append("")
    lines.append("=== IFC PERFORMANCE STANDARDS ALIGNMENT ===")
    if not ic.empty:
        for _, row in ic.iterrows():
            lines.append(f"  {row['standard']} {row['title']}: {row['alignment_tier']}, Score={row['portfolio_score']:.2f}/10, Gap: {row['key_gap']}")

    lines.append("")
    lines.append("=== SIMULATED PCAF FINANCED EMISSIONS (Scope 3 Category 15) ===")
    lines.append("Methodology: IPCC AR6 Africa sector emission intensity proxies; PCAF data quality Score 4")
    if not fe.empty:
        total_emissions = fe["financed_emissions_ktco2e"].sum()
        lines.append(f"Total Portfolio Financed Emissions: {total_emissions:,.0f} ktCO2e")
        for _, row in fe.iterrows():
            lines.append(f"  {row['sector']}: {row['financed_emissions_ktco2e']:,.1f} ktCO2e (intensity: {row['emission_intensity']:.2f} tCO2e/TZS Mn)")

    lines.append("")
    lines.append(f"=== PORTFOLIO IMPLIED TEMPERATURE RISE (ITR) ===")
    lines.append(f"Portfolio ITR: {itr:.2f}°C (vs. Paris Agreement 1.5°C target)")
    lines.append("Methodology: NGFS 2023 sector decarbonisation pathways; PACTA proxy; Data Quality Score 4")
    lines.append("Implication: Portfolio is currently aligned to a ~2.6°C warming pathway — action required to reach 1.5°C")

    lines.append("")
    lines.append("=== PRB (PRINCIPLES FOR RESPONSIBLE BANKING) SCORES ===")
    for pillar, score in PRB_SCORES.items():
        lines.append(f"  {pillar}: {score:.1f}/5.0")

    lines.append("")
    lines.append("=== SASB FN-CB COMMERCIAL BANKS METRICS ===")
    for topic, data in SASB_METRICS.items():
        lines.append(f"  {topic}: {data['status']} ({data['score']:.1f}/5.0) — {data['note']}")

    lines.append("")
    lines.append("=== UN SDG ALIGNMENT ===")
    for sdg, data in SDG_ALIGNMENT.items():
        lines.append(f"  {sdg}: Score {data['score']:.1f}/5.0 — {data['activity']}")

    return "\n".join(lines)
