# GreenCRDB — Tanzania Climate-Finance Risk Intelligence Platform

## About this project

GreenCRDB was built independently by **Dishon Abuya**, an MSc Finance and Investment student at the University of Dundee, as a learning exercise and conversation starter with CRDB Bank on climate-finance disclosure and implementation gaps identified from its 2024 Sustainability Report.

The application combines sector climate risk scoring, borrower ESG assessment, lending decisions, and regulatory compliance reporting in a Streamlit demonstrator.

All portfolio values and borrower data are **simulated and illustrative**. CRDB Group aggregate figures are sourced from the **2024 Integrated Annual Report**.

---

## Live App

**[greencrdb.streamlit.app](https://greencrdb.streamlit.app)**

Demo login (full access): `jkimaro` / `GreenCRDB@2025`

---

## Platform Modules

| Module | Description |
|--------|-------------|
| 🏦 MultiBank Intelligence | Group entity benchmarking, Africa league table, DFI facility tracker |
| 📊 Module 1 — Sector Climate Risk | 5-hazard composite scoring across 12 Tanzania sectors (0–10 scale) |
| 🌱 Module 2 — Borrower ESG | E/S/G pillar scoring, 4-tier classification, sector-filtered views |
| 💡 Module 3 — Finance Decisions | Decision engine, TCFD metrics, IFC PS alignment, scenario analysis |
| 📋 Module 4 — Regulatory Compliance | BoT 2025, PCAF Scope 3, PRB, SASB FN-CB, TNFD readiness |
| 🤖 AI Copilot | Gemini-powered Q&A and formal sustainability report generation |
| 📂 Data Upload Studio | CSV/Excel/PDF ingestion with validation and AI-powered review |
| 👥 User Management | Role and permission matrix (CSO view) |
| ℹ️ About | Platform overview, frameworks, tech stack, roadmap |
| 📖 User Guide | Full scoring logic, role workflows, FAQ |

---

## Scoring Logic

**Module 1 — Composite Climate Risk (0–10)**
```
composite = drought×0.25 + flood×0.20 + temperature×0.20 + transition×0.20 + water_stress×0.15
```
Tiers: Low <4.5 · Medium 4.5–6.0 · High 6.0–7.5 · Critical >7.5

**Module 2 — ESG Score (0–10)**
```
ESG = Environmental×0.40 + Social×0.30 + Governance×0.30
```
Tiers: Green Eligible ≥7.5 · Standard 5.5–7.4 · Watch List 4.0–5.4 · High Risk <4.0

**Module 3 — Decision Score (0–100)**
```
sector_readiness = (10 − composite_climate_risk) × 10   # invert: high risk → low readiness
decision_score   = ESG×10×0.55 + sector_readiness×0.45
```
Thresholds: Approve ≥65 · Conditional ≥52 · Review ≥40 · Decline <40

---

## Role-Based Access

| Role | Username | Access |
|------|----------|--------|
| Chief Sustainability Officer | `jkimaro` | Full — all modules, user management |
| Climate Risk Manager | `smwangi` | Module 1 + Regulatory full; others read |
| ESG Assessment Officer | `dosei` | Module 2 full; sector/region restricted |
| Green Finance Officer | `mtanzania` | Module 3 full; others read |
| Compliance & Reporting Officer | `akassim` | All read + report generation |
| Data Analyst | `gmoshi` | Modules 1–3 read only |

---

## Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Launch web app
streamlit run app.py

# Or run the data pipeline scripts in order
python3 scripts/01_TZCRIP_Module1_Sector_Climate_Risk.py
python3 scripts/02_TZCRIP_Module2_Borrower_ESG_Scoring_Engine.py
python3 scripts/03_TZCRIP_Module3_Climate_Finance_Decision_Engine.py
```

---

## AI Copilot Setup

The AI Copilot requires a free Google Gemini API key:

1. Go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Create an API key (free tier — 1M tokens/day)
3. On Streamlit Cloud: app settings → Secrets → add `GEMINI_API_KEY = "your-key"`
4. Locally: create `.streamlit/secrets.toml` with the same line

---

## Frameworks & Standards

| Framework | Coverage |
|-----------|----------|
| TCFD | Four-pillar disclosure (Governance, Strategy, Risk Mgmt, Metrics) |
| Bank of Tanzania 2025 | 13-item compliance tracker — 12/13 compliant |
| PCAF | Scope 3 Category 15 financed emissions, Data Quality Score 4 |
| IFC Performance Standards | PS1–PS8 alignment per borrower |
| PRB (UNEP FI) | Six principles self-assessment |
| SASB FN-CB | Commercial banking sector standard |
| TNFD v1.0 | LEAP approach readiness tracker |
| UN SDGs | Portfolio SDG contribution mapping |

---

## Project Structure

```
GreenCRDB/
├── app.py                          # Home dashboard
├── auth.py                         # RBAC — users, roles, permissions
├── web_data.py                     # All platform data constants & loaders
├── data_store.py                   # Session + CSV persistence for entered data
├── pages/
│   ├── 0_🏦_MultiBank_Intelligence.py
│   ├── 1_📊_Sector_Risk.py
│   ├── 2_🌱_Borrower_ESG.py
│   ├── 3_💡_Finance_Decisions.py
│   ├── 4_📋_Regulatory_Compliance.py
│   ├── 5_🤖_AI_Copilot.py
│   ├── 6_📂_Data_Upload.py
│   ├── 7_👥_User_Management.py
│   ├── 8_ℹ️_About.py
│   └── 9_📖_User_Guide.py
├── scripts/                        # Offline data pipeline (Module 1–3)
├── config/                         # risk_thresholds.yaml, scoring_weights.yaml
├── data/processed/                 # Pipeline outputs consumed by the web app
├── .streamlit/config.toml          # Theme — CRDB green (#006B3C)
└── requirements.txt
```

---

## Deployment

Hosted on **Streamlit Community Cloud** — auto-deploys on every push to `main`.

`data/raw/` and `outputs/` are excluded from the repo (see `.gitignore`). The web app reads from `data/processed/` which is committed.
